from json import dumps
from os import startfile
from pathlib import Path
from subprocess import check_output
from time import sleep
from zipfile import ZipFile

from dotenv import dotenv_values, set_key
from requests import get
from websocket import create_connection

config = dotenv_values('.env')


def update_loader():
    url = get(config['UPDATE_URL']).text
    zip_path = url.split('/')[-1]
    if zip_path == config['ZIP_PATH']:
        return False

    with open(zip_path, 'wb') as file:
        for chunk in get(url, stream=True).iter_content():
            file.write(chunk)

    old = Path(config['ZIP_PATH'])
    if old.is_file():
        old.unlink(False)

    set_key('.env', 'ZIP_PATH', zip_path, quote_mode='never')
    config['ZIP_PATH'] = zip_path
    return True


def main():
    update_loader()

    with ZipFile(config['ZIP_PATH']) as zf:
        zf.extractall(pwd=b'mh')
        startfile(zf.filelist[0].filename)

    timeout = int(config['TIMEOUT'])
    while timeout > 0:
        out = check_output(['TASKLIST', '/FI', f'imagename eq {config["PROCESS_NAME"]}'])
        if out.splitlines()[-1].startswith(config["PROCESS_NAME"].encode()):
            break
        timeout -= 1
        sleep(1)
    else:
        raise ProcessLookupError('Process not found.')

    ws = create_connection('ws://localhost:9002')
    ws.recv()
    data = {
        'method': 'load',
        'json': {
            'token': config['MDATA'],
            'q': config['B64'],
            'id': config['ID']
        }
    }
    data['json'] = dumps(data['json'])
    json_str = dumps(data)
    ws.send(json_str)


if __name__ == '__main__':
    main()
