---
title: "Digitale Urlaubsplanung mit SharePoint, Power Apps & Power Automate – kompletter Genehmigungsprozess Schritt für Schritt"
date: 2025-01-15T09:00:00+02:00
draft: false
slug: "digitale-urlaubsplanung-sharepoint-powerapps-genehmigungsprozess"
description: "Erstelle eine vollständige digitale Urlaubsplanung inklusive Genehmigungsprozess mit SharePoint, Power Apps und Power Automate. Mit Urlaubsübersicht, Berechnung der Urlaubstage, Kalenderansichten und automatisierter Freigabe – ideal für IT-Abteilungen und Geschäftsführer."
categories: ["Power Platform", "Microsoft 365", "Tutorials"]
tags: ["Power Apps", "Power Automate", "SharePoint", "Urlaubsplanung", "Genehmigungsprozess", "Genehmigung", "Workflow", "Microsoft 365", "Business Apps"]
keywords:
  [
    "digitale urlaubsplanung sharepoint",
    "power apps urlaubsplanung",
    "power automate urlaubsworkflow",
    "urlaubsantrag genehmigungsprozess microsoft 365",
    "sharepoint urlaubsplanung vorlage",
    "urlaubsworkflow power automate tutorial",
    "urlaub berechnung power automate",
    "urlaubskalender sharepoint",
    "microsoft 365 urlaubsantrag"
  ]
cover:
  image: "/images/blogBanner.webp"
  alt: "Digitale Urlaubsplanung mit Genehmigungsprozess in SharePoint, Power Apps und Power Automate."
  caption: "Kompletter Genehmigungsprozess für Urlaubsanträge in Microsoft 365 mit Power Apps und Automatisierung."
  relative: true
translationKey: "digitale-urlaubsplanung-sharepoint-powerapps-genehmigungsprozess"
---

# Digitale Urlaubsplanung mit Genehmigungsprozess – effizient, transparent und ohne Zusatzlizenzen

Wenn die Urlaubsplanung in deinem Unternehmen noch in Excel oder auf Papier erledigt wird, ist jetzt der ideale Zeitpunkt für eine moderne und digitale Lösung. In diesem Beitrag zeige ich dir Schritt für Schritt, wie du eine komplette Urlaubsplanung inklusive Genehmigungsworkflow mit SharePoint, Power Apps und Power Automate aufbaust.

Das Beste:  
Die fertige Lösung kannst du später als Download über meinen Blog beziehen (Bereich Downloads).

Diese Lösung eignet sich besonders für IT-Abteilungen, HR-Teams und Geschäftsführer, die eine strukturierte, nachvollziehbare und skalierbare Urlaubsverwaltung benötigen.

---

# Komponenten der Gesamtlösung

Die Lösung besteht aus drei Bausteinen:

1. SharePoint-Listen als Datenmodell  
2. Power App als Benutzerschnittstelle  
3. Power Automate Flow für Berechnung und Genehmigungsworkflow


---

# SharePoint-Listen

## 1. Liste „Urlaub“ (Mitarbeiterübersicht)

Diese Liste verwaltet:

- Mitarbeiter  
- Vertragliche Urlaubstage  
- Geplanter Urlaub  
- Genehmigter Urlaub  

**Felder:**

- Mitarbeiter (Person – eindeutige Werte empfohlen)  
- Arbeitstage (Zahl)


{{< figure src="/images/urlaubsplanung-sharepoint-liste-urlaub.webp" alt="Liste Urlaub" caption="Die SharPoint Liste Urlaub'" >}}

---

## 2. Liste „Urlaubsplanung“ (Anträge)

In dieser Liste werden die einzelnen Urlaubsanträge gespeichert.

**Felder:**

- Title  
- Beginn  
- Ende  
- Optional: Status  


{{< figure src="/images/urlaubsplanung.webp" alt="Liste Urlaubsplanung" caption="Die SharPoint Liste Urlaubsplanung'" >}}

---

# Power App erstellen

Die App wird direkt aus der SharePoint-Liste generiert.

**Menü:**  
Integrate → Power Apps → Create an app


{{< figure src="/images/urlaubsplanung-powerapp-erstellen.webp" alt="Power App aus Sharepoint Liste erstellen" caption="Die Power App direkt aus der Sharpoint Liste erstellen'" >}}

---

# Anpassungen an der Power App

## 1. Standard-Status „beantragt“

In der Status-Dropdown-Steuerung wird das DefaultSelectedItems-Property gesetzt auf:

```powerfx
[ { Value: "beantragt" } ]
```
---

## 2. Mitarbeiterfeld automatisch füllen

Für das Mitarbeiterfeld wird ein Benutzerobjekt als Default gesetzt:

```json
{
  '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
  Claims: "i:0#.f|membership|" & User().Email,
  DisplayName: User().FullName,
  Email: User().Email
}
```

{{< figure src="/images/urlaubsplanung-powerapp-mitarbeiter-default.webp" alt="Default User Objekt" caption="User Objekt in DefaultSelectedItems'" >}}

---

## 3. Automatischer Titel

