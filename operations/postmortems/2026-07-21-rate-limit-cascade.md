# Incident Post-Mortem: Operator Scan Triggering AWS EC2 API Throttling Cascade

**Incident Date:** 2026-07-21  
**Impact Duration:** 35 minutes  
**Severity:** SEV-2  
**Root Cause:** Asset operator initiated a full-region scan across 12 AWS accounts simultaneously with zero client-side jitter, exhausting the regional token bucket for `DescribeVolumes`. CI/CD Terraform pipelines running concurrently failed with `RequestLimitExceeded`.

## Timeline
* **10:00 UTC:** Scheduled cron triggered multi-account asset scan across 12 AWS accounts.
* **10:03 UTC:** Simultaneous `DescribeVolumes` and `DescribeSnapshots` calls hit AWS regional rate limit.
* **10:07 UTC:** Terraform CI pipelines failed with `RequestLimitExceeded: Rate exceeded`.
* **10:15 UTC:** On-call engineer identified API spike originating from operator IAM role.
* **10:20 UTC:** Operator process killed; API quota recovered immediately.
* **10:35 UTC:** Patch deployed adding token-bucket rate limiting (max 5 req/sec per account) and randomized startup jitter (0-300s).

## Corrective Actions
1. Implemented token-bucket rate limiter in `src/operator/orphan_scanner.py` restricting AWS SDK calls to 5 QPS per account.
2. Configured exponential backoff with full jitter in boto3 client configuration.
3. Added Prometheus metric `cloud_operator_api_throttles_total` to alert before regional exhaustion.
