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

variable "shared_rg" {
  type        = string
  description = "Resource group holding the shared Azure OpenAI resource"
  default     = "rg-shared"
}

variable "openai_name" {
  type        = string
  description = "Name of the existing Azure OpenAI resource"
}

