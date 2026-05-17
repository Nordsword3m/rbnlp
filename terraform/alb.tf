resource "aws_lb" "main" {
  name               = "rbnlp"
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets            = var.subnet_ids
}

resource "aws_lb_target_group" "main" {
  name        = "rbnlp-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
  }

  stickiness {
    type    = "lb_cookie"
    enabled = false
  }

  deregistration_delay = 300
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}
