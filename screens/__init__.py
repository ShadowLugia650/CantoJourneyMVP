from os import path
from glob import glob

# __all__ = [path.basename(f)[:-3] for f in glob(path.join(path.dirname(__file__), "*.py")) if path.isfile(f) and not f.endswith('__init__.py')]
# __all__ = []
# screens = resources.AssetStorage()
for f in glob(path.join(path.dirname(__file__), "*.py")):
    if path.isfile(f) and not f.endswith('__init__.py'):
        # __all__.append(path.basename(f)[:-3])
        # screens.register(**{path.basename(f)[:-3]: __import__("screens." + path.basename(f)[:-3])})
        __import__("screens." + path.basename(f)[:-3])
