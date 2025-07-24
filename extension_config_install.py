import zipfile
import json
import os

import uuid
import base64

def generate_machine_id():
    # mac address da maquina
    mac_int = uuid.getnode()
    mac_address = ':'.join(("%012X" % mac_int)[i:i+2] for i in range(0, 12, 2))

    machine_id = (os.uname()[::])
    machine_id += (mac_address,)

    machine_id_encoded_bytes = str(machine_id).encode('utf-8')
    machine_id_base64_encoded = base64.b64encode(machine_id_encoded_bytes)

    # machine_id_decoded_bytes = base64.b64decode(machine_id_base64_encoded)
    # decoded_string = machine_id_decoded_bytes.decode('utf-8')

    return machine_id_base64_encoded.decode('utf-8')


employee = input('Informe o nome do funcionário: ')
registration = input('Informe a matrícula (opcional): ')
server_address = input('Endereço do servidor: ')

server_address = server_address if server_address != '' else "http://127.0.0.1:5000/"

config = {}
config["server_address"] = server_address
config["employee"] = employee
config["registration"] = registration

config["machine_id"] = generate_machine_id()

# source_directory = cwd = os.path.join(os.getcwd(), 'client-module')
destination_directory = "/home/lucas/Documents/GAISECO"

with zipfile.ZipFile('client-module.zip', 'r') as zipf:
    zipf.extractall(destination_directory)


with open(file=os.path.join(destination_directory, 'gaiseco-chrome-extension', 'config.json'), 
          mode='w') as f:
    json.dump(config, f, indent=2)


# try:
#     shutil.copytree(source_directory, destination_directory)
#     print(f"A pasta: '{source_directory}' e seu conteúdo foram copaidos com sucesso para '{destination_directory}'.")
# except FileExistsError:
#     print(f"A pasta de destino: '{destination_directory}' já existe, informe outro caminho.")
# except Exception as e:
#     print(f"Erro: {e}")
