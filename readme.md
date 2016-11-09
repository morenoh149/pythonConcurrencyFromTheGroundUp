# Python Concurrency From the Ground Up

Code along for https://www.youtube.com/watch?v=MCs5OvhV9S4

## Notes

* first version can only serve one client at a time
* we add Thread to service multiple clients, but due to python's GIL we can only use one cpu
  * response time grows linearly proportional to the number of concurrent requests
  * python, unlike most Operating Systems, will give priority to cpu-bound requests. So a computationally expensive request will tie up the server.
