variable "project" {
  type    = string
  default = "ragapi"
}

variable "env" {
  type        = string
  description = "Environment name (dev, prod)"
}

variable "location" {
  type    = string
  default = "japaneast"
}

variable "suffix" {
  type        = string
  description = "Globally-unique suffix for resource names"
}

variable "my_ip" {
  type        = string
  description = "Your public IP, for the Postgres firewall rule"
}
