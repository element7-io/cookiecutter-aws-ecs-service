SHELL=bash
GREEN="\n\n\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
END=" \033[0m\n"

PROJECT_NAME={{ cookiecutter.project_slug }}
BUILD_AUTOMATION_TOOL={{ cookiecutter.build_automation_tool }}
CF_STACK_NAME=${PROJECT_NAME}-pipeline-stack

check_defined = \
		$(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

create-pipeline:
	@:$(call check_defined, GITHUB_TOKEN)
	@echo -e $(GREEN)Creating Pipeline...$(END)
	aws cloudformation create-stack --stack-name ${CF_STACK_NAME} \
		--template-body file://cfn-pipeline.yaml \
		--enable-termination-protection \
		--capabilities CAPABILITY_IAM \
		--parameters \
			ParameterKey=GitHubOAuthToken,ParameterValue=${GITHUB_TOKEN} \
		--timeout-in-minutes 15
	@echo ""
	@echo Waiting for stack to complete...
	@aws cloudformation wait stack-create-complete --stack-name ${CF_STACK_NAME}
	@echo Create complete!
.PHONY: create-pipeline

update-pipeline:
	@:$(call check_defined, GITHUB_TOKEN)
	@echo -e $(GREEN)Updating Pipeline...$(END)
	aws cloudformation update-stack --stack-name ${CF_STACK_NAME} \
		--template-body file://cfn-pipeline.yaml \
		--capabilities CAPABILITY_IAM \
		--parameters \
			ParameterKey=GitHubOAuthToken,ParameterValue=${GITHUB_TOKEN}
	@echo ""
	@echo Wating for stack update to complete...
	@aws cloudformation wait stack-update-complete --stack-name ${CF_STACK_NAME}
	@echo Stack update complete!
.PHONY: update-pipeline

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