Beispiel:
```powerfx
"Urlaub " & User().FullName
```
---

## 4. Anhänge entfernen

Das Feld „Attachments“ wird vollständig aus dem Formular entfernt.

---

## 5. Nicht benötigte Felder ausblenden

Über das Visible-Property können Felder ausgeblendet werden, die beim Stellen eines Urlaubsantrags nicht gebraucht werden.

---

## 6. Status im Browse Screen anzeigen

In der Gallery kann ein zusätzliches Textfeld eingefügt werden, das zeigt:
```powerfx
ThisItem.Status.Value
```

{{< figure src="/images/urlaubsplanung-powerapp-gallery-status.webp" alt="Neues Textfeld" caption="Neues Textfeld Status in der Browse Gallery'" >}}

---

# Power Automate Flow

Der Flow übernimmt:

1. Berechnung der Urlaubstage  
2. Genehmigungsprozess über den Manager  
3. Aktualisierung der Urlaubsliste  


{{< figure src="/images/urlaubsplanung-flow-uebersicht.webp" alt="Flow zur Urlaubsfreigabe" caption="Power Automate Flow zur Urlaubsplanung und -freigabe'" >}}

---

## Trigger

Der Flow wird ausgelöst durch:  
"When an item is created" in der Liste Urlaubsplanung.

---

## Schritt 1: Mitarbeiterdaten abrufen

Die passende Zeile aus der Urlaub-Liste wird mittels OData Query gefiltert:

Mitarbeiter/Email eq '@{triggerOutputs()?['body/Author/Email']}'


{{< figure src="/images/urlaubsplanung-flow-getitem.webp" alt="Aktion Get Mitarbeiterurlaub" caption="Aktion zum Abrufen der Mitarbeiter Urlaubstage'" >}}

---

## Schritt 2: Mitarbeiterobjekt in Variable speichern

Die gefundene Zeile wird in einer Objekt-Variable abgelegt, um später einfacher darauf zuzugreifen.

---

## Schritt 3: Anzahl der Urlaubstage berechnen

Berechnung der Anzahl der Urlaubstage:

div( sub( ticks(outputs('Begin')), ticks(outputs('Ende')) ), 864000000000 )


{{< figure src="/images/urlaubsplanung-flow-compose-urlaubstage.webp" alt="Aktion Compose Urlaubstage" caption="Berechnung der Urlaubstage zwischen Start- und Endzeitpunkt'" >}}

---

## Schritt 4: Geplanten Urlaub aktualisieren

Der neue geplante Urlaub ist:

add( variables('MitarbeiterObjekt')?['geplanterUrlaub'], outputs('Compose_Urlaubstage') )

---

## Schritt 5: Manager ermitteln

Über die Aktion „Get Manager (V2)“ wird der Manager des Antragstellers abgefragt.

---

## Schritt 6: Genehmigungsanforderung senden

Über „Start and wait for an approval“ wird der Vorgesetzte informiert.

Ergebnisprüfung:

@if(equals(outputs('Approval')?['outcome'], 'Approve'), true, false)


{{< figure src="/images/urlaubsplanung-flow-approval.webp" alt="Aktion Start and wait for an approval" caption="Aktion zum einholen der Urlaubsfreigabe'" >}}

---

## Schritt 7: SharePoint aktualisieren (bei Genehmigung)

Je nach Approval:

**Bei Genehmigung:**

- Status → genehmigt  
- Geplanter Urlaub wird reduziert  
- Genehmigter Urlaub erhöht  
- Resturlaub wird neu berechnet  

**Bei Ablehnung:**

- Status → abgelehnt  

---

# SharePoint Kalenderansicht

Für die bestmögliche Übersicht richtest du eine Kalenderansicht ein.

Einstellungen:

- Startdatum: Beginn  
- Enddatum: Ende  
- Untertitel: Status  


{{< figure src="/images/urlaubsplanung-sharepoint-kalender.webp" alt="Kalendersicht Urlaubsübersicht" caption="Neue Kalenderübersicht für geplante und freigegebene Urlaubstage'" >}}

---

# Farbliche Formatierung

Unter „Format current view“ kann eine visuelle Formatierung ergänzt werden:

- beantragt → gelb  
- genehmigt → grün  
- abgelehnt → rot  

---

# Tests & sinnvolle Erweiterungen

Weiterführende Optimierungsmöglichkeiten:

- Berechtigungen der SharePoint-Listen absichern  
- Automatisches Herausrechnen von Wochenenden und Feiertagen  
- Integration in HR-/Lohnabrechnungssystem  
- Berücksichtigung individueller Arbeitszeitmodelle  

---

# ⬇Download der fertigen Lösung

Die fertige Import-Lösung findest du unter:

jonaskufner.com → Downloads → Urlaubsplanung

Der Download verweist auf das zugehörige GitHub-Repository.

---

# Danke fürs Lesen!

Bei Fragen zur Umsetzung oder bei Bedarf nach Unterstützung in Power Platform Projekten melde dich gerne.
 

{{< confirmed_youtube id="FkT7il9dYpg" >}}


