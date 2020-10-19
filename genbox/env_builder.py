import logging, subprocess
from os import path
from genbox.base import BoxGenerator
from genbox.config_helper import ConfigHelper
from genbox.script_generator import ScriptGenerator
from genbox.exception import BoxError
from genbox.env_lister import EnvLister

class EnvBuilder:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.box_generator = BoxGenerator()
    self.config_helper = ConfigHelper()
    self.script_generator = ScriptGenerator()
    self.env_lister = EnvLister()

  def build(self, configuration_file):
    self.logger.info('Environnement build in progress')
    config = self.config_helper.parse_config(configuration_file)
    if (config == None):
      print("ERROR: Config file %s not found or invalid" % (config_file))
    else:
      self.configure(config)
    self.logger.info("Environnement build completed")
    return config['name']

  def configure(self, config):
    self.logger.debug('Environnement %s configuration in progress', config['name'])
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    if (self.env_lister.is_env_ready(config)):
      self.logger.debug('Environnement %s already configured', config['name'])
    else:
      self.create_env_rootfs(config)
      self.script_generator.generate_config_script(config) 
      self.config_mounts(config) 
      self.create_user(config)
      self.run_config_script(config)

  def run_config_script(self, config):
    self.logger.debug('Environnement {} configuration in progress')    
    script_path = '/tmp/configure.sh'
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    rc=subprocess.call(['/usr/sbin/chroot', env_location, script_path])
    if (rc != 0):
      raise BoxError('unable to chroot to environnement {} with script {}'.format(config['name'], script_path))

  def create_env_rootfs(self, config):
    self.logger.debug('Environnement %s rootfs creation in progress', config['name'])
    if  (not path.exists(self.box_generator.env_directory)):
      self.box_generator.generate()
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    print(env_location)
    if (not path.exists(env_location)):
      rc=subprocess.call(['cp', '-r', self.box_generator.base_directory, env_location])
      if  (rc != 0):
        raise BoxError('unable to copy rootfs')
    self.logger.debug('Environnement %s rootfs creation complete', config['name'])

  def config_mounts(self, config):
    self.logger.debug('Environnement {} proc sys dev mount progress'.format(config['name']))
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    rc=subprocess.call(['mount', '-o', 'bind', '/dev', env_location+'/dev'])
    if (rc != 0):
      raise BoxError('unable to mount /dev')
    rc=subprocess.call(['mount', '-t', 'proc', '/proc', env_location+'/proc'])
    if (rc != 0):
      raise BoxError('unable to mount /proc')
    rc=subprocess.call(['mount', '-t', 'sysfs', '/sys', env_location+'/sys'])
    if (rc != 0):
      raise BoxError('unable to mount /sys')

    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    tmp_directory = '{}{}'.format(env_location, '/tmp')
    print('A')
    print(tmp_directory)
    rc=subprocess.call(['chmod', '1777', tmp_directory])

  def create_user(self, config):
    self.logger.debug('User creation in progress')
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    user = config['user']
    sh_command = 'touch {} {} && /usr/sbin/useradd -R {} {}'.format(env_location,'/etc/{shadow, passwd}', env_location, user)
    print(sh_command)
    rc=subprocess.call(sh_command, shell = True)
    if (rc != 0):
      raise BoxError('unable to create user')
         
