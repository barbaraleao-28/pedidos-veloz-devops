# ============================================================================
# 1. REDE ISOLADA (VPC Multi-AZ para Alta Disponibilidade)
# ============================================================================
resource "aws_vpc" "pedidos_veloz_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.cluster_name}-vpc"
  }
}

resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.pedidos_veloz_vpc.id
  cidr_block        = "10.20.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name                              = "${var.cluster_name}-private-a"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.pedidos_veloz_vpc.id
  cidr_block        = "10.20.2.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name                              = "${var.cluster_name}-private-b"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# ============================================================================
# 2. CLUSTER KUBERNETES GERENCIADO (Amazon EKS + Node Group)
# ============================================================================
resource "aws_iam_role" "eks_cluster_role" {
  name = "${var.cluster_name}-control-plane-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_eks_cluster" "pedidos_veloz" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.30"

  vpc_config {
    subnet_ids              = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
    endpoint_private_access = true
    endpoint_public_access  = true
  }
}

# ============================================================================
# 3. BANCO DE DADOS GERENCIADO (Amazon RDS PostgreSQL 16 Multi-AZ)
# ============================================================================
resource "aws_db_subnet_group" "postgres_subnets" {
  name       = "${var.cluster_name}-db-subnet-group"
  subnet_ids = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
}

resource "aws_db_instance" "pedidos_postgres" {
  identifier             = "veloz-postgres-${var.environment}"
  engine                 = "postgres"
  engine_version         = "16.3"
  instance_class         = "db.t4g.medium"
  allocated_storage      = 50
  max_allocated_storage  = 200
  storage_encrypted      = true
  multi_az               = true
  db_name                = "pedidos_veloz"
  username               = "veloz_admin"
  manage_master_user_password = true
  db_subnet_group_name   = aws_db_subnet_group.postgres_subnets.name
  skip_final_snapshot    = false
}
