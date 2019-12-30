#!/bin/bash
PROJECT_NAME={{ cookiecutter.project_slug }}

mkdir -p dist/config/
cp cfn-*yaml dist/
cp buildspec.yml dist/
cp swagger.yaml dist/
for f in config/*.json
do
    # Add the code checksum tag to the parameters of the CloudFormation 
    # config file. The current git commit id is added as tag on the
    # CloudFormation stack in order to easily determine which version of
    # the application is running live.
    cat $f | \
    jq --arg image_tag $1 '.Parameters |= . + {"ImageTag": $image_tag}' | \
    jq --arg commit_id ${BITBUCKET_COMMIT} '.Tags |= . + {"GitCommitId": $commit_id}' > dist/$f
done
current_dir=$(pwd)
cd dist && zip -r ../${PROJECT_NAME}.zip *
cd $current_dir

