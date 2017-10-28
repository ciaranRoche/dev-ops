# Group of basic functions, using boto3 to setup instances and s3 buckets

#!/usr/bin/env python3
import boto3
import sys
import ascii_logos
import time
import webbrowser
import subprocess

# Creates a new instance in ec2, prompts user for details to customise set up
def create_instance():
    print('''Please enter new instance name:''')
    name = input(' >>  ')
    tag = {"Key": "Name", "Value": name}

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

    #Adds user data if the user wishes, which installs nginx, python35 and starts the nginx server
    data = None
    while(data != 'y' and data != 'n'):
        print('Would you like instance to be launched with nginx: (y/n)')
        data = input(' >>  ')
    if(data=='y'):
        user_data = '''#!/bin/bash
yum -y update 
yum -y install nginx
yum -y install python35 
service nginx start'''
    else:
        user_data = ''

    # Main logic using boto3 to create instance
    try:
        ascii_logos.ec2()
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(
          ImageId='ami-acd005d5',
            MinCount=1,
            MaxCount=1,
            KeyName=key,
            SecurityGroups=[group],
            UserData=user_data,
            InstanceType='t2.micro',
            TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [tag]}]
            )
        print('Woohoo looks like your new instance has been created!\n Please hold till your instance is fully running...')
        new_instance = instance[0]
        # While loop, outputs status, loop breaks when status is finished pending
        while(new_instance.state['Name'] == 'pending'):
            print('Instance state is : %s' % new_instance.state['Name'])
            time.sleep(5)
            new_instance.reload()
        print('Instance state is now : %s' % new_instance.state['Name'])
        print('Instance public DNS is : %s' % new_instance.public_dns_name)
    except Exception as error:
        print('Aww snap, something went wrong')
        print(error)


#Returns a list of instances, including their state and public ipv4 address
def list_instances():
    try:
        ascii_logos.ec2()
        ec2 = boto3.resource('ec2')
        print('  Instance Id              Status          Public IPv4')
        print('(------------------------------------------------------)')
        for instance in ec2.instances.all():
            print (instance.id,'  -  ', instance.state['Name'],'  -  ',  instance.public_ip_address,)
    except:
        print('Aww snap, something went wrong')
        print(error)


#Creates a bucket in s3, prompts user for a bucket name
def create_bucket():
    ascii_logos.s3()
    s3 = boto3.resource("s3")
    print('Please enter a globally unique bucket name:')
    bucket_name = input(' >>  ')
    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print ('Congrats, new bucket created:\n', response)
    except Exception as error:
        print('Aww snap, something went wrong')
        print (error)

# Returns a list of buckets including items in the bucket
def list_buckets():
    ascii_logos.s3()
    s3 = boto3.resource('s3')
    try:
        for bucket in s3.buckets.all():
            print ('Bucket Name: ',bucket.name)
            print ("---Items---")
            for item in bucket.objects.all():
                print ("\t%s" % item.key)
    except Exception as error:
        print('Aww snap, something went wrong')
        print (error)

# Returns list of buckets but does not return the items, used in other functions to show user available buckets
# TODO : change to an array list and prompt user to select a bucket and return bucket for use in other functions
def list_buckets_no_contents():
    s3 = boto3.resource('s3')
    try:
        for bucket in s3.buckets.all():
            print ('Bucket Name: ',bucket.name)
    except Exception as error:
        print('Aww snap, something went wrong')
        print(error)

#Function to delete bucket, prompts user to enter bucket name
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
        print ('Bucket is no more\n',response)
    except Exception as error:
        print('Aww snap, something went wrong')
        print (error)

#Deletes content from buckets
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
            print ('And the contents are not more\n',response)
        except Exception as error:
            print('Aww snap, something went wrong')
            print (error)

#Adds items to bucket, user prompted to enter details
def add_bucket():
    ascii_logos.s3()
    s3 = boto3.resource("s3")
    print('\nList of all Active Buckets:')
    list_buckets_no_contents()
    print('\nPlease enter name of bucket you want to add contents too:')
    bucket_name = input(' >>  ')
    print('\nPlease enter name of file you want to add to bucket ',bucket_name,' :')
    object_name = input(' >>  ')
    #main logic using boto, acl = 'puplic-read', makes added item public
    html_link = 'echo ','<img src="https://s3-eu-west-1.amazonaws.com/' + bucket_name + '/' + object_name + '"/>',' > index.html'
    try:
        response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'), ACL='public-read')
        print ('Looks like everything is where it is meant to be \n',response)
        (status, output) = subprocess.getstatusoutput(html_link)
        ans = None
        #Gives user option to view item in browser
        while (ans != 'y' and ans != 'n'):
            print('\nWould you like to view file? (y/n)')
            ans = input(' >>  ')
            if(ans == 'y'):
                webbrowser.open('https://s3-eu-west-1.amazonaws.com/' + bucket_name + '/' + object_name, new=0, autoraise=True)
            elif(ans == 'n'):
                return
    except Exception as error:
        print('Aww snap, something went wrong')
        print (error)
