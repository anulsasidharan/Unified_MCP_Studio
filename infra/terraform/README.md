# GCP baseline (Phase 8 — TASKS.md SI 26)

This directory contains a **minimal Terraform skeleton** for a dedicated VPC. Extend with Cloud SQL, Memorystore, buckets, and IAM per `docs/GCP-ARCHITECTURE-DESIGN.md` before applying in production.

## Usage

```bash
cd infra/terraform
terraform init
terraform plan -var="gcp_project_id=YOUR_PROJECT"
```

Applying infrastructure requires authenticated `gcloud` / workload identity and project billing enabled.
