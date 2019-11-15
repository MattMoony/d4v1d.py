import os
import random
import colorama
import lib.st4lker
import lib.scr4p3r
from colorama import Fore, Back, Style
from argparse import ArgumentParser

def print_title():
    title = [
        'd8888b.   j88D  db    db  db d8888b.',
        '88  `8D  j8~88  88    88 o88 88  `8D',
        '88   88 j8\' 88  Y8    8P  88 88   88',
        '88   88 V88888D `8b  d8\'  88 88   88',
        '88  .8D     88   `8bd8\'   88 88  .8D',
        'Y8888D\'     VP     YP     VP Y8888D\''
    ]
    colors = [
        Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
        Fore.MAGENTA, Fore.CYAN, Fore.WHITE
    ]
    col = os.get_terminal_size().columns
    
    print('='*col)
    print()
    for l in title:
        print(colors[random.randint(0,len(colors)-1)] +\
              ('{:^'+str(col)+'}').format(l))
    print(Fore.RESET)
    print('='*col)
    
def print_err(msg):
    print(Fore.RED + '[!]: '+ Fore.RESET + msg)

def main():
    colorama.init()
    
    parser = ArgumentParser()
    parser.add_argument('--st4lk', action='store_true', dest='st4lk', help='St4lk user?')
    parser.add_argument('--scr4p3', action='store_true', dest='scr4p3', help='Scr4p3 account?')
    parser.add_argument('-u', '--username', type=str, dest='uname', help='Target username ... ')
    parser.add_argument('-d', '--dest-dir', type=str, dest='dstdir', help='Output directory (for scraped images, etc.)')
    args = parser.parse_args()
    
    print_title()
    
    if args.st4lk:
        if not args.uname:
            print_err('Username (argument: -u) is required!')
            os._exit(1)
        lib.st4lker.st4lk(args.uname)
        
    if args.scr4p3:
        if not args.uname:
            print_err('Username (argument: -u) is required!')
            os._exit(1)
        lib.scr4p3r.scr4p3(args.uname, args.dstdir)
    
if __name__ == '__main__':
    main()