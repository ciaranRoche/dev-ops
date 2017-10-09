#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    print ('Instance:',instance.id, 'is now', instance.state['Name'])
