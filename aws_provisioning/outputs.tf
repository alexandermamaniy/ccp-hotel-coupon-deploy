output "web_instance_ip" {
  description = "IP SERVER"
  value       = aws_instance.web.public_ip
}

output "rds_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.default.endpoint
}
