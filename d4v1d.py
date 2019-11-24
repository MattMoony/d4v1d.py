import os
import random
import colorama
import threading
import lib.st4lker
import lib.scr4p3r
import lib.s3rv3r
from selenium import webdriver
from argparse import ArgumentParser
from colorama import Fore, Back, Style
from selenium.webdriver.chrome.options import Options

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
    parser.add_argument('--visible', action='store_true', dest='visible', help='Should the browser window be visible?')
    parser.add_argument('--log-all', action='store_true', dest='log_a', help='Prints every chromedriver message to the console')
    parser.add_argument('-u', '--username', type=str, dest='uname', help='Target username ... ')
    parser.add_argument('--dest-dir', type=str, dest='dstdir', help='Output directory (for scraped images, etc.)')
    parser.add_argument('--depth', type=int, dest='depth', help='St4lk1ng depth ...', default=0)
    parser.add_argument('--flim', type=int, dest='flim', help='Follower/ing limit ... ', default=500)
    args = parser.parse_args()
    
    print_title()
    
    opts = Options()
    if not args.visible:
        opts.add_argument('--headless')
    else:
        print(Fore.RED + '[!] WARNING: Please do not interact with the browser window, since it might lead to unexpected behaviour ... ')
    if not args.log_a:
        opts.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=opts)

    t = threading.Thread(target=lib.s3rv3r.init, args=(os.path.dirname(os.path.realpath(__file__)),))
    t.start()
    
    if args.st4lk:
        if not args.uname:
            print_err('Username (argument: -u) is required!')
            os._exit(1)
        lib.st4lker.st4lk(driver, args.uname, args.dstdir, args.depth, args.flim)

    if args.scr4p3:
        if not args.uname:
            print_err('Username (argument: -u) is required!')
            os._exit(1)
        lib.scr4p3r.scr4p3(driver, args.uname, args.dstdir)

    input('<: ENTER TO EXIT :>')
    driver.quit()
    
if __name__ == '__main__':
    main()