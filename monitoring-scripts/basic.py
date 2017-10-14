#!/usr/bin/env python3
import boto3
import sys
import ascii_logos
import time

def create_instance():
  print('''Please enter the name of the key you want to use:
Hit enter to default key - "aws-key"''')
  key = input(' >>  ')
  if(key==''):
    key = 'aws-key'

  print('''Please enter the name of the security group you want to use:
Hit enter to default group - "any-ssh-http-https"''')
  group = input(' >>  ')
  if(group==''):
    group = 'any-ssh-http-https'

  print('Would you like instance to be launched with nginx: (y/n)') 
  data = input(' >>  ')
  if(data=='y'):
    user_data = '''#!/bin/bash
yum -y update 
yum -y install nginx 
service nginx start'''
  else:
    user_data = ''

  ascii_logos.ec2()
  ec2 = boto3.resource('ec2')
  instance = ec2.create_instances(
    ImageId='ami-acd005d5',
      MinCount=1,
      MaxCount=1,
      KeyName=key,
      SecurityGroups=[group],
      UserData=user_data,
      InstanceType='t2.micro')
  print('New instance created')
  new_instance = instance[0]
  while(new_instance.state['Name'] == 'pending'):
    print('Instance state is : %s' % new_instance.state['Name'])
    time.sleep(5)
    new_instance.reload()
  print('Instance state is now : %s' % new_instance.state['Name'])
  print('Instance public DNS is : %s' % new_instance.public_dns_name)


def list_instances():
  ascii_logos.ec2()
  ec2 = boto3.resource('ec2')
  for instance in ec2.instances.all():
    print ('Instance:', instance.id, 'is now', instance.state['Name'])

def create_bucket():
  ascii_logos.s3()
  s3 = boto3.resource("s3")
  print('Please enter a globally unique bucket name:')
  bucket_name = input(' >>  ')
  try:
    response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print (response)
  except Exception as error:
    print (error)

def list_buckets():
  ascii_logos.s3()
  s3 = boto3.resource('s3')
  for bucket in s3.buckets.all():
    print ('Bucket Name: ',bucket.name)
    print ("---")
    for item in bucket.objects.all():
        print ("\t%s" % item.key)
  
def list_buckets_no_contents():
  s3 = boto3.resource('s3')
  for bucket in s3.buckets.all():
    print ('Bucket Name: ',bucket.name)

def delete_buckets():
  ascii_logos.s3()
  s3 = boto3.resource('s3')
  print('\nList of all Active Buckets:')
  list_buckets_no_contents()
  print('\nPlease enter name of bucket you want to delete:')
  bucket_name = input(' >>  ')
  bucket = s3.Bucket(bucket_name)
  try:
      response = bucket.delete()
      print (response)
  except Exception as error:
      print (error)

def delete_contents():
  ascii_logos.s3()
  s3 = boto3.resource('s3')
  print('\nList of all Active Buckets:')
  list_buckets_no_contents()
  print('\nPlease enter name of bucket you want to delete contents from:')
  bucket_name = input(' >>  ')
  bucket = s3.Bucket(bucket_name)
  for key in bucket.objects.all():
    try:
      response = key.delete()
      print (response)
    except Exception as error:
      print (error)

def add_bucket():
  ascii_logos.s3()
  s3 = boto3.resource("s3")
  print('\nList of all Active Buckets:')
  list_buckets_no_contents()
  print('\nPlease enter name of bucket you want to add contents too:')
  bucket_name = input(' >>  ')
  print('\nPlease enter name of file you want to add to bucket ',bucket_name,' :')
  object_name = input(' >>  ')
  try:
      response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'))
      print (response)
  except Exception as error:
      print (error)
