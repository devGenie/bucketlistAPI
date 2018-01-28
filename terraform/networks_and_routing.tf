data "aws_availability_zones" "available" {}

/* EXTERNAL NETWORK, IG, ROUTE TABLE */
 resource "aws_internet_gateway" "igw" {
     vpc_id = "${aws_vpc.terraformmain.id}"
     tags {
         Name = "Terraform generated IGW for bucketlist"
     }
 }

 resource "aws_network_acl" "all" {
     vpc_id = "${aws_vpc.terraformmain.id}"
     egress {
         protocol = "-1"
         rule_no = 2
         action = "allow"
         cidr_block = "0.0.0.0/0"
         from_port = 0
         to_port = 0
     }
     ingress {
         protocol = "-1"
         rule_no = 1
         action = "allow"
         cidr_block = "0.0.0.0/0"
         from_port = 0
         to_port = 0
     }
     tags {
         Name = "Bucketlist Open ACL"
     }
 }

 resource "aws_route_table" "public" {
     vpc_id = "${aws_vpc.terraformmain.id}"
     tags {
         Name = "Public"
     }
     route {
         cidr_block = "0.0.0.0/0"
         gateway_id = "${aws_internet_gateway}"
     }
 }