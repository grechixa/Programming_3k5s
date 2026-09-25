import sys

sys.path.append("http://localhost:8000")

import myremotemodule
myremotemodule.myfoo()

import remotepackage
remotepackage.package_info()

from remotepackage import tools
tools.hello()
