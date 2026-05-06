# 1. Permissões (IAM Role) para o Glue acessar o S3
resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role-hadassa"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Anexando políticas de acesso da AWS na Role
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# 2. Fazendo upload do script PySpark para a Landing Zone
resource "aws_s3_object" "etl_script" {
  bucket = aws_s3_bucket.landing_zone.id
  key    = "scripts/etl_script.py"
  source = "etl_script.py" # Aponta para o seu arquivo Python local
  etag   = filemd5("etl_script.py")
}

# 3. O Job do AWS Glue
resource "aws_glue_job" "etl_clientes" {
  name     = "job-customers-transformation"
  role_arn = aws_iam_role.glue_role.arn
  
  # Versão e tipo de máquina (G.1X é a padrão)
  glue_version      = "4.0"
  worker_type       = "G.1X" 
  number_of_workers = 2

  command {
    script_location = "s3://${aws_s3_bucket.landing_zone.id}/scripts/etl_script.py"
    python_version  = "3"
  }

  # Passando os nomes dinâmicos para o script PySpark
  default_arguments = {
    "--BUCKET_LANDING"   = aws_s3_bucket.landing_zone.id
    "--BUCKET_PROCESSED" = aws_s3_bucket.processed.id
  }
}

# 4. Banco de Dados Virtual (Glue Data Catalog)
resource "aws_glue_catalog_database" "db_clientes" {
  name = "db_clientes_portfolio"
}

# 5. O Crawler (Rastreador que lê o Parquet e cria a tabela no Athena)
resource "aws_glue_crawler" "crawler_clientes" {
  database_name = aws_glue_catalog_database.db_clientes.name
  name          = "crawler-clientes-curated"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    # Aponta exatamente para a pasta onde o seu Job salvou os Parquets
    path = "s3://${aws_s3_bucket.processed.id}/clientes_curated/"
  }
}