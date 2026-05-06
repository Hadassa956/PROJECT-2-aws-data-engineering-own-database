provider "aws" {
  region = "us-east-1"
}

# bucket for save terraform state archives
resource "aws_s3_bucket" "terraform_state" {
  bucket = "tfstate-backend-hadassa-2026"
}

#Activating the versioning
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# DynamoDB table for lock
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "tabela-lock-terraform-hadassa"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
