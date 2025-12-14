---
title: "First-Level-Support-Agent mit Microsoft Copilot Studio – KI-gestützte Ticketbearbeitung in Microsoft 365"
date: 2025-12-14T14:00:00+02:00
draft: false
slug: "first-level-support-agent-microsoft-copilot-studio-ticketsystem"
description: "Erstelle einen autonomen First-Level-Support-Agenten mit Microsoft Copilot Studio und integriere ihn in ein Ticketsystem aus SharePoint, Power Apps und Power Automate. Der Agent beantwortet Standardfragen, nutzt eine definierte Wissensbasis und übergibt komplexe Fälle automatisch an menschliche Kollegen."
categories: ["Power Platform", "Microsoft 365", "KI & Automatisierung", "Tutorials"]
tags: ["Microsoft Copilot Studio", "Power Automate", "Power Apps", "SharePoint", "KI-Agent", "Ticketsystem", "First Level Support", "Automation"]
keywords:
  [
    "first level support agent",
    "microsoft copilot studio agent",
    "ki ticketsystem microsoft 365",
    "power automate ki agent",
    "support agent power platform",
    "copilot studio tutorial",
    "ki support workflow",
    "autonomer support agent"
  ]
cover:
  image: "/images/first-level-support-agent-cover.webp"
  alt: "Autonomer First-Level-Support-Agent mit Microsoft Copilot Studio."
  caption: "KI-gestützter Support-Agent integriert in ein Microsoft-365-Ticketsystem."
  relative: true
translationKey: "first-level-support-agent-microsoft-copilot-studio"
---

# First-Level-Support-Agent mit Microsoft Copilot Studio

In diesem Beitrag zeige ich dir, wie du einen autonomen First-Level-Support-Agenten mit Microsoft Copilot Studio erstellst und ihn in ein Ticketsystem auf Basis von SharePoint, Power Apps und Power Automate integrierst.

Der Agent arbeitet ausschließlich mit einer definierten Wissensbasis, beantwortet wiederkehrende Support-Fragen automatisiert und übergibt komplexe oder nicht beantwortbare Anfragen zuverlässig an menschliche Kollegen.


---

# Warum ein autonomer First-Level-Support-Agent?

In vielen Unternehmen erreichen Support-Teams täglich identische oder sehr ähnliche Anfragen, zum Beispiel:

- erste Schritte mit Anwendungen  
- Finden und Öffnen von Apps  
- neue Funktionen und Preview-Features  
- Fragen zu Dataverse  
- typische Fehlermeldungen  

Ein autonomer First-Level-Support-Agent übernimmt genau diese Erstberatung:

- schnelle Antworten rund um die Uhr  
- konsistente Qualität  
- deutliche Entlastung der Support-Teams  

Wichtig dabei:  
Der Agent antwortet **ausschließlich innerhalb seiner Wissensbasis**. Kann eine Frage nicht beantwortet werden, wird sie gezielt an einen menschlichen Kollegen übergeben. Es findet kein Phantasieren statt.

---

# Architektur der Lösung

Die Lösung besteht aus folgenden Komponenten:

- Microsoft Copilot Studio (Support-Agent)
- Wissensbasis (z. B. Microsoft Learn und interne Quellen)
- SharePoint-Liste als Ticketsystem
- Power App als Benutzeroberfläche
- Power Automate Flow zur Prozesssteuerung



{{< figure src="/images/first-level-support-agent-architektur.webp" alt="Lösungsarchitektur" caption="Die Archtiektur bestehend aus  fünf Komponenten." >}}

---

# Support-Agent in Microsoft Copilot Studio erstellen

Wir starten im Microsoft Copilot Studio unter copilotstudio.microsoft.com.

Klicke auf **Erstellen** und anschließend auf **Neuer Agent**, um einen neuen Support-Agenten anzulegen.

---

## Eigenschaften des Agenten definieren

Im ersten Schritt fragt Copilot Studio nach den Eigenschaften des Agenten.  
Hier definieren wir das Verhalten vollständig über einen Prompt in natürlicher Sprache.

Der Agent soll nicht frei antworten, sondern immer ein strukturiertes JSON-Objekt zurückgeben. Dieses Design ermöglicht später eine einfache Verarbeitung in Power Automate.

Der verwendete Prompt lautet:

Handle als First-Level-Experte für die Microsoft Power Platform und biete freundlichen sowie professionellen Support. Beantworte Anfragen ausschließlich in Form eines JSON-Objekts mit den Attributen "Erfolg" (true, wenn eine Antwort gefunden wurde, andernfalls false) und "Antwort" (die gefundene Antwort oder ein leerer String). Unterstütze ausschließlich Themen rund um Getting Started, das Suchen und Ausführen von Apps, neue Funktionen und Preview-Erfahrungen, Pläne, Canvas Apps, modellgesteuerte Apps, die mobile Power Apps App, Dataverse, Ressourcen, Troubleshooting und Responsible AI. Beantworte keine Fragen außerhalb dieser Themen und verwende ausschließlich die deutsche Sprache. Füge niemals Informationen hinzu, die nicht im JSON-Objekt enthalten sind. Kann eine Frage nicht anhand der Wissensbasis beantwortet werden, setze "Erfolg": false und "Antwort": "".

---

## Agent benennen

Im nächsten Schritt vergeben wir einen Namen für den Agenten.

Beispiel:  
FirstLevelSupportAgent

---

## Verhalten des Agenten

Der Agent hat eine klare Aufgabe:

- prüfen, ob eine Antwort in der Wissensbasis existiert  
- wenn ja, ein JSON-Objekt mit Erfolg = true und der Antwort zurückgeben  
- wenn nein, ein JSON-Objekt mit Erfolg = false zurückgeben  

