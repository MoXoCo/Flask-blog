import time

def log(*args):
    t = time.time()
    localtime = time.localtime(t)
    patten = '%Y-%m-%d %H:%M:%S'
    tt = time.strftime(patten, localtime)
    print(tt, *args)