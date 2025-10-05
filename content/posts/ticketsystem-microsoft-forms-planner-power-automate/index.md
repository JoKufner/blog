---
title: "Einfaches Ticketsystem mit Microsoft Forms, Planner & Power Automate – Schritt-für-Schritt zur schnellen Ticketlösung in Microsoft 365"
date: 2025-10-04T09:00:00+02:00
draft: false
slug: "ticketsystem-microsoft-forms-planner-power-automate"
description: "Bauen Sie in < 60 Minuten ein schlankes Ticketsystem auf Basis von Microsoft 365: Formular in Forms, Aufgaben in Planner, Automatisierung mit Power Automate – inkl. Benachrichtigungen in Teams und Abschluss-Workflow. Anleitung mit Ausdrücken & Best Practices."
categories: ["Power Platform", "Microsoft 365", "Tutorials"]
tags: ["Power Platform", "Microsoft 365", "Power Automate", "Microsoft Forms", "Microsoft Planner", "Ticketsystem", "IT-Support", "Teams", "Automatisierung", "Low-Code", "Workflow", "Tutorial", "Best Practices"]
keywords: ["ticketsystem microsoft 365","ticketsystem forms planner power automate","power automate planner aufgabe erstellen","forms response planner task","teams benachrichtigung power automate","checklist email planner auslesen","einfaches ticketsystem ohne programmierung","low code ticketsystem microsoft"]
cover:
  image: "/images/ticketsystem-cover.webp"
  alt: "Ticketsystem mit Microsoft 365 und Power Automate selbst erstellen."
  caption: "Tutorial zur Erstellung eines einfachen Ticketsystems mit Microsoft 365 und Power Automate"
  relative: true


# Optional theme params commonly supported:
# toc: true
# showReadingTime: true
# cover:
#   image: "/images/ticketsystem-forms-planner-power-automate.png"
---

> **Kurzfassung:** Dieses Tutorial zeigt, wie Sie mit **Microsoft Forms**, **Planner** und **Power Automate** in kurzer Zeit ein **einfaches Ticketsystem** aufbauen – inkl. **Teams-Benachrichtigung** bei Anlage und **Abschlussmeldung**.



## Zielbild & Voraussetzungen

**Ziel:** Ein sehr einfaches Ticketsystem, das Einsendungen aus **Forms** automatisiert in **Planner** als Aufgaben anlegt, in Buckets einsortiert und die/den Anfordernde:n in **Teams** informiert. Beim **Abschluss** der Aufgabe erfolgt eine automatische Rückmeldung.

**Voraussetzungen**
- Microsoft 365 Tenant mit Zugriff auf **Forms**, **Planner (Tasks in Teams)**, **Power Automate** und **Teams**  
- Basis-Rechte zum Erstellen von Flows und Planner-Plänen  
- Optional: eine eigene **Sandbox-Gruppe** für den Planner-Plan

---

## Architektur auf einen Blick

Für das gesamte Ticketsystem benötigstst du nur 4 einfache Komponenten:

{{< figure src="/images/Ticketsystem-Architektur.webp" alt="Architekturübersicht M365 Ticketsystem" caption="Die Komponenten des Ticketsystems." >}}

- **Forms**: Ticketaufnahme (Titel, Beschreibung, Kategorie z. B. Hardware/Software, Name/E-Mail)  
- **Planner**: Plan mit Buckets (z. B. „Hardware“, „Software“) – dort landen die Tickets als Aufgaben  
- **Power Automate #1** (*When a new response is submitted – Forms*):  
  Antwort holen → Planner-Aufgabe erstellen → Details/Description setzen → E-Mail des/der Einsendenden in die Checkliste schreiben → nach Kategorie in einen Bucket einsortieren → Teams-Benachrichtigung an die Person  
- **Power Automate #2** (*When a task is completed – Planner*):  
  Auf Abschluss reagieren → Checkliste der Aufgabe auslesen (E-Mail) → Profil holen → Abschluss-Benachrichtigung an die Person in Teams

---

## Schritt 1: Microsoft Forms – Ticketformular anlegen

Die erste Komponente - Das Forms-Formular wird für die Anforderer zur Verfügung stehen, um neue Tickets anzulegen.

1. **Forms** öffnen (z. B. über <a href="https://forms.office.com/" target="_blank">forms.office.com/</a>)
2. Neues Formular, z. B. **„Ticketsystem – YouTube“**.  
3. **Fragen anlegen**
   - *Titel des Tickets* (Kurzantwort, **erforderlich**)  
   - *Beschreibung* (Langantwort, **erforderlich**)  
   - *Kategorie* (Auswahl, z. B. **Hardware**, **Software**, **erforderlich**)  
4. **Einstellungen**
   - Namen/E-Mail miterfassen (je nach Tenant/Datenschutz) → wichtig für Rückmeldung.  
5. Testen: Vorschau ausfüllen und senden.

