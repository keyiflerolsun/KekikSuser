from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, UserChannelsTooMuchError, ChannelInvalidError, UsernameNotOccupiedError, FloodWaitError
import os, json, time, random

SESSION  = 'sessionlar/'
GRUP     = 'gruplar/'

def id_ile_grup_ver(gruplar, grup_id):
    for grup in gruplar:
        if grup_id == int(grup['id']):
            return grup

    return None

def ekleyici():
    with open(f'{SESSION}bilgiler.json', 'r', encoding='utf-8') as f:
	    config = json.loads(f.read())

    clientler = []
    for hesap in config:
        api_id   = hesap['api_id']
        api_hash = hesap['api_hash']
        telefon  = hesap['telefon']
        client = TelegramClient(f'{SESSION}{telefon}', api_id, api_hash)
        client.connect()

        if client.is_user_authorized():
            clientler.append({'telefon': telefon, 'client': client})
        else:
            print(f'{telefon} giriş yapamadı...')

    sohbetler    = []
    son_tarih    = None
    parca_boyutu = 200
    gruplar      = []

    sonuc = clientler[-1]['client'](GetDialogsRequest(
                 offset_date    = son_tarih,
                 offset_id      = 0,
                 offset_peer    = InputPeerEmpty(),
                 limit          = parca_boyutu,
                 hash           = 0
             ))
    sohbetler.extend(sonuc.chats)

    for sohbet in sohbetler:
        try:
            if sohbet.megagroup== True:
                gruplar.append(sohbet)
        except AttributeError:
            continue

    print('\n\tHangi Gruba SUSER Eklemek İstiyorsunuz?\n')
    say = 0
    grup_idleri = []
    for grup in gruplar:
        print(f'{say} - {grup.title}')
        grup_idleri.append(grup.id)
        say += 1

    grup_index     = input("\nLütfen Numara Seçin!: ")
    eklenecek_grup = grup_idleri[int(grup_index)]

    filtrelenmis_client = []
    for sec_client in clientler:
        telefon   = sec_client['telefon']
        grup_yolu = f'{GRUP}{telefon}.json'

        if os.path.isfile(grup_yolu):
            with open(grup_yolu, 'r', encoding='utf-8') as f:
                gruplar = json.loads(f.read())

            # Eğer UserBot Gruba Dahilse
            hedeflenen_grup    = id_ile_grup_ver(gruplar, eklenecek_grup)
            if hedeflenen_grup:
                grup_hash      = int(hedeflenen_grup['hash'])
                grubun_kendisi = InputPeerChannel(eklenecek_grup, grup_hash)

                grup_suser_yolu = f'{GRUP}{eklenecek_grup} - {telefon}.json'
                if os.path.isfile(grup_suser_yolu):
                    sec_client['eklenecek_grup'] = grubun_kendisi

                    with open(grup_suser_yolu, encoding='utf-8') as f:
                        sec_client['users'] = json.loads(f.read())

                    filtrelenmis_client.append(sec_client)
                else:
                    print(f'{telefon} kaynak grupta değil..')
                    return
            else:
                print(f'{telefon} hedef grupta değil..')
                return
        else:
            print(f'{telefon} Lütfen Session Oluşturun..')
            return
    
    # print(filtrelenmis_client)

    # diz_turu   = int(input("\n\n1 - KullanıcıAdıyla\n2 - ID ile\nSeçim Yapın: "))

    suser_nickleri = []
    with open('KekikSuser.json', "r+", encoding='utf-8') as json_dosyasi:
        json_suserler = json.loads(json_dosyasi.read())
        try:
            for nick in json_suserler:
                suser_nickleri.append(nick['nick'])
        except TypeError:
            suser_nickleri.extend(json_suserler)

    var_olan_kisiler = []
    v_suserler = clientler[0]['client'].get_participants(eklenecek_grup, aggressive=True)
    for suser in v_suserler:
        if (suser.username) and (not suser.bot) and (not suser.scam) and (not suser.deleted):
            var_olan_kisiler.append(f'@{suser.username}')

    client_sayisi    = lambda : len(filtrelenmis_client)
    print(f'\n\t[!] - {client_sayisi()} Adet - Client\'in var..')
    # kullanici_sayisi = len(filtrelenmis_client[0]['users'])

    client_index = 0
    eklenen_suser_sayisi = 0
    for suser in suser_nickleri:
        rastgele = random.randrange(len(suser_nickleri))
        bilgi    = suser_nickleri[rastgele]
        if client_sayisi() == 0:
            print(f'\n\n\tClient Kalmadı!!\n\n\t| Toplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu.."')
            with open('KekikSuser.json', "w+", encoding='utf-8') as cli_bitti:
                cli_bitti.write(json.dumps(suser_nickleri, ensure_ascii=False, sort_keys=False, indent=2))
            return

        if client_index == client_sayisi():
            client_index = 0

        if (not bilgi) or (bilgi in var_olan_kisiler):
            suser_nickleri.remove(bilgi)
            continue

        uyku = lambda : time.sleep(random.randrange(1, 3))  # Burası eklemeler arası bekleme süresi saniye cinsinden
        gecerli_client = filtrelenmis_client[client_index]
        try:
            eklenecek_suser = gecerli_client['client'].get_input_entity(bilgi)

            print(f"\n\n[~] {gecerli_client['telefon']} | {bilgi}\'i Eklemeyi Deniyorum..")
            gecerli_client['client'](InviteToChannelRequest(gecerli_client['eklenecek_grup'], [eklenecek_suser]))
            eklenen_suser_sayisi += 1
            print(f"[+] {bilgi}\'i Ekledim\t| Toplam Eklenen : {eklenen_suser_sayisi} Kişi Oldu..")

            client_index += 1
            uyku()
            continue
        except PeerFloodError as flood:
            print(f'[!] Takıldı | Flood Yemişsin Kanka.. » ({flood}) | {gecerli_client["telefon"]} Düşürdüm..')
            filtrelenmis_client.remove(gecerli_client)
            gecerli_client['client'].disconnect()
            client_index = 0
            print(f'\n\t[!] - {client_sayisi()} Adet - Client\'in Kaldı..!!')
            uyku()
            continue
        except UserPrivacyRestrictedError:
            print('[!] Takıldı | Malesef Gizlilik Ayarları Kanka..')
            suser_nickleri.remove(bilgi)
            client_index += 1
            uyku()
            continue
        except UserNotMutualContactError:
            print('[!] Kullanıcı Karşılıksız İletişim Hatası..')
            suser_nickleri.remove(bilgi)
            client_index += 1
            uyku()
            continue
        except UserChannelsTooMuchError:
            print('[!] Takıldı | Kullanıcı Çok Fazla Yere Üye..')
            suser_nickleri.remove(bilgi)
            client_index += 1
            uyku()
            continue
        except ChannelInvalidError:
            print('[!] Takıldı | ChannelInvalidError')
            suser_nickleri.remove(bilgi)
            client_index += 1
            uyku()
            continue
        except UsernameNotOccupiedError:
            print('[!] Takıldı | UsernameNotOccupiedError')
            suser_nickleri.remove(bilgi)
            client_index += 1
            uyku()
            continue
        except FloodWaitError as fw:
            print(f"\t[!] Takıldı | ({fw}) | {bilgi}")
            fw_suresi = int(str(fw).split()[3])
            if fw_suresi > 1000:
                filtrelenmis_client.remove(gecerli_client)
                gecerli_client['client'].disconnect()
                client_index = 0
                print(f'\n\t[!] - {client_sayisi()} Adet - Client\'in Kaldı..!!')
            continue
        except Exception as hata:
            print(f"\t[!] Takıldı | ({type(hata).__name__}) | {hata}")
            continue

