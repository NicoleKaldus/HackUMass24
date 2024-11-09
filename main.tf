provider "aws" {
  region = "us-east-1"  # or any AWS region you prefer
}

# Define a Security Group for MongoDB
resource "aws_security_group" "mongodb_sg" {
  name_prefix = "mongodb-sg"

  # Allow SSH access from your IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow MongoDB port from a specific CIDR block or IP range
  ingress {
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Change to allow wider access if needed
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define an EC2 instance to host MongoDB
resource "aws_instance" "mongodb_instance" {
  ami           = "ami-0b0ea68c435eb488d"  # Amazon Linux 2 AMI ID (use latest)
  instance_type = "t2.micro"
  key_name      = "hackathon"       # Replace with your SSH key name
  security_groups = [aws_security_group.mongodb_sg.name]

  tags = {
    Name = "MongoDB-Server"
  }

  # Run a script to install MongoDB on startup
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install -y mongodb4.0
              systemctl start mongod
              systemctl enable mongod
              EOF
}
