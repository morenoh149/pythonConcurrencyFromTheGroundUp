# Python Concurrency From the Ground Up

Code along for https://www.youtube.com/watch?v=MCs5OvhV9S4

## Notes

* first version can only serve one client at a time
* we add Thread to service multiple clients, but due to python's GIL we can only use one cpu
  * response time grows linearly proportional to the number of concurrent requests
  * python, unlike most Operating Systems, will give priority to cpu-bound requests. So a computationally expensive request will tie up the server.
* we add a pool so a cpu-bound requests don't affect shorter requests
* we move away from threads and use generators to achieve concurrency.
  * still only use 1 cpu
  * still have linear growth in response time
  * still have cpu-bound tasks slowing short tasks down
* punt coroutine work to a thread pool
