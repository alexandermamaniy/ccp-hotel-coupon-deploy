
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region                   = "us-east-1"
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "jose_account"
}

resource "aws_key_pair" "mtc_auth" {
  key_name   = "mtckey"
  public_key = file("~/.ssh/mtckey.pub")
}



# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = var.vcp_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "terraform-vpc"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "terraform-gateway"
  }
}

# Create a Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr_block
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "terraform-public-subnet"
  }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr_block_2
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "terraform-public-subnet_2"
  }
}


# Create a Route Table for the Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "terraform-public-rt"
  }
}

# Associate the Route Table with the Public Subnet
resource "aws_route_table_association" "public_association" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Associate the Route Table with the Public Subnet
resource "aws_route_table_association" "public_association_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}


# Security Group for EC2 Instance
resource "aws_security_group" "ec2_sg" {
  name        = "ec2_sg"
  description = "Allow SSH and HTTP access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API_REST"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "terraform-ec2-sg"
  }
}

# Provision an EC2 Instance with a Public IP
resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu24_image.id
  key_name                    = aws_key_pair.mtc_auth.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  user_data                   = file("userdata.tpl")
  tags = {
    Name = "TerraformEC2"
  }

  provisioner "local-exec" {
    command = templatefile("linux-ssh-config.tpl", {
      hostname     = self.public_ip,
      user         = "ubuntu",
      identityfile = "~/.ssh/mtckey"
    })
    interpreter = var.host_os == "linux" ? ["/bin/bash", "-c"] : ["Powershell", "-Command"]
  }

  provisioner "local-exec" {
    command = templatefile("environment_variables.tpl", {
      instance   = "house_billing_nat_instance",
      public_ip  = self.public_ip,
      private_ip = self.private_ip,
    })
    interpreter = var.host_os == "linux" ? ["/bin/bash", "-c"] : ["Powershell", "-Command"]
  }

}

# Security Group for RDS MySQL
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow MySQL access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "MySQL"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "terraform-rds-sg"
  }
}

# Create a DB Subnet Group using the public subnet
resource "aws_db_subnet_group" "default" {
  name       = "terraform-db-subnet-group"
  subnet_ids = [aws_subnet.public.id, aws_subnet.public_2.id]

  tags = {
    Name = "terraform-db-subnet-group"
  }
}

# Provision an RDS MySQL Instance (publicly accessible)
resource "aws_db_instance" "default" {
  engine              = var.setting.database.engine
  engine_version      = var.setting.database.engine_version
  multi_az            = var.setting.database.multi_az
  identifier          = var.setting.database.identifier
  username            = var.db_username
  password            = var.db_pawssword
  instance_class      = var.setting.database.instance_class
  allocated_storage   = var.setting.database.allocated_storage
  db_name             = var.setting.database.db_name
  skip_final_snapshot = var.setting.database.skip_final_snapshot
  publicly_accessible    = true
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name = "TerraformRDS"
  }
}
