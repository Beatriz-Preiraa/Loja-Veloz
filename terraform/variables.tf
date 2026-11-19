variable "project_name" {
  description = "Nome do projeto na nuvem"
  type        = string
  default     = "loja-veloz"
}

variable "environment" {
  description = "Ambiente de implantacao (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "Regiao onde o cluster sera provisionado"
  type        = string
  default     = "us-east-1"
}

variable "node_desired_capacity" {
  description = "Quantidade desejada de nos workers no cluster Kubernetes"
  type        = number
  default     = 2
}