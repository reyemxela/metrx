from logging import getLogger

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
      'fields': {
      }
    }
    self.logger.debug(data)
    self.db.write(data)
