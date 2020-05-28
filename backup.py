import subprocess
import re
import sys
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

def backup_container_to_image(container_ids, timestamps):
    for i, container_id in enumerate(container_ids):
        new_container_name = container_names[i] + '_' + timestamps

        print('> committing container id:', container_id)
        execute_shell(['docker', 'commit', '-p', container_id, new_container_name])
        print('> container id: %s has been committed to image: %s' % (container_id, new_container_name))

def backup_image_to_tar(container_ids, timestamps):
    for i, container_id in enumerate(container_ids):
        new_image = container_names[i] + '_' + timestamps
        tar_file = new_image + '.tar'

        print('> saving image repository:', new_image)
        execute_shell(['docker', 'save', '-o', tar_file, new_image])
        print('> image repository: %s has been saved to tar file: %s' % (new_image, tar_file))

def remove_container(container_ids):
    for i, container_id in enumerate(container_ids):
        print('> stopping current container id:', container_id)
        execute_shell(['docker', 'container', 'stop', container_id])
        print('> container id: %s has been stopped' % container_id)
        execute_shell(['docker', 'container', 'rm', container_id])
        print('> container id: %s has been removed' % container_id)

timestamps = format_datetime(datetime.now())
ps_output = execute_shell(['docker', 'ps', '--format', '{{.ID}}|{{.Image}}|{{.Ports}}'])

if (len(ps_output) == 0):
    print('> no container(s) to backup.')
    sys.exit()

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

backup_container_to_image(container_ids, timestamps)
backup_image_to_tar(container_ids, timestamps)
remove_container(container_ids)
