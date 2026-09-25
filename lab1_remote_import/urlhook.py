import re
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from url_finder import URLFinder


def _get_listing(url):
    try:
        with urlopen(url, timeout=5) as page:
            return page.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise ImportError(f"Remote host is unavailable: {url}") from exc


def url_hook(some_str):
    if not some_str.startswith(("http://", "https://")):
        raise ImportError

    data = _get_listing(some_str.rstrip("/") + "/")

    # Files such as myremotemodule.py are modules.
    files = re.findall(r'href=["\']([^"\']+\.py)["\']', data)
    modules = {
        name[:-3]
        for name in files
        if "/" not in name.rstrip("/")
        and name != "__init__.py"
    }

    # Directory links such as remotepackage/ are packages.
    dirs = re.findall(r'href=["\']([^"\']+)/["\']', data)
    packages = {name for name in dirs if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name)}

    return URLFinder(some_str.rstrip("/"), modules, packages)


if url_hook not in sys.path_hooks:
    sys.path_hooks.append(url_hook)
