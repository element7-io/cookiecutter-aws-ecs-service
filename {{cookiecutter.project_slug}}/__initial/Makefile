SHELL=bash

PROJECT_NAME={{ cookiecutter.project_slug }}
AWS_ACCOUNT_ID={{ cookiecutter.aws_account_id }}
BUILD_AUTOMATION_TOOL={{ cookiecutter.build_automation_tool }}
AWS_DEFAULT_REGION={{ cookiecutter.aws_default_region }}

ECR_REPO_NAME=${PROJECT_NAME}-repo
ECR_REPO_URL=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPO_NAME}
ARTIFACT_BUCKET={{ cookiecutter.artifact_s3_bucket }}
CF_STACK_NAME=${PROJECT_NAME}-pipeline-stack

build:
	{%- if cookiecutter.build_automation_tool == "Maven" %}
	./mvnw package
	{%- else %}
	# Gradle build
	./gradlew --init-script init.gradle --stacktrace -PbuildNumber=commit-${BITBUCKET_COMMIT} build
	# Unzip fatjar
	mkdir -p build/raw
	(cd build/raw; jar -xf ../libs/*.jar)
	{%- endif %}
.PHONY: build

run:
	java -jar target/{{ cookiecutter.artifact_name }}-0.0.1-SNAPSHOT.jar

build-docker:
	# Spring Boot with Docker: https://spring.io/guides/gs/spring-boot-docker/
	./mvnw compile jib:build
.PHONY: build-docker

docker-push:
	docker tag ${PROJECT_NAME}:latest ${ECR_REPO_URL}:${LABEL}
	docker push ${ECR_REPO_URL}:${LABEL}
.PHONY: docker-push

# run: build-gradle build-docker
# 	docker run -e SPRING_PROFILES_ACTIVE='test' -p {{ cookiecutter.container_port }}:{{ cookiecutter.container_port }} ${PROJECT_NAME}:latest
# .PHONY: run

debug: build-gradle build-docker
	docker run -ti --rm -e SPRING_PROFILES_ACTIVE='test' ${PROJECT_NAME}:latest /bin/ash
.PHONY: run

upload:
	./create_zip.sh sha-${BITBUCKET_COMMIT}
	aws s3 cp ${PROJECT_NAME}.zip s3://${ARTIFACT_BUCKET}/${PROJECT_NAME}/${PROJECT_NAME}.zip
	aws s3 cp ${PROJECT_NAME}.zip s3://${ARTIFACT_BUCKET}/${PROJECT_NAME}/cicd/${PROJECT_NAME}-${BITBUCKET_COMMIT}.zip
.PHONY: upload

upload-test:
	./create_zip.sh t_sha-${BITBUCKET_COMMIT}
	aws s3 cp ${PROJECT_NAME}.zip s3://${ARTIFACT_BUCKET}/${PROJECT_NAME}/${PROJECT_NAME}-test.zip
	aws s3 cp ${PROJECT_NAME}.zip s3://${ARTIFACT_BUCKET}/${PROJECT_NAME}/cicd/${PROJECT_NAME}-${BITBUCKET_COMMIT}.zip
.PHONY: upload-test

# Create the CodePipeline
create-pipeline:
	@echo  "Deploying CodePipeline..."
	@aws cloudformation package --template-file cfn-pipeline.yaml \
		--s3-bucket ${ARTIFACT_BUCKET} \
		--s3-prefix ${PROJECT_NAME} \
		--output-template-file cfn-pipeline-out.yaml \
		--force-upload
	@aws cloudformation deploy --stack-name ${CF_STACK_NAME} \
		--template-file cfn-pipeline-out.yaml \
		--s3-bucket ${ARTIFACT_BUCKET} \
		--s3-prefix ${PROJECT_NAME} \
		--force-upload \
		--capabilities CAPABILITY_IAM \
		--tags Application=${PROJECT_NAME}
	@echo "Waiting for Cloudformation stack to complete..."
	@aws cloudformation wait stack-exists --stack-name ${CF_STACK_NAME}
	@echo "Deployment complete!"
	@echo "Activating stack termination protection..."
	@aws cloudformation update-termination-protection \
		--stack-name ${CF_STACK_NAME} \
		--enable-termination-protection
	@echo "Termination protection activated."
.PHONY: create-pipeline

# Update the CodePipeline
update-pipeline:
	@echo  "Updating CodePipeline..."
	@aws cloudformation package --template-file cfn-pipeline.yaml \
		--s3-bucket ${ARTIFACT_BUCKET} \
		--s3-prefix ${PROJECT_NAME} \
		--output-template-file cfn-pipeline-out.yaml \
		--force-upload
	@aws cloudformation deploy --stack-name ${CF_STACK_NAME} \
		--template-file cfn-pipeline-out.yaml \
		--s3-bucket ${ARTIFACT_BUCKET} \
		--s3-prefix ${PROJECT_NAME} \
		--force-upload \
		--capabilities CAPABILITY_IAM \
		--tags Application=${PROJECT_NAME}
	@echo "Waiting for Cloudformation stack to complete..."
	@aws cloudformation wait stack-update-complete --stack-name ${CF_STACK_NAME}
	@echo "Stack update complete!"
.PHONY: update-pipeline

# Delete the CloudFormation stack.
delete-pipeline:
	@echo "Removing termination protection from stack..."
	aws cloudformation update-termination-protection \
		--stack-name ${CF_STACK_NAME} \
		--no-enable-termination-protection
	@echo "Deleting CodePipeline..."
	@aws cloudformation delete-stack --stack-name ${CF_STACK_NAME}
	@echo "Waiting for Cloudformation delete stack to complete..."
	@aws cloudformation wait stack-delete-complete --stack-name ${CF_STACK_NAME}
	@echo "Stack removed!"
.PHONY: delete-pipeline
