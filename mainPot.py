#!/usr/bin/python
import socket
import time
import geoip2.database
import threading
import os
import queue
import signal

q = queue.Queue()
num_of_threads = 5
jobs_to_do = [1, 2, 3, 4, 5, 6, 7]



THREADS = []

def handler(signal, frame):
    global THREADS
    print ("Ctrl-C.... Exiting")
    for t in THREADS:
        t.alive = False
    sys.exit(0)




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dt = geoip2.database.Reader('GeoLite2-City.mmdb')

def geo_locate(tgt):
    try:
        gi = dt.city(tgt)
        try:
            
            print ('[+] {}'.format(tgt))
        except:
            print ('[-] couldnt identify the target')
        try:
            city = gi.city.name
            print ('[+] {}'.format(city))
        except:
            print ('[-] Couldnt identify the city')
        try:
            country = gi.country.name
            print ('[+] {}'.format(country))
        except:
            print ('[-] Couldnt identify the country')
        try:
            longe = gi.location.latitude
            lat = gi.location.latitude
            print ('LON: {} / LAT: {}'.format(longe, lat))
        except:
            print ('[-] Couldnt geo locate the target')
    except:
        print('Ip not found in the database')


def http_pot(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 80))
    print ('[*] HTTP pot LISTENING....')
    while True:
        s.listen(6)

        soc, addr = s.accept()
        if len(str(geo_locate(tgt=addr[0]))) != 0 and str(geo_locate(addr[0])) != None:
            print ('HTTP HoneyPot Victim: ', addr[0],'\n')
            geo_locate(addr[0])
        time.sleep(1)

        soc.close()


def ssh_pot(host):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 22))
    print ('[*] SSH pot LISTENING.....\n')
    while True:
        s.listen(6)
        soc, addr = s.accept()
        print ('[+] SSH pot victim: ', addr[0], '\n')
        geo_locate(addr[0])
        soc.close()


def ftp_pot(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 21))
    print ('[*] FTP pot is LISTENING...\n')
    while True:
        s.listen(5)
        sock, addr = s.accept()
        print ('[+] FTP pot victim : ', addr[0], '\n')
        geo_locate(addr[0])
        sock.close()


def postgresql_pot(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 5432))
    print ('[*] POSTGRESQL pot is LISTENING...\n')
    while True:
        s.listen(5)
        sock, addr = s.accept()
        print ('[+] POSTGRESQL pot victim : ', addr[0], '\n')
        geo_locate(addr[0])

def mysql_pot(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 3306))
    print ('[*] MYSQL pot is LISTENING....\n')
    while True:
        s.listen(5)
        sock, addr = s.accept()
        print ('[+] MYSQL pot victim : ', addr[0])
        geo_locate(addr[0])
        sock.close()


def create_worker():
    for threads in range(num_of_threads):
        t = threading.Thread(target=work, args=())
        t.daemon = True
        THREADS.append(t)
        t.start()


host = '127.0.0.1'


def Ishell():
    while True:
        x = os.getlogin() + '@' + os.uname()[1] + ':~# '
        l = raw_input(str(x))
        if l == 'clear':
            os.system('clear')
        if l == 'quit':
            exit(0)


def work():
    x = q.get()
    if x == 1:
        http_pot(host)
    if x == 2:
        ftp_pot(host)
    if x == 3:
        ssh_pot(host)
    if x == 4:
        postgresql_pot(host)
    if x == 5:
        mysql_pot(host)
    if x == 6:
        Ishell()

    q.task_done()


def create_jobs():
    for job in jobs_to_do:
        q.put(job)
    q.join()


def main():
    create_worker()
    create_jobs()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, handler)
	main()
	


	#ips = ['1.66.7.156','27.217.81.123','63.209.214.145','232.120.52.252','14.111.114.49']

	#for ip in ips:
		#geo_locate(ip)
		#print("-*-"*20)