import requests


class URLLoader:
    def create_module(self, spec):
        return None

    def exec_module(self, module):
        try:
            response = requests.get(module.__spec__.origin, timeout=5)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ImportError(
                f"Cannot download module: {module.__spec__.origin}"
            ) from exc

        code = compile(response.content, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)
