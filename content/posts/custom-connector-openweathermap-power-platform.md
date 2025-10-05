---
title: "Custom Connector für OpenWeatherMap in der Power Platform (Power Apps & Power Automate)"
slug: "custom-connector-openweathermap-power-platform"
date: 2025-10-02T09:00:00+02:00
draft: false
description: "Schritt-für-Schritt-Anleitung: Erstelle einen benutzerdefinierten Connector für die OpenWeatherMap API, teste ihn mit Postman und nutze ihn in Power Automate und Power Apps (Canvas)."
tags: ["Power Platform", "Power Apps", "Power Automate", "Custom Connector", "API", "OpenWeatherMap", "Power FX", "Postman"]
categories: ["Tutorial"]
keywords: ["benutzerdefinierter Connector", "Custom Connector Power Apps", "Power Automate Wetter", "OpenWeatherMap API Key", "Postman Test", "Swagger", "Canvas App", "Dataverse"]
toc: true
canonicalURL: "https://jonaskufner.com/posts/custom-connector-openweathermap-power-platform/"
cover:
  image: "/images/custom-connector-cover.webp"
  alt: "Benutzerdefinierter OpenWeatherMap Connector in der Microsoft Power Platform"
  caption: "Aus der Praxis: Wetterdaten via Custom Connector in Power Automate & Power Apps"
  relative: true
---

