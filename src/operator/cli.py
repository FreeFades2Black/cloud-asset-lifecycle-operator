"""
Automated Certificate & Cloud Asset Lifecycle Operator
CLI Application & Command Center.
Commands:
  - cert-guard audit-certs
  - cert-guard scan-orphans
  - cert-guard iam-hygiene
  - cert-guard full-dossier
"""

import typer
import json
import csv
from pathlib import Path
from datetime import datetime, timezone
from src.operator.tls_auditor import TLSCertificateAuditor
from src.operator.orphan_scanner import OrphanResourceScanner
from src.operator.iam_auditor import IAMHygieneAuditor

app = typer.Typer(
    name="cert-guard",
    help="[+] Automated Certificate & Cloud Asset Lifecycle Operator -- Multi-Cloud FinOps & Security Hygiene",
    add_completion=False
)


@app.command()
def audit_certs(
    warning_days: int = typer.Option(30, help="Days before expiration to trigger warning"),
    output_format: str = typer.Option("table", help="Output format: table, json, or csv")
):
    """Audit TLS/SSL certificates and detect imminent expiration risks."""
    auditor = TLSCertificateAuditor(warning_threshold_days=warning_days)
    results = auditor.audit_simulated_fleet()

    if output_format == "json":
        typer.echo(json.dumps(results, indent=2))
        return

    typer.echo("\n[TLS / SSL CERTIFICATE LIFECYCLE AUDIT REPORT]")
    typer.echo("=" * 95)
    typer.echo(f"{'Domain / ARN':<38} {'Days Left':<12} {'Status':<25} {'Issuer':<20}")
    typer.echo("-" * 95)

    for c in results:
        status_color = c['lifecycle_status']
        typer.echo(f"{c['resource_id']:<38} {c['days_remaining']:<12} {status_color:<25} {c['issuer'][:20]:<20}")
    typer.echo("=" * 95)


@app.command()
def scan_orphans(
    output_format: str = typer.Option("table", help="Output format: table, json, or csv")
):
    """Scan for orphaned EBS volumes, idle Elastic IPs, and stale NAT gateways."""
    scanner = OrphanResourceScanner()
    report = scanner.scan_simulated_fleet()

    if output_format == "json":
        typer.echo(json.dumps(report, indent=2))
        return

    typer.echo("\n[ORPHANED CLOUD ASSETS & FINOPS AUDIT REPORT]")
    typer.echo("=" * 85)
    typer.echo(f"Estimated Monthly Cloud Waste: ${report['estimated_monthly_waste_usd']} USD / Month")
    typer.echo(f"Estimated Annual Cloud Waste:  ${report['estimated_annual_waste_usd']} USD / Year")
    typer.echo("-" * 85)
    typer.echo(f"{'Resource Type':<25} {'Resource ID':<25} {'Monthly Cost':<15} {'Details':<20}")
    typer.echo("-" * 85)

    for v in report["orphaned_ebs_volumes"]:
        typer.echo(f"{'Orphaned EBS (gp3)':<25} {v['volume_id']:<25} ${v['monthly_cost_usd']:<14} {v['size_gb']} GB ({v['created_days_ago']}d ago)")

    for e in report["unassociated_elastic_ips"]:
        typer.echo(f"{'Idle Elastic IP':<25} {e['ip_address']:<25} ${e['monthly_cost_usd']:<14} {e['idle_days']}d unassociated")

    for n in report["idle_nat_gateways"]:
        typer.echo(f"{'Idle NAT Gateway':<25} {n['nat_gateway_id']:<25} ${n['monthly_cost_usd']:<14} {n['vpc_id']}")

    typer.echo("=" * 85)


@app.command()
def iam_hygiene():
    """Audit IAM access keys older than 90 days and missing MFA credentials."""
    auditor = IAMHygieneAuditor()
    report = auditor.audit_simulated_iam_posture()

    typer.echo("\n[IAM CREDENTIAL HYGIENE & SECRET ROTATION AUDIT]")
    typer.echo("=" * 85)
    typer.echo(f"Total Users Audited: {report['total_users_audited']} | Stale Keys (>90d): {report['stale_access_keys_count']} | Missing MFA: {report['missing_mfa_count']}")
    typer.echo("-" * 85)
    typer.echo(f"{'Username':<25} {'Key ID':<25} {'Age (Days)':<15} {'Compliance Status':<20}")
    typer.echo("-" * 85)

    for u in report["credential_audit_records"]:
        typer.echo(f"{u['username']:<25} {u['access_key_id'][:20]:<25} {u['key_age_days']:<15} {u['status']:<20}")
    typer.echo("=" * 85)


@app.command()
def full_dossier(
    output_file: str = typer.Option("CLOUD_ASSET_LIFECYCLE_REPORT.json", help="Path to save full audit JSON")
):
    """Execute complete unified audit across TLS, FinOps Orphans, and IAM Hygiene."""
    tls_auditor = TLSCertificateAuditor()
    orphan_scanner = OrphanResourceScanner()
    iam_auditor = IAMHygieneAuditor()

    full_report = {
        "audit_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "tls_certificates": tls_auditor.audit_simulated_fleet(),
        "orphaned_assets": orphan_scanner.scan_simulated_fleet(),
        "iam_hygiene": iam_auditor.audit_simulated_iam_posture()
    }

    out_path = Path(output_file)
    if out_path.parent:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)

    typer.echo(f"[OK] Full Cloud Asset Lifecycle Dossier exported successfully to: {output_file}")


if __name__ == "__main__":
    app()
