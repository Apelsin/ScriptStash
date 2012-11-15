import sys
import os
import stat

dirpath = os.path.dirname(sys.argv[0])
f = open( os.path.join(dirpath, '..', sys.argv[1]), 'w')
f.write("""\
DIR=$(cd "$(dirname "$0")"; pwd)
python $DIR/ScriptStash/%s.py "${@:1}"\
""" % sys.argv[1])

mode = os.stat(f.name).st_mode
os.chmod(f.name, mode | stat.S_IEXEC)