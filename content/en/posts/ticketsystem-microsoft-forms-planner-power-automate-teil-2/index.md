---
title: "Ticketsystem mit Microsoft 365 – Teil 2: SharePoint-Referenzliste & Statusbenachrichtigungen"
date: '2025-10-14T21:13:42+02:00'
slug: "ticketsystem-microsoft-365-sharepoint-referenzliste-statusbenachrichtigungen"
description: "Zweiter Teil der Reihe zum Ticketsystem mit Microsoft 365 und Power Automate. Wir ergänzen eine SharePoint-Liste, um E-Mail des Anforderers und Statusreferenzen zu speichern – für volle Checklisten-Nutzung und automatische Status-Updates."
categories: ["Microsoft 365", "Power Automate", "SharePoint", "Tutorials"]
tags: ["Ticketsystem", "Planner", "Forms", "SharePoint-Liste", "OData", "Get items", "Create item", "Power Automate Flow", "User Profile (V2)"]
keywords: ["Ticketsystem Microsoft 365", "Power Automate", "SharePoint Referenzliste", "Planner", "Microsoft Forms", "Statusbenachrichtigungen", "OData Filter"]
draft: true
cover:
  image: "/images/Ticketsystem_Part2_Cover.webp"
  alt: "Coverbild für Ticketsystem-Serie – Teil 2"
  caption: "Tutorial zur Erstellung eines einfachen Ticketsystems mit Microsoft 365 und Power Automate - Teil 2"
---

> **Hinweis**: Du liest hier menschgemachten Content. Die Funktion der hier beschriebenen Logik wurde getestet und entstammt keiner "KI-Phantasie". Ich hoffe du findest hier Erkenntnis und Mehrwert für dich oder dein Unternehmen. Viel Freude beim Lesen.



> **Kurzfassung:** Zweiter Teil der Reihe zum Ticketsystem mit Microsoft 265 und Power Automate. Den ersten Teil findest du hier: [Einfaches Ticketsystem mit Microsoft Forms, Planner & Power Automate – Schritt-für-Schritt zur schnellen Ticketlösung in Microsoft 365]({{< ref "ticketsystem-microsoft-forms-planner-power-automate" >}})



# Ausgangssituation und Zielbild
Im ersten Teil dieser Reihe wuede ein kleines Ticketsystem mittels Microsoft Forms und Microsoft Planner erstellt. Die Logik wurde in Power Automate ergänzt. Um die Kommunikation mit den Anforderern sicherzustellen wurde die übermittelte E-Mail Adresse im ersten Checklisten-Element der Planner-Aufgabe gespeichert.

Im zweiten Teil wird nun eine kleine Sharepoint-Liste ergänzt. Diese hat zum Zweck die Anforderer-E-Mail sowie einen Referenzstatus zu speichern. Damit werden zwei neue Features ermöglicht:
- Die Checkliste kann in vollem Umfang genutzt werden.
- Statusänderungen können erkannt werden. Anforderer können so über Änderungen am Ticketstatus informiert werden. Z.B. "das Ticket ist nun in Bearbeitung".


# Die Sharpoint-Liste

Um eine Sharepoint-Liste zu erstellen wechseln Sie auf eine geeignete Sharepoint-Seite (z.B.: [office.com]({{< ref "http://office.com" >}})) / Apps / Sharepoint / <<Eine Ihrer SP-Seiten>>. Hier finden Sie unter Webseiteninhalte die Möglichkeit eine neue Liste zu erstellen.

Für dieses Beispiel habe ch eine Liste "Planner-Ticketsystem-Referenz" mit folgenden Spalten erstellt:
- Titel (Default-Titel. Wird systemseitig mit der Liste erstellt)
- E-Mail (Text)
- Statusreferenz (Text)

{{< figure src="/images/Sharepoint-Liste Planner-Ticketsystem-Referenz.webp" alt="Sharepoint-Liste Sharepoint-Liste Planner-Ticketsystem-Referenz" caption="Spalten der Sharepoint-Liste." >}}

# Anpassung Power Automate Flow "YT_Ticketsystem_neues_Ticket"
Im letzten Teil wurde der Flow "YT_Ticketsystem_neues_Ticket" erstellt. Dieser wird nun ergänzt, um E-Mail (der Anforderer) sowie den letzten bekannten Status in die Referenzliste zu schreiben.

