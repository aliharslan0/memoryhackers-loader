import json
import os
import pathlib
import socket
import subprocess
import time
import zipfile
from datetime import datetime

import requests
import websocket


def parse_dotenv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return {line.split('=')[0]: line.split('=')[1].strip() for line in lines if line and not line.startswith('#')}


config = parse_dotenv('.env')


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
    return input('mData: ').replace('\n', '').strip()


def update_loader():
    url = requests.get('https://raw.githubusercontent.com/sbyteui-bot/ldr/main/data/link.txt').text
    zip_path = url.split('/')[-1]
    if zip_path == config['ZIP_PATH']:
        return False

    with open(zip_path, 'wb') as file:
        content = requests.get(url).content
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

    process_found = False
    for i in range(9):
        out = subprocess.check_output(['TASKLIST', '/FI', 'imagename eq gtnszz.exe'])
        if b'gtnszz.exe' in out:
            process_found = True
            break
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

    for i in range(9):
        try:
            ws = websocket.create_connection('ws://localhost:9002', timeout=1)
            break
        except (ConnectionError, socket.timeout):
            time.sleep(1)

    ws.recv()
    payload = {
        'method': 'load',
        'json': {
            'token': config['MDATA'],
            'q': config['B64'],
            'id': config['ID']
        }
    }
    payload['json'] = json.dumps(payload['json'])
    payload = json.dumps(payload)

    ws.send(payload)

    if update_mdata:
        set_key('.env', 'MDATA', config['MDATA'], quote_mode='never')
        set_key('.env', 'LAST_RUN', config['LAST_RUN'], quote_mode='never')


if __name__ == '__main__':
    main()
