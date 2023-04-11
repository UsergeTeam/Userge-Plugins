""" Neo Commands """

import sourcedefender
import aiohttp
import socket
import requests
import sys
from pyrogram import enums
from userge import userge, Message
from ...builtin import system
import include
sys.path.append('/usr/lib/python3.9')
import vpnneo.neo as neo


@userge.on_cmd(
    "set-key", about={
    'header': "Set ApiKey",
    'usage': "{tr}setkey [apikey]",
    'examples': ["{tr}setkey xxxxxxx"]}, allow_channels=False)
async def _setkey(message: Message):
    """ Set ApiKey """
    await message.edit("`Proses Tuan...`")
    var_name = "NEOKEY"
    var_value = message.input_str
    if not var_value:
        await message.err("`Masukkan ApiKey`")
        return
    await system.set_env(var_name, var_value)
    await message.edit(f"ApiKey baru telah berhasil disimpan")


@userge.on_cmd(
    "cek-key", about={
    'header': "Cek ApiKey",
    'usage': "{tr}cekkey",
    'examples': ["{tr}cekkey"]}, allow_channels=False)
async def _cekkey(message: Message):
    """ Cek ApiKey """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    turu = neo.cek_key(NeoKey)
    await message.edit(f"`{turu}`")

@userge.on_cmd(
    "cek-saldo", about={
    'header': "Cek Saldo",
    'usage': "{tr}ceksaldo",
    'examples': ["{tr}ceksaldo"]}, allow_channels=False)
async def _ceksaldo(message: Message):
    """ Cek Saldo """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    turu = neo.cek_saldo(NeoKey)
    await message.edit(f"`{turu}`")

@userge.on_cmd(
    "server-ssh", about={
    'header': "List Server SSH",
    'usage': "{tr}server-ssh",
    'examples': ["{tr}server-ssh"]}, allow_channels=False)
async def _server_ssh(message: Message):
    """ List Server SSH """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    tipe = 'ssh'
    turu = neo.list_server(NeoKey, tipe)
    await message.edit(f"{turu}")
    
@userge.on_cmd(
    "server-vmess", about={
    'header': "List Server Vmess",
    'usage': "{tr}server-vmess",
    'examples': ["{tr}server-vmess"]}, allow_channels=False)
async def _server_vmess(message: Message):
    """ List Server Vmess """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    tipe = 'vmess'
    turu = neo.list_server(NeoKey, tipe)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "server-trojan", about={
    'header': "List Server Trojan",
    'usage': "{tr}server-trojan",
    'examples': ["{tr}server-trojan"]}, allow_channels=False)
async def _server_trojan(message: Message):
    """ List Server Trojan """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    tipe = 'trojan_ws'
    turu = neo.list_server(NeoKey, tipe)
    await message.edit(f"{turu}")
        
@userge.on_cmd(
    "buat-ssh", about={
    'header': "Buat Akun SSH",
    'usage': "{tr}buat-ssh [server] [username] [password] [durasi]",
    'examples': ["{tr}buat-ssh contabo mendingturu 1"]}, allow_channels=False)
async def _buat_ssh(message: Message):
    """ Pembuatan Akun SSH """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # if message.input_str less than 4 args
    if len(message.input_str.split()) < 4:
        await message.err("`Masukkan semua argumen`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    passw = message.input_str.split()[2]
    durasi = message.input_str.split()[3]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if passw is None:
        await message.err("`Masukkan Password`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.buat_ssh(NeoKey, serv, user, passw, durasi)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "buat-vmess", about={
    'header': "Buat Akun Vmess",
    'usage': "{tr}buat-vmess [server] [username] [password] [durasi]",
    'examples': ["{tr}buat-vmess hurricane3 mending turu 1"]}, allow_channels=False)
async def _buat_vmess(message: Message):
    """ Pembuatan Akun Vmess """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Durasi`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    durasi = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.buat_vmess(NeoKey, serv, user, durasi)
    await message.edit(f"{turu}")


@userge.on_cmd(
    "buat-trojan", about={
    'header': "Buat Akun Trojan",
    'usage': "{tr}buat-trojan [server] [username] [durasi]",
    'examples': ["{tr}buat-trojan hurricane3 mendingturu 1"]}, allow_channels=False)
async def _buat_trojan(message: Message):
    """ Pembuatan Akun Trojan """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Durasi`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    durasi = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.buat_trojan(NeoKey, serv, user, durasi)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "renew-ssh", about={
    'header': "Perpanjang Akun SSH",
    'usage': "{tr}renew-ssh [server] [username] [durasi]",
    'examples': ["{tr}renew-ssh melbi2 mendingturu 1"]}, allow_channels=False)
async def _renew_ssh(message: Message):
    """ Perpanjang Akun SSH """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Durasi`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    durasi = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.renew_ssh(NeoKey, serv, user, durasi)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "renew-vmess", about={
    'header': "Perpanjang Akun Vmess",
    'usage': "{tr}renew-vmess [server] [username] [durasi]",
    'examples': ["{tr}renew-vmess hurricane3 mendingturu 1"]}, allow_channels=False)
async def _renew_vmess(message: Message):
    """ Perpanjang Akun Vmess """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Durasi`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    durasi = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.renew_vmess(NeoKey, serv, user, durasi)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "renew-trojan", about={
    'header': "Perpanjang Akun Trojan-WS",
    'usage': "{tr}renew-trojan [server] [username] [durasi]",
    'examples': ["{tr}renew-trojan biznet12 mendingturu 1"]}, allow_channels=False)
