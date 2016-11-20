#!/usr/bin/env python

import sys
import os
import termios

## function to do `cd` using `xd` add this to your .bashrc
## then use `xd usdpf' instead of `cd /usr/share/doc/python/faq/'
# xd()
# {
#     cd `/home/hans/bin/xd.py "$@"`
# }

class DontBlock:
    def __init__(self):
        self.error = False
        self.old_settings = termios.tcgetattr(0)
        if not self.old_settings:
            self.error = True
            return
        new_settings = termios.tcgetattr(0)
        new_settings[3] &= ~(termios.ECHO | termios.ICANON)
        new_settings[6][termios.VMIN] = 1
        new_settings[6][termios.VTIME] = 0

        if termios.tcsetattr(0, termios.TCSAFLUSH, new_settings):
            termios.tcsetattr(0, termios.TCSANOW, old_settings)
            self.error = True
            return

    def __del__(self):
        self.set_blocking()

    def set_blocking(self):
        if not self.old_settings:
            return
        if termios.tcsetattr(0, termios.TCSAFLUSH, self.old_settings):
            termios.tcsetattr(0, termios.TCSANOW, self.old_settings)
            self.old_settings = None

def choose(paths):
    db = DontBlock()
    if db.error:
        sys.stderr.write('Could not get non-blocking IO\n')

    indices = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(len(paths)):
        sys.stderr.write('{0:s}: {1:s}\n'.format(indices[i], paths[i]))

    try:
        x = 'spiny norman'
        while x not in indices[:len(paths)]:
            x = sys.stdin.read(1)
    except Exception as e:
        sys.stderr.write('Error {0:s}\n'.format(sys.exc_info()[1]))
    finally:
        db.set_blocking()

    return paths[indices.find(x)]

def find_paths(abbr):
    paths = ['/']
    for l in abbr:
        paths = find_paths2(l, paths)
        if not paths:
            break
    return paths

def find_paths2(l, paths):
    newpaths = []
    for p in paths:
        newpaths += [os.path.join(p, f) \
                     for f in os.listdir(p) \
                     if os.path.isdir(os.path.join(p, f)) \
                        and f[0] == l]
    return newpaths

def main(argv):
    if len(argv) == 1:
        return

    abbr = argv[1]
    paths = find_paths(abbr)
    paths.sort()
    if len(paths) == 1:
        sys.stdout.write('{0:s}\n'.format(paths[0]))
        return
    if len(paths) < 63:
        sys.stdout.write('{0:s}\n'.format(choose(paths)))
        return
    sys.stderr.write('ERROR: too many options.\n')


if __name__ == '__main__':
    main(sys.argv)
