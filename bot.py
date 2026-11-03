import os
import json
import requests
import webuntis
from datetime import date

USER = os.environ.get("UNTIS_USER")
PASSWORD = os.environ.get("UNTIS_PASSWORD")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# Schuldaten
UNTIS_SERVER = "gaensewinkel.webuntis.com"
UNTIS_SCHOOL = "gaensewinkel"

# Deine fest eingetragene Discord User-ID für den Ping
DISCORD_USER_ID = "699686432293519532"

STATE_FILE = "last_timetable.json"

def load_last_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return None

def save_current_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"[-] Fehler beim Speichern des Zustands: {e}")

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
            useragent="UntisDiscordBot_v5"
        )
        
        # Einloggen
        s.login()
        
        # Stundenplan über die WebUntis API-Schnittstelle abrufen
        today = date.today()
        date_str = int(today.strftime('%Y%m%d'))
        
        timetable = s._request('getTimetable', {
            'options': {
                'startDate': date_str,
                'endDate': date_str,
                'element': {
                    'id': 0,
                    'type': 5
                }
            }
        })
        
        if not isinstance(timetable, list):
            timetable = []

        # Stundenplan in eine vergleichbare Struktur umwandeln
        current_state = []
        for entry in timetable:
            current_state.append({
                'id': entry.get('id'),
                'startTime': entry.get('startTime'),
                'endTime': entry.get('endTime'),
                'su': entry.get('su'), # Fächer
                'te': entry.get('te'), # Lehrer
                'ro': entry.get('ro'), # Räume
                'code': entry.get('code') # status (z.B. cancelled)
            })

        last_state = load_last_state()

        # Prüfen, ob dies der erste Durchlauf ist
        if last_state is None:
            save_current_state(current_state)
            print("[+] Erster Start: Stundenplan-Zustand initialisiert.")
            return

        # Bei einer Änderung Nachricht mit Ping senden
        if current_state != last_state:
            save_current_state(current_state)
            
            nachricht = f"🚨 <@{DISCORD_USER_ID}> **Stundenplan-Änderung erkannt!** Es gab ein Update in deinem Untis-Stundenplan für heute."
            
            response = requests.post(WEBHOOK_URL, json={"content": nachricht})
            if response.status_code in (200, 204):
                print("[+] Änderung erkannt und Discord-Benachrichtigung mit Ping gesendet!")
            else:
                print(f"[-] Fehler beim Senden an Discord: {response.status_code}")
        else:
            print("[*] Keine Änderungen im Stundenplan festgestellt.")
        
    except Exception as e:
        error_msg = f"⚠️ **Untis-Bot Fehler:** {e}"
        print(error_msg)
    finally:
        if s:
            try:
                s.logout()
            except:
                pass

if __name__ == "__main__":
    check_untis()
