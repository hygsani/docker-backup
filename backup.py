import subprocess
import re
from datetime import datetime

def format_datetime(now):
    return now.strftime('%y%m%d-%H%M%S')

def create_file(curr_timestamps):
    open('containers_' + curr_timestamps, 'w')

def write_file(curr_timestamps, content):
    f = open('containers_' + curr_timestamps, 'w')
    f.write(content)
    f.close()

def get_file_content(file):
    content = []

    with open(file, 'r') as reader:
        for line in reader.readlines():
            row = re.sub('\n', '', line)
            content.append(row)

    return content

def split_content(content, delimiter='|'):
    return content.split(delimiter)

def execute_shell(cmd):
    return subprocess.check_output(cmd, universal_newlines=True)

def backup_container_to_image(container_ids):
    for i, container_id in enumerate(container_ids):
        new_container_name = container_names[i] + '_' + timestamps

        print('> committing container id:', container_id)
        execute_shell(['docker', 'commit', '-p', container_id, new_container_name])
        print('> container id: %s have been committing to image: %s' % (container_id, new_container_name))

ps_output = execute_shell(['docker', 'ps', '--format', '{{.ID}}|{{.Image}}|{{.Ports}}'])
timestamps = format_datetime(datetime.now())

create_file(timestamps)
write_file(timestamps, ps_output)

containers = get_file_content('containers_' + timestamps)

container_ids = []
container_names = []
container_ports = []

for row in containers:
    container_ids.append(split_content(row)[0])
    container_names.append(split_content(row)[1].split('_')[0])
    container_ports.append(split_content(row)[2])

backup_container_to_image(container_ids)
