from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
from urlloader import URLLoader


class URLFinder(PathEntryFinder):
    def __init__(self, url, available_modules, available_packages):
        self.url = url.rstrip("/")
        self.available_modules = available_modules
        self.available_packages = available_packages

    def find_spec(self, name, target=None):
        if name in self.available_packages:
            origin = f"{self.url}/{name}/__init__.py"
            loader = URLLoader()
            return spec_from_loader(
                name,
                loader,
                origin=origin,
                is_package=True,
            )

        if name in self.available_modules:
            origin = f"{self.url}/{name}.py"
            loader = URLLoader()
            return spec_from_loader(
                name,
                loader,
                origin=origin,
                is_package=False,
            )

        return None
