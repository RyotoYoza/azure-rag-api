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

variable "image_tag" {
  type    = string
  default = "v1"
}

variable "openai_api_version" {
  type = string
}

variable "chat_deployment" {
  type    = string
  default = "gpt-5-mini"
}

variable "embed_deployment" {
  type    = string
  default = "text-embedding-3-small"
}
