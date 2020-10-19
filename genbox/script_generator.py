import logging, subprocess
from genbox.base import BoxGenerator
from genbox.exception import BoxError

class ScriptGenerator:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.box_generator = BoxGenerator()

  def generate_config_script(self, config):
    self.logger.debug("Configuration script generation in progress")
    try: 
      repositories = config['repositories']
      requirements = config['requirements']
      script = "\
#!/bin/bash \n\
apt update && apt upgrade -y \n\
apt install -y dirmngr gnupg apt-transport-https software-properties-common ca-certificates curl \n\
"
      for element in repositories:
        key = element['key']
        repository = element['repository']
        script = '{}curl -fsSL {} | apt-key add - \n'.format(script, key)
        script = '{}add-apt-repository \'{}\'\n'.format(script, repository)
      script = '{}apt update\n'.format(script)
      for requirement in requirements:
        script = '{}apt install -y {}'.format(script, requirement)
      env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
      script_path = '{}{}'.format(env_location, '/tmp/configure.sh')
      f = open(script_path, "w")
      f.write(script)
      f.close()
      rc = subprocess.call(['chmod', '+x', script_path])
      if (rc != 0):
        raise BoxError('unable to chmod +x configuration script')
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError("unable to generate configuration script")

  def generate_run_script(self, config):
    self.logger.debug("Run script generation in progress")
    try:
      run = config['run']
      script = ""
      line = "#!/bin/bash"
      script = '{}{}\n'.format(script, line)
      line = 'ARGS="$@"'
      script = '{}{}\n'.format(script, line)
      line = "for ARG in $ARGS"
      script = '{}{}\n'.format(script, line)
      line = "  do"
      script = '{}{}\n'.format(script, line)
      line = "    if [[ \"$ARG\" == \"-c\" ]]; then"
      script = '{}{}\n'.format(script, line)
      line = "      COMMAND=1"
      script = '{}{}\n'.format(script, line)
      line = "      ARGS=( \"${ARGS[@]/$ARG}\" )"
      script = '{}{}\n'.format(script, line)
      line = "    fi"
      script = '{}{}\n'.format(script, line)
      line = "  done"
      script = '{}{}\n'.format(script, line)
      line = "if [[ $COMMAND -eq 1 ]]; then"
      script = '{}{}\n'.format(script, line)
      line = "  eval $ARGS"
      script = '{}{}\n'.format(script, line)
      line = "else"
      script = '{}{}\n'.format(script, line)
      run = config['run'].split('\n')[0].strip()
      line = ' {}'.format(run)
      script = '{}{}\n'.format(script, line)
      line = "fi"
      script = '{}{}\n'.format(script, line)
      env_location = '{}/{}'.format(self.box_generator.env_directory, config['name'])
      script_path = '{}{}'.format(env_location, '/tmp/run.sh')
      f = open(script_path, "w")
      f.write(script)
      f.close()
      rc = subprocess.call(['chmod', '+x', script_path])
      if (rc != 0):
        raise BoxError('unable to chmod +x run script')
    except Exception as exc:
      self.logger.exception(exc)
      raise BoxError('unable to generate run script')
