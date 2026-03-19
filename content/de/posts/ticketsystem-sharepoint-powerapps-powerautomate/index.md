---
title: "Ticketsystem mit SharePoint, Power Apps und Power Automate – inkl. automatischem Status-Workflow"
date: 2025-11-30T09:00:00+02:00
draft: false
slug: "ticketsystem-sharepoint-powerapps-powerautomate"
description: "Erstelle ein flexibles Ticketsystem mit SharePoint, Power Apps und Power Automate. Inklusive Statusmodell, Modulverantwortlichen, automatischem Workflow, Triggerbedingungen und Formular. Ideal für IT-Teams und interne Services."
categories: ["Power Platform", "Microsoft 365", "Tutorials"]
tags: ["Power Automate", "Power Apps", "SharePoint", "Ticketsystem", "Workflow", "Serviceprozess", "Automation"]
keywords:
  [
    "ticketsystem sharepoint",
    "ticketsystem powerapps",
    "ticketsystem power automate",
    "ticket workflow microsoft 365",
    "support system sharepoint",
    "sharepoint ticketsystem vorlage",
    "power automate triggerbedingung",
    "status workflow sharepoint liste"
  ]
cover:
  image: "/images/sh_ticketsystem_thumbnail.webp"
  alt: "Ticketsystem mit SharePoint, Power Apps und Power Automate."
  caption: "Schritt-für-Schritt Anleitung für ein Ticketsystem auf Basis von Microsoft 365."
  relative: true
translationKey: "ticketsystem-sharepoint-powerapps-powerautomate"
---

# Ticketsystem mit SharePoint, Power Apps und Power Automate

In diesem Beitrag zeige ich dir, wie du ein vollständiges Ticketsystem mit SharePoint-Listen, einer Power App und einem automatisierten Workflow mit Power Automate aufbaust. Die Lösung funktioniert vollständig mit Microsoft 365 Standardlizenzen und lässt sich flexibel erweitern – bis hin zum Einsatz eines autonomen KI-Agenten.


---

# Ziel des Ticketsystems

Wir bauen ein Support-System, das in diesem Beispiel Fragen rund um Power Apps verarbeitet. Die Struktur kann aber frei an deine Unternehmensanforderungen angepasst werden.

Wesentliche Elemente:

- Kategorisierung von Tickets über Module  
- Automatische Verantwortlichkeit  
- Statusmodell  
- Automatischer Flow bei Statusänderung  
- Unterstützung von Anhängen  
- Power App als Benutzeroberfläche

{{< figure src="/images/sp_ticketsystem_komponentenuebersicht.webp" alt="Die Komponenten des Ticketsystems in der Übersicht" caption="Die Power App schreibt in die zentrale SP-Liste. Diese triggert wiederum den Power Automate Flow zur Anwenderkommunikation" >}}
sp

---

# SharePoint-Listen als Datenbasis

Wir benötigen drei Listen:

1. Tickets (AI_Ticketsystem)  
2. Status (AI_Ticketstatus)  
3. Module (AI_Ticketmodule)

---

## Liste „Status“

Diese Liste wird später als Lookup im Ticketsystem verwendet.

**Felder:**

- Title (Standard)

**Einträge:**

- Neu  
- In Bearbeitung  
- Abschluss durch KI-Agenten  
- Abgeschlossen  

{{< figure src="/images/sp_ticketsystem_liste_status.webp" alt="SP-Liste Status" caption="In der Liste Status werden alle relevanten Status des Ticketsystems hinterlegt." >}}


---

## Liste „Module“

Hier werden Themenbereiche definiert sowie Verantwortliche hinterlegt. Die Idee ist, dass mit der ersten Übermittlung eines Tickets direkt ein (erster) Verantwortlicher hinterlegt werden kann. Die Verantwortlichkeit kann im Anschluss angepasst werden.

**Felder:**

- Title  
- Verantwortlich (Person oder Gruppe)

**Einträge:**

- SharePoint  
- Dataverse  
- Others

{{< figure src="/images/sp_ticketsystem_liste_status.webp" alt="SP-Liste Module" caption="In der Liste Module werden alle relevanten Module und Verantwortlichkeiten des Ticketsystems hinterlegt." >}}

---

## Liste „Tickets“

Diese Liste bildet das Herzstück des Systems.

**Felder:**

- Title  
- Fragestellung (Text)  
- Antwort (Text)  
- Status (Lookup Status)  
- StatusRef (Lookup Status, zur Prüfung auf Änderungen)  
- Modul (Lookup Module, Pflichtfeld)  
- Verantwortlich (Person/Gruppe)

