'''total_request'''
create view total_request as
select date(time) as day, count(*) as total
from log group by day order by total;

'''error_request'''
create view error_request as
select date(time) as day, count(*) as error from log
where status not like '%200%'
group by day
order by error DESC;

'''error_percent'''
create view error_percent as
select total_request.day,
round(100.0*error_request.error/total_request.total,2) as error_pct
from total_request, error_request
where total_request.day = error_request.day;
