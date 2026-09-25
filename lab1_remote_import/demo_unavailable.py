import sys
import urlhook

sys.path.append("http://localhost:65500")

try:
    import myremotemodule
except ImportError as exc:
    print("Handled remote import error:")
    print(exc)
