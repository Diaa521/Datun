from colorama import Fore as F, init, Style as Stl
import datetime as date
import time as zeit
import geocoder
import keyboard
import requests
import webbrowser
import re
init()


# Darstellung des aktuellen Datums und der Anfang.
heute = date.datetime.now()
print('')# Leerzeile
print(f'Heute ist der| ' + F.LIGHTWHITE_EX + f'{heute.day}.{heute.month}.{heute.year}' + Stl.RESET_ALL)
Uhr = heute.strftime('%H:%M:%S')
print(f'Aktuelle Uhrzeit: {F.LIGHTWHITE_EX}{Uhr} {Stl.RESET_ALL}')
print(F.LIGHTBLUE_EX +"-          -          -          -          -          -          -          -" + F.RESET)

name_user = ''
# Websiten
websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com/results?search_query=Aktuelle+lage+der+Welt+%22Wetter%22",
    "wetter": "https://www.wetter.com"
}


# Haubtfunktion
def internationale_datum_funktion():
    global websites, name_user, heute, Uhr
    known_new_moon = date.datetime(2025, 9, 15)  # Beispiel: letzte Neumond
    days_since_new_moon = (heute - known_new_moon).days % 29.53  # Mondzyklus ≈ 29.53 Tage



    if days_since_new_moon < 1.5:
        phase = "🌑 Neumond"
    elif days_since_new_moon < 7.4:
        phase = "🌒 Zunehmend"
    elif days_since_new_moon < 14.7:
        phase = "🌕 Vollmond"
    elif days_since_new_moon < 22:
        phase = "🌘 Abnehmend"
    else:
        phase = "🌑 Neumond naht"

    feiertage = {
    (1, 1): "Neujahr",
    (25, 12): "Weihnachten",
    (31, 10): "Halloween",
    (14, 2): "Valentinstag",
    (1, 5): "Tag der Arbeit",
    (3, 10): "Tag der Deutschen Einheit",
    (31, 12): "Silvester"
}

    while True:
        tag = input(F.RESET + 'ask Datune'+F.LIGHTBLACK_EX +" or 'help'" + F.LIGHTWHITE_EX + ': ')

        # Reinigung der Eingabe
        tag = re.sub(r'[?,]', '', tag)  # Entfernt Kommas UND Fragezeichen
        tag = re.sub(r'\s{2,}', ' ', tag).strip()  # Glättet Leerzeichen

        
        if tag.lower() in ["datum", "date", "today", "heute"]:
            print(F.LIGHTMAGENTA_EX + "- " + F.RESET + "Heute ist der|" + F.LIGHTWHITE_EX + f'{heute.day}.{heute.month}.{heute.year}' + Stl.RESET_ALL)
        elif tag.lower() in ["uhrzeit", "time", "now", "aktuelle uhrzeit", "uhr", "aktuelle zeit"]:
            aktuelle_zeit = date.datetime.now().strftime('%H:%M:%S')
            print(F.LIGHTMAGENTA_EX + "- " + F.RESET + f'Aktuelle Uhrzeit: {F.LIGHTWHITE_EX}{aktuelle_zeit} {Stl.RESET_ALL}')
        elif tag.lower() in ["mondphase", "mondphase heute", "mondphase jetzt"]:
            print(F.LIGHTMAGENTA_EX + "- " + F.RESET + f'Heutige Mondphase {heute.day}.{heute.month}.{heute.year}:' + F.LIGHTWHITE_EX + f'{phase}')
        elif tag.lower() in ["feiertage", "feiertag", "feiertage heute", "feiertag heute"]:
            feiertag_name = feiertage.get((heute.month, heute.day))
            if feiertag_name:
                print(F.LIGHTMAGENTA_EX + '- ' + F.RESET + f'Heute ist {feiertag_name}')
            else:
                print(F.LIGHTMAGENTA_EX + '- ' + F.RESET + 'Heute ist kein Feiertag.')      
        elif tag.lower() in ["mein standort", "standort", "meine ort", "wo bin ich", "wo befidne ich mich", "my location", "location"]: 
               geometrie()
        elif tag.lower() in ["wetter", "wetter heute", "wie sit das wetter", "sag mir das wetter", "wie wetter"]:
                hole_wetter()       
        elif tag.lower().startswith("öffne "):
            site_key = tag.lower()[7:].strip()  # Entfernt "öffne " und glättet Leerzeichen
            url = websites.get(site_key)
            if url:
                print(F.LIGHTMAGENTA_EX + '- ' + F.RESET + f'Öffne {site_key}: {url}')
            else:
                print(F.LIGHTBLACK_EX + '- ' + F.RESET + "Unbekannte Webseite. Verfügbare Seiten: " + ', '.join(websites.keys()) + F.RESET)
        elif tag.lower() in ["einstellungen", "setting", "settings", "hilfe", "help"]:
                datune_einstellungen()
        else:
            print(F.LIGHTBLACK_EX +"unknown command." + F.RESET)
            


