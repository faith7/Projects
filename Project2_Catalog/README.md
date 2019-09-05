# Item Catalog Project

&nbsp;
## About this Project
Item Catalog Project is part of Udacity Full Stack NanoDegree Program. 
This project is to build an application that  that provides **a list of items within different categories** and provide a user registration and authentication system. 
Registered users have the ability to make a **CRUD(create, read, edit and delete) operation** on their own items.

&nbsp;
## Technologies for this project 
  - Flask framework
  - Restful API
  - OAuth authentication(Google OAuth)
  - Bootstrap for front end development

&nbsp;
## Program Environment Requirements 
  - [Python3](https://www.python.org/downloads/)
  - [Linux-based Virtual Machine (VM)](https://www.virtualbox.org/wiki/Download_Old_Builds) 
  - [Virtual Machine Management tool - Vagrant](https://www.vagrantup.com/downloads.html)
  - [Flask](https://pypi.org/project/Flask/)
  - [SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy)
  - [Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjw5MLrBRClARIsAPG0WGzviTAg6Fa8-kxRQ3a6-ktgW-Ftjwzbe2WXAc-eofRSmF6MWQnMg8IaAmvDEALw_wcB&gclsrc=aw.ds)
  

> VM & Vagratn Program requirements can also be downloaded at 
https://github.com/udacity/fullstack-nanodegree-vm

&nbsp;
## Run the Program 
#### 1. Git clone to download required programs. 
``` sh
$ git clone https://github.com/udacity/fullstack-nanodegree-vm
```

#### 2. Change directory to vagrant and git clone [this](https://github.com/faith7/Udacity_Projects_FullStack) repository. 
```sh
$ cd /vagrant 
$ git clone https://github.com/faith7/Udacity_Projects_FullStack
```

#### 3. Bring virtual machine on and log in. 
```sh
$ vagrant up
$ vagrant ssh
```

#### 4. Set up database environment& data and run the server. 
To run the app, after running vagrant, change directory to Project2_Catalog
```sh
$ sudo pip install -U Flask-SQLAlchemy
$ cd /vagrant/Project2_Catalog
$ python database_setup.py 
$ python database_data.py
$ python app.py 
```

#### 5. Open your favorite browser and redirect to localhost:5000. Run the application. 
>You can create, edit, delete categories and items after sign-in. 
&nbsp;
>**Only the person who created the item can manage(edit/delete)** the specific item as a part of local permission system. 
Please check out the following for further demonstration.

&nbsp;
## Application demo 
&nbsp;
### 1. Browse five latest movies/shows on the first page.
![](https://github.com/faith7/Udacity_Projects_FullStack/blob/master/Project2_Catalog/result_view_gif/first_page.gif) 
&nbsp;
### 2. On the second page, log in to manage each categories. 
![](https://github.com/faith7/Udacity_Projects_FullStack/blob/master/Project2_Catalog/result_view_gif/manage_category.gif)
&nbsp;
### 3. Manage each item within a specific category.
![](https://github.com/faith7/Udacity_Projects_FullStack/blob/master/Project2_Catalog/result_view_gif/manage_item.gif)
&nbsp;
### 4. Public view for each item before you sign-in.
![](https://github.com/faith7/Udacity_Projects_FullStack/blob/master/Project2_Catalog/result_view_gif/manage_item.gif) 

&nbsp;
## Coding Style Test
 - PEP8 style recommendation is followed for python.
 - Beautify selection is followed for Html/Css/Javascript.
   Downloaded as visual studio code editor extension.
 
```sh
$ pip3 install pycodestyle
$ pycodestyle app.py
```

&nbsp;
## Further improvement/Limitaions 
 - Other types of Oauth like Facebook log-in is not implemented.
&nbsp;
 - Bootstrap is used for the front end development. 
&nbsp;
 - Header.html include script tags instead of using separate css file due to  inheritance problem of form styles in css files.
&nbsp;
 - Udacity provided python2 development environment. 
   I upgraded to python3 (Python 3.7.4) for this project and  updated pip accordingly.
&nbsp;
- Logout file did not use css format. Redirect page did not format correctly. 
  Further study needed to format json response with CSS properly.
  
```sh
$ touch .bashrc
$ vim .bashrc 
  (write alias in .bashrc file to use python command using python3.7 version) 
   alias python = python3.7 
$ sudo apt install python3-pip (to install pip)
```

&nbsp;
## Credits to data used for this project 
| Source | Usage | License/Credits|
| ------ | ------ | ------ |
| Wikipedia/Wikimedia | [movie or show urls](https://github.com/faith7/Udacity_Projects_FullStack/blob/master/Project2_Catalog/database_data.py) | Each License information is found at wikimedia file upload page
|Unsplash photos  | background images |(twinsfisch@twinsfisch)[https://unsplash.com/photos/5tlxS_jlVGY],(Charles 🇵🇭@charlesdeluvio)[https://unsplash.com/photos/jtmwD4i4v1U],(Mikhail Vasilyev@miklevasilyev)[https://unsplash.com/photos/NodtnCsLdTE]|
| wikipedia black hole image| when no picture is given |(blackhole)[https://en.wikipedia.org/wiki/File:Black_hole_-_Messier_87_crop_max_res.jpg]| 
|screentogif app | demo gif files| (screentogif)[https://www.screentogif.com/] |
| Dilinger | readme file| (dillinger)[https://dillinger.io/]|
