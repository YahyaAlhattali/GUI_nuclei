from rq import Queue
from redis import Redis

redis_conn = Redis()
q = Queue(connection=redis_conn)

# Getting the number of jobs in the queue
# Note: Only queued jobs are counted, not including deferred ones
print(len(q))

# Retrieving jobs
queued_job_ids = q.job_ids # Gets a list of job IDs from the queue
queued_jobs = q.jobs # Gets a list of enqueued job instances
job = q.fetch_job('my_id') # Returns job having ID "my_id"

# Emptying a queue, this will delete all jobs in this queue
q.empty()

# Deleting a queue
q.delete(delete_jobs=True) # Passing in `True` will remove all jobs in the queue
# queue is now unusable. It can be recreated by enqueueing jobs to it.