import os
import importlib

package_dir = os.path.dirname(__file__)

for module_name in os.listdir(package_dir):

    if module_name == "__init__.py" or not module_name.endswith(".py"):
        continue
    module_name = module_name[:-3]

    importlib.import_module(f".{module_name}", package=__name__)
