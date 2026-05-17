ecs_cluster_name = "rbnlp-cluster"
ecs_service_name = "rbnlp-service"

security_group_ids = ["sg-010be622476101800"]

subnet_ids = [
  "subnet-03d7da34a0cf63f1f",
  "subnet-0af32799fdf854ccf",
  "subnet-0d7eb5216b3672fbb",
]

vpc_id = "vpc-01304652baeb25843"

task_definition_arn = "arn:aws:ecs:eu-west-2:423623828513:task-definition/rbnlp:5"
