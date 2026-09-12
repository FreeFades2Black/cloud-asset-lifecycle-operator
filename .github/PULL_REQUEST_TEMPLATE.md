## FinOps & Asset Operator Operational Overview
*Describe modifications to lifecycle auditing rules, resource discovery, or quarantine actions.*

- [ ] Resource Scanner (EBS, Snapshot, EIP, RDS)
- [ ] IAM Auditor & Unused Role Pruner
- [ ] TLS Certificate Scanner
- [ ] FinOps Cost Estimation Engine

## Safety & Blast Radius Verification
- **Dry-Run Validated:** Verified scanning with `--dry-run` flag to ensure zero unintended resource deletions.
- **Grace Period Verified:** Verified 48-hour quarantine state before destruction.

## Verification Checklist
- [ ] Unit & integration tests passing: `pytest tests/ -v`
- [ ] Docker container build succeeds cleanly: `docker build -t operator:latest .`
- [ ] Memory footprint under load < 256MB
