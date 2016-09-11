import getpass
from pwd import getpwnam

username = getpass.getuser()
print getpwnam(username)[2]

