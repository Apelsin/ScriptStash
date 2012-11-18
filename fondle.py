import sys
import shutil
import optparse
import os
import time

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def reverse_enum(L):
   for index in reversed(xrange(len(L))):
      yield index, L[index]

def flipped_enum(L):
    l = len(L)
    for index in reversed(xrange(l)):
        yield l - index - 1, L[index]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def Main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--descending', dest="descending", action="store_true", help="Sort in descending order")
    parser.add_option('-p', '--prefix', dest="prefix", default=None, help="Rename files followed by index number")
    options, remainder = parser.parse_args()
    files = remainder # TO-DO: seek file paths right to left until non file name or beginning of list, use subset to the right
    files.sort(key=lambda x: x)
    count = len(files)
    
    temp_folder_path = None
    temp_folder_created = False
    if(options.prefix):
        temp_folder_path = os.path.join(os.path.dirname(sys.argv[0]), "___temp")
        temp_folder_created = ensure_dir(temp_folder_path)
    
    moveback = []
    
    for index, filepath in flipped_enum(files) if options.descending else enumerate(files):
        #touch(filepath, (int(time.time()) - count + index,) * 2)
        #print "touch -t %i %s" % (index , filepath)
        if options.prefix is not None:
            name, ext = os.path.splitext(filepath)
            dirpath = os.path.dirname(filepath)
            new_name = options.prefix + "_%i%s" % (index + 1, ext)
            new_path = os.path.join(temp_folder_path, new_name)
            #print "   moving %s to %s" % (filepath, new_path)
            shutil.move(filepath, os.path.join(temp_folder_path, new_name))
            moveback.append({'current': new_path, 'destination': dirpath})
    if options.prefix is not None:
        for pathchange in moveback:
            #print "returning %s to %s" % (pathchange['current'], pathchange['destination'])
            shutil.move(pathchange['current'], pathchange['destination'])
        if temp_folder_created:
            os.rmdir(temp_folder_path)
        
            
Main()