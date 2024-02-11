from mcrcon import MCRcon
from logging import getLogger

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.host = config.get('host')
    self.port = config.get('port')
    self.password = config.get('password')

  def run(self):
    try:
      with MCRcon(host=self.host, password=self.password, port=self.port) as mcr:
        resp = mcr.command('showplayers')
      players = len(resp.splitlines())-1
    except Exception as e:
      self.logger.error(f'{self.name} - {e}')
      return

    data = {
      'measurement': self.name,
      'fields': {
        'players': players,
      }
    }
    self.logger.debug(data)
    self.db.write(data)
