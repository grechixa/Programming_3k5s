import sys

import urlhook


print("Custom URL import mechanism is active.")
print("Current sys.path:")
for path in sys.path:
    print("  ", path)