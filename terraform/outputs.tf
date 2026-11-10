output "vpc_id" {
  description = "ID da VPC criada para a Loja Veloz"
  value       = aws_vpc.pedidos_veloz_vpc.id
}

output "eks_cluster_endpoint" {
  description = "Endpoint do Control Plane do Kubernetes (EKS)"
  value       = aws_eks_cluster.pedidos_veloz.endpoint
}

output "rds_postgres_endpoint" {
  description = "Host do banco de dados PostgreSQL Multi-AZ"
  value       = aws_db_instance.pedidos_postgres.address
}
