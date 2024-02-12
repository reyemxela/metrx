from logging import getLogger

"""This is the minimal framework for a module.

- The class name is always 'Module'
- __init__ receives the following arguments when loaded:
  - name: the friendly name of the service
  - config: a dict of the `config` section of config.yaml for that service
  - db: a reference to the InfluxDB helper with the `write` method
- There also needs to be a `run` function, it gets called at the scheduled interval
"""

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.cfg1 = config.get('cfg1')
    self.cfg2 = config.get('cfg2')

  def run(self):
    # get data

    data = {
      'measurement': self.name,
      'tags': {}, # optional
      'fields': {},
    }
    self.logger.debug(data)
    self.db.write(data)
