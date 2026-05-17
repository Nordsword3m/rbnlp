data "aws_ecs_cluster" "main" {
  cluster_name = var.ecs_cluster_name
}

resource "aws_ecs_task_definition" "main" {
  family                   = var.task_definition_family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = var.execution_role_arn

  container_definitions = jsonencode([
    {
      name  = "rbnlp"
      image = var.container_image
      portMappings = [
        {
          containerPort = 80
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/rbnlp"
          "awslogs-region"        = "eu-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "main" {
  name                    = var.ecs_service_name
  cluster                 = data.aws_ecs_cluster.main.arn
  task_definition         = aws_ecs_task_definition.main.arn
  scheduling_strategy     = "REPLICA"
  desired_count           = 1
  platform_version        = "LATEST"
  enable_ecs_managed_tags = true
  enable_execute_command  = false

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    base              = 0
    weight            = 1
  }

  network_configuration {
    assign_public_ip = true
    security_groups  = var.security_group_ids
    subnets          = var.subnet_ids
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = "rbnlp"
    container_port   = 80
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  depends_on = [aws_lb_listener.http]
}
