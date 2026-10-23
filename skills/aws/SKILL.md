---
name: aws
description: How we work with AWS safely, covering SSO and OIDC authentication without long-lived keys, least-privilege IAM, infrastructure as code with CDK or Terraform, Lambda runtimes, S3, secrets, logging and cost guardrails. Use whenever deploying to or changing AWS, writing CDK or Terraform for AWS, configuring IAM roles or policies, setting up GitHub Actions deploys to AWS, choosing or upgrading Lambda runtimes, using the AWS SDK or CLI, or investigating AWS costs or permissions errors.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, cloud, aws, infra]
---

# AWS

The expensive AWS mistakes are deploying to the wrong account, over-broad
IAM, public data and runaway cost. Every step below guards against one of
those.

## Before you start

1. **Confirm the account and region before any change:**
   `aws sts get-caller-identity` and `aws configure get region` (or the
   profile in use). Say which account you're about to change.
2. Find the infrastructure-as-code tool (`cdk.json`, `*.tf`, SAM
   `template.yaml`, Serverless, Pulumi). Change infrastructure through it,
   not the console, or the next deploy reverts or conflicts with your change.
3. Check how environments are separated. Separate accounts per environment
   (via AWS Organizations) is what we want; prefixes in one account are a
   weaker fallback.

## Defaults for new work

- **Humans:** IAM Identity Center (SSO) with `aws configure sso` /
  `aws sso login`. No IAM users with access keys.
- **CI (GitHub Actions):** OIDC federation (`aws-actions/configure-aws-credentials`
  with `role-to-assume`), with the role's trust policy scoped to the repo
  and branch/environment.
- **IaC:** AWS CDK v2 (TypeScript), or Terraform/OpenTofu if the project
  already uses it. Run `cdk-nag` or `checkov` on templates.
- **Compute:** Lambda for event/API glue (prefer `arm64`), ECS Fargate for
  long-running containers.
- **Secrets:** Secrets Manager or SSM Parameter Store (SecureString),
  read at runtime with an IAM-scoped role.
- **SDKs:** JS v3 modular clients (`@aws-sdk/client-*`), boto3,
  `aws-sdk-go-v2`. JS SDK v2 and Go SDK v1 are end-of-support.

## Verify loop

```bash
aws sts get-caller-identity         # right account?
npx cdk synth && npx cdk diff       # read the diff, especially IAM and replacements
npx cdk deploy <stack>              # only after the diff is understood
# Terraform: terraform fmt -check && terraform validate && terraform plan
```

Treat any diff showing **resource replacement** of a database, bucket or
user pool as a stop-and-ask.

## Rules that matter

- **Least privilege:** scope IAM actions and resources; no `"Action": "*"` or
  `"Resource": "*"` outside break-glass roles. Prefer CDK `grant*` methods
  over hand-written policies.
- **S3:** Block Public Access on, Object Ownership "bucket owner enforced",
  encryption on; serve public assets through CloudFront with Origin Access
  Control.
- **Data stores:** deletion protection and backups on for RDS/DynamoDB;
  `RemovalPolicy.RETAIN` for stateful CDK resources.
- **Logs:** set CloudWatch log retention explicitly. The default is never
  expire, which quietly costs money.
- **Cost:** AWS Budgets alerts on every account, cost allocation tags, and
  watch NAT Gateway data processing (VPC endpoints for S3/DynamoDB help).
- **Networking:** databases in private subnets; security groups reference
  other security groups, not `0.0.0.0/0`.

## Changed recently (checked 2026-10-23)

- **Lambda runtimes:** use `nodejs24.x` (deprecation scheduled 2028-04-30)
  and `python3.14` (2029-06-30). `nodejs26.x` and `python3.15` are in
  preview only. Node 20 and Python 3.10 runtimes are at or near deprecation;
  check the live runtime page before choosing.
- **CDK:** the CLI (`aws-cdk`, 2.1xxx versions) is versioned separately from
  the library (`aws-cdk-lib` 2.2xx). Upgrade both, but they no longer share
  version numbers.

## Pitfalls

- Long-lived access keys in `.env`, CI secrets or code. Use SSO/OIDC.
- Wildcard trust policies on OIDC roles (any repo or branch can assume them).
- Lambda in a VPC without endpoints or NAT, so it can't reach AWS APIs and
  times out silently.
- Copying console-created resources into IaC without importing them, so
  they end up duplicated.

## Sources

- `research/2026-10-23-stack-baseline.md` → AWS section.
