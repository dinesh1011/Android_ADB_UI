import asyncio
import time
from datetime import datetime

async  def is_prime(numb):
    for itr in range(2, numb):
        if(numb % itr == 0):
            return False
    return True

async def primes(start_number, end_number):
    for num in range(start_number, end_number+1):
        #prime_flag = lib.is_prim(num)
        prime_flag = await is_prime(num)
        if(prime_flag):
            print(str(num) + "is prime")
        else:
            print(str(num) + "is not prime")

async def runall():
    await primes(1, 100)
    await primes(101, 300)


start = time.time()
my_event_loop = asyncio.get_event_loop()

task_obj = [
    my_event_loop.create_task(primes(1, 100)),
    my_event_loop.create_task(primes(101, 200))
]

#my_event_loop.call_soon(asyncio.async, task_obj)

my_event_loop.close()
end = time.time()
print("Total time: {}".format(end - start))

