import os
import requests
import webuntis

USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Deine Schuldaten
UNTIS_SERVER = "gaensewinkel.webuntis.com"
UNTIS_SCHOOL = "Staedtische Gesamtschule Gaensewinkel"  # Hier exakten Schulnamen eintragen

def check_untis():
    if not USER or not PASSWORD or not WEBHOOK_URL:
        print("[-] Fehler: Secrets fehlen.")
        return

    s = None
    try:
        # Session mit stabilen Parametern initialisieren
        s = webuntis.Session(
            server=UNTIS_SERVER,
            username=USER,
            password=PASSWORD,
            school=UNTIS_SCHOOL,
            useragent="UntisDiscordBot_v2"
        )
        
        # Einloggen
        s.login()
        
        # Test, ob der Stundenplan abgerufen werden kann
        timetable = s.get_timetable()
        
        nachricht = "🔔 **Untis-Bot (Cloud):** Verbindung und Stundenplan-Abruf erfolgreich!"
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
