import threading

def print1():
    for i in range(10):
        print(i)
    return 5


def print2():
    for i in range(10, 20):
        print(i)
    return 6
t1 = threading.Thread(target=print1, name='t1')
t2 = threading.Thread(target=print2, name='t2')

t1.start()
t2.start()

