# server.py
# Fib microservice

from socket import *
from fib import fib
from collections import deque
from select import select
from concurrent.futures import ThreadPoolExecutor as Pool

pool = Pool(10)
tasks = deque()
recv_wait = { }  # Mapping sockets -> tasks (generators)
send_wait = { }

def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # no active tasks to run
            # wait for I/O
            can_recv, can_send, [] = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))

        task = tasks.popleft()
        try:
            why, what = next(task)  # Run to the yield
            if why == 'recv':
                # Must go wait somewhere
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            else:
                raise RuntimeError('ARG!')
        except StopIteration:
            print('task done')

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept()  # blocking
        print('Connection', addr)
        tasks.append(fib_handler(client))

def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100)  # blocking
        if req.strip() == b'' or not req:
            break
        n = int(req.strip())
        future = pool.submit(fib, n)
        result = future.result()  # Blocks
        resp = str(result).encode('ascii') + b'\n'
        print(resp)
        yield 'send', client
        client.send(resp)  # blocking
    print('Closed')

tasks.append(fib_server(('', 25000)))
run()
