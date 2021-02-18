# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikSuser import taban, konsol, sessioncu, ayiklayici, ekleyici

import os
from time import sleep


def acilis_sayfasi():
    konsol.print("""
    [green][[/][yellow] 1 [/][green]][/] [cyan]Session Oluştur[/]
    [green][[/][yellow] 2 [/][green]][/] [cyan]Gruptan User Dızla[/]
    [green][[/][yellow] 3 [/][green]][/] [cyan]Hedef Gruba Ekle[/]
    """)

    konum = os.getcwd()
    konum = konum.split("\\") if taban.isletim_sistemi == "Windows" else konum.split("/")
    secenek = str(konsol.input(f"[red]{taban.oturum}:[/][cyan]~/../{konum[-2] + '/' + konum[-1]} >> "))

    #-----------------------#
    if secenek == '1':
        taban.temizle
        taban.logo_yazdir()
        taban.bilgi_yazdir()


        sessioncu()
        # sleep(2)
        # acilis_sayfasi()
    #-----------------------#
    elif secenek == '2':
        taban.temizle
        taban.logo_yazdir()
        taban.bilgi_yazdir()

        ayiklayici()
        # sleep(2)
        # acilis_sayfasi()
    #-----------------------#
    elif secenek == '3':
        taban.temizle
        taban.logo_yazdir()
        taban.bilgi_yazdir()

        ekleyici()
        # sleep(2)
        # acilis_sayfasi()
    #-----------------------#
    elif secenek.lower() == 'q':
        import sys
        sys.exit()
    #-----------------------#
    else:
        taban.temizle
        acilis_sayfasi()


if __name__ == '__main__':
    acilis_sayfasi()