import sys
import os
from math import log10

def Main():
    if(len(sys.argv) > 1):
        for filepath in sys.argv[1:]:
            with open(filepath) as f:
                line_count = sum(1 for line in f)
                f.seek(0)
                zs = int(log10(line_count))
                for index, line in enumerate(f):
                    print str(index + 1).zfill(zs), ''.join([c for c in line.decode('utf-8').encode('unicode-escape')])
    else:
        print "usage:\n$: pcat file [file1...filen]"
Main()