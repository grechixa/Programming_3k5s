import re
import sys
import requests

from url_finder_requests import URLFinder


def _get_listing(url):
    try:
        response = requests.get(url.rstrip("/") + "/", timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise ImportError(f"Remote host is unavailable: {url}") from exc


def url_hook(some_str):
    if not some_str.startswith(("http://", "https://")):
        raise ImportError

    data = _get_listing(some_str)

    files = re.findall(r'href=["\']([^"\']+\.py)["\']', data)
    modules = {
        name[:-3]
        for name in files
        if "/" not in name.rstrip("/")
        and name != "__init__.py"
    }

    dirs = re.findall(r'href=["\']([^"\']+)/["\']', data)
    packages = {name for name in dirs if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name)}

    return URLFinder(some_str.rstrip("/"), modules, packages)


if url_hook not in sys.path_hooks:
    sys.path_hooks.append(url_hook)
