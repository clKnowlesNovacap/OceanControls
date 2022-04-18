from ocean_controls import Ocean_Controls
import time
import signal

def main():
    oc.set_port("COM7")
    oc.acci(1,10)
    oc.accs(100)
    oc.accf(1,3000)
    while True:
        oc.rmov(1,10000)
        oc.rmov(1,-10000)

def handler(signum, frame):
    res = input("Exit? y/n ")
    if res == 'y':
        oc.close_port()
        exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    oc = Ocean_Controls()
    main()