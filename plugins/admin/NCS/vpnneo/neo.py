
import sourcedefender
import aiohttp
import socket
import requests
import sys
import Crypto


def cek_key(NeoKey):
    url = 'https://www.vpnneo.com/XApi/check-apikey'
    myobj = {'apikey': NeoKey}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return "ApiKey Valid"
    else:
        return "ApiKey Tidak Valid"

def cek_saldo(NeoKey):
    url = 'https://www.vpnneo.com/XApi/cek-saldo'
    myobj = {'apikey': NeoKey}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"`Saldo Tuan : {json['saldo']}`")
    else:
        return (f"`ApiKey Tidak Valid`")

def list_server(NeoKey, tipe):
    url = 'https://www.vpnneo.com/XApi/list-server'
    myobj = {'apikey': NeoKey, 'type': tipe}
    x = requests.post(url, json = myobj)
    json = x.json()

    server_list = []
    for server in x.json():
        server_list.append((server['nama'], server['harga_jual']))
    server_list = [f"**{server[0]}**  —  Rp.{server[1]:,.0f}" for server in server_list]
    server_list = "\n".join(server_list)
    return (f"**Daftar Server {tipe.upper()}**\n━━━━━━━━━━\n{server_list}")

def buat_ssh(NeoKey, serv, user, passw, durasi):
    url = 'https://www.vpnneo.com/XApi/beli-ssh'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'password': passw, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def buat_vmess(NeoKey, serv, user, durasi):
    url = 'https://www.vpnneo.com/XApi/beli-vmess'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def buat_trojan(NeoKey, serv, user, durasi):
    url = 'https://www.vpnneo.com/XApi/beli-trojan'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'durasi': durasi}  
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def daftar_script(NeoKey, sc, ip, durasi):
    url = 'https://www.vpnneo.com/XApi/beli-script'
    myobj = {'apikey': NeoKey, 'script': sc, 'ip': ip, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def renew_ssh(NeoKey, serv, user, durasi):
    url = 'https://www.vpnneo.com/XApi/renew-ssh'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def renew_vmess(NeoKey, serv, user, durasi):
    url = 'https://www.vpnneo.com/XApi/renew-vmess'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def renew_trojan(NeoKey, serv, user, durasi):
    url = 'https://www.vpnneo.com/XApi/renew-trojan'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def renew_script(NeoKey, sc, ip, durasi):
    url = 'https://www.vpnneo.com/XApi/renew-script'
    myobj = {'apikey': NeoKey, 'script': sc, 'ip': ip, 'durasi': durasi}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])
    
def pindah_ssh(NeoKey, serv, user, servbaru):
    url = 'https://www.vpnneo.com/XApi/change-server-ssh'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'domaintujuan': servbaru}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def pindah_vmess(NeoKey, serv, user, servbaru):
    url = 'https://www.vpnneo.com/XApi/change-server-vmess'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'domaintujuan': servbaru}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def pindah_trojan(NeoKey, serv, user, servbaru):
    url = 'https://www.vpnneo.com/XApi/change-server-trojan'
    myobj = {'apikey': NeoKey, 'domain': serv, 'username': user, 'domaintujuan': servbaru}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])


def topup(NeoKey, nominal):
    url = 'https://www.vpnneo.com/XApi/topup-saldo'
    myobj = {'apikey': NeoKey, 'nominal': nominal}
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        return (f"**{json['message']}**\n━━━━━━━━━━\n{json['detail']}")
    else:
        return (json['message'])

def cek_server(NeoKey, serv):
    url = 'https://www.vpnneo.com/XApi/cek-server'
    myobj = {'apikey': NeoKey, 'domain': serv}  
    x = requests.post(url, json = myobj)
    json = x.json()
    if json['status'] == 'success':
        pesan = f"**{json['message']}**\n━━━━━━━━━━\n"
        for key, value in json['data'].items():
            pesan += f"**{key} : {value}**\n"
        pesan += "━━━━━━━━━━\n"
        pesan += f"**Slot Tersisa : {json['slot']}**\n"
        return (pesan)
    else:
        return (json['message'])

def myQRIS(NeoKey):
    url = 'https://www.vpnneo.com/XApi/paymentku'
    myobj = {'apikey': NeoKey}  
    x = requests.post(url, json = myobj)
    json = x.json()
    pesan = f"**\n━━━━━━━━━━\n{json['message']}**\n"
    qris = json['qris']
    return {'qris': qris, 'pesan': pesan}

def ipinfo(ips):
    try :
        ip = socket.gethostbyname(ips)
    except socket.gaierror:
        return "`IP atau Domain Tidak Valid!`"
    url = (
        f"https://ipinfo.io/{ip}?token=3451483e9e9e87"
    )
    values = requests.get(url).json()
    if "status" in values:
        return "`IP atau Domain Tidak Valid!`"
    pesan = f"**Berikut Detail Dari `{ips}`**\n━━━━━━━━━━\n"
    for key, value in values.items():
        pesan += f"**{key}** : `{value}`\n"
    return pesan


