from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class URLLoader:
    def create_module(self, spec):
        return None

    def exec_module(self, module):
        try:
            with urlopen(module.__spec__.origin, timeout=5) as page:
                source = page.read()
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise ImportError(
                f"Cannot download module: {module.__spec__.origin}"
            ) from exc

        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)
