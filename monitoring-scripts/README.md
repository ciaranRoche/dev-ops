# Welcome to Developer Operations Assignment 1

To view and clone the project visit my [GitHub](https://github.com/ciaranRoche/dev-ops/tree/master/monitoring-scripts).

## About

The overall objective of this assignment is to automate using Python 3 the process of creating, launching and monitoring a public-facing web server in the Amazon cloud. The web server will run on an EC2 instance and display some static content that is stored in S3.

## Getting Started

It is assumed that you will have your Amazon credentials saved in a config file (~/.aws/credentials). This saves the use of credentials being stored in the program

* `$ python3 --version` - To check python 3 is installed
* `$ python3 run_newwebserver.py` - To launch program

## Project layout

    scripts/
        README.md           # Project Readme
        ascii_logos.py      # Contains amazon logos in ascii
        basic.py            # Contains basic scripts ranging from launching an instance to deleteing an instance
        check_webserver.py  # Script to check if nginx is running on an instance
        control_scripts.py  # Contains functions that control and monitor instances, eg, issue a command remotely
        menu.py             # Menu system to bring all scripts together
        run_newwebserver.py # Kicks off the entire program

## Program Run Through
The following run through will explain how to create an instance in ec2, get an nginx server running, create a bucket on s3 and put some content in the bucket. 
Run a check to ensure nginx is running, copy a html file to the server and host it on the nginx server.

![image](https://i.gyazo.com/80ef612f341297b58b8e981a4f7a1c24.png)
When the program launches user is met with two options. 1, Basic Config and 2. Advanced Config/Monitoring. To create an instance in ec2 the user must first select Basic Config.
![image2](https://i.gyazo.com/8373419678fbf8ee9ef5c07a49f87666.png)
Here the user must select option 1 to create and launch an instance. The user is then asked to input options like security group, key etc, followed by if they would like the instance to be launced with nginx. If the user selects yes, user data is added to the instance, to install and start nginx, along with python35 to allow for monitoring later on.

Next the user must select option 3 to create an s3 bucket, the user is then asked to enter a globally unique name for the bucket, if successful the user will be greated with a success message or a message indicating the name is not unique.

To put an item in the bucket the user must selete option 7, here the user is prompted to enter the bucket name, and file location on their own machine, this will then insert the item into the bucket.

![image3](https://i.gyazo.com/1f173f76d96ab72b488e79bba4ec6e24.png)
In order to host a html file on the nginx server the user must go back to the start menu and select advanced config, here they select upload file, they are given a list of instances and their state, the select the instance they want from the list, they are prompted to enter the key and the file they wish to upload along with the directory they want to file to be copied too.

For this assignment it is needed to upload the html to the current directory, by simply entering '.'

Once the html is upload, the user then must select issue command, again the user is shown a list of instances and must select one, then prompted to enter key and a command, in order to get this html file hosted the command needed is `sudo cp index.html /usr/share/nginx/html` 

To check if the nginx server is running, the user must select upload file, follow the steps, but this time upload the script 'check_webserver.py'

Return to menu and issue a command, first the user must make the file executable by using the command `sudo chmod 700 check_webserver.py`
Then repeat the step but issue the command `python35 check_webserver.py`