{{< figure src="/images/Ticketsystem-Formular.webp" alt="Microsoft Forms - Formular für das M365 Ticketsystem" caption="Das fertige Formular" >}}

---

## Schritt 2: Microsoft Planner – Plan & Buckets erstellen

Der Planner bzw. der Plan in Planner wird dafür genutzt angelegte Tickets zu verwalten bzw. zu bearbeiten.

1. **Planner** öffnen (Tasks in Teams oder `office.com` → **Planner**).  
2. Neuer Plan, z. B. **„YouTube Ticketsystem“**, in passender Microsoft 365-Gruppe (z. B. **Sandbox**).  
3. **Buckets** einrichten: **Hardware**, **Software**  
4. Optional: Prioritäten, Labels/Farbkategorien vorbereiten.

{{< figure src="/images/Planner-Aufgabenplan.webp" alt="Microsoft Planner - Der Aufgabenplan für das M365 Ticketsystem" caption="Der fertige Aufgabenplan" >}}

> **Hinweis:** Buckets sind der Schlüssel fürs automatische Einsortieren.

---

## Schritt 3: Power Automate Flow #1 – Ticket anlegen & melden

Der erste Flow wird genutzt, um auf neu angelegte Tickets (über das Forms-Formular) zu reagieren. Der Flow wird Aufgaben im Planner anlegen sowie die Anforderer über die erfolgreiche Anlage informieren.

**Ziel:** Aus jeder Formulareinsendung automatisch eine Planner-Aufgabe erzeugen, Beschreibung/Metadaten setzen, E-Mail des/der Einsendenden speichern, Bucket wählen und eine **Teams**-Nachricht senden.

### 3.1 Flow anlegen
- **Automated cloud flow**  
- Trigger: **When a new response is submitted (Microsoft Forms)**  
- Parameter: **Form ID** → Ihr Ticketformular

### 3.2 Antwortdetails abrufen
- Aktion: **Get response details (Microsoft Forms)**  
  - Form Id: Ihr Formular  
  - Response Id: **Dynamic content → Response Id** des Triggers

### 3.3 Planner-Aufgabe erstellen
- Aktion: **Create a task (Planner)**  
  - **Group**: Ihre Gruppe (z. B. Sandbox)  
  - **Plan**: „YouTube Ticketsystem“  
  - **Title**: *Form-Feld „Titel des Tickets“*  
  - (Optional) **Due date/priority**

### 3.4 Aufgabendetails aktualisieren
- Aktion: **Update task details (Planner)**  
  - **Task Id**: **ID** aus „Create a task“  
  - **Description**: *Form-Feld „Beschreibung“*

### 3.5 E-Mail des/der Einsendenden in Checkliste hinterlegen
- Aktion: **Update checklist item (Planner task)**  
  - **Task Id**: aus „Create a task“  
  - **Checklist item Id**: `0`  
  - **Title**: **Responder’s Email** aus Forms (dynamischer Inhalt)  
  - **Is checked**: `false`

> **Warum Checkliste?** Sehr schlank, um die E-Mail am Ticket zu speichern und im Abschluss-Flow wiederzufinden.

### 3.6 Buckets automatisch setzen (Switch)
1. **Initialize variable**  
   - Name: `BucketId` (String)
2. **Switch** (on: *Form-Feld „Kategorie“*)  
   - **Case „Hardware“** → **Set variable `BucketId`** auf **Bucket-ID „Hardware“**  
   - **Default (Software)** → **Set variable `BucketId`** auf **Bucket-ID „Software“**

**Bucket-IDs ermitteln (einmalig):** Temporär **List buckets (Planner)** → Gruppe+Plan wählen → Ausgabe prüfen → IDs kopieren → Hilfsaktion wieder entfernen.

- **Update task (Planner)**  
  - **Task Id**: aus „Create a task“  
  - **Bucket Id**: `variables('BucketId')`

### 3.7 Teams-Benachrichtigung an Anfordernde:n (personalisieren)
- **Get user profile (Office 365 Users)**  
  - **User (UPN)**: Forms **Responder’s Email**
- **Post message in a chat or channel (Teams)** – **Chat with Flow bot**  
  - **Recipient**: Forms **Responder’s Email**  
  - **Message (Beispiel):**
    ```text
    Hallo @{outputs('Get_user_profile')?['body/givenName']},

    dein Ticket "**@{outputs('Get_response_details')?['body/<FormFieldTitle>']}**"
    wurde angelegt. Wir melden uns, sobald es abgeschlossen ist.
    ```
    *Ersetzen Sie `<FormFieldTitle>` durch den internen Namen Ihres Formularfelds (oft „Title“/„Titel_des_Tickets“).*


{{< figure src="/images/flow_neues_ticket.webp" alt="Microsoft Power Automate - Der erste Flow für das M365 Ticketsystem" caption="Der erste Flow zur Verarbeitung der Formularinformationen." >}}

---

## Schritt 4: Power Automate Flow #2 – Abschluss automatisch melden

