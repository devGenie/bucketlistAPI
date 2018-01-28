provider "aws" {
    region = "${var.region}"
}

resource "aws_vpc" "terraformmain" {
    cidr_block = "${var.vpc-fullcidr}"
    enable_dns_support = true
    enable_dns_hostname = true
    tags {
        Name = "Sample terraform"
    }
}