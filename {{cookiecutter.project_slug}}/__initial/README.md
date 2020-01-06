# {{ cookiecutter.project_name }}

## Requirements
* python 3 (check (V3.7): `pip3 --version`) 
* aws cli (check: `aws --version`)
* docker (+ CLI) (check: docker --version) : https://docs.docker.com/install/#supported-platforms

## Resources

* ECR repository: {{ cookiecutter.aws_account_id }}.dkr.ecr.{{ cookiecutter.aws_default_region }}.amazonaws.com/{{ cookiecutter.project_slug }}-repo
* CodePipeline: {{ cookiecutter.project_slug }}-pipeline-cfn
* Artifact S3 bucket: {{ cookiecutter.artifact_s3_bucket }}

The ECR repository and CodePipeline resources are automatically created when the `cfn-pipeline.yaml` are deployed onto AWS (`./make.sh deploy-pipeline`).

## Usage

This repository contains the {{ cookiecutter.project_name }} service. 
It contains the necessary cloudformation templates and configuration files to be deployed on AWS. 
The repository was bootstrapped using the [Cookiecutter ECS service template](https://github.com/element7-io/cookiecutter-aws-ecs-service).

Using bitbucket pipelines, the application will automatically be built and packaged in a docker image which is automatically uploaded into the above ECR 
repository. 
In addition a zipfile (containing the `cfn-template.yaml` file and `config/` directory) are uploaded onto the Artifact S3 bucket.

The CodePipeline is triggered by the file on S3. This pipeline deploys the ACC and PROD stacks.

To deploy code changes:

* Update the code (`src` directory)
* Commit and merge changes into `master` branch.

To make configuration changes (eg. increasing memory of the containers):

* Update the corresponding parameter(s) in the json files in the `config` directory.
* Commit and merge changes into `master` branch.

To add/change/remove AWS resources deployed by the CF template:

* Reflect the changes in the CF template (`cfn-template.yaml`).
* Commit and merge changes into `master` branch.

### interaction with Docker & deployment

    ./make.sh help

