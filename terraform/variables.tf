variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "bastion_ssh_cidr" {
  description = "Public IPv4 CIDR allowed to SSH to the Bastion; must be the laptop IPv4 address with /32"
  type        = string
  nullable    = false

  validation {
    condition = can(cidrhost(var.bastion_ssh_cidr, 0)) && can(
      regex("^([0-9]{1,3}\\.){3}[0-9]{1,3}/32$", var.bastion_ssh_cidr)
    )
    error_message = "bastion_ssh_cidr must be a public IPv4 address in /32 notation, for example 203.0.113.10/32."
  }
}

variable "hf_token" {
  description = "Hugging Face Token for gated models (like Gemma)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "model_id" {
  description = "Hugging Face Model ID to serve"
  type        = string
  default     = "google/gemma-4-E2B-it"
}

variable "enable_gpu" {
  description = "Set to true to deploy the optional GPU + vLLM LLM inference node instead of the default CPU + LightGBM node"
  type        = bool
  default     = false
}

variable "cpu_instance_type" {
  description = "Instance type for the default CPU (LightGBM) compute node"
  type        = string
  default     = "t3.medium"
}

variable "gpu_instance_type" {
  description = "Instance type for the optional GPU (vLLM) compute node"
  type        = string
  default     = "g4dn.xlarge"
}
