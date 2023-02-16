import math
import random
import time
from multiprocessing import Process, Value, Lock
from multiprocessing.sharedctypes import Synchronized
from multiprocessing.synchronize import Lock as LockType

# Assume a circle radius of 1.
def dist(x1, y1, x2=0, y2=0):
  return math.sqrt(math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2))


def throw_darts(pid, num_darts, num_in_circle: Synchronized, lock: LockType):
  cur_in_circle = 0
  for i in range(num_darts):
    x1 = random.random()
    y1 = random.random()
    if (dist(x1, y1) <= 1):
      cur_in_circle += 1

  with lock:
    num_in_circle.value += cur_in_circle


def pi(n_darts, n_procs):
  procs = []
  num_in_circle = Value("l")
  lock = Lock()
  for pid in range(n_procs):
    p = Process(target=throw_darts, args=(pid, n_darts // n_procs, num_in_circle, lock))
    procs.append(p)

  for p in procs:
    p.start()

  for p in procs:
    p.join()

  return 4 * (num_in_circle.value / n_darts)


if __name__ == '__main__':
  avg_pi_val = 0
  num_iters = 10
  for i in range(num_iters):
    t1 = time.time()
    pi_val = pi(n_darts=50000000000, n_procs=24)
    t2 = time.time()
    avg_pi_val += pi_val
    print(f"pi_val = {pi_val}\t iteration = {i}\t time = {t2-t1}")
  avg_pi_val /= num_iters
  print(f"avg_pi_val = {avg_pi_val}\t num_iters = {num_iters}")
