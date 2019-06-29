2# Logs Analysis Project
Logs analysis is part of Udacity Full Stack NanoDegree Program.  This project is to build an **internal reporting tool**  that will use information from database to find what kind of articles the site's readers like.  Python **psycopg2** module is used to connect to the database. 

## Program Environment Requirements 
 
  - [Python3](https://www.python.org/downloads/)
  - [Linux-based Virtual Machine (VM)](https://www.virtualbox.org/wiki/Download_Old_Builds) 
  - [Virtual Machine Management tool - Vagrant](https://www.vagrantup.com/downloads.html)
 
 > VM & Vagratn Program requirements can also be downloaded at 
https://github.com/udacity/fullstack-nanodegree-vm


## Run the Program

Bring virtual machine online and log in. 
```sh
$ vagrant up
$ vagrant ssh
```
Install postgresql to use PostgreSQL. 
```sh
$ sudo apt-get install postgresql
```

Database for this project is in **newsdata.sql**. To load the data, change directory to vagrant where PostgreSQL database and supporting software resides.
```sh
$ cd /vagrant 
$ psql
$ -d news
$ -f newsdata.sql
```

# What are we reporting? 
     1. What are the most popular three articles of all time? 
     2. Who are the most poular article authors of all time? 
     3. On which days did more than 1% of requests lead to errors?
 
# SQL views 

*CREATE VIEW  [view name]  AS  [sql view queries]*

| View Name | SQL view queries |
| ------ | ------ |
| total_request| select date(time) as day, count(*) as total from log group by day order by total; 
| error_request | select date(time) as day, count(*) as error from log where status not like '%200%' group by day order by error desc; 
| error_percent | select total_request.day, round(100.0*error_request.error/total_request.total,2) as error_pct from total_request, error_request where total_request.day = error_request.day; |


### Development
 Want to contribute? Great!
 Feel free to pull or send me a message! 
