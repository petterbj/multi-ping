import subprocess
import time
import multiprocessing
TIME_OUT = 1000
def ping(host):
    try:
        total_time = 0
        result = subprocess.check_output(['ping', '-c', '3', host])
        for line in result.splitlines()[1:-4]:
            if line.startswith('Request timeout'):
                total_time = total_time + TIME_OUT;
            elif line.endswith('data bytes'):
                total_time = total_time
            elif line == '':
                total_time = total_time
            else:
                total_time = total_time + float(line.rpartition('=')[-1].rpartition(' ')[0])
        print total_time/3.0, host
        return [total_time/3.0,host]
    except subprocess.CalledProcessError:
        print 'CalledProcessError ' + host
        return [TIME_OUT,host]
def cmp(a,b):
    if a[0]==b[0]:
        return 0
    elif a[0]>b[0]:
        return 1
    elif a[0]<b[0]:
        return -1
    else:
        print 'Error'
        return
if __name__ == '__main__':
    start = time.time()
    iplist = open('iplist.ini').read().splitlines()
    pool = multiprocessing.Pool()
    results = []
    for ip in iplist:
        results.append(pool.apply_async(ping,args=(ip,)))
    pool.close()
    pool.join()
    array = []
    for result in results:
        array.append(result.get())
    array.sort(cmp)
    print array[0:10]
    print "total time spent is ", time.time()-start

