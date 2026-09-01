"""
Automated Certificate & Cloud Asset Lifecycle Operator
Orphaned Cloud Resource Discovery & FinOps Waste Estimator.
Detects unattached EBS volumes, unassociated Elastic IPs, and orphaned NAT gateways.
"""

from typing import Dict, List, Any


class OrphanResourceScanner:
    """Discovers orphaned, dangling, and idle cloud assets and calculates monthly FinOps waste."""

    # AWS Standard Monthly Unit Costs (us-east-1 estimates)
    EBS_GP3_GB_MONTH = 0.08
    UNASSOCIATED_EIP_MONTH = 3.60
    IDLE_NAT_GATEWAY_MONTH = 32.40
    UNUSED_ALB_MONTH = 22.50

    def scan_simulated_fleet(self) -> Dict[str, Any]:
        """Scans multi-account resources and isolates orphaned assets."""
        orphaned_ebs = [
            {"volume_id": "vol-0a8819f8e71b29", "size_gb": 500, "type": "gp3", "created_days_ago": 65, "last_attached_instance": "i-0991823dead (Terminated)", "monthly_cost_usd": round(500 * self.EBS_GP3_GB_MONTH, 2)},
            {"volume_id": "vol-03b901fc812a14", "size_gb": 1000, "type": "gp3", "created_days_ago": 120, "last_attached_instance": "i-0881726a11 (Terminated)", "monthly_cost_usd": round(1000 * self.EBS_GP3_GB_MONTH, 2)},
            {"volume_id": "vol-0dfa8829103e91", "size_gb": 200, "type": "gp3", "created_days_ago": 45, "last_attached_instance": "None (Snapshot Restore)", "monthly_cost_usd": round(200 * self.EBS_GP3_GB_MONTH, 2)}
        ]

        orphaned_eips = [
            {"ip_address": "54.210.89.12", "allocation_id": "eipalloc-019283f", "association_id": None, "idle_days": 42, "monthly_cost_usd": self.UNASSOCIATED_EIP_MONTH},
            {"ip_address": "3.88.192.45", "allocation_id": "eipalloc-098231a", "association_id": None, "idle_days": 18, "monthly_cost_usd": self.UNASSOCIATED_EIP_MONTH}
        ]

        idle_nat_gateways = [
            {"nat_gateway_id": "nat-09817263b", "vpc_id": "vpc-019283a (Dev Sandbox)", "active_connections": 0, "monthly_cost_usd": self.IDLE_NAT_GATEWAY_MONTH}
        ]

        unreferenced_security_groups = [
            {"group_id": "sg-0918237192", "group_name": "legacy-dev-db-access", "network_interfaces_attached": 0, "status": "STALE_ORPHAN"}
        ]

        total_monthly_waste = sum(v["monthly_cost_usd"] for v in orphaned_ebs) + \
                              sum(e["monthly_cost_usd"] for e in orphaned_eips) + \
                              sum(n["monthly_cost_usd"] for n in idle_nat_gateways)

        return {
            "total_orphaned_assets": len(orphaned_ebs) + len(orphaned_eips) + len(idle_nat_gateways) + len(unreferenced_security_groups),
            "estimated_monthly_waste_usd": round(total_monthly_waste, 2),
            "estimated_annual_waste_usd": round(total_monthly_waste * 12, 2),
            "orphaned_ebs_volumes": orphaned_ebs,
            "unassociated_elastic_ips": orphaned_eips,
            "idle_nat_gateways": idle_nat_gateways,
            "unreferenced_security_groups": unreferenced_security_groups
        }
