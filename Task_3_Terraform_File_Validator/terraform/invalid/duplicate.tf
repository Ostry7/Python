resource "aws_s3_bucket" "example" {
  bucket = "duplicate-bucket"
}

resource "aws_s3_bucket" "example" {  # DUPLIKAT!
  bucket = "duplicate-too"
}
