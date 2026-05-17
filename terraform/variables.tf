variable "ecs_cluster_name" {
  description = "Name of the existing ECS cluster"
  type        = string
  default     = "rbnlp-cluster"
}

variable "ecs_service_name" {
  description = "Name for the ECS service"
  type        = string
  default     = "rbnlp-service"
}

variable "security_group_ids" {
  description = "Security group IDs for the load balancer and ECS service"
  type        = list(string)
  default     = ["sg-010be622476101800"]
}

variable "subnet_ids" {
  description = "Subnet IDs for the load balancer and ECS service"
  type        = list(string)
  default     = ["subnet-03d7da34a0cf63f1f", "subnet-0af32799fdf854ccf", "subnet-0d7eb5216b3672fbb"]
}

variable "vpc_id" {
  description = "VPC ID where resources are deployed"
  type        = string
  default     = "vpc-01304652baeb25843"
}

variable "task_definition_family" {
  description = "ECS task definition family name (latest active revision is used automatically)"
  type        = string
  default     = "rbnlp"
}