Der zweite Flow wird auf den Abschluss einer Aufgabe reagieren und die Anforderer entsprechend über den Abschluss des Tickets informieren.

**Ziel:** Sobald eine Planner-Aufgabe **Completed** ist, wird die Person aus dem Formular in **Teams** informiert.

### 4.1 Flow anlegen
- **Automated cloud flow**  
- Trigger: **When a task is completed (Planner)**  
  - **Group**: Sandbox  
  - **Plan**: YouTube Ticketsystem

### 4.2 Aufgabendetails holen (inkl. Checkliste)
- Aktion: **Get task details (Planner)**  
  - **Task Id**: **Task Id** aus dem Trigger

### 4.3 E-Mail aus der Checkliste extrahieren
Je nach Umgebung ist `checklist` **Array** oder **Objekt**. In vielen Fällen funktioniert folgende (aus dem Video stammende) Adressierung:

```text
body('Get_task_details')?['checklist'][0]?['value']?['title']
```
Alternativ kannst du auch mittels first() das erste Element des Arrays referenzieren:

```text
first(body('Get_task_details')?['checklist'])?['value']['title']
```

### 4.4 Display-Name laden

- Get user profile (Office 365 Users)

  - User (UPN): E-Mail aus 4.3

### 4.5 Teams-Nachricht versenden

- Post message in a chat or channel (Teams) – Chat with Flow bot

  - Recipient: E-Mail aus 4.3

  - Message (Beispiel):


{{< figure src="/images/flow-abschluss-ticket.webp" alt="Microsoft Power Automate - Der zweite Flow zur Information der Anforderer nach Abschluss des Tickets" caption="Der zweite Flow zur Information der Anforderer nach Abschluss der Bearbeitung." >}}

---


## Erweiterungen & Best Practices

- Anhänge im Formular: Datei-Upload aktivieren (Speicherort/Compliance beachten); Link in Description oder Kommentar der Aufgabe speichern.

- Zuweisung nach Kategorie: Nach dem Erstellen „Assign task“ nutzen, um je Bucket feste Bearbeiter:innen zuzuweisen.

- Prioritäten & Fälligkeiten: Aus Formularfeldern übernehmen.

- Datenhaltung: E-Mail statt Checkliste z. B. in Beschreibung oder in Dataverse persistieren (skalierbar).

- Alternativ E-Mail-Benachrichtigung: „Send an email (V2)“ aus Outlook – gleiche E-Mail-Variable verwenden.

- Mehrsprachigkeit: Flows und Felder klar benennen (DE/EN) für gemischte Tenants.

- Sicherheit/Datenschutz: Nur notwendige personenbezogene Daten erfassen; Lösch-/Aufbewahrungsfristen definieren.



{{< figure
    src="/images/YouTube-Ticketsystem-Link-Image.webp"
    alt="Ticketsystem mit Microsoft 365 erstellen | Forms, Planner & Power Automate Schritt-für-Schritt"
    caption="Videotutorial zum Blogbeitrag (YouTube | externer Link)"
    link="https://www.youtube.com/watch?v=5spVT3m35a4"
    target="_blank"
    rel="external noopener nofollow"
    title="YouTube: Ticketsystem mit Microsoft 365 erstellen | Forms, Planner & Power Automate Schritt-für-Schritt"
>}}

## Fazit & Kontakt

Mit Forms + Planner + Power Automate entsteht schnell ein bewusst einfaches Ticketsystem – ideal für kleine IT-Teams, Vereine oder Fachabteilungen. Es ist jederzeit erweiterbar (Zuweisung, Priorisierung, Dataverse, Genehmigungen).

👉 Fragen oder Unterstützung beim Aufbau?
Nutzen Sie gern mein [Kontaktformular]({{<ref "/contact/">}})
 – ich helfe beim Design, bei Best Practices und bei der Skalierung auf die Power Platform.

 <script type="application/ld+json"> { "@context":"https://schema.org", "@type":"FAQPage", "mainEntity":[ { "@type":"Question", "name":"Kann ich Dateien am Ticket mitschicken?", "acceptedAnswer":{"@type":"Answer","text":"Ja. Aktivieren Sie in Microsoft Forms den Datei-Upload und verarbeiten Sie den Upload-Link in Power Automate, z. B. in der Aufgabendescription oder als Kommentar."} }, { "@type":"Question", "name":"Wie weise ich Tickets automatisch zu?", "acceptedAnswer":{"@type":"Answer","text":"Nutzen Sie im Flow einen Switch auf die Kategorie und fügen Sie nach dem Anlegen der Aufgabe eine 'Assign task'-Aktion hinzu, um je Bucket bestimmte Bearbeiter:innen zuzuweisen."} }, { "@type":"Question", "name":"Wie informiere ich per E-Mail statt Teams?", "acceptedAnswer":{"@type":"Answer","text":"Ersetzen oder ergänzen Sie die Teams-Aktion durch 'Send an email (V2)' aus Outlook und verwenden Sie die gleiche extrahierte E-Mail-Adresse."} } ] } </script>