# def ekleyici():
#     if os.path.isfile(os.path.join(os.getcwd(), 'bilgiler.json')) == False:
#         api_id    = input('API ID: ')
#         api_hash  = input('API HASH: ')
#         telefon   = input('Telefon(+95xxxx): ')

#         with open('bilgiler.json', 'w+') as bilgiler:
#             bilgiler.write(json.dumps({
#                 'id'    : api_id,
#                 'hash'  : api_hash,
#                 'tel'   : telefon
#             }, indent=2, ensure_ascii=False, sort_keys=False))
#     else:
#         config = json.load(open('bilgiler.json'))
#         api_id    = config['id']
#         api_hash  = config['hash']
#         telefon   = config['tel']

#     client    = TelegramClient(telefon, api_id, api_hash)
#     client.connect()

#     if not client.is_user_authorized():
#         client.send_code_request(telefon)
#         client.sign_in(telefon, input('Doğrulama Kodu: '))
#         client.disconnect()

#     async def ana():
#         # Şuan bütün client methodlarını kullanabilirsiniz örneğin;
#         await client.send_message('me', '__Merhaba, Ben **Ayıklayıcı** Tarafından Gönderildim!__')

#     with client:
#         client.loop.run_until_complete(ana())

#     client.connect()

#     sohbetler    = []
#     son_tarih    = None
#     parca_boyutu = 200
#     gruplar      = []

