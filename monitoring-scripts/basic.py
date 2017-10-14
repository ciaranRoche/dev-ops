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
  
def list_buckets_no_contents():
  s3 = boto3.resource('s3')
  for bucket in s3.buckets.all():
    print ('Bucket Name: ',bucket.name)

def delete_buckets():
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
