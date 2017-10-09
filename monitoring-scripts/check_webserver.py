#!/usr/bin/python3

import subprocess
import sys


command = 'ps –A | grep nginx | grep –v grep'
(status, output) = subprocess.getstatusoutput(command)

def check():
  print('Checking nginx . . . ')
  if (status > 0):
    print('nginx server is not running')
    sys.exit(1)
  else: 
    print('nginx server is running')

def main():
  check()

if __name__ == '__main__':
  main()
