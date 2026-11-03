import os
import requests
import webuntis
from datetime import date

USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Deine Schuldaten
UNTIS_SERVER = "gaensewinkel.webuntis.com"
UNTIS_SCHOOL = "gaensewinkel"  # Hier den exakten Schulnamen eintragen

def check_untis():
    if not USER or not PASSWORD or not WEBHOOK_URL:
        print("[-] Fehler: Secrets fehlen.")
        return

    s = None
    try:
        # Session initialisieren
        s = webuntis.Session(
            server=UNTIS_SERVER,
            username=USER,
            password=PASSWORD,
            school=UNTIS_SCHOOL,
            useragent="UntisDiscordBot_v2"
        )
        
        # Einloggen
        s.login()
        
        # Den aktuellen Stundenplan für heute abrufen (korrekte webuntis-Syntax)
        today = date.today()
        timetable = s.get_timetable(start=today, end=today)
        
        nachricht = f"🔔 **Untis-Bot (Cloud):** Erfolgreich eingeloggt! {len(timetable)} Einträge für heute gefunden."
        requests.post(WEBHOOK_URL, json={"content": nachricht})
        
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
