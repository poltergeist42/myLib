import time
import sys

width = 100

def do_task():
        time.sleep(0.1)
        

def example_1(n):
    v_char = '#'
    spaces = ' ' * (width-1)
    backspace = '\b' * (width+4)
    v_percent = 0
    print('Starting [{}] {:03}%{}'.format(spaces, v_percent, backspace), end='')
    sys.stdout.flush()
    steps = n / width
    for i in range(n):
        v_percent+=1
        spaces = ' ' * (width - i )
        backspace = '\b' * ((width+6)-i)
        do_task()
        if i % steps == 0:
            print("{}{}] {:03}%{}".format(v_char, spaces, v_percent, backspace), end='')
            sys.stdout.flush()   


example_1(100)