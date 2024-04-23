from mcstatus import JavaServer
from logging import getLogger

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.host = config.get('host')
    self.port = config.get('port')
    
  def run(self):
    try:
      server = JavaServer.lookup(f'{self.host}:{self.port}')
      status = server.status()
      players = status.players.online
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
    self.db.write(self.name, data)