> **Video zum Blogpost:** 👉 [YouTube-Tutorial ansehen](https://www.youtube.com/watch?v=SPGXvE3D4cs)

## Kurzüberblick

In diesem Beitrag zeige ich, wie du **einen benutzerdefinierten Connector** (Custom Connector) für die **OpenWeatherMap-API** erstellst und ihn anschließend **in Power Automate** und **Power Apps (Canvas)** verwendest.  
Wir gehen Schritt für Schritt vor: **API testen (Postman)** → **Connector anlegen** → **Aktion definieren** → **Verbindung testen** → **in Flows & Apps nutzen**.


---

## Warum ein benutzerdefinierter Connector?

Die Microsoft Power Platform bringt viele **Out-of-the-Box**-Connectoren mit. Aber: Wenn *dein* System oder *deine* API nicht dabei ist, brauchst du eine flexible Lösung.  
Mit einem **Custom Connector** bindest du **beliebige REST-APIs** an – z. B. Projektmanagement, Buchhaltung oder KI-Services. Für dieses Tutorial verwenden wir **OpenWeatherMap** als einfaches, praxistaugliches Beispiel.

---

## Voraussetzungen

- Microsoft Power Platform Zugriff (Power Apps / Power Automate)  
- Ein **kostenloser OpenWeatherMap-Account** inkl. **API-Key**  
- **Postman** zum schnellen API-Test (kostenlos)

---

## Schritt 1: API-Aufruf mit Postman prüfen

Vor der tatsächlichen Erstellung des benutzerdefinierten Konnektors macht es Sinn den API-Aufruf mittels Powtman zu testen. Das ist optional, hilft aber für die folgenden Schritte.

1. **Neue Anfrage** anlegen (GET).  
2. URL aus der OWM-Doku übernehmen, z. B.:  https://api.openweathermap.org/data/2.5/weather?lat=48.17&lon=11.61&units=metric&appid=DEIN_API_KEY
3. **Send** klicken – bei Erfolg erhältst du **Statuscode 200** und eine **JSON-Antwort** mit Wetterdaten.

{{< figure src="/images/postman-test.webp" alt="Postman Test: GET /data/2.5/weather" caption="Postman: Erfolgreicher GET-Call mit Status 200 und JSON-Antwort." >}}

**Typische Felder der Antwort (gekürzt):**
```json
{
"weather":[{"main":"Clear","description":"clear sky"}],
"main":{"temp":21.3,"feels_like":21.0,"humidity":45},
"wind":{"speed":3.6},
"name":"Munich",
"coord":{"lat":48.17,"lon":11.61}
}
```

## Schritt 2: Custom Connector in Power Apps anlegen

Wechsle zu make.powerapps.com → Benutzerdefinierte Konnektoren.

2.1 Allgemein

- Name: z. B. OpenWeather Connector
- Host: api.openweathermap.org
- Basis-URL: /data/2.5/
- Beschreibung (Beispieltext):
„Der Custom Connector bietet die Aktion Aktuelles Wetter an. Diese liefert Wetterinformationen für einen definierten Standort. Datenquelle ist openweathermap.org.“

Optional: Symbol & Farbe für eine bessere Wiedererkennung.

{{< figure src="/images/connector-general.webp" alt="Connector Allgemein: Host & Basis-URL" caption="Power Apps: Bereich Allgemein mit Host api.openweathermap.org und Basis-URL /data/2.5/." >}}

2.2 Sicherheit

- Authentifizierungstyp: „API-Schlüssel“

- Parameterbezeichnung: frei wählbar (z. B. „OpenWeather API Key“)

- Parametername: appid (muss zur API passen)

- Parameterstandort: Query (wie im Postman-Test)

{{< figure src="/images/connector-security.webp" alt="Connector Sicherheit: API-Schlüssel in Query" caption="Power Apps: Bereich Sicherheit – Authentifizierungstyp API-Schlüssel, Parametername appid, Standort Query." >}}


2.3 Definition (Aktionen)

- Neue Aktion anlegen:
- Zusammenfassung: Aktuelles Wetter

Beschreibung: Liefert das aktuelle Wetter für eine Position (lat/lon).

Vorgangs-ID: AktuellesWetterFuerStandort (eindeutig, keine Leerzeichen)

Anforderung:

Importiere die Beispiel-Anfrage (z. B. aus Postman oder als Beispiel-URL).

Entferne appid aus den Parametern der Aktion, weil der Wert über die Verbindung geliefert wird.

Lasse lat und lon als Query-Parameter bestehen.

{{< figure src="/images/connector-definition.webp" alt="Connector Definition: Aktion Aktuelles Wetter" caption="Power Apps: Bereich Definition – Aktion Aktuelles Wetter mit Query-Parametern lat & lon." >}}

2.4 Code (optional)

Hier könntest du API-Antworten transformieren (z. B. nur bestimmte Felder weiterreichen). Für das erste Setup überspringen wir diesen Teil.

2.5 Testen

Connector speichern → dann im Reiter Testen eine Verbindung anlegen.

API-Key (dein appid) hinterlegen.

lat/lon eingeben, z. B. 48.17 und 11.61 (Englischer Garten, München).

Aufrufen – du solltest die JSON-Antwort sehen.

{{< figure src="/images/connector-test.webp" alt="Connector Test: Verbindung & Aufruf" caption="Power Apps: Bereich Testen – Verbindung mit API-Key und Testaufruf mit lat=48.17, lon=11.61." >}}

## Schritt 3: Einsatz in Power Automate

Neuen Flow erstellen (z. B. „Manuell ausgelöst“).

Aktion → Benutzerdefinierte → deinen OpenWeather Connector auswählen.

Parameter übergeben: lat & lon.

Flow speichern und testen.

Die Ausgabe enthält alle Wetterdaten, mit denen du weiterarbeiten kannst (z. B. Bedingung, Nachricht, Teams-Post, E-Mail).

{{< figure src="/images/flow-action.webp" alt="Power Automate: Aktion aus Custom Connector" caption="Power Automate: Flow-Aktion aus dem benutzerdefinierten Connector mit Ausgabe der Wetterdaten." >}}

Beispiel: Felder aus der Antwort weiterverwenden

body('AktuellesWetterFuerStandort')?['main']?['temp']

body('AktuellesWetterFuerStandort')?['weather']?[0]?['description']

## Schritt 4: Einsatz in Power Apps (Canvas)

Datenquelle hinzufügen → deinen OpenWeather Connector auswählen.

In Power FX die Aktion aufrufen, Parameter als Record übergeben.

Beispiel (OnSelect eines Buttons):

Set(
    gblWeather,
    OpenWeatherConnector.AktuellesWetterFuerStandort(
        { lat: 48.17, lon: 11.61 }
    )
)


Beispiel (Textlabel):

"Temp: " & Round(gblWeather.main.temp, 1) & " °C — " & 
First(gblWeather.weather).description


{{< figure src="/images/tests-powerapps.webp" alt="Power Apps Canvas: Ausgabe der Wetterdaten" caption="Power Apps (Canvas): Label, das Temperatur & Beschreibung aus gblWeather anzeigt." >}}

Tipp: Definiere units=metric in der Aktion oder als optionalen Query-Parameter, damit Temperaturen in °C zurückkommen.



## Zusammenfassung

- Was? Eigener Connector für OpenWeatherMap

- Warum? Jede REST-API in Power Platform nutzbar

- Wie? Postman testen → Connector definieren → in Flows & Apps einsetzen

- Code? Power FX für Aufruf & Anzeige

- Nächster Schritt: Packaging als Solution & weitere Business-APIs anbinden

Video: Schritt-für-Schritt ansehen

👉 Hier geht’s zum Tutorial:
Custom Connector – OpenWeatherMap (YouTube)


{{< figure
    src="/images/YouTube-Link-image.webp"
    alt="Vorschaubild: Jede API mit der Power Platform verbinden 🚀 | Custom Connector Tutorial"
    caption="Videotutorial zum Blogbeitrag(YouTube | externer Link)"
    link="https://www.youtube.com/watch?v=SPGXvE3D4cs"
    target="_blank"
    rel="external noopener nofollow"
    title="YouTube: Jede API mit der Power Platform verbinden 🚀 | Custom Connector Tutorial"
>}}


Ich plane im nächsten Schritt eigene Schnittstellen zwischen Geschäftsanwendungen aufzubauen (z. B. Projektmanagement, Buchhaltung, KI-Dienste).
Welche Anwendungen würdest du gerne verknüpfen? Schreib’s mir in die Kommentare!