#!/usr/bin/env python3
import sys, os
import basic

menu_actions = {}

def main_menu():
  os.system('clear')
  print('''      __          _______ 
     /\ \        / / ____|
    /  \ \  /\  / / (___  
   / /\ \ \/  \/ / \___ \ 
  / ____ \  /\  /  ____) |
 /_/    \_\/  \/  |_____/  ''')

  print("\nWelcome to an AWS Management System \n")
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
  print('(---------------------)')
  print('      Basic Config')
  print('(---------------------)')
  print('1. Create Instance')
  print('2. List Instances')
  print('3. Create Bucket')
  print('4. List Buckets')
  print('5. Delete Bucket')
  print('6. Delete Bucket Contents')
  print('7. Add Items to Bucket')
  print('\n9. Back')
  print('0. Quit')
  choice = input(" >>  ")
  while choice != 0:
    if choice == '1':
      basic.create_instance()
      break
    if choice == '2':
      basic.list_instances()
      break
    if choice == '3':
      basic.create_bucket()
      break
    if choice == '4':
      basic.list_buckets()
      break
    if choice == '5':
      basic.delete_buckets()
      break
    if choice == '6':
      basic.delete_contents()
      break
    if choice == '7':
      basic.add_bucket()
      break
    if choice == '9':
      exec_menu(choice)
    if choice == '0':
      exec_menu(choice)  
  menu1()
  return

def menu2():
  print('(---------------------)')
  print('  Monitoring Services')
  print('(---------------------)')

  print('\n9. Back')
  print('0. Quit')
  choice = input(" >>  ")
  while choice != 0:
    if choice == '9':
      exec_menu(choice)
    if choice == '0':
      exec_menu(choice)
  menu2
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
