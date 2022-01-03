import re
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    return ('command not found' in command.output.lower()
            and ' ' in command.script)


@sudo_support
def get_new_command(command):
    return re.sub(' ', ' ', command.script)
