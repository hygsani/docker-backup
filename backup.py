import subprocess
from datetime import datetime

def format_datetime(now):
    return now.strftime('%y%m%d_%H%M%S')

def create_file(curr_timestamps):
    open('containers_' + curr_timestamps, 'w')

def write_file(curr_timestamps, content):
    f = open('containers_' + curr_timestamps, 'w')
    f.write(content)
    f.close()

def execute_shell(cmd):
    return subprocess.check_output(cmd, universal_newlines=True)

ps = execute_shell(['docker', 'ps', '--format', '{{.ID}}|{{.Image}}|{{.Ports}}'])

timestamps = format_datetime(datetime.now())

create_file(timestamps)
write_file(timestamps, ps)