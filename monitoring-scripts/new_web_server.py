#!/usr/bin/env python3

import boto3
import sys
import ascii_logos
import time
import subprocess
import random

def automated_run():
    ascii_logos.ec2()
    print('''Don't even trip, we got you dog.
  We are going to do an automated run, where we will launch a new instance with nginx, 
  then we will render custom html page, where we link an image that we just uploaded to 
  a bucket in s3.
  So sit back relax, have a cup of coffee, take the dog for a walk, while we run this.''')
    time.sleep(5)
    print('Just make sure the key "aws-key" is in this folder :)')

    ec2 = boto3.resource('ec2')
    s3 = boto3.resource('s3')
    try:
        instance = ec2.create_instances(
          ImageId='ami-acd005d5',
          MinCount = 1,
          MaxCount = 1,
          KeyName = 'aws-key',
          SecurityGroups = ['any-ssh-http-https'],
          UserData = '''#!/bin/bash
yum -y update 
yum -y install nginx
yum -y install python35 
service nginx start''',
          InstanceType = 't2.micro',
          TagSpecifications = [{'ResourceType' : 'instance', 'Tags' : [{'Key' : 'Name', 'Value' : 'Auto created Instance'}]}]
        )
        new_instance = instance[0]
        print('Ok so it looks like the new instance has been created, let us check its status....')
        while(new_instance.state['Name'] == 'pending'):
            print('Instance is in a state of %s while Amazon performs some checks.' % new_instance.state['Name'])
            time.sleep(5)
            new_instance.reload()
        print('Ok Amazon have given the thumbs up and your instance is in a state of ',new_instance.state['Name'])
    except Exception as error:
        print('Aww snap, looks like something went wrong')
        print(error)



    # print('''Time to set up an s3 bucket, you know you need a unique name right....
    # Again we got you dog :)''')
    # print('Please mash the key board and generate a unique bucket name:')
    # bucket_name = input(' >>  ')
    # try:
    #     response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    #     print('I think we are good', response)
    # except Exception as error:
    #     print('Aww snap, something went wrong')
    #     print(error)


    print('Lets send up any files we need to host our custom page')
    ip = new_instance.public_ip_address
    command = 'scp -o StrictHostKeyChecking=no -i aws-key.pem index.html ec2-user@' + ip + ':.'
    try:
        time.sleep(45)
        (status, output) = subprocess.getstatusoutput(command)
        if(status > 0):
            print('Damn dog, looks like something went wrong uploading the html file :( ')
        else:
            print('File has been upload successfully')
    except Exception as error:
        print('Aww snap something went wrong :( ')
        print(error)

    upload_check_webserver = 'scp -i aws-key.pem check_webserver.py ec2-user@' + new_instance.public_ip_address + ':.'
    try:
        (status, output) = subprocess.getstatusoutput(upload_check_webserver)
        if (status > 0):
            print('Damn dog, looks like something went wrong uploading the check webserver file :( ')
        else:
            print('File has been upload successfully')
    except Exception as error:
        print('Aww snap something went wrong :( ')
        print(error)

    set_permission = 'sudo chmod 700 check_webserver.py'
    ssh_command_set = 'ssh -t -i aws-key.pem ec2-user@' + ip + ' "' + set_permission + '"'
    print('ok with that done, we got to set some permissions and move some files around :)')
    try:
        (status, output) = subprocess.getstatusoutput(ssh_command_set)
        if(status > 0):
            print('Aww snap, looks like something went wrong issuing set permission command :(')
        else:
            print('Permissions set successfully')
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

    move_file = 'sudo cp index.html /usr/share/nginx/html'
    ssh_command_move = 'ssh -t -i aws-key.pem ec2-user@' + ip + ' "' + move_file + '"'
    try:
        (status, output) = subprocess.getstatusoutput(ssh_command_move)
        if(status > 0):
            print('Aww snap, looks like something went wrong issuing copy command :(')
        else: 
          print('Copy command issued successfully')
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)





def main():
    automated_run()

if __name__ == '__main__':
    main()
