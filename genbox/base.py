import logging, os, tarfile
from genbox.exception import BoxError

class BoxGenerator:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.archive_name = 'rootfs.tar.xz'
    self.box_directory = '/var/lib/box'
    self.base_directory = '/var/lib/box/base'
    self.env_directory = '/var/lib/box/env'

  def generate(self):
    self.create_box_directory()
    self.create_base_directory()
    self.create_env_directory()    
    self.create_box_rootfs()

  def create_box_directory(self):
    self.logger.debug('Create directory %s', self.box_directory)
    try:
      os.makedirs(self.box_directory)
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('ERROR: unable to create {} directory'.format(self.box_directory))

  def create_base_directory(self):
    self.logger.debug('Create directory %s', self.base_directory)
    try:
      os.makedirs(self.base_directory)
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('ERROR: unable to create {} directory'.format(self.base_directory))

  def create_env_directory(self):
    self.logger.debug('Create directory %s', self.env_directory)
    try:
      os.makedirs(self.env_directory)
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('ERROR: unable to create {} directory'.format(self.env_directory))

  def create_box_rootfs(self):
    self.logger.debug('Decompress archive %s in %s directory'.format(self.archive_name, self.base_directory))
    try:
      with tarfile.open(self.archive_name) as f:
        f.extractall(self.base_directory)
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('ERROR: unable to decompress archive %s in directory %s'.format(self.archive_name, self.base_directory))



