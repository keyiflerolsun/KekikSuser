# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikSuser import konsol

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os, json

SESSION  = 'sessionlar/'
if not os.path.isdir(SESSION):
    os.mkdir(SESSION)

def sessioncu():
    "Gelen İnput ile session oluşturur."
    api_id    = konsol.input('[yellow]API ID        : [/]')
    api_hash  = konsol.input('[yellow]API HASH      : [/]')
    telefon   = konsol.input('[yellow]Telefon(+xxxx): [/]').replace(' ', '')

    try:
        client = TelegramClient(f"{SESSION}{telefon}", api_id, api_hash)
        client.connect()
    except Exception as hata:
        os.remove(f'{SESSION}{telefon}.session')
        print(f'[cyan]Hata Var !\n\t`{type(hata).__name__}`\n\t{hata}')
        exit()

    if not client.is_user_authorized():
        client.send_code_request(telefon)
        try:
            client.sign_in(telefon, konsol.input('[yellow]\nDoğrulama Kodu: '))
        except SessionPasswordNeededError:
            client.sign_in(password=konsol.input('[yellow]\nİki Aşamalı Doğrulama Şifresi: '))
        except Exception as hata:
            os.remove(f'{SESSION}{telefon}.session')
            konsol.print(f'[cyan]Hata Var !\n\t`{type(hata).__name__}`\n\t{hata}')
            exit()
        finally:
            client.disconnect()

    bilgilerim = {}
    async def ana():
        # Şuan bütün client methodlarını kullanabilirsiniz örneğin;
        ben = await client.get_me()

        bilgilerim['nick'] = f"@{ben.username}"
        bilgilerim['ad']   = f"{ben.first_name} {ben.last_name}"
        bilgilerim['uid']  = ben.id
        await client.send_message('me', f'__Merhaba, Ben **KekikSuser** Tarafından Gönderildim!__\n\n__Senin Bilgilerin;__\n\n**ID :** `{api_id}`\n**Hash :** `{api_hash}`\n**Telefon :** `{telefon}`\n\n**Kendi gizliliğin için bunları kimseyle paylaşma..**')

    with client:
        client.loop.run_until_complete(ana())

    dict2json({
            'api_id'        : api_id,
            'api_hash'      : api_hash,
            'telefon'       : telefon,
            'kullanici_id'  : bilgilerim['uid'],
            'kullanici_nick': bilgilerim['nick'],
            'kullanici_adi' : bilgilerim['ad']

        }, dosya_adi=f'{SESSION}bilgiler.json')

    konsol.print(f'\n\n\t\t[red]{telefon} Session Kayıt Edildi..!')



def dict2json(sozluk:dict, dosya_adi:str):
    if os.path.isfile(dosya_adi):
        with open(dosya_adi, encoding='utf-8') as gelen_json:
            gelen_veri = json.load(gelen_json)

        gelen_veri.append(sozluk)

        with open(dosya_adi, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(gelen_veri, indent=2, ensure_ascii=False, sort_keys=False))

    else:
        with open(dosya_adi, mode='w', encoding='utf-8') as f:
            liste = [sozluk]
            essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in liste}]
            a_z   = sorted(essiz, key=lambda sozluk: sozluk['api_id'])
            f.write(json.dumps(a_z, indent=2, ensure_ascii=False, sort_keys=False))