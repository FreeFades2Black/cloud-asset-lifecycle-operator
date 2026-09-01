"""
Automated Certificate & Cloud Asset Lifecycle Operator
TLS / SSL Certificate Lifecycle Discovery and Expiration Auditing.
Discovers ACM certificates and domain endpoints, grading urgency and renewal requirements.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import ssl
import socket


class TLSCertificateAuditor:
    """Audits TLS/SSL certificates across AWS ACM and remote public/private domain endpoints."""

    def __init__(self, warning_threshold_days: int = 30, critical_threshold_days: int = 14):
        self.warning_threshold_days = warning_threshold_days
        self.critical_threshold_days = critical_threshold_days

    def evaluate_certificate_dates(
        self, domain_or_arn: str, not_after: datetime, issuer: str = "DigiCert / Let's Encrypt", sans: List[str] = None
    ) -> Dict[str, Any]:
        """Calculates days remaining and assigns an operational lifecycle status."""
        now = datetime.now(timezone.utc)
        if not_after.tzinfo is None:
            not_after = not_after.replace(tzinfo=timezone.utc)

        days_remaining = (not_after - now).days

        if days_remaining <= 0:
            status = "EXPIRED"
            urgency = "CRITICAL"
        elif days_remaining <= self.critical_threshold_days:
            status = "CRITICAL_ACTION_REQUIRED"
            urgency = "CRITICAL"
        elif days_remaining <= self.warning_threshold_days:
            status = "EXPIRING_SOON"
            urgency = "WARNING"
        else:
            status = "HEALTHY"
            urgency = "LOW"

        return {
            "resource_id": domain_or_arn,
            "issuer": issuer,
            "expiration_date": not_after.isoformat(),
            "days_remaining": days_remaining,
            "lifecycle_status": status,
            "urgency_level": urgency,
            "subject_alternative_names": sans or [domain_or_arn]
        }

    def audit_simulated_fleet(self) -> List[Dict[str, Any]]:
        """Generates a realistic enterprise certificate inventory across core domains."""
        now = datetime.now(timezone.utc)

        simulated_certs = [
            ("api.worldacceptance.com", now + timedelta(days=8), "Amazon ACM (Auto-Renew Failed)", ["api.worldacceptance.com", "*.api.worldacceptance.com"]),
            ("auth.tdsynnex.com", now + timedelta(days=22), "DigiCert Global Root G2", ["auth.tdsynnex.com"]),
            ("portal.mobility.michelin.com", now + timedelta(days=140), "Let's Encrypt Authority X3", ["portal.mobility.michelin.com"]),
            ("telemetry.bmw-spartanburg.internal", now + timedelta(days=4), "Internal Vault Enterprise CA", ["telemetry.bmw-spartanburg.internal"]),
            ("scada.ge-vernova.power.net", now + timedelta(days=320), "Sectigo Enterprise SSL", ["scada.ge-vernova.power.net"]),
            ("legacy-vpn.defense.internal", now - timedelta(days=3), "Self-Signed Legacy CA", ["legacy-vpn.defense.internal"])
        ]

        results = []
        for domain, expiry, issuer, sans in simulated_certs:
            results.append(self.evaluate_certificate_dates(domain, expiry, issuer, sans))

        results.sort(key=lambda x: x["days_remaining"])
        return results
