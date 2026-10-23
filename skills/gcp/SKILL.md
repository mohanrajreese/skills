---
name: gcp
description: How we work with Google Cloud, covering gcloud and Application Default Credentials, Workload Identity Federation for CI with no service account keys, Cloud Run services, jobs and functions, Artifact Registry, Secret Manager, Cloud SQL, IAM and cost guardrails. Use whenever deploying to or changing Google Cloud, writing Terraform for GCP, setting up GitHub Actions deploys to GCP, configuring service accounts or IAM, debugging permission or quota errors, or using gcloud. For Firebase products use the firebase skill.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, cloud, gcp, infra]
---

# Google Cloud

Container-first: build an image, push it to Artifact Registry and run it on
Cloud Run under a dedicated service account. Credentials come from identity
federation, never from downloaded keys.

## Before you start

1. **Confirm the project and account:** `gcloud config list` (account,
   project, region). Multiple configurations (`gcloud config configurations
   list`) are common; say which project you're about to change.
2. Find the IaC (Terraform `google` provider, Pulumi, Deployment Manager) or
   deploy scripts. Change infrastructure through them.
3. Note that project **ID** ≠ project **number**; some IAM principals and
   APIs need the number.

## Defaults for new work

- **Local auth:** `gcloud auth login` for the CLI and
  `gcloud auth application-default login` for code using client libraries
  (ADC). No JSON key files on laptops.
- **CI:** Workload Identity Federation via
  `google-github-actions/auth` (`workload_identity_provider` +
  `service_account`), with the attribute condition restricted to our
  repository. Enforce the org policy that disables service-account key
  creation.
- **Compute:** Cloud Run services for HTTP, Cloud Run jobs for batch, Cloud
  Run functions (formerly Cloud Functions) for small event handlers. Use GKE
  only with a concrete need.
- **Images:** Artifact Registry (`REGION-docker.pkg.dev/PROJECT/REPO/IMAGE`).
- **Secrets:** Secret Manager, mounted into Cloud Run as env vars or files,
  pinned to a version for reproducible deploys.
- **Databases:** Cloud SQL for Postgres via the Cloud SQL connector or Auth
  Proxy, preferably with IAM database authentication.

## Verify loop

```bash
gcloud config list
gcloud run deploy SERVICE --image IMAGE --region REGION --service-account SA_EMAIL
gcloud run services describe SERVICE --region REGION   # check revision, SA, env, ingress
gcloud run services logs read SERVICE --region REGION --limit 50
# Terraform: terraform fmt -check && terraform validate && terraform plan
```

## Rules that matter

- **One service account per workload**, with only the roles it needs. The
  default compute service account has broad Editor-like access; never run
  services as it.
- Grant roles at the narrowest level (resource > project > folder); avoid
  basic roles (Owner/Editor/Viewer) for workloads.
- Cloud Run: set `--ingress` and authentication deliberately
  (`--no-allow-unauthenticated` for internal services), set concurrency and
  min/max instances, and remember CPU is throttled outside requests unless
  instance-based billing is enabled.
- Enable APIs explicitly in IaC (`google_project_service`); "API not
  enabled" errors are the most common first-deploy failure.
- **Cost:** a budget with alerts on every billing account; set log
  retention/exclusions for noisy logs; set max instances so a traffic spike
  can't run up the bill.

## Changed recently (checked 2026-10-23)

- **Container Registry (`gcr.io`) is shut down.** Images live in Artifact
  Registry; `gcr.io` URLs only work via Artifact Registry gcr.io-domain
  repositories. Update old `gcr.io/...` references in CI and manifests.
- **Cloud Functions are now "Cloud Run functions"**; 2nd-gen functions run
  on Cloud Run, so the Cloud Run limits and IAM apply.

## Pitfalls

- Region mismatches between Cloud Run, Cloud SQL, Artifact Registry and
  buckets, which add latency and egress cost.
- `allUsers` IAM bindings added "to make it work" and never removed.
- Assuming eventual IAM propagation is instant; a fresh grant can take a
  minute or more to apply.

## Sources

- `research/2026-10-23-stack-baseline.md` → Google Cloud section.
