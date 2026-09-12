# Operational Runbook: Diagnosing Cloud Provider API Throttling (`RequestLimitExceeded`)

**Severity:** P2 / Performance Degraded  
**Target Systems:** Asset Lifecycle Operator, AWS EC2 / EBS API, CloudWatch

## Diagnostic Workflow

### 1. Check Operator Logs for Rate Limit Exceptions
```bash
docker logs cloud-asset-operator | grep -E "(RequestLimitExceeded|Throttling|Rate exceeded)"
```

### 2. Identify High-Frequency CloudTrail API Calls
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DescribeInstances \
  --start-time $(date -u -d '2 hours ago' +%s) \
  --query 'Events[].EventName' | wc -l
```

### 3. Step-by-Step Remediation
1. Increase operator scan interval in `docker-compose.yml` or Kubernetes ConfigMap:
   ```yaml
   OPERATOR_SCAN_INTERVAL_SECONDS: "43200" # 12 hours
   AWS_MAX_ATTEMPTS: "10"
   AWS_RETRY_MODE: "adaptive"
   ```
2. Enable client-side caching in operator CLI:
   ```bash
   python -m src.operator.cli --cache-ttl 3600 --report-out /tmp/report.json
   ```
