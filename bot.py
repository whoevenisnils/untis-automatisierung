import os
import requests
import webuntis
from datetime import date

USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Deine Schuldaten
UNTIS_SERVER = "gaensewinkel.webuntis.com"
UNTIS_SCHOOL = "gaensewinkel"

def check_untis():
    if not USER or not PASSWORD or not WEBHOOK_URL:
        print("[-] Fehler: Secrets (UNTIS_USER, UNTIS_PASSWORD, DISCORD_WEBHOOK) fehlen.")
        return

    s = None
    try:
        # Session initialisieren
        s = webuntis.Session(
            server=UNTIS_SERVER,
            username=USER,
            password=PASSWORD,
            school=UNTIS_SCHOOL,
            useragent="UntisDiscordBot_v3"
        )
        
        # Einloggen
        s.login()
        
        # Eigenen Stundenplan für den heutigen Tag abrufen
        today = date.today()
        timetable = s.get_timetable(start=today, end=today)
        
        # Nachricht für Discord vorbereiten
        nachricht = f"🔔 **Untis-Bot (Cloud):** Erfolgreich eingeloggt! {len(timetable)} persönliche Einträge für heute gefunden."
        
        # An Discord senden
        response = requests.post(WEBHOOK_URL, json={"content": nachricht})
        if response.status_code in (200, 204):
            print("[+] Discord-Benachrichtigung erfolgreich gesendet!")
        else:
            print(f"[-] Fehler beim Senden an Discord: {response.status_code}")
        
    except Exception as e:
        error_msg = f"⚠️ **Untis-Bot Fehler:** {e}"
        print(error_msg)
        requests.post(WEBHOOK_URL, json={"content": error_msg})
    finally:
        if s:
            try:
                s.logout()
            except:
                pass

if __name__ == "__main__":
    check_untis()
