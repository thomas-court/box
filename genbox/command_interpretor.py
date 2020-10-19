import logging
from genbox.env_builder import EnvBuilder
from genbox.env_lister import EnvLister
from genbox.env_runner import EnvRunner


class CommandInterpretor: 
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)

  def interpret(self, args):
    self.logger.debug("interpretCommand %s", str(args))
    if (len(args)<3):
      print("ERROR SYNTAX")
      self.usage()
    else:
      command = args[1]
      command_args_and_options=args[1:]
      rc = self.check_command(command)
      if (rc != 0):
         print("COMMAND INVALID %s"  %(command))
         self.usage()
      else:
        self.interpret_command(command, command_args_and_options)


  def usage(self):
    print("Usage")
    print("\tbox command command_arguments\n")
    print("\tAvailable commands:")
    print("\t\tbuild configuration_file")
    print("\t\tenv list")
    print("\t\trun [OPTIONS] command [command_args]")
  
  def check_command(self, command):
    available_commands = ['build', 'env', 'run']
    found = 0
    for element in available_commands:
      if (element == command):
        found = 1
        break
    if not found:
      return -1
    else:
      return 0
 
  def interpret_command(self, command, command_arg_and_options):
    command = command_arg_and_options[0]
    if (command == 'build'):
      config_file = command_arg_and_options[1]
      env_builder = EnvBuilder()
      try:
        env_name = env_builder.build(config_file)
        print("Environement %s is ready for use" % (env_name))
      except Exception as exc:
        self.logger.exception(exc)
        print("build command ERROR: %s" %(str(exc)))
    elif (command == 'env'):
      command_arg = command_arg_and_options[1]
      if (command_arg == 'list'):
        env_lister = EnvLister()
        try: 
          env_lister.list()
        except Exception as exc:
          self.logger.exception(exc)
          print("list command ERROR: {}".format(str(exc)))
      else:
        print('Invalid Command Argument {}'.format(command_arg))
        self.usage()
        return -1
    else:
      run_args_and_options = command_arg_and_options[1:]
      option_name = None
      option_value = None
      if ((len(run_args_and_options)>=3) and  (run_args_and_options[0].startswith('--'))):
        option_name = run_args_and_options[0][2:]
        option_value = run_args_and_options[1]
        command = run_args_and_options[2]
        command_args = run_args_and_options[3:]
      else:
        command = run_args_and_options[0]
        command_args = run_args_and_options[1:]
      env_runner = EnvRunner()
      try:
        env_runner.run(command, option_value, command_args)
      except Exception as exc:
        self.logger.exception(exc)
