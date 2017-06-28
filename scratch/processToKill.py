import sys
import time

def main():

    i=0
    try:
        while True:
            time.sleep(1)
            print i
            i+=1
    except KeyboardInterrupt:
        print "Goodbye"
        sys.exit()

if __name__ == "__main__":
    main()
