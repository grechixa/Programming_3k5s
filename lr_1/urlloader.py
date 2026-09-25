from urllib.request import urlopen


class URLLoader:
    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()

        code = compile(
            source,
            module.__spec__.origin,
            mode="exec"
        )

        exec(code, module.__dict__)