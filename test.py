from app import get_db_connection
import datetime
import time
def DateTimeConvert(date_in):
    date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    return int(time.mktime(datetime.datetime(*date_processing).timetuple()))
conn = get_db_connection()
posts = conn.execute("select * from posts where DATE(created) == strftime('%Y-%m-%d','2021-04-27')").fetchall()
conn.close()
intimes = []
outtimes =[]
for i in posts:
    print(i[1])
    print(DateTimeConvert(i[1]))
    intimes.append(DateTimeConvert(i[1]))
    outtimes.append(DateTimeConvert(i[5]))

first_entry = min((intimes))
last_exit = max((outtimes))

print('-----------------------')

step = 60
period = 600
max_number = 0
startTime = 0
endTIme = 0
for i in range(first_entry,last_exit,step):
    count = 0
    for out in outtimes:
        if out >= i and out <=i+period:
            count+=1
    if count>max_number:
        max_number = count
        startTime = i
        endTIme = i+period

print(max_number)
print(startTime)
print(endTIme)
print(datetime.datetime.fromtimestamp(startTime / 1e3))
print(datetime.datetime.fromtimestamp(endTIme / 1e3))
print(datetime.datetime.fromtimestamp(startTime))
# // 9:00 9:10
# // exitTime > 9:10 ===> counter
# // 9:11 9:20
# // exitTime > 9:20 ==> counter

# // 00:00 00:10

# date 
# days first entry



# 5
# 10
# 20
# 

# 9:30 - 11:30


# greatere than created but less than created + 10 and exit > created + 10
# posts = conn.execute('SELECT id,whom_to_meet FROM posts').fetchall() 2021-04-27T18:00 strftime('%s', 'now')
# posts = conn.execute("select id  from posts  where created > strftime('%Y-%m-%dT%H:%M','27-04-2021T18:00')  ").fetchall()
# posts = conn.execute("SELECT count(id) FROM posts WHERE exit BETWEEN '2021-04-27T18:00' AND '2021-4-27T19:01';").fetchall()
# posts = conn.execute('SELECT id,whom_to_meet,COUNT(whom_to_meet) FROM posts GROUP BY whom_to_meet ORDER BY whom_to_meet DESC LIMIT 1').fetchall()
# posts = conn.execute("SELECT DATE(created) AS date, strftime ('%H',created) hour, COUNT(id) AS TOTALVISITER FROM posts GROUP BY date, hour ORDER BY date, hour, TOTALVISITER DESC").fetchall()
