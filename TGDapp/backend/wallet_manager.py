import requests
import datetime
import hmac
import hashlib
import base64
import json  # 确保导入 json 模块
from mnemonic import Mnemonic
from pycoin.symbols.btc import network

def create_wallet():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(128)
    seed = mnemo.to_seed(mnemonic, passphrase="")
    wallet = network.keys.bip32_seed(seed)
    addr = wallet.subkey_for_path("44'/0'/0'/0/0").address()
    return {"mnemonic": mnemonic, "address": addr}

def import_wallet(wallet_details):

    return {"status": "success", "message": "Wallet imported successfully"}

def generate_signature(secret_key, timestamp, method, request_path, body):
    message = timestamp + method + request_path + body
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def create_wallet_account(api_key, secret_key, passphrase, project_id, addresses):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    request_path = '/api/v5/wallet/account/create-account'
    body = json.dumps({"addresses": addresses})
    method = 'POST'
    signature = generate_signature(secret_key, timestamp, method, request_path, body)
    headers = {
        'Content-Type': 'application/json',
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'OK-ACCESS-PROJECT': project_id
    }
    response = requests.post('https://www.okx.com' + request_path, headers=headers, data=body)
    if response.status_code == 200:
        data = response.json()
        wallet_info = create_wallet()
        data.update(wallet_info)
        return {"status": "success", "data": data}
    else:
        return {"status": "error", "message": response.text}

# 示例调用
addresses = [
    {
        "chainIndex": "1",
        "address": "0x561815e02bac6128bbbbc551005ddfd92a5c24db",
        "publicKey": "02012db63bf0380294a6ecf87615fe869384b0510cb910a094254b6844af023ee2",
        "signature": "62acda5e471d9bf0099add50f4845256868d980821c161095651a918d3ef8a6b2286f512028172eabbe46ec2c9c2c20e5c40ff1fb23e1cdfdbed033ad924ce521b"
    }
]

api_key = 'c911eee9-a43c-4deb-956f-480a6bd77e32'
secret_key = '727CA0D42745E5DCA562400CA6B93FFB'
passphrase = '14F!Main@Network'
project_id = 'a9839711fcb8faa15245001df4db7424'

create_wallet_account(api_key, secret_key, passphrase, project_id, addresses)