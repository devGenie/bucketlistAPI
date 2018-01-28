resource "aws_instance" "jenkins_app" {
    ami = "${data.aws_ami.bucketlist_image.id}"
    instance_type = "t2.micro"
    associate_public_ip_address = "true"
    subnet_id = "${aws_subnet.PublicSubnet.id}"
    vpc_security_group_ids = ["${aws_security_group.API.id}"]
    tags {
        Name = "bucketListAPI"
    }
}