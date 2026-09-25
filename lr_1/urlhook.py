import re
import sys
from urllib.request import urlopen

from url_finder import URLFinder


def url_hook(path):
    if not path.startswith(("http://", "https://")):
        raise ImportError

    try:
        with urlopen(path, timeout=5) as page:
            data = page.read().decode("utf-8")

    except Exception as error:
        raise ImportError(
            f"Cannot access remote repository: {path}"
        ) from error

    filenames = re.findall(
        r"[a-zA-Z_][a-zA-Z0-9_]*\.py",
        data
    )

    modnames = {
        filename[:-3]
        for filename in filenames
    }

    return URLFinder(path.rstrip("/"), modnames)


sys.path_hooks.append(url_hook)

print("URL import hook activated.")