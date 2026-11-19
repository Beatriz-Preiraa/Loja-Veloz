output "cluster_name" {
  description = "Nome do cluster Kubernetes provisionado"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Endpoint da API do Kubernetes"
  value       = module.eks.cluster_endpoint
}

output "vpc_id" {
  description = "ID da VPC criada para o ambiente"
  value       = module.vpc.vpc_id
}