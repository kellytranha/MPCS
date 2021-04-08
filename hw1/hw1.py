
"""HW1 CLI
Usage:
    hw1.py
    hw1.py <name>
    hw1.py -h|--help
Options:
    <name>  Optional name argument.
    -h --help  Show this screen.
"""

from docopt import docopt

def reserve(name):
    return("Hello {}!".format(name))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['<name>']:
        print(say_hello(arguments['<name>']))
    else:
        print(arguments)