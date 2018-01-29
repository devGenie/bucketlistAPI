provider "aws" {
    region = "${var.region}"
    access_key = "${var.secret_id}"
    secret_key = "${var.secret_key}"
}

resource "aws_vpc" "terraformmain" {
    cidr_block = "${var.vpc-fullcidr}"
    enable_dns_support = true
    enable_dns_hostnames = true
    tags {
        Name = "Sample terraform"
    }
}