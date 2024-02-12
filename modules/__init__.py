
"""This package loads all built-in and custom modules

After importing, run `load_modules()` to populate the MODULES dict with `'name': Module` entries.
"""


import os
import importlib
from logging import getLogger


MODULES = {}


def load_modules():
  """Loads all modules from the `modules/` folder, then from `custom/`.
  
  Custom modules will override built-in modules with the same name
  """
  
  logger = getLogger(__name__)

  mod_dir = os.path.dirname(__file__)
  custom_dir = os.path.join(mod_dir, 'custom')

  for path,package in (
    (mod_dir, __package__),
    (custom_dir, f'{__package__}.custom')
  ):
    if not os.path.isdir(path):
      continue
    for file in os.listdir(path):
      if (
        not os.path.isfile(os.path.join(path, file)) or
        file.startswith('__') or
        not file.endswith('.py')
      ):
        continue
      
      name = file.removesuffix('.py')
      mod = importlib.import_module(f'.{name}', package)

      if not hasattr(mod, 'Module'):
        logger.warn(f'Module {package}.{name} is missing "run" method. Skipping')
        continue
      logger.info(f'Loaded module {package}.{name}')

      MODULES[name] = mod.Module
