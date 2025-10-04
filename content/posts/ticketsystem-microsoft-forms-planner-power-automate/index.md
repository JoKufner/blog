---
title: "Einfaches Ticketsystem mit Microsoft Forms, Planner & Power Automate – Schritt-für-Schritt zur schnellen Ticketlösung in Microsoft 365"
date: 2025-10-04T09:00:00+02:00
draft: true
slug: "ticketsystem-microsoft-forms-planner-power-automate"
description: "Bauen Sie in < 60 Minuten ein schlankes Ticketsystem auf Basis von Microsoft 365: Formular in Forms, Aufgaben in Planner, Automatisierung mit Power Automate – inkl. Benachrichtigungen in Teams und Abschluss-Workflow. Anleitung mit Ausdrücken & Best Practices."
categories: ["Power Platform", "Microsoft 365", "Tutorials"]
tags: ["Power Platform", "Microsoft 365", "Power Automate", "Microsoft Forms", "Microsoft Planner", "Ticketsystem", "IT-Support", "Teams", "Automatisierung", "Low-Code", "Workflow", "Tutorial", "Best Practices"]
keywords: ["ticketsystem microsoft 365","ticketsystem forms planner power automate","power automate planner aufgabe erstellen","forms response planner task","teams benachrichtigung power automate","checklist email planner auslesen","einfaches ticketsystem ohne programmierung","low code ticketsystem microsoft"]
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

- **Forms**: Ticketaufnahme (Titel, Beschreibung, Kategorie z. B. Hardware/Software, Name/E-Mail)  
- **Planner**: Plan mit Buckets (z. B. „Hardware“, „Software“) – dort landen die Tickets als Aufgaben  
- **Power Automate #1** (*When a new response is submitted – Forms*):  
  Antwort holen → Planner-Aufgabe erstellen → Details/Description setzen → E-Mail des/der Einsendenden in die Checkliste schreiben → nach Kategorie in einen Bucket einsortieren → Teams-Benachrichtigung an die Person  
- **Power Automate #2** (*When a task is completed – Planner*):  
  Auf Abschluss reagieren → Checkliste der Aufgabe auslesen (E-Mail) → Profil holen → Abschluss-Benachrichtigung an die Person in Teams

---

## Schritt 1: Microsoft Forms – Ticketformular anlegen

1. **Forms** öffnen (z. B. über `office.com` → **Forms**).  
2. Neues Formular, z. B. **„Ticketsystem – YouTube“**.  
3. **Fragen anlegen**
   - *Titel des Tickets* (Kurzantwort, **erforderlich**)  
   - *Beschreibung* (Langantwort, **erforderlich**)  
   - *Kategorie* (Auswahl, z. B. **Hardware**, **Software**, **erforderlich**)  
4. **Einstellungen**
   - Namen/E-Mail miterfassen (je nach Tenant/Datenschutz) → wichtig für Rückmeldung.  
5. Testen: Vorschau ausfüllen und senden.

> **SEO-Tipp:** Nutzen Sie klare Feldnamen („IT-Ticket Titel“, „Ticketbeschreibung“, „Kategorie (Hardware/Software)“) – gut für Screenshots und interne Suche.

---

## Schritt 2: Microsoft Planner – Plan & Buckets erstellen

1. **Planner** öffnen (Tasks in Teams oder `office.com` → **Planner**).  
2. Neuer Plan, z. B. **„YouTube Ticketsystem“**, in passender Microsoft 365-Gruppe (z. B. **Sandbox**).  
3. **Buckets** einrichten: **Hardware**, **Software**  
4. Optional: Prioritäten, Labels/Farbkategorien vorbereiten.

> **Hinweis:** Buckets sind der Schlüssel fürs automatische Einsortieren.

---

## Schritt 3: Power Automate Flow #1 – Ticket anlegen & melden

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

---

## Schritt 4: Power Automate Flow #2 – Abschluss automatisch melden

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
