# Log analysis of news database code

import psycopg2
import bleach

query1_title = " What are the most popular three articles of all time? \n"
query1 = '''
select articles.title, count(*) as views from articles join log
on log.path like concat('%', articles.slug)
group by articles.title order by views desc limit 3
'''

# alternative way
'''
query1 = select title, count(*) as views from articles, log
where log.path = concat('/article/', articles.slug)
group by articles.title limit 3
'''

query2_title = " Who are the most popular article authors of all time? \n"
query2 = '''
select authors.name, count(*) as views from articles join authors 
on authors.id = articles.author
join log on log.path=concat('/article/', articles.slug)
group by authors.name order by views desc
'''

# create views
'''
1. total_request
create view total_request as
select date(time) as day, count(*) as total from log
group by day 
order by total; 

2. error_request 
create view error_request as 
select date(time) as day, count(*) as error from log
where status not like '%200%'
group by day 
order by error DESC; 

3. error_percent
create view error_percent as 
select total_request.day, 
round(100.0*error_request.error/total_request.total,2) as error_pct 
from total_request, error_request
where total_request.day = error_request.day;
'''

query3_title = ''' On which days did more than 1 percent of requests lead to errors? \n'''

query3 = '''
select to_char(day,'Mon DD, YYYY'), error_percent.error_pct as error from error_percent 
where error_pct > 1.0 ;
'''


def get_queries(query_num):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query_num)
    query_result = c.fetchall()
    for i in range(len(query_result)):
        result=query_result[i][0]
        views=query_result[i][1]
        if (query_num == query3):
            print(" * %s -- %.2f errors" %(result, views))  
        else:
            print(" * %s -- %d views" %(result, views))
        

    db.close()
    


if __name__ == "__main__":
    print("\n")
    print(query1_title)
    get_queries(query1)
    print("\n")

    print(query2_title)
    get_queries(query2)
    print("\n")
    
    print(query3_title)
    get_queries(query3)
    print("\n")