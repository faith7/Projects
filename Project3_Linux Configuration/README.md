# Linux Server Configuration

## About this Project
Linux Server Configuration is a part of Udacity Full Stack NanoDegree Program. 
This project is to deploy the web application from the previous project(Project 2 - Item catalog) that used to be hosted on a local machine. Using apache server 

## Technologies for this project 
  - Amazon AWS Lightsail(Ubuntu 18.04.3)
  - Linux Server
  - Apache2 
  - Flask
  - Postgresql 

&nbsp;
## Configuration steps 
#### 1. Create an Amazon AWS Lightsail instance. 
- Go to amazon lightsail https://aws.amazon.com/lightsail/
- Create an instance with os only ubuntu 18.04.3 
- Choose the plan. (Cheapest plan is enough for this project)
- Create an instance with the desired name 

#### 2. Set up SSH key. 
- Go to the account tab on the right top side of amazon AWS account page
- Select SSH keys tab and download LightsailDefaultPrivateKey-*.pem
- On your local machine, go to the download folder and cut LightsailDefaultPrivateKey-*.pem
- Paste LightsailDefaultPrivateKey-*.pem to local .ssh folder
  (It is usually in c/Users/<your User name>/.ssh) 
- Change file name to lightsail_key.rsa 
- Run chmod 600 lightsail_key.rsa
- Check the public IP address on the amazon AWS instance(My public IP: 54.172.77.105)

```sh
$ cd /c/Users/<your User name>/.ssh
$ ssh -i ~/.ssh/lightsail_key.rsa ubuntu@54.172.77.105 
```

#### 3. Update and upgrade installed packages.
```sh
$ sudo apt-get update
$ sudo apt-get upgrade
```

#### 4. Change SSH port from 22 to 2200. 
```sh
$ sudo nano /etc/ssh/sshd_config
 >> Change port number from 22 to 2200
 >> Ctrl + x and confirm with Y and press Enter
$ sudo service ssh restart 
```

#### 5. Configure Uncomplicated Firewall (UFW) 
> Project needs the server to only allow incoming connection for SSH(port 2200), HTTP(port 80) and NTP(port 123)  

```sh
$ sudo ufw status
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
$ sudo ufw allow 2200/tcp
$ sudo ufw allow www
$ sudo ufw allow 123/udp
$ sudo ufw deny 22
$ sudo ufw enable
$ sudo ufw status
```

> On Amazon lightsail instance next to your instance name, click on Manage tab. 
> Edit Firewall rules. Delete SSH TCP 22. Add UDP port 123 and TCP 2200. 


#### 6. Create grader user and manage grader access.
```sh
$ sudo adduser grader
 >> enter a password 
$ sudo visudo
>> under root privileges add the following
   grader ALL=(ALL:ALL) ALL
$ su -grader 
$ sudo -l
```

#### 7. Manage ssh access for grader.
On local machine generate keys and post public key content on virtual machine.
```sh
[On local machine] 
$ cd ~/.ssh
$ ssh-keygen
 >> This will generate two files (~/.ssh/grader_key && ~/.ssh/grader_key.pub) 

$ cat ~/.ssh/grader_key.pub
>> copy the contents  
```

```sh
[On grader machine - virtual]
$ su - grader 
$ mkdir .ssh
$ sudo nano ~/.ssh/authorized_keys
$ chmod 700 .ssh
$ chmod 644 .ssh/authorized_keys
$ sudo nano /etc/ssh/sshd_config 
>> check if passwordauthnetication is no 
$ sudo service ssh restart
$ exit
```
```sh
[On local machine]
$ ssh -i ~/.ssh/grader_key -p 2200 grader@54.172.77.105 
```

#### 8. Install Aphache2 and wsgi module.
```sh 
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi-py3 
$ sudo a2enmod wsgi
$ sudo service apache2 start
```

#### 9. Install git
```sh 
$ sudo apt-get install git
```

