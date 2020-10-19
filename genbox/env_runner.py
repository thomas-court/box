import logging, os, fnmatch, subprocess
from genbox.script_generator import ScriptGenerator
from genbox.exception import BoxError
from genbox.env_lister import EnvLister
from genbox.config_helper import ConfigHelper
from genbox.base import BoxGenerator

class EnvRunner:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.script_generator = ScriptGenerator()
    self.env_lister = EnvLister()
    self.config_helper = ConfigHelper()
    self.box_generator = BoxGenerator()

  def run(self, env_name, share, command_args):
    self.logger.debug('Running env {}'.format(env_name))
    config = self.get_env_config(env_name) 
    if (not self.env_lister.is_env_ready(config)):
      raise BoxError('environnement {} is not ready for use'.format(config['name']))
    self.generate_run_script(config)
    self.run_command_in_env(config, share, command_args)

  def generate_run_script(self, config):
    self.logger.debug('Run script generation in progress')
    try:
      self.script_generator.generate_run_script(config)
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('unable to generate run script')

  def run_command_in_env(self, config, share, command_args):
    self.logger.debug('Run command in env {} command: {} command ARGS: {} '.format(config['name'], config['run'].split('\n')[0], command_args))
    env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
    user = config['user']
    cwd=self.get_cwd()
    if (share):
      paths = share.split(':')
      path_in_host = paths[0]
      path_in_env = '{}{}'.format(env_location, paths[1])
      if (not path_in_host.startswith('/')):
        path_in_host = '{}{}'.format(cwd, path_in_host)
      sh_command = 'touch {} && chmod 777 {} && mount --bind {} {}'.format(path_in_env, path_in_env, path_in_host, path_in_env)
      rc=subprocess.call(sh_command, shell=True)
      if (rc != 0):
        raise BoxError('unable to share directory: path_in_host {} path_in_env {}'.format(path_in_host, path_in_env))
    call_arguments = ['/usr/sbin/chroot', '--userspec', '{}:{}'.format(user,user), env_location, '/tmp/run.sh']
    call_arguments = call_arguments+command_args 
    rc = subprocess.call(call_arguments)
    if (rc != 0):
      raise BoxError('unable to chroot to {}'.format(env_location))

  def get_env_config(self, env_name):	
    config_files = fnmatch.filter(os.listdir('.'), '*.yml')
    for config_file in config_files:
      config = self.config_helper.parse_config(config_file)
      if (config['name'] == env_name):
        return config

  def get_cwd(self):
    cwd=os.path.dirname(os.path.realpath(__file__))
    i=cwd.find('venv')
    cwd=cwd[:i]
    return cwd


