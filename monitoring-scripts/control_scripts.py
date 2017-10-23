#!/usr/bin/env python3
import boto3
import sys
import ascii_logos
import subprocess
import run_newwebserver
import webbrowser

def upload():
    instance = pick_instance()
    print("Please enter key:")
    key = input(' >>  ')
    print("Please enter file you wish to upload:")
    file = input(' >>  ')
    print("Please enter directory where you want file to be placed:")
    direc = input(' >>  ')
    command = 'scp -i ' + key + ' ' + file + ' ' + 'ec2-user@' + instance.public_ip_address + ':' + direc
    print(command)

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

def uploadFolder():
    instance = pick_instance()
    print("Please enter key:")
    key = input(' >>  ')
    print("Please enter file you wish to upload:")
    file = input(' >>  ')
    print("Please enter directory where you want file to be placed:")
    direc = input(' >>  ')
    command = 'scp -i ' + key + ' -r ' + file + ' ' + 'ec2-user@' + instance.public_ip_address + ':' + direc
    print(command)

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
    instance = pick_instance()
    print("Please enter key:")
    key = input(' >>  ')
    print("Please enter command you want to issue:")
    cmd = input(' >>  ')
    command = 'ssh -t -i ' + key + ' ' + 'ec2-user@' + instance.public_ip_address + ' "' + cmd + '"'
    try:
        (status, output) = subprocess.getstatusoutput(command)
        if(status > 0):
            print('Aww snap, looks like something went wrong, please ensure details are correct.')
        else:
            print('Everything looks good. \n',output)
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)

def pick_instance():
    ascii_logos.ec2()
    ec2 = boto3.resource('ec2')
    instance_list = []
    print('Gathering a list of Instances for you to choose from....')
    try:
        for inst in ec2.instances.all():
            instance_list.append(inst)
        print('  Number        Instance Id         Instance State')
        print('(------------------------------------------------------)')
        for i in range (0, len(instance_list)):
            print('    ',str(i), ' - ' , instance_list[i].id,' - ', instance_list[i].state['Name'])
        print('Please choose the number of the instance:')
        choice = input(' >>  ')
        instance = instance_list[int(choice)]
    except Exception as error:
        print('Aww snap, looks like something went wrong, we are trying our best')
        print(error)
    return instance


def start_instance():
    instance = pick_instance()
    try:
        if(instance.state['Name'] == 'running'):
            print('Instance is running so dont even trip dog')
        elif(instance.state['Name'] == 'terminated'):
            print('Instance can not be started, it is TERMINATED - hasta la vista baby!')
        else:
            instance.start()
            print('Instance is booting up :)')
    except Exception as error:
        print('Aww snap, looks like something went wrong')
        print(error)

def stop_instance():
    instance = pick_instance()
    try:
        if(instance.state['Name'] == 'stopped'):
            print('Instance is already stopped')
        elif(instance.state['Name'] == 'terminated'):
            print('Instance can not be stopped, it is TERMINATED - hasta la vista baby!')
        else:
            instance.stop()
            print('Instance is stopping :(')
    except Exception as error:
        print('Aww snap, looks like something went wrong')
        print(error)

def terminate_instance():
    instance = pick_instance()
    try:
        if(instance.state['Name'] == 'terminated'):
            print('Instance is already TERMINATED - hasta la vista baby!')
        else:
            instance.terminate()
            print('Instance is been TERMINATED - hasta la vista baby!')
    except Exception as error:
        print('Aww snap, looks like something went wrong')
        print(error)

def visit_website():
    instance = pick_instance()
    try :
        dns = instance.public_dns_name
        webbrowser.open("http://" + dns)
    except Exception as error:
        print("Aww snap, looks like something went wrong")
        print(error)

def main():
    terminate_instance()

if __name__ == '__main__':
    main()
