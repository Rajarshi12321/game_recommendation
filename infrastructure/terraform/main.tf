resource "aws_instance" "Game_Recommender" {
  ami           = var.ami_os  # Ubuntu 24.04 LTS AMI ID for ap-south-1, change accordingly
  instance_type = "t2.micro"
  tags = {
    Name = var.instance_name
  }

  # # Open all traffic to the instance
  # security_groups = ["default"]

  # Configure block device mapping
  root_block_device {
    volume_type           = "gp3"  # Change to the desired volume type, e.g., gp2
    volume_size           = var.volume_size     # Specify the size in GB
    delete_on_termination = true   # Set to false if you want to keep the volume after instance termination
  }
}

data "aws_security_group" "default" {
  for_each = aws_instance.Game_Recommender.security_groups

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

resource "aws_security_group_rule" "custom_tcp_ingress" {
  for_each = data.aws_security_group.default

  type                     = "ingress"
  from_port                = var.post_number
  to_port                  = var.post_number
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = each.value.id
}

resource "aws_security_group_rule" "custom_22_tcp_ingress" {
  for_each = data.aws_security_group.default

  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = each.value.id
}

resource "aws_security_group_rule" "custom_80_tcp_ingress" {
  for_each = data.aws_security_group.default

  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = each.value.id
}

resource "aws_security_group_rule" "custom_443_tcp_ingress" {
  for_each = data.aws_security_group.default

  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = each.value.id
}


resource "aws_ecr_repository" "Game_Recommender" {
  name = var.aws_ecr_repository_name
  tags = {
    Name = "latest"
  }
}



output "ec2_public_ipv4" {
  description = "EC2 Public IP"
  value = aws_instance.Game_Recommender.public_ip
}

output "ecr_repository_uri" {
  description = "URI of ECR Repository"
  value = aws_ecr_repository.Game_Recommender.repository_url
}