#     sonuc = client(GetDialogsRequest(
#                  offset_date    = son_tarih,
#                  offset_id      = 0,
#                  offset_peer    = InputPeerEmpty(),
#                  limit          = parca_boyutu,
#                  hash           = 0
#              ))
#     sohbetler.extend(sonuc.chats)

#     for sohbet in sohbetler:
#         try:
#             if sohbet.megagroup== True:
#                 gruplar.append(sohbet)
#         except AttributeError:
#             continue

#     print('\n\tHangi Gruba SUSER Eklemek İstiyorsunuz?\n')
#     say = 0
#     for grup in gruplar:
#         print(str(say) + ' - ' + grup.title)
#         say += 1

#     grup_index = input("\nLütfen Numara Seçin!: ")
#     eklenecek_grup = gruplar[int(grup_index)]
#     hedef      = InputPeerChannel(eklenecek_grup.id, eklenecek_grup.access_hash)

#     print('\n\n\tHangi JSON\'u Kullanmak İstiyorsunuz?')
#     say      = 0
#     dosyalar = []
#     for dosya in os.listdir('.'):
#         if (dosya.endswith('.json')) and not dosya.startswith('bilgiler'):
#             print(str(say) + ' - ' + dosya)
#             dosyalar.append(dosya)
#             say += 1
    
#     dosya_index = input("\nLütfen Numara Seçin!: ")
#     hedef_json  = dosyalar[int(dosya_index)]

#     diz_turu   = int(input("\n\n1 - KullanıcıAdıyla\n2 - ID ile\nSeçim Yapın: "))

#     with open(hedef_json, "r+", encoding='utf-8') as json_dosyasi:
#         suserler = json.loads(json_dosyasi.read())

#     for suser in suserler:
#         if diz_turu == 1:
#             if not suser['nick']:
#                 continue
#             eklenecek_suser = client.get_input_entity(suser['nick'])
#             bilgi           = suser['nick']
#         if diz_turu == 2:
#             eklenecek_suser = InputPeerUser(suser['id'], suser['hash'])
#             bilgi           = suser['id']
        
#         print(f"\n\n[~] {bilgi}\'i Eklemeyi Deniyorum..")
#         try:
#             client(InviteToChannelRequest(hedef, [eklenecek_suser]))
#             print(f"[+] {bilgi}\'i Ekledim")
#         except PeerFloodError:
#             accik = random.randrange(60, 90)
#             print(f'[!] Flood Yemişsin Kanka.. {accik}sn Bekleyelim')
#             time.sleep(accik)
#         except UserPrivacyRestrictedError:
#             print('[!] Malesef Gizlilik Ayarları Kanka..')
#             time.sleep(random.randrange(5, 10))
#         except UserNotMutualContactError:
#             print('[!] Kullanıcı Karşılıksız İletişim Hatası..')
#             time.sleep(random.randrange(5, 10))
#         except UserChannelsTooMuchError:
#             print('[!] Kullanıcı Çok Fazla Yere Üye..')
#             time.sleep(random.randrange(5, 10))
