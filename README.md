# Cookiecutter aws-ecs-service

Cookiecutter is a tool that creates projects from project templates. **This repository contains an cookiecutter template to deploy a docker container as a fargate service on an existing ECS Cluster.**

## Feautures
-  Supported Git Repository: GitHub.
-  InfraStructure As Code with CloudFormation.
-  GitOps with an embedded CodePipeline to Continuously Deploy both your Application and
   Infrastructure.
 - Support for AutoScaling and Scheduled Scaling.
 - Support for CloudWatch Alerts with SNS Alarm actions.
 - [Native Container Image Scanning in Amazon
   ECR](https://aws.amazon.com/blogs/containers/amazon-ecr-native-container-image-scanning/)
- Support for API Gateway
- Support for X-Ray


### Spring Boot
Out of box the Docker container comes with a Hello World Spring boot installed.
This Spring Boot application is a web application with a REST Api generated using [Spring Initializr](https://start.spring.io/)

Both Maven an Gradle are supported as build tool for your Java application.  

### Spring Boot with Docker
The Spring boot app is setup based on the document: [Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker/)

[jib](https://github.com/GoogleContainerTools/jib) has been chosen to Containerize the Spring boot Application


## Prerequisites

In order to run this cookiecutter template, you need to install following:

#### \*nix an OS X

- python 3 (`check: python3 --version`)
- [Cookiecutter](https://github.com/audreyr/cookiecutter):
	```
	pip3 install cookiecutter
	```
- aws cli (`check: aws --version`)
- make tools (`make --version`)
- docker
- [Amazon ECR Docker Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper)

#### Windows

On Windows, with [chocolatey](https://chocolatey.org) and [sudo](https://chocolatey.org/packages/sudo) installed 

```
sudo choco install python
sudo choco install awscli
pip install cookiecutter
```

#### Required AWS Resources

- **AWS CLI:** you should be logged.
- **An ECS Cluster:** your could use [cookiecutter-aws-ecs-cluster](https://github.com/element7-io/cookiecutter-aws-ecs-cluster)
- **An ALB:** also part of [cookiecutter-aws-ecs-cluster](https://github.com/element7-io/cookiecutter-aws-ecs-cluster)
- **An Artefacts S3 bucket:** this bucket needs to be versioned.
- **An ECR Repository:


### Configuration

**Create a cookiecutter config file containing the configuration for your service.** Cookiecutter will use the values from the config file as defaults when bootstrapping this template.

Find a cookiecutter config file example below:
```
default_context:
    # Project settings
    project_name: hello world
    cloudformation_resource_prefix: helloworld

    # AWS Account Settings
    aws_account_id: 123456789012
    aws_default_region: eu-west-1

    # Non-prod Cluster & ALB settings
    non_prod_cluster_name: some-cluster-name
    non_prod_vpc_id: vpc-8013c2e7
    non_prod_private_subnets: subnet-x,subnet-y,subnet-z
    non_prod_alb_name: some-alb-name
    non_prod_alb_arn: arn:aws:...
    non_prod_alb_security_group: sg-xyz
    non_prod_alb_hosted_zone: Z...
    non_prod_alb_dns: ....elb.amazonaws.com
    non_prod_alb_https_listener_arn: arn:aws:elasticloadbalancing:...

    # Production Cluster & ALB settings
    # Optional, see below for the exact values

    # Service settings
    build_automation_tool: Maven
    service_healthcheck_path: /actuator/info
    main_class: hello.HelloworldApplication
    container_port: 8080
    container_cpu: 512
    container_memory: 1024
    enable_xray: True
    service_discovery_namespace: ""
    deploy_acc: True
    acc_service_dnsname: helloworld.example.com
    acc_custom_domainname: helloworld-api.example.com
    deploy_prod: False

    # Service Auto Scaling settings
    non_prod_minimum_containers: 1
    non_prod_maximum_containers: 2
    prod_minimum_containers: 2
    prod_maximum_containers: 4
    cpu_scale_out_threshold: 60
    cpu_scale_in_threshold: 30
    non_prod_enable_scheduled_scaling: True
    non_prod_timed_scale_in_schedule: cron(0 20 ? * MON-FRI *)
    non_prod_timed_scale_in_min_containers: 0
    non_prod_timed_scale_in_max_containers: 0
    non_prod_timed_scale_out_schedule: cron(0 7 ? * MON-FRI *)
    prod_enable_scheduled_scaling: False

    # Global settings
    artifact_s3_bucket: some-s3-bucket
    alerting_sns_topic: arn:aws:sns:...
    non_prod_ssl_certificate_arn: arn:aws:acm:...
    prod_ssl_certificate_arn: arn:aws:acm:...
```

*Note: depending on the environments in your AWS account you should/could provide empty values for the prod or nonprod variables (don't omit these variables as this will break Cookiecutter, use empty strings as value instead).*

service_log_group (optional): a Custom Clouwdwacht log group name

## Usage

### New application

1. Run cookiecutter in the directory where you usually checkout your git repositories. Cookiecutter will create a new sub-folder in this directory. 

        $ cookiecutter --config-file .cookiecutter_example --no-input -f https://github.com/element7-io/cookiecutter-aws-ecs-service.git
1. Move to the newly created project

        $ cd yet-another-test-project

1. Enable git for this project:

        git init
        git add .
        git commit -m "Initial setup"

1. Create a new GitHub repository.
1. Push your code to GitHub.
1. **To finish the setup read the `README.md` file in the newly created project.**


## Contributing
This cookiecutter template is **Community Driven**, so everybody is free to contribute. Read the [Contributors' Guide](CONTRIBUTING.md) for details on how-to contribute.