Weitere Topics oder Verhaltensvarianten sind möglich, werden hier aber bewusst nicht genutzt.

---

## Wissensbasis definieren

Als Wissensbasis hinterlegen wir offizielle Dokumentation rund um die Microsoft Power Platform.

Quelle:  
https://learn.microsoft.com/de-de/power-platform/

Zusätzlich können später interne Dokumente, Wikis oder weitere Quellen ergänzt werden:


{{< figure src="/images/copilot-studio-wissensbasis.webp" alt="Wissensquellen für den Copilot Agenten" caption="Der zweite Flow zur Information der Anforderer nach Abschluss der Bearbeitung." >}}

---

## Test des Agenten

Beispiel einer erfolgreichen Anfrage:  
Wie kann ich eine Canvas-App anlegen?

Der Agent gibt ein JSON-Objekt mit Erfolg = true und einer passenden Antwort zurück.

Beispiel einer nicht unterstützten Anfrage:  
Wie kann ich in Camunda einen Workflow beschreiben?

Der Agent gibt Erfolg = false zurück. Diese Information nutzen wir später zur Übergabe an einen menschlichen Bearbeiter.

{{< figure src="/images/copilot-studio-agent-test.webp" alt="Test des Agentenverhaltens" caption="Der Agent gibt ein strukturiertes JSON-Objekt zurück." >}}

---

# Integration in das Ticketsystem

Der Support-Agent wird nun in ein bestehendes Ticketsystem integriert. Dieses wird im Blog ([Sharepoint Ticketsystem]({{< ref "ticketsystem-sharepoint-powerapps-powerautomate" >}})) bzw. auf YouTube (<a href='https://www.youtube.com/watch?v=naz1TnPs7NY'>Ticketsystem mit SharePoint & Power Automate | Komplettes Tutorial Schritt für Schritt</a>) beschrieben. 

Das Ticketsystem besteht aus:

- einer zentralen SharePoint-Liste  
- einer Power App zur Ticketanlage  
- einem Power Automate Flow zur Statusverarbeitung  

Wird ein Ticket neu angelegt oder der Status geändert, verarbeitet der Flow das Ticket automatisch.

---

## Anpassung des Power-Automate-Flows

Der KI-Agent soll nur aktiv werden, wenn ein Ticket neu angelegt wurde.

Dazu prüfen wir am Ende des bestehenden Flows, ob der Status des Tickets gleich „Neu“ ist.

Die Übersicht des Flows zeigt alle Aktionen, die in weiter unten kurz erläutert werden:

{{< figure src="/images/ticketsystem-flow-anpassung-fuer-ai-support-agent.webp" alt="Angepasster Flow" caption="Der für den KI-Agenten angapasste Flow. Die Änderungen sind gelb markiert" >}}




---

## Agent ausführen und auf Antwort warten

Ist das Ticket neu, wird die Aktion „Execute Agent and wait“ ausgeführt.

Diese Aktion ruft den Support-Agenten auf und wartet auf dessen Antwort.  
Die Rückgabe ist ein String, der ein JSON-Objekt beschreibt.

---

## JSON-Antwort verarbeiten

Im nächsten Schritt wandeln wir den String in ein echtes JSON-Objekt um.

Dazu verwenden wir in einer Compose-Aktion folgenden Ausdruck:

```WDL
json(body('Execute_Agent_and_wait')?['lastResponse'])
```

Ab diesem Zeitpunkt können wir gezielt auf die Inhalte zugreifen.

---

## Entscheidung auf Basis der Agent-Antwort

Prüfung, ob der Agent eine Antwort gefunden hat:
```WDL
outputs('Compose_lastResponse')?['Erfolg']
```
Zugriff auf die eigentliche Antwort:
```WDL
outputs('Compose_lastResponse')?['Antwort']
```
---

## Ticket automatisch aktualisieren

Hat der Agent eine Lösung gefunden:

- die Antwort wird in das SharePoint-Ticket geschrieben  
- Status und Referenzstatus werden aktualisiert  
- der Anforderer wird per E-Mail informiert  

Wichtig:  
Der Referenzstatus wird am Ende immer auf den aktuellen Status gesetzt. So wird verhindert, dass der Flow erneut startet und eine Endlosschleife entsteht.


{{< figure src="/images/ai_supportagent_referenzstatus_status_gleichsetzen.webp" alt="Gleichgeschaltener Referenzstatus" caption="Referenzstatus muss in diesem Flow zum Abschluss des Flows dem Status gleichgesetzt werden. So wird eine Dauerschleife vermieden." >}}



---

# Fazit

Mit Microsoft Copilot Studio lassen sich mit überschaubarem Aufwand leistungsfähige First-Level-Support-Agenten erstellen. In Kombination mit Power Automate können diese Agenten direkt in bestehende Geschäftsprozesse integriert werden.

Das Ergebnis:

- geringerer Supportaufwand  
- schnellere Reaktionszeiten  
- kontrollierte, nachvollziehbare KI-Nutzung  

---

# YouTube

Zum Blogbeitrag gibt es ein entsprechenden YouTube-Beitrag. Mit dem Laden des YouTube Videos werden ggf. Personenbezogene Daten von YouTube verarbeitet. Mit dem Klick auf "Video laden" akzeptierst du das. Vgl. auch [Datenschutz]({{< ref "datenschutz.md" >}})

{{< confirmed_youtube id="jvELUdB6akY" >}}

---

Vielen Dank fürs Lesen.  
Wenn du Fragen oder Anregungen hast, melde dich gerne.
