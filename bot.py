import os
import requests
import webuntis

# Daten sicher aus den GitHub Secrets laden
USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Server & Schulname deiner Schule (hier anpassen!)
UNTIS_SERVER = "gaensewinkel.webuntis.com"   # Z. B. mese.webuntis.com, ente.webuntis.com etc.
UNTIS_SCHOOL = "Gesamtschule_Gänsewinkel_Schwerte"    # Der exakte Name deiner Schule bei WebUntis

def check_untis():
    if not USER or not PASSWORD or not WEBHOOK_URL:
        print("[-] Fehler: Secrets (UNTIS_USER, UNTIS_PASSWORD, DISCORD_WEBHOOK) fehlen.")
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
        
        # Testnachricht an Discord senden
        nachricht = "🔔 **Untis-Bot (Cloud):** Verbindung erfolgreich! Der Bot überwacht den Stundenplan."
        
        response = requests.post(WEBHOOK_URL, json={"content": nachricht})
        if response.status_code in (200, 204):
            print("[+] Discord-Benachrichtigung erfolgreich gesendet!")
        else:
            print(f"[-] Fehler beim Senden an Discord: {response.status_code}")
        
        s.logout()
    except Exception as e:
        error_msg = f"⚠️ **Untis-Bot Fehler:** {e}"
        print(error_msg)
        requests.post(WEBHOOK_URL, json={"content": error_msg})

if __name__ == "__main__":
    check_untis()

