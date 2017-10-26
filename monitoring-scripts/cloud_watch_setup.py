
#Sets up basic cloud watch client on an instance
#TODO: Add create user type to help with setting client

import boto3
import sys
import subprocess
import run_newwebserver
import webbrowser
import control_scripts

#Creates client on an instance
def setup():
    print('Welcome to Cloud Watch Client Setup')
    print('Ensure you have access keys for a user with on Cloud Watch privileges')
    #Shows list of instance, user promted to select one
    instance = control_scripts.pick_instance()
    print('''Please enter the name of the key associated with that instance:
Hit enter to default key - "aws-key.pem"''')
    key = input(' >>  ')
    if(key==''):
        key = 'aws-key.pem'
    print('''Ok now we need your AWS credentials. 
These will be stored on your instance to allow the Cloud Watch Client gather the data on your behalf

Please enter your access key''')
    access_key = input(' >>  ')
    print('Please enter your secret key')
    secret_key = input(' >>  ')

    print('Ok, now we have everything we need we are just going to set up the client for you, we will walk you through the process...')

    #Installs nessasary packages to instance
    install_client = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "sudo yum install perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https -y"'
    try:
        (status, output) = subprocess.getstatusoutput(install_client)
        if(status > 0):
            print('\nAww snap, looks like something went wrong, please ensure details are correct.\n', output)
        else:
            print('\nEverything looks good, we just installed the client to your instance. \n',output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

    #Uses curl to pull in a zip file of cloud watch client
    move_client = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "curl http://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.1.zip -O"'
    try:
        (status, output) = subprocess.getstatusoutput(move_client)
        if(status > 0):
            print('\nAww snap, looks like something went wrong, please ensure details are correct.\n', output)
        else:
            print('\nEverything looks good, we just moved the client to your current instance directory for ease of access. \n',output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

    #Unzips the client, and removes the zip file
    unzip = '''unzip CloudWatchMonitoringScripts-1.2.1.zip
rm CloudWatchMonitoringScripts-1.2.1.zip'''
    unzip_client = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "' + unzip + '"'
    try:
        (status, output) = subprocess.getstatusoutput(unzip_client)
        if(status > 0):
            print('\nAww snap, looks like something went wrong, please ensure details are correct.\n', output)
        else:
            print('\nEverything looks good, we just unzipped the client \n',output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

    #Pipes in the access keys a conf file
    pipe = '''echo "AWSAccessKeyId=%(access)s" >> awscreds.conf
echo "AWSSecretKey=%(secret)s" >> awscreds.conf
cp awscreds.conf ./aws-scripts-mon/
rm awscreds.conf''' % {'access' : access_key, 'secret' : secret_key}
    create_conf = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "' + pipe + '"'
    try:
        (status, output) = subprocess.getstatusoutput(create_conf)
        if(status > 0):
            print('\nAww snap, looks like something went wrong, please ensure details are correct.\n', output)
        else:
            print('\nEverything looks good, we just created a conf file for you :) \n',output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

    #Finally verifies everything works, and cloud watch client is ready to go
    verify = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "./aws-scripts-mon/mon-put-instance-data.pl --mem-util --verify --verbose"'
    success = 'Verification completed successfully'
    try:
        (status, output) = subprocess.getstatusoutput(verify)
        if(status > 0):
            print('\nAww snap, looks like something went wrong, please ensure details are correct.\n', output)
        else:
            if success in output:
                print('\nWoohoo, everything is in working order, now you can start your cloud watch monitoring on this instance.')
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

#Prompts user to enter time in hours, and returns stats for the previous n time hours
def checkStats():
    instance = control_scripts.pick_instance()
    print('Please enter key associated with this instance: (Hit enter to default to "aws-key.pem")')
    key = input(' >>  ')
    if(key == ''):
      key = 'aws-key.pem'
    print('Please enter a number in hours you wish to see stats for:')
    hours = input(' >>  ')
    command = 'ssh -t -i ' + key + ' ec2-user@' + instance.public_ip_address + ' " ./aws-scripts-mon/mon-get-instance-stats.pl --recent-hours=' + hours + ' "'
    try:
        (status, output) = subprocess.getstatusoutput(command)
        if (status > 0):
          print('Aww snap, looks like something went wrong\n', output)
        else:
          print(output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

#Sets cron on instance to return check information every 5 minutes on the instance, basic set up config
def setCron():
    instance = control_scripts.pick_instance()
    print('Please enter key associated with this instance: (Hit enter to default to "aws-key.pem")')
    key = input(' >>  ')
    if(key == ''):
      key = 'aws-key.pem'
    command = 'ssh -t -i ' + key + ' ec2-user@' + instance.public_ip_address + ' " ~/aws-scripts-mon/mon-put-instance-data.pl --mem-used-incl-cache-buff --mem-util --disk-space-util --disk-path=/ --from-cron "'
    try: 
        print('Please wait while we configure and set the cron schedule for you :)')
        (status, output) = subprocess.getstatusoutput(command)
        if (status > 0):
            print('Aww snap, looking like something went wrong\n', output)
        else:
            print(output)
            print('Everything looks good, you can now check the AWS console for monitoring stats on your instance')
    except Exception as error:
        print('Aww snap something went wrong')
        print(error)
