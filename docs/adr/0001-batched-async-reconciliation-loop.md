# ADR-0001: Batched Asynchronous Reconciliation Loop with Exponential Jitter vs Real-Time Webhooks

**Status:** Accepted  
**Date:** 2026-06-25  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
Managing cloud resource lifecycles across thousands of EC2 volumes, snapshots, Elastic IPs, and Kubernetes PVCs requires regular auditing and cleanup. Listening synchronously to cloud API lifecycle events (e.g. AWS CloudTrail EventBridge) caused duplicate invocation storms during batch terraform provisioning runs.

## 2. Options Considered
* **Option A: Synchronous Event-Driven Lambdas on Resource Creation**
  - *Evaluation:* Immediate tagging validation, but triggers AWS API throttling (`RequestLimitExceeded`) during burst deployments and fails to catch zombie resources that outlive their owner tags.
* **Option B: Batched Asynchronous Reconciliation Loop with Rate-Limited Token Bucket**
  - *Evaluation:* Operates on a configurable cadence (default: every 6 hours), uses pagination with exponential backoff and jitter, and generates consolidated FinOps audit reports.

## 3. Decision & Trade-Off Accepted
We adopted **Option B (Batched Asynchronous Reconciliation)**.  
**Trade-Off Accepted:** Zombie resources may persist for up to 6 hours before detection and quarantine, but cloud API rate limits are protected and FinOps reporting is aggregated deterministically.
