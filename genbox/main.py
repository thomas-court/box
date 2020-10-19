import sys,logging,logging.config
from genbox.command_interpretor import CommandInterpretor

def main():
  try:
   logging.config.fileConfig('logging.conf')
   print("OK")
  except Exception as exc:
    print(exc)

  command_interpretor = CommandInterpretor()
  command_interpretor.interpret(sys.argv)

if __name__ == "__main__":
  main()
