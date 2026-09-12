# ADR-0002: Declarative TTL Tag Contract (`lifecycle:ttl` and `owner:contact`)

**Status:** Accepted  
**Date:** 2026-07-08  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
Development and ephemeral test environments generate unattached EBS volumes, unassociated Elastic IPs, and orphaned test clusters that accumulate unbudgeted cloud spend. Manual cleanup leads to accidental deletion of persistent shared resources.

## 2. Options Considered
* **Option A: Blanket Deletion of Resources Older than 14 Days**
  - *Evaluation:* Simple, but causes severe production incidents when long-lived static baseline infrastructure is inadvertently purged.
* **Option B: Explicit Metadata Tag Contract with Quarantine Grace Period**
  - *Evaluation:* Resources must declare `lifecycle:ttl` (e.g. `7d`, `30d`, `permanent`) and `owner:contact`. Resources missing required tags enter a 48-hour `quarantine` status with automated Slack alerts before deletion.

## 3. Decision & Trade-Off Accepted
We adopted **Option B (Explicit Tag Contract with Quarantine)**.  
**Trade-Off Accepted:** Requires engineering discipline across infrastructure teams to maintain tags; requires a 48-hour quarantine state storage mechanism.
