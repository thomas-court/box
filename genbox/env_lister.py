import logging, os,fnmatch, subprocess
from genbox.base import BoxGenerator
from genbox.config_helper import ConfigHelper

class EnvLister:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.box_generator = BoxGenerator()
    self.config_helper = ConfigHelper()

  def list(self):
    if (not os.path.exists(self.box_generator.base_directory)): 
      self.box_generator.generate()
    print('{} | {} | {} | {} | {}'.format('Name', 'Location', 'Env build command', 'Ready', 'Run command'))
    config_files = fnmatch.filter(os.listdir('.'), '*.yml')
    for config_file in config_files:
      config = self.config_helper.parse_config(config_file)
      env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
      env_ready = self.is_env_ready(config)
      env_build_command = 'box build {}'.format(config_file)
      env_run_command = 'box run {}'.format(config['name'])
      print('{} | {} | {} | {} | {}'.format(config['name'], env_location, env_build_command, str(env_ready), env_run_command))

  def is_env_ready(self, config):
    self.logger.debug('Check if environnement {} is already configured'.format(config['name']))
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    env_proc_mount = '{}/proc'.format(env_location)
    cp = subprocess.run(['cat', '/proc/mounts'], universal_newlines = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output_lines = cp.stdout.split('\n')
    found = False
    for element in output_lines:
      if (env_proc_mount in element):
        found = True
        break
    return found
       
