#!/usr/bin/python3
import subprocess
import sys

cmd = 'ps -A | grep nginx'
(status, output) = subprocess.getstatusoutput(cmd)

def start_nginx():
  print('Would you like to turn on nginx server? (y/n)')
  choice = input(' >>  ')
  if(choice == 'y'):
    print('nginx is firing up')
    subprocess.run(["sudo","service","nginx","start"])
  else:
    sys.exit(0)
  
def close_nginx():
  print('Would you like to shut down nginx server? (y/n)')
  choice = input(' >>  ')
  if(choice == 'y'):
    print('nginx if shutting down')
    subprocess.run(["sudo","service","nginx","stop"])
  else:
    sys.exit(0)

def check():
  if(status > 0):
    print('Nginx server is offline')
    start_nginx()
  else:
    print('Nginx server is online')
    close_nginx()


def main():
  check()


if __name__ == '__main__':
  main()
