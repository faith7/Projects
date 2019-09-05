# Item Catalog Project
Item Catalog Project is part of Udacity Full Stack NanoDegree Program. This project is to build an application that  that provides **a list of items within different categories** and provide a user registration and authentication system. Registered users have the ability to make a **CRUD(create, read, edit and delete) operation** on their own items.

# Technologies for this project 
  - Flask framework
  - Restful API
  - OAuth authentication(Google OAuth)
  - Bootstrap for front end development

# Program Environment Requirements 
  - [Python3](https://www.python.org/downloads/)
  - [Linux-based Virtual Machine (VM)](https://www.virtualbox.org/wiki/Download_Old_Builds) 
  - [Virtual Machine Management tool - Vagrant](https://www.vagrantup.com/downloads.html)
  - [Flask](https://pypi.org/project/Flask/)
  - [SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy)
  - [Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjw5MLrBRClARIsAPG0WGzviTAg6Fa8-kxRQ3a6-ktgW-Ftjwzbe2WXAc-eofRSmF6MWQnMg8IaAmvDEALw_wcB&gclsrc=aw.ds)
  

> VM & Vagratn Program requirements can also be downloaded at 
https://github.com/udacity/fullstack-nanodegree-vm

# Run the Program 
#### 1. Git clone to download required programs. 
``` 
$ git clone https://github.com/udacity/fullstack-nanodegree-vm
```

#### 2. Change directory to vagrant and git clone [this](https://github.com/faith7/Udacity_Projects_FullStack) repository. 
```
$ cd /vagrant 
$ git clone https://github.com/faith7/Udacity_Projects_FullStack
```

#### 3. Bring virtual machine on and log in. 
```
$ vagrant up
$ vagrant ssh
```

#### 4. set up database environment& data and run the server. 
To run the app, after running vagrant, change directory to Project2_Catalog
```
$ sudo pip install -U Flask-SQLAlchemy
$ cd /vagrant/Project2_Catalog
$ python database_setup.py 
$ python database_data.py
$ python app.py 
```

#### 5. open your favorite browser and redirect to localhost:5000. Test the application. 
You can create, edit, delete categories and items after sign-in. Only the person who created the item can manage(edit/delete) the specific item as a part of local permission system. Please check out the following for further demonstration.
 
# application demo 
![1.Five latest movies/shows](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project2_Catalog/result_view_gif/first_page.gif) 
![2.Manage categories](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project2_Catalog/result_view_gif/manage_category.gif) 
![3.Manage items](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project2_Catalog/result_view_gif/manage_item.gif)
![4.Public item view page before sign-in](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project2_Catalog/result_view_gif/item_publicpage.gif) 

# Coding Style Test
 - PEP8 style recommendation is followed for python.
 - Beautify selection is followed for Html/Css/Javascript.
   Downloaded as visual studio code editor extension.
 
```
$ pip3 install pycodestyle
$ pycodestyle app.py
```

# Further improvement/Limitaions 
- Other types of Oauth like Facebook log-in is not implemented.
- Bootstrap is used for the front end development. 
  Header.html include script tags instead of using separate css file due to inheritance problem of form styles in css files.
- Udacity provided python2 development environment. 
  I upgraded to python3 (Python 3.7.4) for this project and  updated pip accordingly. 
- Logout file did not use css format. Redirect page did not format correctly. 
  Further study needed to format json response with CSS properly.
  
```
$ touch .bashrc
$ vim .bashrc 
- write alias in .bashrc file to use python command using python3.7 version
  alias python = python3.7 
  $ sudo apt install python3-pip (to install pip)
```

# Data credits for this project 
- Wikipedia/Wikimedia for movie or show urls. 
  Each poster url links can be found in database_data file in this repository.
  Licensing and usage is on the guide provided from each Wikipedia/Wikimedia links.

- Unsplash photos for background images 
  1) https://source.unsplash.com/16Tu8S18pu4
      twinsfisch@twinsfisch
  
  2) https://source.unsplash.com/jtmwD4i4v1U
      Charles 🇵🇭@charlesdeluvio
  
  3) When the application could not find url, the following image is used.
      https://source.unsplash.com/NodtnCsLdTE
      Mikhail Vasilyev@miklevasilyev

- When user did not provide the image url, the application uses black hole image from 
  https://en.wikipedia.org/wiki/File:Black_hole_-_Messier_87_crop_max_res.jpg

- [screentogif app](https://www.screentogif.com/) for application demo
- [dillinger](https://dillinger.io/) for the readme file
