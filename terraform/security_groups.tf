resource "aws_security_group" "API" {
    name = "API"
    tags {
        Name = "API"
    }

    description = "Only HTTP connections inbound"
    vpc_id = "${aws_vpc.terraformmain.id}"

    ingress {
        from_port = 80
        to_port = 80
        protocol = "TCP"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}