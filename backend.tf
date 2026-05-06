terraform {
  backend "s3" {
    bucket = "tfstate-backend-hadassa-2026"

    key = "customers-project/terrafom.tfstate"

    region = "us-east-1"

    encrypt = true

    use_lockfile = true
  }
}