#### 10. Add catalog.wsgi.
```sh 
$ cd /var/www
$ sudo mkdir catalog
$ sudo chown -R grader:grader catalog
$ cd /var/www/catalog
$ sudo nano catalog.wsgi
>> add the following code in cataglog.wsgi 
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/")

from catalog import app as application
application.secret_key = 'super_secret_key'
```

#### 11. Clone the Item Catalog Project.  
```sh
$ git clone https://github.com/faith7/Item_Catalog_for_Project3.git catalog

>> After this, folder structure will be as follows
 var/www
      |_ catalog
      |        |_ catalog(formerly Item_Catalog_for_Project3.git repo) 
      |
      |_ catalog.wsgi
```

#### 12. Install dependencies
```sh
[On grader machine -virtual] 
$ sudo apt-get install python3-pip
$ pip3 install httplib2 
$ pip3 install requests
$ pip3 install --upgrade oauth2client
$ pip3 install sqlalchemy
$ pip3 install flask
$ sudo apt-get install python3-flask
$ pip3 install psycopg2
$ pip3 install flask_bootstrap
$ python3 -m pip3 install flask-bootstrap
```

#### 13. Configure virtual host
```sh
$ sudo nano /etc/apache2/sites-available/catalog.conf
```
>> Add the following code to configure virtual host

<VirtualHost *:80>
    ServerName 54.172.77.105
    ServerAdmin admin@webtesting
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

#### 14. Revise Flask project files for deployment
1) For google developer console, download a new client secret json file after updating google developer console - credentials part. I purchased google domain name (graceruns.com) and linked Amazon aws linux server to DNS. Replace the contents with current client_secrets.json. 

- Authorized JavaScript origins
   http://www.graceruns.com	 

-  Authorized redirect URIs
   http://www.graceruns.com/catalog	
   http://www.graceruns.com/login	
   http://www.graceruns.com/gconnect

```sh 
$ sudo nano client_secrets.json
```   

2-1) In __init__.py file, update client_id in login.html file as shown in client_secrets.json. 

2-2) In __init__.py file, add absolute path for client_secrets.json 
```sh
    APP_PATH = '/var/www/catalog/catalog/' 
    CLIENT_ID = json.loads(open(APP_PATH + 'client_secrets.json', 'r').read())['web']['client_id']
```
 
2-3) In __init__.py file, change host and port number.  
    # app.run(host='0.0.0.0, post=5000) 
    =>>> app.run() 


#### 15. Configure PostgreSQL.
```sh 
$ sudo apt-get install postgresql
$ sudo su - postgres (to change postgres user)
$ psql (To open interactive terminal)
$ postgres=# CREATE DATABASE catalog;
$ postgres=# CREATE USER catalog; 
$ postgres=# ALTER ROLE catalog WITH PASSWORD 'password'; 
$ postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
$ postgres=# \du; (to check existing roles)
$ postgres=# \q; (to quit postgresql)    
```

#### 16. Update database related python files for deployment.
[database_setup.py]
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)
==>>> engine = create_engine('postgresql://catalog:password@localhost/catalog')

[database_data.py]
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)
==>>> engine = create_engine('postgresql://catalog:password@localhost/catalog') 


#### 17. Disable the default Apache site and restart server. Refer to error logs and file structure for debugging.
```sh
$ sudo a2dissite 000-default.conf (to disable default page)
$ sudo a2ensite catalog (to enable flask app page)
$ sudo service apache2 restart (to restart apache)
$ sudo tail -f /var/log/apache2/error.log
$ sudo apt-get install tree (to check folder structure)
$ tree <$path$> (ex. tree /var/www/)
```

## References
- Apache2 configuration: https://tutorials.ubuntu.com/tutorial/install-and-configure-apache#4 
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- https://github.com/jungleBadger/-nanodegree-linux-server
- https://github.com/jungleBadger/-nanodegree-linux-server-troubleshoot/tree/master/ 
  python3%2Bvenv%2Bwsgi
- https://github.com/boisalai/udacity-linux-server-configuration
- stack overflow
