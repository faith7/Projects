# Logs Analysis Project
Logs analysis is part of Udacity Full Stack NanoDegree Program.  This project is to build an **internal reporting tool**  that will use information from database to find what kind of articles the site's readers like.  Python **psycopg2** module is used to connect to the database. 

### What are we reporting? 
     1. What are the most popular three articles of all time? 
     2. Who are the most poular article authors of all time? 
     3. On which days did more than 1% of requests lead to errors?

# Program Environment Requirements 
  - [Python3](https://www.python.org/downloads/)
  - [Linux-based Virtual Machine (VM)](https://www.virtualbox.org/wiki/Download_Old_Builds) 
  - [Virtual Machine Management tool - Vagrant](https://www.vagrantup.com/downloads.html)
  - [PostgreSql](https://www.postgresql.org/)
  - [Psycopg2](http://initd.org/psycopg/)
  - [newsdata.sql (Data)](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project1_Log%20Analysis/data)

> VM & Vagratn Program requirements can also be downloaded at 
https://github.com/udacity/fullstack-nanodegree-vm

# Run the Program 
#### 1. Git clone to download required programs. 
``` 
$ git clone https://github.com/udacity/fullstack-nanodegree-vm
```

#### 2. Bring virtual machine on and log in. 
```
$ vagrant up
$ vagrant ssh
```

#### 3. Download and unzip the data- newsdata   [here](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project1_Log%20Analysis/data) . 
To load data, change directory to vagrant and use the command psql -d news -f newsdata.sql

```
$ cd /vagrant 
$ psql 
$ -d news
$ -f newsdata.sql
```

#### 4. Create views in news database. 
 You can also refer to my git repository for text version of creating view SQL command [here](https://github.com/faith7/Udacity_Projects_FullStack/tree/master/Project1_Log%20Analysis).

```
$ cd /vagrant 
$ psql -d news
$ create view [view name] as [sql view queries] 
```
#### SQL Views 

| View Name | SQL view queries |
| ------ | ------ |
| total_request| select date(time) as day, count(*) as total from log group by day order by total; 
| error_request | select date(time) as day, count(*) as error from log where status not like '%200%' group by day order by error desc; 
| error_percent | select total_request.day, round(100.0*error_request.error/total_request.total,2) as error_pct from total_request, error_request where total_request.day = error_request.day; |


#### 5. Run the reporting program. 
```python
$ python reporting.py
```
## Coding Style Test
 PEP8 style recommendation is followed. 
```
$ pip3 install pycodestyle
$ pycodestyle reporting.py
```

### Author
 * Grace C.(faith7) 
 