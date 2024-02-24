# UDP, TCP chat
- **Název projektu**: UDP, TCP chat
- **Autor**: Jakub César
- **Email**: cesar@spsejecna.cz
- **LinkedIn**: [LinkedIn - Jakub César](https://tr.linkedin.com/in/jakub-c%C3%A9sar-714584243)
- **Github**: [Github - Jakub César](https://github.com/cesarjakub)
    - **Github odkaz na repozitář projektu**: [Github - repo](https://github.com/cesarjakub/alpha_4)
- **Datum vypracování**: 25.02.2024
- **Škola**: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30 
- **Projekt**: Jedná se o školní projekt

## Popis používání

## Specifikace požadavků

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

## Závěr