def geometrie():
    # Standort über IP ermitteln
    geo = geocoder.ip('me')

    if geo.ok:
        print('Internet erforderlich...')
        zeit.sleep(1)
        print(F.LIGHTCYAN_EX + '- ' + F.RESET + f'📍 Dein Standort: {geo.city}, {geo.country}')
        zeit.sleep(2.5)
        return
    else:
        print('Internet erforderlich...')
        zeit.sleep(0.5)
        print("Standort konnte nicht ermittelt werden." + F.LIGHTBLACK_EX + "Prüfe Inernetverbindung." + F.RESET)
        zeit.sleep(2.5)
        return


# Wetterdaten abrufen (Open-Meteo API – keine Anmeldung nötig)
def hole_wetter():
    geo = geocoder.ip('me')
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.45,
        "longitude": 7.01,
        "current_weather": True
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        daten = response.json()["current_weather"]
        temperatur = daten["temperature"]
        wind = daten["windspeed"]
        wettercode = daten["weathercode"]
        zeitpunkt = daten["time"]

        beschreibung = {
            0: "Klarer Himmel",
            1: "Überwiegend klar",
            2: "Teilweise bewölkt",
            3: "Bewölkt",
            45: "Nebel",
            48: "Nebelfrost",
            51: "Leichter Regen",
            61: "Mäßiger Regen",
            71: "Leichter Schnee",
            80: "Regenschauer",
            95: "Gewitter"
        }.get(wettercode, "Unbekanntes Wetter")

        print(F.LIGHTWHITE_EX + "╭───────────── Wetter ─────────────╮" + Stl.RESET_ALL)
        print(F.CYAN + f"│ 📍 Standort: {geo.city}, {geo.country:<15} │" + Stl.RESET_ALL)
        print("|")
        print(F.LIGHTWHITE_EX + f"│ 🌡️ Temperatur: {temperatur:>5}°C               │" + Stl.RESET_ALL)
        print(F.LIGHTWHITE_EX + f"│ 💨 Wind:      {wind:>5} km/h              │" + Stl.RESET_ALL)
        print(F.LIGHTWHITE_EX + f"│ 🌦️ Wetter:"  +    F.LIGHTWHITE_EX +f"      {beschreibung:<22}│" + Stl.RESET_ALL)
        print(F.LIGHTWHITE_EX + "╰─────────────────────────────────╯" + Stl.RESET_ALL)
        zeit.sleep(2.5)
        return
    else:
        print(F.LIGHTBLACK_EX + "Fehler beim Abrufen der Wetterdaten." + Stl.RESET_ALL)
        zeit.sleep(1)
        return


def Daten_Bank():
    global name_user
    # Standort über IP ermitteln
    geo = geocoder.ip('me')
    print('----- Daten Bank -----')
    print('')# Leerzeile
    if name_user == '':
        print(F.LIGHTWHITE_EX + 'Dein Name: ' + F.RESET + 'Kein Name gesetzt' + Stl.RESET_ALL)
    else:
        print(f"Dein Name:{name_user} ")
    if geo.ok:
        print(F.LIGHTWHITE_EX + 'Dein Standort: ' + F.RESET + f'{geo.city}, {geo.country}' + Stl.RESET_ALL)
        zeit.sleep(2.5)
        return
    else:
        print(F.LIGHTWHITE_EX + 'Dein Standort: ' + F.RESET + F.LIGHTBLACK_EX + 'Standort konnte nicht geladen werden.' + Stl.RESET_ALL)   
        zeit.sleep(2)
        return

# Datune Einstellungen
def datune_einstellungen():
    print(F.LIGHTWHITE_EX +'----- Datune Einstellungen -----')
    print('Datune reagiert auf: Uhr, datum, mondphase, feiertage, mein standort, wetter, öffne <webseite>.')
    input(F.LIGHTBLACK_EX + "Drücke Enter um zurückzukehren." + F.RESET)
    return
    


# Starte Datune in der Haubtfunktion
zeit.sleep(0.4)
internationale_datum_funktion()           
