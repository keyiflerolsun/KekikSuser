from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import ChannelPrivateError
import os, json

SESSION  = 'sessionlar/'
GRUP     = 'gruplar/'
if not os.path.isdir(GRUP):
    os.mkdir(GRUP)

def ayiklayici():
    "sessionlar/bilgiler.json 'dan Elimizdeki UserBotları Tutuyoruz."
    with open(f'{SESSION}bilgiler.json', 'r', encoding='utf-8') as dosya:
	    sessionlar = json.loads(dosya.read())

    clientler = []
    for session in sessionlar:
        client = TelegramClient(f'{SESSION}{session["telefon"]}', session["api_id"], session["api_hash"])
        client.connect()
        if not client.is_user_authorized():
            print(f'\n\t[!] - {session["kullanici_nick"]} Giriş Başarısız! Önce Session Oluşturmalısınız..')
            continue

        clientler.append({
            "session" : session,
            "client"  : client,
        })
    
    print(f'\n\t[~] - {len(clientler)} Adet - Client\'in var..\n\n')

    gezilen_gruplar = []
    for client in clientler:
        print(f"\t[!] - {client['session']['kullanici_adi']} - [!]")
        sohbetler = []
        sonuc     = client['client'](GetDialogsRequest(
                    offset_date    = None,
                    offset_id      = 0,
                    offset_peer    = InputPeerEmpty(),
                    limit          = 200,
                    hash           = 0
                )
        )
        sohbetler.extend(sonuc.chats)

        dahil_olunan_gruplar = []
        for sohbet in sohbetler:
            try:
                if sohbet.megagroup == True:
                    dahil_olunan_gruplar.append({
                        'baslik': str(sohbet.title),
                        'id'    : str(sohbet.id),
                        'hash'  : str(sohbet.access_hash)
                    })

                    suserler = client['client'].get_participants(sohbet, aggressive=True)

                    liste = [{
                        # 'grup': sohbet.title,
                        'id': suser.id,
                        # 'hash': suser.access_hash,
                        'nick': f'@{suser.username}' if suser.username else None,
                        'ad': suser.first_name or None,
                        'soyad': suser.last_name or None,
                        # 'tel': f'+{suser.phone}' if suser.phone else None,
                        # 'dil': suser.lang_code or None
                    } for suser in suserler if (suser.username) and (not suser.bot) and (not suser.scam) and (not suser.deleted)]

                    essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in liste}] # Listedeki Eş Verileri Sil
                    a_z   = sorted(essiz, key=lambda sozluk: sozluk['id'])                                 # İD'Ye göre sırala
                    veri  = json.dumps(a_z, ensure_ascii=False, sort_keys=False, indent=2)                 # Json'a Çevir

                    with open(f"{GRUP}{sohbet.id} - {client['session']['telefon']}.json", "w+", encoding='utf-8') as dosya:
                        dosya.write(veri)

                    print(f'[+] - {len(liste)} Adet Suser Ayıklandı » {sohbet.title}')
                    gezilen_gruplar.append(sohbet.id)
            except (AttributeError, ChannelPrivateError):
                continue

        with open(f"{GRUP}{client['session']['telefon']}.json", 'w', encoding='utf-8') as dosya:
            json.dump(dahil_olunan_gruplar, dosya, indent=4, ensure_ascii=False)
    
    birlestir() # Bütün iş Bitince Dızlanan Suser'leri KekikSuser.json a çevir..


def birlestir():
    birlesik_kisiler = []
    for grup_json in os.listdir('gruplar'):
        if not grup_json.startswith('+'):
            with open(f'{GRUP}{grup_json}', 'r', encoding='utf-8') as bakalim:
                birlesik_kisiler.extend(json.load(bakalim))

    essiz = [dict(sozluk) for sozluk in {tuple(liste_ici.items()) for liste_ici in birlesik_kisiler}]
    a_z   = sorted(essiz, key=lambda sozluk: sozluk['id'])
    veri  = json.dumps(a_z, ensure_ascii=False, sort_keys=False, indent=2)

    with open('KekikSuser.json', 'w', encoding='utf-8') as ksuser:
        ksuser.write(veri)

    print(f'\nToplamda {len(essiz)} Adet Benzersiz Suser Ayıklandı ve Kaydedildi..')