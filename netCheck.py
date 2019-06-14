import os

ip="www.baidu.com"
num=1

def ping_netCheck():
    cmd = "ping " +ip + ' -c '+str(num)
    exit_code = os.system(cmd)
    if exit_code:
        return False
    return True

if __name__ == "__main__":
    if ping_netCheck():
        print('connected!')
    else:
        print('failed!')