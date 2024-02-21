from threading import Thread
from time import sleep

total_sum = 0
def gauss_sumation(name, n):
    """The Gaus gauss_sumation"""
    global total_sum
    for i in range(1, n + 1):
        sleep(0.01)
        print(f"thread {name}: actual total_sum  {total_sum + i}, operation: {total_sum} + {i}")
        total_sum += i


# create threads
t1 = Thread(target = gauss_sumation, args = ("1", 10,), daemon = True)
t2 = Thread(target = gauss_sumation, args = ("2", 10,), daemon = True)

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()

print(f'The final total_sum is {total_sum}')
