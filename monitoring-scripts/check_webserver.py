#!/usr/bin/python3
import subprocess

cmd = 'ps -A | grep nginx'
(status, output) = subprocess.getstatusoutput(cmd)

def start_nginx():
  print('nginx is firing up')
  subprocess.run(["sudo","service","nginx","start"])
  

def check():
  if(status > 0):
    print('she is off lad')
    start_nginx()
  else:
    print('she is on lad')


def main():
  check()


if __name__ == '__main__':
  main()
