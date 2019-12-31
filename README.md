# Cookiecutter aws-ecs-service

Cookiecutter is a tool that creates projects from project templates. **This repository contains an cookiecutter template to deploy a docker container as a fargate service on an existing ECS Cluster.**

### Prerequisites

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

#### Windows

On Windows, with [chocolatey](https://chocolatey.org) and [sudo](https://chocolatey.org/packages/sudo) installed 

```
sudo choco install python
sudo choco install awscli
pip install cookiecutter
```

#### Required AWS Resources

- **AWS CLI:** you should be logged in (using onelogin).
- **An ECS Cluster:** your could use https://bitbucket.org/persgroep/cookiecutter-aws-ecs-cluster
- **An ALB:** also part of https://bitbucket.org/persgroep/cookiecutter-aws-ecs-cluster
- [Lambda for CloudWatch Custom Resources](https://bitbucket.org/persgroep/lucifer/src/master/cf_custom_resources/)
- **Artefacts S3 bucket:** this bucket needs to be versioned.
- **Logs bucket stack:** created from [https://bitbucket.org/persgroep/aws-iac-modules/src/master/cloudformation/storage/s3_log_bucket.yaml](https://bitbucket.org/persgroep/aws-iac-modules/src/master/cloudformation/storage/s3_log_bucket.yaml)
- **IAM user for the Bitbucket pipeline**
	- This user should have only **"Programmatic access"** and **NO** "AWS Management Console access".
	- The user should have only write access to your artefacts bucket.


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
    squad_name: ateam

    # Non-prod Cluster & ALB settings
    non_prod_cluster_name: shared1-nonprod-cluster-cf
    non_prod_vpc_id: vpc-04ddb062
    non_prod_private_subnets: subnet-858936cd,subnet-3303ea69,subnet-be5ef0d8
    non_prod_alb_name: shared1-nonprod-public-alb-cf
    non_prod_alb_arn: arn:aws:elasticloadbalancing:eu-west-1:400007416746:loadbalancer/app/shared1-nonprod-public-alb-cf/e3c9d44c9873bfc2
    non_prod_alb_security_group: sg-0454ee9358510ed7d
    non_prod_alb_hosted_zone: Z76H9KK093R5T2
    non_prod_alb_dns: shared1-nonprod-public-alb-cf-515606587.eu-west-1.elb.amazonaws.com
    non_prod_alb_https_listener_arn: arn:aws:elasticloadbalancing:eu-west-1:400007416746:listener/app/shared1-nonprod-public-alb-cf/e3c9d44c9873bfc2/6851af0e7c137fe7

    # Production Cluster & ALB settings
    prod_cluster_name: shared1-prod-cluster-cf
    prod_vpc_id: vpc-04ddb062
    prod_private_subnets: subnet-858936cd,subnet-3303ea69,subnet-be5ef0d8
    prod_alb_name: shared1-prod-public-alb-cf
    prod_alb_arn: arn:aws:elasticloadbalancing:eu-west-1:400007416746:loadbalancer/app/shared1-prod-public-alb-cf/e3c9d44c9873bfc2
    prod_alb_security_group: sg-0987ee9358510ee0o
    prod_alb_hosted_zone: Z8Hk89YJN6H7U5
    prod_alb_dns: shared1-prod-public-alb-cf-515606587.eu-west-1.elb.amazonaws.com
    prod_alb_https_listener_arn: arn:aws:elasticloadbalancing:eu-west-1:400007416746:listener/app/shared1-prod-public-alb-cf/e3c9d44c9873bfc2/6851af0e7c137fe7

    # Service settings
    build_automation_tool: Maven
    service_healthcheck_path: /actuator/info
    service_log_group: /ateam/${EnvironmentName}/ApplicationLog
    main_class: be.persgroep.SomeApplication
    container_port: 8080
    container_cpu: 512
    container_memory: 1024
    enable_xray: True
    service_discovery_namespace: ""
    test_service_dnsname: helloworld-test.ateam.persgroep.cloud
    test_custom_domainname: helloworld-test-api.ateam.persgroep.cloud
    deploy_test: True
    acc_service_dnsname: helloworld-acc.ateam.persgroep.cloud
    acc_custom_domainname: helloworld-acc-api.ateam.persgroep.cloud
    deploy_acc: True
    prod_service_dnsname: helloworld-prod.ateam.persgroep.cloud
    prod_custom_domainname: helloworld-prod-api.ateam.persgroep.cloud
    deploy_prod: True

    # Pipeline Settings
    enable_pipeline_approvals: True
    approvals_notification_topic: arn:aws:sns:eu-west-1:400007416746:codepipeline-approvals

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

    # API Gateway settings
    enable_api_gateway: True
    alb_secret: s0m3s3cr3t

    # Global settings
    artifact_s3_bucket: dpp-artifacts-123456789012-eu-west-1-cfn
    alerting_sns_topic: arn:aws:sns:eu-west-1:123456789012:CloudWatchSns2HipChatLambda-cf
    non_prod_ssl_certificate_arn: arn:aws:acm:eu-west-1:400007416746:certificate/f5081dc0-7758-4385-991a-ea6fb3cd2c12
    prod_ssl_certificate_arn: arn:aws:acm:eu-west-1:400007416746:certificate/f5081dc0-7758-4385-991a-ea6fb3cd2c12
```

*Note: depending on the environments in your AWS account you should/could provide empty values for the prod or nonprod variables (don't omit these variables as this will break Cookiecutter, use empty strings as value instead).*


## Usage

### New application

1. Run cookiecutter in the directory where you usually checkout your git repo's. Cookiecutter will create a new sub-folder in this directory. You'll be 
prompted with a number of questions to help bootstrapping the new project.

        $ cookiecutter --config-file .cookiecutter_service_xyz --no-input -f git@bitbucket.org:persgroep/cookiecutter-java-docker.git
1. Move to the newly created project

        $ cd yet-another-test-project

1. Enable git for this project:

        git init
        git add .
        git commit -m "Initial setup"

1. Create a new repository in Bitbucket.

1. Push your code to BitBucket.

        git remote add origin git@bitbucket.org:persgroep/yet-another-test-project.git
        git push -u origin master

1. Enable **Bitbucket pipelines** for your new repository.
    - Enable pipelines:`Settings` > `Pipelines` > `Settings` > Enable Pipelines
    - Add environment variables:
 		- `Settings` > `Pipelines` > `Repository variables` and add:
        	- `AWS_ACCESS_KEY_ID`
        	- `AWS_SECRET_ACCESS_KEY` (as secured variable).
        	- `AWS_DEFAULT_REGION` (most likely 'eu-west-1')
        	- In case your dependencies are stored in Artifactory, also add `ARTIFACTORY_USER` and `ARTIFACTORY_PASSWORD` (as secured variable).

1. Deploy the Pipeline. (this step also creates the ECR repository to contain the docker images).

        make deploy-pipeline
        
	***Important note: this is a typical "chicken or egg" case. The AWS CodePipeline will fail initially because of a missing artefact. This is normal! Running the Bitbucket pipeline will create the missing artefact and fix the CodePipeline.***
	
1. Push a change to Bitbucket to trigger the Bitbucket pipeline (which will then trigger the AWS CodePipeline). The AWS CodePipeline should now create your ECS cluster(s). 

1. Now, your service should be available at **[https://{project-service-dns-name}/actuator/info](https://{project-service-dns-name}/actuator/info)**. (e.g. [https://test-project.saw.persgroep.cloud/actuator/info](https://test-project.saw.persgroep.cloud/actuator/info))


### Existing Gradle application

To integrate AWS resources into an existing application, execute following steps.

1. Clone the application's existing repository locally.

	```
	$ git clone git@bitbucket.org:persgroep/johan-cookiecutter-test-project.git
	```
1. Create a new branch

	```
	$ git checkout -b feature/cookiecutter
	```
	
1. Run cookiecutter in the directory where the application was cloned. As project slug 
be sure to enter the directory name of the existing repository.

	```
	$ cookiecutter -f git@bitbucket.org:persgroep/cookiecutter-java-docker.git
	...
	project_slug [...]: johan-cookiecutter-test-project
	...
	```
1. Check the output of cookiecutter for files that cookiecutter would have instantiated, but that already existed in the project. ```git status``` is your friend.

1. Commit the changes and push the code to bitbucket.
	
	```
	git push -u origin feature/cookiecutter
	```

1. Enable **Bitbucket pipelines** for your new repository.
    - Enable pipelines:`Settings` > `Pipelines` > `Settings` > Enable Pipelines
    - Add environment variables:
 		- `Settings` > `Pipelines` > `Repository variables` and add:
        	- `AWS_ACCESS_KEY_ID`
        	- `AWS_SECRET_ACCESS_KEY` (as secured variable).
        	- `AWS_DEFAULT_REGION` (most likely 'eu-west-1')
        	- In case your dependencies are stored in Artifactory, also add `ARTIFACTORY_USER` and `ARTIFACTORY_PASSWORD` (as secured variable).

1. Deploy the Pipeline. (this step also creates the ECR repository to contain the docker images).
	```
	make deploy-pipeline	
	```
	
### Existing Maven application

##### Pre-requisites

- Maven 3
- POM.xml
    * `<packaging>jar</packaging>`
    * parent is Spring cloud : e.g. (check version)
   ~~~
    <parent>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-parent</artifactId>
        <version>Camden.SR5</version>
    </parent>
    ~~~
	
    * only 1 JAR file may exist with the same name (see Dockerfile)
    * remove POM references to as-procs / on-premise servers
    * remove profiles dev / test / acc / prod (Docker uses Springboot's properties)
    
- all system and environment properties must be moved to the Springboot properties files (in /resources)
- remove any "webapp" JBoss files
- remove /README.md (will be replaced with Cookie-Cutter's generated doc)

##### Steps

1. Clone the application's existing repository locally.

	```
	$ git clone git@bitbucket.org:persgroep/johan-cookiecutter-test-project.git
	```
1. Create a new branch

	```
	$ git checkout -b feature/cookiecutter
	```
1. Run cookiecutter in the directory where the application was cloned. As project slug 
be sure to enter the directory name of the existing repository.

	```
	$ cookiecutter -f git@bitbucket.org:persgroep/cookiecutter-java-docker.git
	...
	project_slug [...]: johan-cookiecutter-test-project
	...
	```
1. Check the output of cookiecutter for files that cookiecutter would have instantiated, but that already existed in the project. ```git status``` is your friend.

1. Commit the changes and push the code to bitbucket.
	
	```
	git push -u origin feature/cookiecutter
	```

1. Update the generated files if you have more than 1 module; see `Multi-modules project adjustments`.

1. Enable **Bitbucket pipelines** for your new repository.
    - Enable pipelines:`Settings` > `Pipelines` > `Settings` > Enable Pipelines
    - Add environment variables:
 		- `Settings` > `Pipelines` > `Repository variables` and add:
        	- `AWS_ACCESS_KEY_ID`
        	- `AWS_SECRET_ACCESS_KEY` (as secured variable).
        	- `AWS_DEFAULT_REGION` (most likely 'eu-west-1')
        	- In case your dependencies are stored in Artifactory, also add `ARTIFACTORY_USER` and `ARTIFACTORY_PASSWORD` (as secured variable).

1. Deploy the Pipeline. (this step also creates the ECR repository to contain the docker images).
	```
	make deploy-pipeline	
	```

#### Multi-modules project adjustments for Maven

1. File 'Dockerfile'

    * adapt the source JAR folder, e.g.
        * generated: `ADD target/{{ cookiecutter.project_slug }}*.jar /home/appuser/app.jar`
        * in submodule 'my-module': `ADD `**my-module**`/target/{{ cookiecutter.project_slug }}*.jar /home/appuser/app.jar`



## Contributing
This cookiecutter template is **Community Driven**, so everybody within De Persgroep is free to contribute. Read the [Contributors' Guide](CONTRIBUTING.md) for details on how-to contribute.


## Architecture

### Deployment Pipeline (Bitbucket -> CodePipeline)
If triggered the bitbucket pipelines will perform the following steps:

* Build the java app (using Maven or Gradle)
* Build the docker image
* Push the docker image to an ECR repository
* Create a zipfile containing
	- the CloudFormation template used to deploy all resources on AWS  
	- a directory (`config/`) with one configuration file per environment that will be used by CodePipeline when deploying the CloudFormation templates as stack
* Upload the above zipfile onto the artefact S3 bucket 
* The uploaded zip file on S3 will trigger the start of CodePipeline in AWS
