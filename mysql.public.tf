variable "project" {
  type = string
}

variable "region" {
  type = string
}

variable "dbname" {
  type = string
}

variable "dbversion" {
  type = string
  default = "MYSQL_5_7"
}

variable "tier" {
  type = string
  default = "db-n1-standard-1"
}


provider "google" {
  credentials = file("account.json")
  project     = var.project
  region      = var.region
}

resource "google_project_service" "project" {
  project = var.project
  service = "sqladmin.googleapis.com"

  disable_dependent_services = true
}

locals {
  ip_addr = ["0.0.0.0/0"]
}


resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "gcp-cloud-sql" {
  name             = "${var.dbname}-${random_id.db_name_suffix.hex}"
  database_version = var.dbversion
  region           = var.region

  settings {
    tier = var.tier
    ip_configuration {
      dynamic "authorized_networks" {
        for_each = local.ip_addr
        iterator = ip_addr
        content {
          name  = "ip_addr-${ip_addr.key}"
          value = ip_addr.value
        }
      }
    }
  }
  depends_on = [
    google_project_service.project
  ]
}

resource "google_sql_user" "users" {
  name     = "commander"
  instance = google_sql_database_instance.gcp-cloud-sql.name
  host     = "%"
  password = "commander"
  project = var.project
}

output "db_public_ip" {
  value       = google_sql_database_instance.gcp-cloud-sql.public_ip_address
}
