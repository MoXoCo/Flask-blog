import time

def log(*args):
    t = time.time()
    tt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    print(tt, *args)

