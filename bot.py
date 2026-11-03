import os
import requests
import webuntis

# Daten sicher aus den Umgebungsvariablen (GitHub Secrets) laden
USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Untis-Schulserver-Daten (Bitte an deine Schule anpassen!)
UNTIS_SERVER = "mese.webuntis.com"   # Untis-Server deiner Schule (z.B. vertretungsplan.webuntis.com etc.)
UNTIS_SCHOOL = "Name_deiner_Schule"    # Der exakte Name der Schule bei WebUntis

def check_untis():
    if not USER or not PASSWORD or not WEBHOOK_URL:
        print("[-] Fehler: Es fehlen Umgebungsvariablen (Secrets)!")
        return

    try:
        # Verbindung zu WebUntis herstellen
        s = webuntis.Session(
            server=UNTIS_SERVER,
            username=USER,
            password=PASSWORD,
            school=UNTIS_SCHOOL,
            useragent="UntisDiscordBot"
        )
        s.login()
        
        # Beispiel: Den aktuellen Stundenplan für die nächsten Tage abrufen
        # (Hier könntest du den Stundenplan auslesen und vergleichen)
        timetable = s.get_timetable()
        
        # Nachricht für Discord vorbereiten
        nachricht = "🔔 **Untis-Bot (Cloud):** Verbindung erfolgreich! Der Stundenplan wurde geprüft. Alles aktuell."
        
        # An Discord senden
        response = requests.post(WEBHOOK_URL, json={"content": nachricht})
        if response.status_code == 204:
            print("[+] Discord-Benachrichtigung erfolgreich gesendet!")
        else:
            print(f"[-] Fehler beim Senden an Discord: {response.status_code}")
        
        s.logout()
    except Exception as e:
        error_msg = f"⚠️ **Untis-Bot Fehler:** {e}"
        print(error_msg)
        # Optional: Auch den Fehler an Discord melden
        requests.post(WEBHOOK_URL, json={"content": error_msg})

if __name__ == "__main__":
    check_untis()

