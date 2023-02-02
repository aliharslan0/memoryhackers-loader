import json
import os
import pathlib
import re
import socket
import subprocess
import time
import urllib.request
import zipfile
from datetime import datetime


def parse_dotenv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return {line.split('=')[0]: line.split('=')[1].strip() for line in lines if line and not line.startswith('#')}


config = parse_dotenv('.env')
pattern = re.compile(r"^[a-zA-Z0-9_]+\.[a-zA-Z0-9-]+\.([a-zA-Z0-9-]+\.)*[a-zA-Z0-9_]+$")


def set_key(file_path, key, value, quote_mode='never'):
    quote = '' if quote_mode == 'never' else "'"
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        found = False
        for line in lines:
            if line.startswith(f"{key}="):
                f.write(f"{key}={quote}{value}{quote}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"{key}={quote}{value}{quote}\n")


def get_m_data():
    input_string = input('mData: ')
    if re.match(pattern, input_string):
        return input_string
    else:
        return None


def update_loader():
    url = urllib.request.urlopen('https://raw.githubusercontent.com/sbyteui-bot/ldr/main/data/link.txt').read().decode()
    zip_path = url.split('/')[-1]
    if zip_path == config['ZIP_PATH']:
        return False

    with open(zip_path, 'wb') as file:
        content = urllib.request.urlopen(url).read()
        file.write(content)

    old_path = pathlib.Path(config['ZIP_PATH'])
    if old_path.is_file():
        old_path.unlink()

    set_key('.env', 'ZIP_PATH', zip_path, quote_mode='never')
    config['ZIP_PATH'] = zip_path
    return True


def main():
    update_loader()

    with zipfile.ZipFile(config['ZIP_PATH']) as zf:
        zf.extractall(pwd=b'mh')
        os.startfile(zf.filelist[0].filename)

    timeout = 10
    process_found = False
    while timeout > 0:
        out = subprocess.check_output(['TASKLIST', '/FI', 'imagename eq gtnszz.exe'])
        if b'gtnszz.exe' in out:
            process_found = True
            break
        timeout -= 1
        time.sleep(1)

    if not process_found:
        raise ProcessLookupError('Process not found.')

    current_time = datetime.now()
    last_run = datetime.fromisoformat(config['LAST_RUN']) if config['LAST_RUN'] else current_time
    update_mdata = False
    if len(config['MDATA']) != 428 or (current_time - last_run).total_seconds() > 3600:
        config['MDATA'] = get_m_data()
        config['LAST_RUN'] = current_time.isoformat()
        update_mdata = True

    for i in range(10):
        try:
            ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ws.settimeout(1)
            ws.connect(("localhost", 9002))
            break
        except (ConnectionRefusedError, socket.timeout) as e:
            if i == 9:
                raise e

    ws.recv(1024)
    payload = {
        'method': 'load',
        'json': {
            'token': config['MDATA'],
            'q': config['B64'],
            'id': config['ID']
        }
    }

    payload['json'] = json.dumps(payload['json'])
    json_str = json.dumps(payload)

    ws.send(json_str.encode("utf-8"))

    ws.close()

    if update_mdata:
        set_key('.env', 'MDATA', config['MDATA'], quote_mode='never')
        set_key('.env', 'LAST_RUN', config['LAST_RUN'], quote_mode='never')


if __name__ == '__main__':
    main()
