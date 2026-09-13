"""
Automated Certificate & Cloud Asset Lifecycle Operator
Test Suite for TLS Auditing, Orphan Scanning, and IAM Hygiene Analysis.
"""

from datetime import datetime, timedelta, timezone

from src.operator.iam_auditor import IAMHygieneAuditor
from src.operator.orphan_scanner import OrphanResourceScanner
from src.operator.tls_auditor import TLSCertificateAuditor


def test_tls_certificate_expiration_evaluation():
    """Verify correct status classification across expired, critical, and healthy dates."""
    auditor = TLSCertificateAuditor(warning_threshold_days=30, critical_threshold_days=14)
    now = datetime.now(timezone.utc)

    # 1. Critical Expiration (<14d)
    crit = auditor.evaluate_certificate_dates("api.test.com", now + timedelta(days=5))
    assert crit["lifecycle_status"] == "CRITICAL_ACTION_REQUIRED"
    assert crit["urgency_level"] == "CRITICAL"

    # 2. Warning Expiration (15-30d)
    warn = auditor.evaluate_certificate_dates("auth.test.com", now + timedelta(days=20))
    assert warn["lifecycle_status"] == "EXPIRING_SOON"
    assert warn["urgency_level"] == "WARNING"

    # 3. Healthy Expiration (>30d)
    healthy = auditor.evaluate_certificate_dates("portal.test.com", now + timedelta(days=90))
    assert healthy["lifecycle_status"] == "HEALTHY"
    assert healthy["urgency_level"] == "LOW"


def test_orphan_resource_scanner():
    """Verify detection of orphaned EBS volumes and waste calculation."""
    scanner = OrphanResourceScanner()
    report = scanner.scan_simulated_fleet()
    assert report["total_orphaned_assets"] > 0
    assert report["estimated_monthly_waste_usd"] > 0.0
    assert len(report["orphaned_ebs_volumes"]) >= 3
    assert len(report["unassociated_elastic_ips"]) >= 2


def test_iam_hygiene_auditor():
    """Verify detection of access keys older than 90 days."""
    auditor = IAMHygieneAuditor()
    report = auditor.audit_simulated_iam_posture()
    assert report["total_users_audited"] >= 4
    assert report["stale_access_keys_count"] >= 2
