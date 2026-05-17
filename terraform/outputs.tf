output "task_definition_arn" {
  description = "The ARN of the managed task definition."
  value       = aws_ecs_task_definition.main.arn
}

output "cluster_name" {
  description = "The created ECS cluster."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service" {
  description = "The created service."
  value       = aws_ecs_service.main.name
}

output "load_balancer" {
  description = "The created load balancer."
  value       = aws_lb.main.arn
}

output "listener" {
  description = "The created listener."
  value       = aws_lb_listener.http.arn
}

output "target_group" {
  description = "The created target group."
  value       = aws_lb_target_group.main.arn
}