{{< figure src="/images/sp_ticketsystem_liste_tickets.webp" alt="SP-Liste Tickets" caption="In der Liste Tickets werden Tickets und Referenzen auf Status, Module und Verantwortliche gespeichert." >}}


---

# Power Automate Flow

Der Flow übernimmt folgende Aufgaben:

- Prüfen, ob ein Verantwortlicher gesetzt ist  
- Falls nicht: Modulverantwortlichen laden  
- Anforderer per E-Mail informieren  
- Referenzstatus aktualisieren (Verhinderung von Endlosschleifen)

{{< figure src="/images/sp_ticketsystem_flow_uebersicht.webp" alt="SP-Liste Tickets" caption="In der Liste Tickets werden Tickets und Referenzen auf Status, Module und Verantwortliche gespeichert." >}}


---

## Trigger

Als Trigger verwenden wir:

"When an item is created or modified"

Der Flow soll aber nur starten, wenn sich der Status geändert hat. Dafür nutzen wir eine Triggerbedingung.

Triggerbedingung:

```powerfx
@not(equals(triggerOutputs()?['body/Status/Value'],triggerOutputs()?['body/StatusRef/Value']))
```

Nur wenn Status und StatusRef ungleich sind, startet der Flow.


{{< figure src="/images/sp_ticketsystem_Triggerbedingung.webp" alt="Flow Trigger" caption="Der Flow startet nur, wenn sich Status und Statusreferenz unterscheiden. Hierfür wird eine Triggerbedingung genutzt." >}}


---

## Prüfung der Triggerbedingung

Zur Kontrolle kannst du eine Compose-Aktion anlegen und den Ausdruck dort testweise einfügen. 

---

## Initialisieren der Variable „Verantwortlich“

Variable:

Name: Verantwortlich  
Typ: String

Wert wird später dynamisch befüllt.

---

## Setzen der Variable „Verantwortlich“ (falls bereits vorhanden)

Der Wert wird aus dem aktuellen Ticket übernommen. Diese Aktion schlägt fehl, wenn kein Verantwortlicher hinterlegt ist. Das ist gewollt, denn dann greifen wir im nächsten Schritt auf die Module-Liste zurück.

{{< figure src="/images/sp_ticketsystem_ermittlung_verantwortlicher.webp" alt="Ermittlung Verantwortliche" caption="Die Verantwortliche Person wird entweder aus dem bestehenden Tiket ermittlt. Schlägt das fehl, so wird die verantwortliche Person aus der Liste Module ermittelt. Die Kennzeichnung (Vgl. gelbe Markierung kennzeichnet die Ausführungsbedingungg für eie Aktion 'Get item Modul')." >}}

---

## Modulverantwortlichen laden

Aktion: Get item  
Quelle: AI_Ticketmodule  
ID: Modul-ID aus dem Ticket

Diese Aktion wird nur ausgeführt, wenn der vorherige Schritt fehlgeschlagen ist.

{{< figure src="/images/sp_ticketsystem_verantwortlicher_aus_modul.webp"  alt="Ermittlung Verantwortliche aus Modul" caption="Zu sehen ist die Konfiguration der Ausführungsoption. Die Aktion soll nur dann ausgeführt werden, wenn die Vorgängeraktion fehlgeschlagen ist - also wenn noch keine verantwortliche Peron im Ticket hinterlegt war." >}}


---

## Setzen der Variable aus der Modulliste

Die Variable "Verantwortlich" wird nun mit dem Claim-Wert aus der Modul-Liste gefüllt.



{{< figure src="/images/sp_ticketsystem_set_var_verantwortlich.webp" alt="Variable verantwortlich" caption="Die aus der Modul-Liste ermittelte Person wird in der Variable 'Verantwortlich' gespeichert. Die Variable ist vom Typ 'Objekt'." >}}

---

## E-Mail an Anforderer senden

Empfänger: Created by Email  
Betreff: z. B. Titel des Tickets  
Body: Status und direkter Link zum Element

Diese Aktion soll sowohl bei erfolgreicher als auch übersprungener Vorgängeraktion ausgeführt werden.

{{< figure src="/images/sp_ticketsystem_send_email.webp" alt="E-Mail senden" caption="Die E-Mail an den Anforderer / die Anforderin soll in allen Fällen versendet werden. Also sowohl wenn die verantwortliche Person aus dem Ticket selbst ermittelt werden konnte als auch wenn die verantwortliche Person aus der Liste Module ermittelt wurde. Dies ist in der Ausführungskonfiguration entsprechend zu berücksichtigen." >}}