Hierfür sinc folgende Tätigkeiten notwendig:
1. Löschen der Aktion "Update task detail" und
2. Ergänzen einer Aufgabe "Create Item" um die Referenzzeile in die SP-Liste zu schreiben


## Aktion Create item
Um die Neue Aktion anzulegen Suche den Connector "Sharepoint" und die Aktion "Create item" (deutsch: Element ersellen).

Wählen Sie folgendes in der Aktion aus
- Site Address: Adresse deine Sharpont-Seite (Drop-Down)
- List Name: Die neu erstellte Liste
- Titel: Die id der neu erstellten Planner-Aufgabe (Aus Aktion "Create a Task").
- E-Mail: Die E-Mail des übermittelnden Benutzers (Responders E-Mail (aus dem Trigger))

Die fertige Aufgabe sollte so aussehen:

{{< figure src="/images/Action Create item.webp" alt="Aktion Create item" caption="Die neue Aktion 'Create item'" >}}

Schematisch sieht das ganze nun so aus:
{{< figure src="/images/Schema Anlage Ticket.webp" alt="Anlageschema" caption="Die Anlage eines neuen Tickets" >}}

1. Das Foms-Formular wird übermittelt und Triggert den PA-Flow
2. Der Flow legt die Planner-Aufgabe als auch das SP-Listenelement an. Das SP-Listenelement enthält eine Referenz auf die Planner-Aufgabe.

Ein erster Eintrag in der Sp-Liste:

{{< figure src="/images/Eintrag in der SP-Liste.webp" alt="Eintrag in der SP-Liste" caption="Ein erster Eintrag in der SP-Liste. Die Statusreferenz unbekannt ist so gewollt um einabweichen vom eigentlichen Status zu erkennen">}}

# Anpassung Flow "YT Ticketsystem_Abschluss"
Um im Rahmen des Abschlusses des Tickets (im Planner) an die Anforderer zu kommunizieren muss noch der Flow "YT Ticketsystem_Abschluss" angepasst werden:

1. Ergänze eine Aktion "Get items"
2. Referenziere für die Empfänger-E-Mail (Teams-Nachricht) das erste Element aus Get items

## Aktion Get items

Get items fragt die SP-Listenelemente aus der neu erstellten Liste ab. Um nur das eine relevante Listenelement zurückzubekommen muss ein OData Query-Filter ergänzt werden:

Der OData-Filter:

```òdata
Title eq '@{outputs('Get_task_details')?['body/id']}'
```

{{< figure src="/images/Aktion Get items.webp" alt="Aktion Get items" caption="Die neue Aktion 'get items'" >}}


## Aktion "Get user profile (V2)"
Die o.g. Aktion ruft den anforderndern Benutzer im Azur AD ab. Die Ermittelten Informationen (Anredename und E-Mail) werden darauf folgend genutzt, um eine Information an den anfordernden Nutzer zu senden.

Um hier nun die E-Mail aus der Sharepoint-Liste zu referenzieren gib in der Aktion (Feld User (UPN)) folgenden Ausdruck ein:

```
body('Get_items')?['value'][0]['E_x002d_Mail']
```

Der Ausdruck referenziert das erste Element [0] aus dem Array 'value' im body der Aktion get items.

Eingabe des Ausdrucks:

{{< figure src="/images/Ausdruck für Get user profile.webp" alt="Ausdruck für die E-Mail" caption="Ausdruck zur Ermittlung der User-E-Mail ">}}

# Zusammenfassung
Der zweite Teil der Serie zur erstellung eines einfachen Ticketsystems mit Microsoft 365 und Power Automate hat die Komponente Sharpoint bzw. eine Sharepoint-Liste ergänzt. Folgende Features werden damit unterstützt:
- Die Checkliste in der Planner-Aufgabe kann wieder vollumfänglich genutzt werden.
- Die Voraussetzung zur Überwachung der Statusänderung (z.B. wechsel von neues Ticket auf Ticket in Bearbeitung) ist gegeben.

# Ausblick
Im dritten Teil dieser Reihe wird die erwähnte Statusüberwachung implementiert. Damit können Anwender über Aktionen am Ticket (z.B. Ticket ist nun in Bearbeitung, es gibt Rückfragen zum Ticket, etc.) informiert werden.







