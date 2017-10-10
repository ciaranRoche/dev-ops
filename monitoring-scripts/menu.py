import sys, os
import boto3

def create_instance():
  ec2 = boto3.resource('ec2')
  instance = ec2.create_instances(
      ImageId='ami-acd005d5',
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro')
  print (instance[0].id)


menu_actions = {}

def main_menu():
  os.system('clear')

  print("Welcome to an AWS Management System \n")
  print("Please choose the menu you want to start:")
  print("1. Basic Config")
  print("2. Monitoring Services")
  print("\n0. Quit")
  choice = input(" >>  ")

  exec_menu(choice)

  return

def exec_menu(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions['main_menu']()
  else:
    try:
      menu_actions[ch]()
    except KeyError:
      print("Invalid selection, please try again. \n")
      menu_actions['main_menu']()
  return

def menu1():
  print('Basic Config')
  print('1. Create Instance')
  print('9. Back')
  print('0. Quit')
  choice = input(" >>  ")
  while choice != 0:
    if choice == '1':
      create_instance()
  exec_menu(choice)
  return

def menu2():
  print('Monitoring Services')
  print('9. Back')
  print('0. Quit')
  choice = input(" >>  ")
  exec_menu(choice)
  return

def back():
  menu_actions['main_menu']()

def exit():
  print('Killing all Processess....')
  sys.exit()

menu_actions = {
  'main_menu' : main_menu,
  '1' : menu1,
  '2' : menu2,
  '9' : back,
  '0' : exit,
}

if __name__ == "__main__":
  main_menu()
