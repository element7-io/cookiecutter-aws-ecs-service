#!/usr/bin/env python
# coding=utf-8
import boto3
import json
import logging

logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('boto3').setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


cfn = boto3.client("cloudformation")
ecs = boto3.client("ecs")
cpl = boto3.client("codepipeline")


# Get CFN stack tags
def get_tags(stackname):
    logger.info("####### Getting stack tags..")
    logger.debug(stackname)
    output = []
    try:
        response = cfn.describe_stacks(
                StackName=stackname)
        tags = (response["Stacks"][0]["Tags"])
        parameters = (response["Stacks"][0]["Parameters"])
        logger.debug('## Prameters: {}'.format(parameters))
        for item in tags:
            newmap = {}
            newmap["key"] = item["Key"]
            newmap["value"] = item["Value"]
            output.append(newmap)
        logger.debug('## Tags retrieved from parameters: {}'.format(output))
        return output
    except Exception as e:
        logger.error(e)


# Get current tags
def get_current_tags(clustername, servicename):
    ''' get the service current tags '''
    logger.info("####### Get current tags..")
    logger.debug(
        '## clustername: {} - servicename: {}'.format(clustername, servicename)
    )
    try:
        response = ecs.describe_services(
            cluster=clustername,
            services=[
                servicename
            ],
            include=[
                'TAGS',
            ]
        )
        current_tags = response["services"][0]["tags"]
        return current_tags
    except Exception as e:
        logger.error(e)


# Remove current tags
def untag(resource, tags):
    logger.info("####### Remove current tags")
    logger.debug(tags)
    tag_keys = [v for item in tags for k, v in item.items() if k == 'key']
    logger.debug(tag_keys)
    try:
        ecs.untag_resource(
            resourceArn=resource,
            tagKeys=tag_keys
        )
    except Exception as e:
        logger.error(e)


# Set new tags
def set_tags(resource, tags):
    logger.info("####### Set new tags..")
    try:
        ecs.tag_resource(
            resourceArn=resource,
            tags=tags
        )
    except Exception as e:
        logger.error(e)


# Handler
def handler(event, context):
    jobid = event["CodePipeline.job"]["id"]

    try:
        # Get codepipeline lambda User Attributes
        userparams = event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"]["UserParameters"]
        data = json.loads(userparams)

        # define variables
        clustername = data["clustername"]
        servicename = data["servicename"]
        servicearn = "arn:aws:ecs:" + data["region"] + ":" + data["accountid"] + ":service/" + clustername + "/" + servicename

        # Remove possible existing tags
        current_tags = get_current_tags(clustername, servicename)
        if current_tags is not None:
            untag(servicearn, current_tags)

        # Set the new tags
        tags = get_tags(data["stackname"])
        set_tags(servicearn, tags)

        # Send status to codepipeline
        cpl.put_job_success_result(jobId=jobid)

    except Exception as e:
        logger.error(e)
        cpl.put_job_failure_result(
            jobId=jobid,
            failureDetails={
                'type': 'JobFailed',
                'message': 'something went wrong'
                }
        )
