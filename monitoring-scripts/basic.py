#!/usr/bin/env python3
import boto3
import sys

def create_instance():
  ec2 = boto3.resource('ec2')
  instance = ec2.create_instances(
    ImageId='ami-acd005d5',
      MinCount=1,
      MaxCount=1,
     InstanceType='t2.micro')
  print (instance[0].id)

def list_instances():
  ec2 = boto3.resource('ec2')
  for instance in ec2.instances.all():
    print ('Instance:', instance.id, 'is now', instance.state['Name'])

def create_bucket():
  s3 = boto3.resource("s3")
  print('Please enter a globally unique bucket name:')
  bucket_name = input(' >>  ')
  try:
    response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print (response)
  except Exception as error:
    print (error)

def list_buckets():
  s3 = boto3.resource('s3')
  for bucket in s3.buckets.all():
    print ('Bucket Name: ',bucket.name)
    print ("---")
    for item in bucket.objects.all():
        print ("\t%s" % item.key)