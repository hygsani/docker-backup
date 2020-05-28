import subprocess

def create_file(curr_timestamps):
    open('containers_200528', 'w')

def write_file(curr_timestamps):
    f = open('containers_200528', 'w')
    f.write('hello world')
    f.close()

def execute_shell(cmd):
    return subprocess.check_output(cmd, universal_newlines=True)

ps = execute_shell(['docker', 'ps', '--format', '{{.ID}}|{{.Image}}|{{.Ports}}'])
create_file()
write_file()