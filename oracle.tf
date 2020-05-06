variable "dbname" {
  type = string
}

variable "region" {
  type = string
  default = "us-east-1"
}

variable "skipFinalSnap" {
  type = bool
  default = true
}

variable "engine" {
  type = string
}

variable "dbversion" {
  type = string
  default = "12.1"
}

variable "user" {
  type = string
  default = "commander"
}

variable "password" {
  type = string
  default = "commander"
}

variable "tier" {
  type = string
  default = "db.t3.micro"
}

variable "storageType" {
  type = string
  default = "gp2"
}

variable "allocatedStorage" {
  type = string
  default = "20"
}

variable "db-security-group" {
  type = string
  default = "oracle-sg"
}

variable "publicAccess" {
  type = string
  default = true
}

variable "vpcId" {
  type = string
  default = "default"
}

provider "aws" {
  profile = "default"
  region = var.region
}

data "aws_vpc" "selected" {
  id = var.vpcId
}

data "aws_subnet_ids" "vpcsubnets" {
  vpc_id = data.aws_vpc.selected.id
}

data "aws_subnet" "vpcsubnet" {
  for_each = data.aws_subnet_ids.vpcsubnets.ids
  id       = each.value
}

resource "aws_db_parameter_group" "pg" {
  name   = "tf-pg-mysql"
  family = "${var.engine}-${var.dbversion}"

  parameter {
    name  = "open_cursors"
    value = "1000"
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "db-subnet-group"
  subnet_ids = [ for subnet in data.aws_subnet.vpcsubnet : subnet.id ]
}

data "aws_security_group" "selected" {
  name = var.db-security-group
  vpc_id = var.vpcId
}

resource "aws_db_instance" "database" {
  identifier           = var.dbname
  allocated_storage    = var.allocatedStorage
  #max_allocated_storage = 1000
  storage_type         = var.storageType
  engine               = var.engine
  engine_version       = var.dbversion
  instance_class       = var.tier
  username             = var.user
  password             = var.password
  license_model        = "license-included"
  parameter_group_name = aws_db_parameter_group.pg.name
  db_subnet_group_name = aws_db_subnet_group.default.name
  character_set_name = "UTF8"
  skip_final_snapshot = var.skipFinalSnap
  final_snapshot_identifier = var.dbname
  publicly_accessible = var.accessType
  vpc_security_group_ids = [
    data.aws_security_group.selected.id
  ]
}

output "db-endpoint" {
  value = aws_db_instance.database.endpoint
}