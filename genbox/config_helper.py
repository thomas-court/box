import logging, yaml
from genbox.exception import BoxError

class ConfigHelper:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)

  def parse_config(self, configuration_file):
    self.logger.debug('Parsing configuration file %s', configuration_file)
    try:
      with open(configuration_file, 'r') as stream: 
        config = yaml.safe_load(stream)
        return config
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('ERROR: unable to parse configuration file {}'.format(configuration_file))
