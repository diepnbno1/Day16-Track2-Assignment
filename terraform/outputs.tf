output "bastion_public_ip" {
  value = try(aws_instance.bastion[0].public_ip, null)
}

output "alb_dns_name" {
  value       = aws_lb.ai_alb.dns_name
  description = "The DNS name of the ALB to access the inference endpoint"
}

output "endpoint_url" {
  value = "http://${aws_lb.ai_alb.dns_name}/v1/completions"
}

output "gpu_private_ip" {
  value = aws_instance.gpu_node.private_ip
}

output "cpu_instance_id" {
  value       = aws_instance.gpu_node.id
  description = "CPU benchmark instance ID for AWS Systems Manager"
}
