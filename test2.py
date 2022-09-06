from redis import Redis
from rq import Queue
import time
from ssssssssss import count_words_at_url
# queue = Queue(connection=Redis())
#
# job = queue.enqueue(count_words_at_url, 'http://nvie.com')
# print(job.result)

redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
job = q.enqueue(count_words_at_url,"http://nvie.com")
print(job.result)   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result)   # => None
