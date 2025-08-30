
variable "host_os" {
  type    = string
  default = "linux"
}

variable "vcp_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr_block" {
  type        = string
  description = "Public subnet cidr blocks definition"
  default     = "10.0.1.0/24"
}

variable "public_subnet_cidr_block_2" {
  type        = string
  description = "Public subnet cidr blocks definition"
  default     = "10.0.2.0/24"
}

variable "setting" {
  description = "Configuration settings"
  type        = map(any)
  default = {
    database = {
      engine              = "mysql"
      engine_version      = "8.0"
      multi_az            = false
      identifier          = "house-billing-db-instance"
      instance_class      = "db.t3.micro"
      allocated_storage   = 200
      db_name             = "hoteldb"
      skip_final_snapshot = true
    }
  }
}

variable "db_username" {
  type        = string
  description = "Database master user password"
  sensitive   = true
}

variable "db_pawssword" {
  type        = string
  description = "Database master user password"
  sensitive   = true
}

variable "my_ip" {
  type        = string
  description = "IP address to allow SSH access"
  sensitive   = true
}
