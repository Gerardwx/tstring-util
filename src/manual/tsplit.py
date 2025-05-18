import subprocess
from tstring import safe_split
injection = '/tmp;rm -fr /'
command = t'ls -l {injection}'
clist = safe_split(command)
subprocess.run(clist)
# ls: cannot access '/tmp;rm -fr /': No such file or directory
