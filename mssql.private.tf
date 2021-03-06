variable "project" {
  type = string
}

variable "region" {
  type = string
  default = "us-east1"
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


provider "google-beta" {
  credentials = file("account.json")
  project     = var.project
  region      = var.region
}

provider "google" {
  credentials = file("account.json")
  project     = var.project
  region      = var.region
}

data "google_compute_network" "private_network" {
  name = "default"
  project = var.project
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = data.google_compute_network.private_network.self_link
  project = var.project
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = data.google_compute_network.private_network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "google_project_service" "networking" {
  project = var.project
  service = "servicenetworking.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "sqladmin" {
  project = var.project
  service = "sqladmin.googleapis.com"

  disable_dependent_services = true
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "random_id" "db_root_paas_suffix" {
  byte_length = 8
}

resource "google_sql_database_instance" "gcp-cloud-sql" {
  provider = google-beta
  project = var.project
  name   = "${var.dbname}-${random_id.db_name_suffix.hex}"
  region = var.region
  database_version = var.dbversion
  root_password = random_id.db_root_paas_suffix.hex
  depends_on = [ 
    google_service_networking_connection.private_vpc_connection,
    google_project_service.networking,
    google_project_service.sqladmin
  ]

  settings {
    tier = var.tier
    ip_configuration {
      ipv4_enabled    = false
      private_network = data.google_compute_network.private_network.self_link
    }
  }
}

resource "google_sql_user" "users" {
  name     = "commander"
  instance = google_sql_database_instance.gcp-cloud-sql.name
  host     = "%"
  password = "commander"
  project = var.project
}

output "db_private_ip" {
  value       = google_sql_database_instance.gcp-cloud-sql.private_ip_address
}
