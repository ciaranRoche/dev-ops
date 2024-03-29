
# Basic menu system for command line application

#!/usr/bin/env python3
import sys, os
import basic
import ascii_logos
import control_scripts
import cloud_watch_setup

menu_actions = {}

#renders main menu
def main_menu():
  os.system('clear')
  ascii_logos.aws()
  print("Welcome to an AWS Management System \n")
  print("Please choose the menu you want to start:")
  print("1. Basic Config")
  print("2. Advanced Config/Monitoring")
  print("3. Cloud Watch Client")
  print("\n0. Quit")
  choice = input(" >>  ")
  #choice sent to exec_menu to be checked
  exec_menu(choice)
  return

#checks user choice
def exec_menu(choice):
  #clears terminal screen
  os.system('clear')
  ch = choice.lower()
  #if choice is blank call main menu again
  if ch == '':
    menu_actions['main_menu']()
  else:
    try:
      # try and see if choice is in menu_actions
      menu_actions[ch]()
    except KeyError:
      print('Aww snap! Invalid selection made, try again. \n')
      menu_actions['main_menu']()
  return

#renders menu1
def menu1():
  while True:
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
    menu1_exec(choice)

#menu logic, checks user choice
def menu1_exec(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu1_actions['menu1']()
  else:
    try:
      menu1_actions[ch]()
    except KeyError:
      print('Aww snap, invalid selection, please try again. \n')
      menu1_actions['menu1']()
  return

#renders menu2
def menu2():
  while True:
    print('(---------------------)')
    print('   Advanced Config')
    print('(---------------------)')
    print('1. Upload File to Ec2 Instance')
    print('2. Upload Folder to Ec2 Instance')
    print('3. Issue Command')
    print('4. Start an Instance')
    print('5. Stop an Instance')
    print('6. Terminate Instance')
    print('\n7. View Instance Webpage')

    print('\n9. Back')
    print('0. Quit')
    choice = input(" >>  ")
    menu2_exec(choice)

#checks menu2 choice
def menu2_exec(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu2_actions['main_menu']()
  else:
    try:
      menu2_actions[ch]()
    except KeyError:
      print('Aww snap, invalid selection, please try again. \n')
      menu2_actions['menu2']()
  return

#renders menu3
def menu3():
  while True:
    print('(---------------------)')
    print('  Cloud Watch Client')
    print('(---------------------)')
    print('1. Cloud Watch Setup')
    print('2. Get Instance Stats')
    print('3. Set Cron - 5 Minute Checks')

    print('\n9. Back')
    print('0. Quit')
    choice = input(" >>  ")
    menu3_exec(choice)

#checks menu3 choice
def menu3_exec(choice):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu3_actions['main_menu']()
  else:
    try:
      menu3_actions[ch]()
    except KeyError:
      print('Aww snap, invalid selection, please try again. \n')
      menu3_actions['menu3']()
  return

#function to call main-menu
def back():
  menu_actions['main_menu']()

#ends application
def exit():
  print('Killing all Processess....')
  sys.exit()

#key value pairs for menu 3
menu3_actions = {
  'menu3' : menu3,
  '1' : cloud_watch_setup.setup,
  '2' : cloud_watch_setup.checkStats,
  '3' : cloud_watch_setup.setCron,
  '9' : back,
  '0' : exit,
}

#ley value pairs for menu 2
menu2_actions = {
  'menu2' : menu2,
  '1': control_scripts.upload,
  '2': control_scripts.uploadFolder,
  '3': control_scripts.control,
  '4': control_scripts.start_instance,
  '5': control_scripts.stop_instance,
  '6': control_scripts.terminate_instance,
  '7': control_scripts.visit_website,
  '9': back,
  '0': exit,
}

#key value pairs for menu1
menu1_actions = {
  'menu1' : menu1,
  '1': basic.create_instance,
  '2': basic.list_instances,
  '3': basic.create_bucket,
  '4': basic.list_buckets,
  '5': basic.delete_buckets,
  '6': basic.delete_contents,
  '7': basic.add_bucket,
  '9': back,
  '0': exit,
}

#key value pairs for main menu
menu_actions = {
  'main_menu' : main_menu,
  '1' : menu1,
  '2' : menu2,
  '3' : menu3,
  '9' : back,
  '0' : exit,
}
