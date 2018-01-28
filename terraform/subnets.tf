resource "aws_subnet" "PublicSubnet" {
    vpc_id = "${aws_vpc.terraformmain.id}"
    cidr_block = "${var.Subnet-public}"
    tags {
        Name = "Public Subnet"
    }
    availability_zone = "us-east-2a"
}

resource "aws_route_table_association" "PublicRT" {
    subnet_id = "${aws_subnet.PublicSubnet.id}"
    route_table_id = "${aws_route_table.public.id}"
}