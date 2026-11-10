variable "aws_region" {
  description = "Região AWS para provisionamento da Loja Veloz (São Paulo)"
  type        = string
  default     = "sa-east-1"
}

variable "environment" {
  description = "Ambiente de execução (staging ou production)"
  type        = string
  default     = "production"
}

variable "cluster_name" {
  description = "Nome do cluster Kubernetes gerenciado (EKS)"
  type        = string
  default     = "loja-veloz-eks-prod"
}

variable "vpc_cidr" {
  description = "Bloco CIDR da VPC isolada da plataforma Pedidos Veloz"
  type        = string
  default     = "10.20.0.0/16"
}

variable "node_desired_capacity" {
  description = "Quantidade inicial de Worker Nodes no Node Group"
  type        = number
  default     = 3
}
