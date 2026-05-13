terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "gcp_project_id" {
  type        = string
  description = "GCP project ID for Unified MCP Studio infrastructure"
}

variable "region" {
  type        = string
  description = "Primary region"
  default     = "us-central1"
}

provider "google" {
  project = var.gcp_project_id
  region  = var.region
}

resource "google_compute_network" "mcpstudio_vpc" {
  name                    = "mcpstudio-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "mcpstudio_subnet" {
  name          = "mcpstudio-subnet"
  ip_cidr_range = "10.10.0.0/16"
  region        = var.region
  network       = google_compute_network.mcpstudio_vpc.id
}
