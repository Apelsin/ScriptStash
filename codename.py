import sys
import os
from re import match, sub

def Main():
    if(len(sys.argv) > 1):
        for filepath in sys.argv[1:]:
            with open(filepath) as f:
                next(f)
                for line in f:
                    if(match(".*\w.*", line)):
                        #print "Line: " + line
                        name, ext = os.path.splitext(filepath)
                        dirpath = os.path.dirname(filepath)
                        name_new = sub("[^\w\s]", "", line).strip() + ext
                        os.rename(filepath, os.path.join(dirpath, name_new))
                        break;
    else:
        print "usage:\n$: codename file [file1...filen]"
Main()