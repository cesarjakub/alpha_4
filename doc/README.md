# Peer-to-peer chat (P2P)
- **Název projektu**: peer-to-peer chat (P2P)
- **Autor**: Jakub César
- **Email**: cesar@spsejecna.cz
- **LinkedIn**: [LinkedIn - Jakub César](https://tr.linkedin.com/in/jakub-c%C3%A9sar-714584243)
- **Github**: [Github - Jakub César](https://github.com/cesarjakub)
    - **Github odkaz na repozitář projektu**: [Github - repo](https://github.com/cesarjakub/alpha_4)
- **Datum vypracování**: 25.02.2024
- **Škola**: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30 
- **Projekt**: Jedná se o školní projekt

## Popis používání
- Po [instalaci a puštění programu](#instalace-a-spuštění-aplikace).
- Připojení se k chatu:
  - Po spuštění aplikace začne automaticky vyhledávat ostatní peery v síti pomocí UDP.
  Pokud se připojí jiný peer, aplikace naváže s ním TCP spojení a zobrazí v konzoli zprávu o úspěšném navázání spojení.

- Odesílání zpráv:
  - Pro odeslání zprávy použijte metodu send_tcp_msg(message), kde message je text zprávy, kterou chcete odeslat.
  Tato metoda pošle zprávu všem ostatním připojeným peerům pomocí TCP spojení.

- Příjem zpráv:
  - Aplikace automaticky naslouchá na příchozí zprávy od ostatních peerů.
Pokud obdržíte zprávu, aplikace ji zpracuje a zobrazí v konzoli.

## Specifikace požadavků
- UDP discovery
- TCP protocol
- Webové api
  - [Doména](http://s-cesar-3.dev.spsejecna.net/)
- Systémový daemon

## Popis architektury
- Peer-to-peer (P2P) architektura
  - Decentralizovaný model počítačové sítě, ve které spolu komunikují přímo klienti bez nutnosti serveru.
  - P2P síti si každý klient nese zodpovědnost za sdílení a ukládání dat a zároveň může využívat data a služby sdílené ostatními klienty.

## Nastavení config souboru
- Před používáním je třeba nastavit konfiguraci aplikace
- najdeme ji ve složce `/config/config.ini`
- zde je třeba upravit
  - **peer_id** - port pro naslouchání
  - **broadcast_address** - ip adresa na naslouchání
  - **port** - nastavení libovolného id 'peera'

## Instalace a Spuštění aplikace
- Aplikace běží na VM, ketrý mi byl přidělen panem učitelem `Moličem`
- Po správném vyplnění [config souboru](#nastavení-config-souboru) můžeme pokračovat dále
  - Chat se spouští příkazem `sudo systemctl start cesar`
  - Příkazem `sudo systemctl status cesar` si můžeme zobrazit status chatu
  - Chat se stopuje příkazem `sudo systemctl stop cesar`

## Chybové stavy
- Chyby při [nevyplnění konfiguračního souboru](#nastavení-config-souboru)
- Chyby přo síťové komunikaci
  - UDP
  - TCP
- Chyby spojené s thready

## Knihovy třetích stran
- knihovny:
  - **socket**
  - **json**
  - **threading**
  - **datetime**
  - **time**
  - **flask**

## Závěr
- Tento projekt představuje implementaci peer-to-peer chatu s využitím TCP a UDP pro 
komunikaci mezi klienty. 
- Při používání tohoto chatu je klíčové správné nastavení konfiguračního souboru, 
který umožňuje individualizaci každé instance aplikace
- Během běhu aplikace mohou nastat chybové stavy spojené především s nedostupností sítě 
nebo problémy s vlákny, vše by mělo být odchyceno try except blokem