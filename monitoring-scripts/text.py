#!/usr/bin/python3
import subprocess

cmd = 'ps -A | grep nginx'
(status, output) = subprocess.getstatusoutput(cmd)

def check():
  if(status > 0):
    print('she is off lad')
  else:
    print('she is on lad')

def main():
  check()

if __name__ == '__main__':
  main()
