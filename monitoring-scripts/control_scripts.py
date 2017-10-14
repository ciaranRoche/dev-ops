#!/usr/bin/env python3
import boto3
import sys
import ascii_logos
import subprocess
import run_newwebserver

def upload():
  ascii_logos.ec2()
  print("Please enter key:")
  key = input(' >>  ')
  print("Please enter file you wish to upload:")
  file = input(' >>  ')
  print("Please enter public iPv4 of instance:")
  ip = input(' >>  ')
  print("Please enter directory where you want file to be placed:")
  direc = input(' >>  ')
  command = 'scp -i ' + key + ' ' + file + ' ' + 'ec2-user@' + ip + ':' + direc  

  try:
    (status, output) = subprocess.getstatusoutput(command)
    if(status > 0):
      print('Aww snap, looks like something went wrong, please ensure details are correct.')
    else:
      print('File uploaded :)')
  except Exception as error:
    print('Aww snap something went wrong :(')
    print(error)
  return (status, output)


def control():
  ascii_logos.ec2()
  print("Please enter key:")
  key = input(' >>  ')
  print("Please enter public iPv4 of instance:")
  ip = input(' >>  ')
  print("Please enter command you want to issue:")
  cmd = input(' >>  ')

  command = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + ip + ' "' + cmd + '"'
  
  try:
    (status, output) = subprocess.getstatusoutput(command)
    if(status > 0):
      print('Aww snap, looks like something went wrong, please ensure details are correct.')
    else:
      print(output)
  except Exception as error:
    print('Aww snap something went wrong :(')
    print(error)