---

## Update des Tickets

Zum Abschluss aktualisieren wir das Ticket:

1. Das Feld StatusRef wird auf denselben Wert wie Status gesetzt  
2. Das Feld Verantwortlich wird auf die Variable Verantwortlich gesetzt  

Damit wird eine Endlosschleife im Trigger verhindert.


{{< figure src="/images/sp_ticketsystem_update_referenzstatus.webp" alt="Referenzstatus aktualisieren" caption="Die letzte Aufgabe im Flow aktualisiert den Referenzstatus sowie die verantwortliche Person für das Ticket. Die Anpassung des Referenzstatus (Referenzstatus = Status) ist wichtig! Hierdurch wird eine Dauerscheife des Flows verhindert." >}}


---

# Power App Formular

Wir erstellen eine einfache Power App direkt aus der SharePoint-Liste:

**Integrieren → Power Apps → App erstellen**

{{< figure src="/images/sp_ticketsystem_power_app_erstellen.webp" alt="Power App erstellen" caption="Eine Standard Power App zum Bearbeiten Lesen und Bearbeiten der Zeilen einer Sharepoint-Liste lässt sich direkt über die Liste in Sharepoint erstellen. Auf diese Basis können wir aufauen und die App an eigene Anforderungen anpassen." >}}

---

## Formular anpassen
Im nächsten Schritt kann das Formular der Power App angepasst werden. Hierfür werden nicht benötigte Felder ausgeblendet, Standard-Werte (für den Status) werden hinterlegt.

### Nicht benötigte Felder entfernen
Für die Anlage nicht benötigte Felder (z.B. die Antwort auf die Fragestellung) kann direkt aus dem Formular entfernt werden:

{{< figure src="/images/sp_ticketsystem_power_app_formularfelder_entfernen.webp" alt="Felder aus Power App Formular entfernen" caption="Nicht relevante Felder (z.B. Antwort / Lösungsansatz) werden am besten direkt aus den Formular entfernt. Die Felder werden später im Prozess relevant." >}}

Im Sinne einer Anlage eines neuen Tickets macht es Sinn folgende Felder aus dem Formular zu entfernen:
- Antwort
- StatusRef
- Verantwortlich




### Default für Status setzen

Das Feld Status muss für diesen Ansatz zum Zeitpunkt des Anlegens des Tickets immer "Neu" sein. So unterscheidet sich der Status vom Referenzstatus und der Flow zur Verarbeitung der Anlage kann starten.

Im Attribut DefaultSelectedItems:

{
  '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedReference",
  Id: "1",
  Value: "Neu"
}

### Feld Status ausblenden  

Da der Status immer "Neu" ist zum Zeitpunkt der Anlage, ist der Informationswert hier nicht relevant. Es macht Sinn das Feld "Status" über das Attribut "Visible" unsichtbar zu machen:

{{< figure src="/images/sp_ticketsystem_status_visible_false.webp" alt="Felder unsichtbar machen" caption="Felder mit Default-Werten müssen im Formular verbleiben. Da der Wert immer gleich ist macht es aus Nutzersicht Sinn das Feld auszublenden." >}}


# Test

Erstelle ein Ticket, verändere den Status und prüfe:

- Wird der Flow ausgelöst?  
- Wird ein Verantwortlicher gesetzt?  
- Wird die Benachrichtigung korrekt gesendet?  
- Wird der Referenzstatus aktualisiert?

---

# Ausblick und Erweiterungen

In zukünftigen Ausbaustufen könnten ergänzt werden:

- Autonomer KI-Support-Agent  
- Tickets per E-Mail erstellen  
- Tickets über Chatbots erzeugen  
- Fotos direkt vom Smartphone hochladen  
- Weitere Logiken nach Community-Feedback

---

# Download

Die Lösung kannst du herunterladen. Den Link findest du hier unter Downloads. Dieser verweist auf ein GitHub Repository.

---

# YouTube
Du findest diesen Beitrag auch in meinem YouTube Kanal

{{< confirmed_youtube id="naz1TnPs7NY" >}}

# Unterstützung
Du brauchst Unterstützung bei der Implementierung eines Ticketsystems in deinem Unternehmen? Du hast Anforderungen, die du gerne einmal dieskutierenmöchtest? Du kannst dir eine Zusammenarbeit vorstellen?

Kontaktiere mich gerne. Möglichkeiten zur Kontaktaufnahme findest du unter [Kontakt]({{< ref "contact" >}})
