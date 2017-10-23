import boto3
import sys
import subprocess
import run_newwebserver
import webbrowser
import control_scripts

def setup():
  print('Welcome to Cloud Watch Client Setup')
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



def main():
    setup()

if __name__ == '__main__':
    main()