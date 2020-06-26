import requests
from threading import Thread
from queue import Queue
from colored import fg, bg, attr

x = Queue() #defining x to hold the queue for subdominas 

def subs(domain):
    global x
    while True:
        sdomain = x.get()
        location = f"http://{sdomain}.{domain}"
        try:
            requests.get(location)
        except requests.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            print('%s [-] Unavailable url: %s' % (fg(1), attr(0)), location)
        except UnicodeError:
             print ('%s%s The unicode character was not recognized from the wordlist %s' % (fg(1), bg(15), attr(0)))
        else:
            print('%s [+] Active url: %s' % (fg(10), attr(0)) , location)
        x.task_done()
    while True:
        sdomain = x.get()
        location = f"https://{sdomain}.{domain}"
        try:
            requests.get(location)
        except requests.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            print('%s [-] Unavailable url: %s' % (fg(1), attr(0)), location)
        except UnicodeError:
            print('%s There was some error in Unicode%s' % (fg(5), attr(0)))
        else:
            print('%s [+] Active url: %s' % (fg(10), attr(0)) , location)
        x.task_done()
        
def main(domain,sub,nthreads):
    global x

    for j in sub:
        x.put(j)

    for t in range(nthreads):
        kam = Thread(target=subs, args=(domain,))
        kam.daemon = True
        kam.start()


if __name__ == "__main__":
    import argparse
    

    parser = argparse.ArgumentParser(description='Noob script bruteforce some sub domains by @gamerited')
    parser.add_argument("domain", help="Hit down the domain you wana bruteforce (e.g. google.com)")
    parser.add_argument("-w", "--wordlist", help="Enter the location of your wordlist that you wana use to Bruteforce the domain")
    parser.add_argument("-t","--num-threads", help="Please enter the number of threads you want to use.(default is 10)",default=20,type=int)
    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    nthreads = args.num_threads
    
    main(domain=domain, nthreads=nthreads, sub=open(wordlist, encoding="ISO-8859-1").read().splitlines())

    x.join()










