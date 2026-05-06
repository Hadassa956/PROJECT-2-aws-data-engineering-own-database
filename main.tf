resource "aws_s3_bucket" "landing_zone" {
  bucket = "${var.project_name}-landing-zone"
}

resource "aws_s3_bucket" "processed" {
  bucket = "${var.project_name}-processed"
}