async def _renew_trojan(message: Message):
    """ Perpanjang Akun Trojan """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Durasi`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    durasi = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if durasi is None:
        await message.err("`Masukkan Durasi`")
        return
    if not durasi.isnumeric():
        await message.err("`Durasi harus angka`")
        return
    if int(durasi) > 12:
        await message.err("`Durasi maksimal 12 bulan`")
        return
    if int(durasi) < 1:
        await message.err("`Durasi minimal 1 bulan`")
        return
    turu = neo.renew_trojan(NeoKey, serv, user, durasi)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "pindah-ssh", about={
    'header': "Pindah Server SSH",
    'usage': "{tr}pindah-ssh [server] [username] [serverbaru]",
    'examples': ["{tr}pindah-ssh hurricane3 mendingturu hurricane2"]}, allow_channels=False)
async def _pindah_ssh(message: Message):
    """ Pindah Server SSH """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Server Baru`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    servbaru = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if servbaru is None:
        await message.err("`Masukkan Server Baru`")
        return
    turu = neo.pindah_ssh(NeoKey, serv, user, servbaru)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "pindah-vmess", about={
    'header': "Pindah Server Vmess",
    'usage': "{tr}pindah-vmess [server] [username] [serverbaru]",
    'examples': ["{tr}pindah-vmess biznet12 mendingturu biznet13"]}, allow_channels=False)
async def _pindah_vmess(message: Message):
    """ Pindah Server Vmess """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Server Baru`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    servbaru = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if servbaru is None:
        await message.err("`Masukkan Server Baru`")
        return
    turu = neo.pindah_vmess(NeoKey, serv, user, servbaru)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "pindah-trojan", about={
    'header': "Pindah Server Trojan",
    'usage': "{tr}pindah-trojan [server] [username] [serverbaru]",
    'examples': ["{tr}pindah-trojan biznet12 mendingturu biznet13"]}, allow_channels=False)
async def _pindah_trojan(message: Message):
    """ Pindah Server Trojan """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 3:
        await message.err("`Masukkan Server, Username, Server Baru`")
        return
    serv = message.input_str.split()[0]
    user = message.input_str.split()[1]
    servbaru = message.input_str.split()[2]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    if user is None:
        await message.err("`Masukkan Username`")
        return
    if servbaru is None:
        await message.err("`Masukkan Server Baru`")
        return
    turu = neo.pindah_trojan(NeoKey, serv, user, servbaru)
    await message.edit(f"{turu}")

@userge.on_cmd(
    "topup", about={
    'header': "Topup Saldo",
    'usage': "{tr}topup [nominal]",
    'examples': ["{tr}topup 50000"]}, allow_channels=False)
async def _topup(message: Message):
    """ TopUp Saldo """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 1:
        await message.err("`Masukkan Nominal`")
        return
    nominal = message.input_str.split()[0]
    if nominal is None:
        await message.err("`Masukkan Nominal`")
        return
    if not nominal.isnumeric():
        await message.err("`Nominal harus angka`")
        return
    if int(nominal) < 50000:
        await message.err("`Nominal minimal 50000`")
        return
    turu = neo.topup(NeoKey, nominal)
    await message.edit(f"{turu}")


@userge.on_cmd(
    "cek-server", about={
    'header': "Cek Server",
    'usage': "{tr}cek-server [server]",
    'examples': ["{tr}cek-server hurricane3"]}, allow_channels=False)
async def _cek_server(message: Message):
    """ Cek Status Server """
    await message.edit("`Proses Tuan...`")
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    # serv = message.input_str butuh di split
    if len(message.input_str.split()) < 1:
        await message.err("`Masukkan Server`")
        return
    serv = message.input_str.split()[0]
    if serv is None:
        await message.err("`Masukkan Domain Server`")
        return
    turu = neo.cek_server(NeoKey, serv)
    await message.edit(f"{turu}")


@userge.on_cmd(
    "pay", about={
    'header': "Kirim QRIS",
    'usage': "{tr}myQRIS",
    'examples': ["{tr}myQRIS"]}, allow_channels=False)
async def _myQRIS(message: Message):
    """ Kirim QRIS """
    NeoKey = system.get_env("NEOKEY")
    if NeoKey is None:
        await message.err("`ApiKey belum diset`")
        return
    turu = neo.myQRIS(NeoKey)
    qris = turu['qris']
    pesan = turu['pesan']
    await message.client.send_photo(message.chat.id, qris, caption=pesan)


@userge.on_cmd(
    "ipinfo", about={
        'header': "A IPLookUp Plugin",
        'description': "Put IP Address to get some details about that.",
        'usage': "{tr}iplook [IP Address]"})
async def _ip_look_up(message: Message):
    await message.edit("`Checking IP Address ...`")
    if not message.input_str:
        await message.edit("`No IP Address Found!`")
        return
    pesan = neo.ipinfo(message.input_str)
    await message.edit(
        text=pesan,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
