#!/usr/bin/env python3
import boto3

ec2 = boto3.resource('ec2')
instances = ec2.create_instances(
    ImageId='ami-acd005d5',           # Change if not in Ireland region
    KeyName='jmcgkey',                # replace with your key name
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['sg-1d846d7b'], # replace with your security group ID
    UserData='''#!/bin/bash 
                yum -y install nginx
                service nginx start
                chkconfig nginx on''', 
    InstanceType='t2.micro')

instance = instances[0]               # first element in list of instance objects

print ("An instance with ID", instance.id, "has been created.")

instance.reload()     # ensures instance object has current live instance data

