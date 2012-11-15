import sys
import os

def Main():
    if(len(sys.argv) > 2):
        for filepath in sys.argv[1:-1]:
            #print "Line: " + line
            name, ext = os.path.splitext(filepath)
            dirpath = os.path.dirname(filepath)
            os.rename(filepath, os.path.join(dirpath, name + sys.argv[-1]))
    else:
        print "usage:\n$: rext file [file1...filen] extension"
Main()