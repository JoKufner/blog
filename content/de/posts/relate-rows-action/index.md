---
title: "Relate Rows in Power Automate – Dataverse-Zeilen einfach verknüpfen"
slug: "relate-rows-power-automate"
date: "2025-10-29T10:00:00+01:00"
description: "Lerne, wie du mit der Power Automate-Aktion 'Relate rows' Dataverse-Zeilen korrekt verknüpfst – Schritt-für-Schritt erklärt am Beispiel von Songs und Alben."
draft: false
categories:
  - Power Platform
  - Microsoft Dataverse
  - Power Automate
tags:
  - Power Platform
  - Power Automate
  - Dataverse
  - Relate Rows
  - Low-Code
  - Tutorial
  - Microsoft 365
keywords:
  - relate rows power automate
  - dataverse relate rows beispiel
  - dataverse zeilen verknüpfen
  - power automate dataverse lookup
  - relate rows erklärung
  - power automate tutorial dataverse
translationKey: "relate-rows-power-automate"
cover:
  image: "/images/relate-rows-cover.webp"
  alt: "Ticketsystem mit Microsoft 365 und Power Automate selbst erstellen."
  caption: "Tutorial zur Erstellung eines einfachen Ticketsystems mit Microsoft 365 und Power Automate"
  relative: true
author: "Jonas Kufner"
---


## Das Beispiel

> Die gewöhnungsbedürftige plurale Schreibweise "Albums" ist dem englischen Plural von Album geschuldet. Ich bitte dies zu entschuldigen. Gemeint sind natürlich Alben.

Ich möchte die Funktion von Relate Rows an einem kleinen Beispiel aufzeigen:

Es gibt zwei Tabellen Alben (bzw. "Albums" Vgl. Hinweis oben) und "Songs", wobei Songs einen Lookup auf die Tabelle Albums hat:

{{< figure src="/images/album-song-relation.webp" alt="Microsoft Planner - Der Aufgabenplan für das M365 Ticketsystem" caption="Die Relation zwischen Album und Song" >}}


## Der Flow

{{< figure src="/images/relate-rows-flow.webp" alt="Der Flow zum Verknüpfen von Album und Song" caption="Der Flow zum Verknüpfen von Album und Song" >}}

Im Flow werden erst das Album und dann der Song mit Hilfe der entsprechenden ID geladen.

Im Anschluss wird die Verknüpfung mit der Aktion "Relate rows" erstellt.

### Aktion Relate Rows

Relate Rows hat 3 Parameter:

 - Table name: Wähle hier die unabhängige Entität aus. Also in unserem Beispiel Album. 
 - Row-ID: Hier ist die ID der Zeile der ersten Tabelle zu wählen. Die ID (oder eindeutiger Bezeichner) ist i.d.R. wie die Tabelle benannt. Um das am Beispiel fest zu machen: Album (eingdeutiger Bezeichner). Im Hintergrund ist das exakt die Row-ID wie oben zu sehen ("c44db2ac...b1b1")
 - Relationship: Wähle hier die angelegte Relationship, welche mit der Anlage der Lookup-Spalte automatisch erstellt wurde. Beispiel: Songs - jk_songs_Album_jk_album ("jk" bezieht sich auf den Publisher in meiner Entwicklungsumgebung)
 - Relate with: Hier ist die <b>OData Id</b> (nicht die Id) der abhängigen Entität (Beispiel: Songs) zu wählen.

Mit diesem Vorgehen klappt die Verknüpfung zuverlässig. Wichtig ist:
 - Wähle als erstes die Unabhängige Entität (Bei 1:n-Relation die 1)
 - Wähle als RowID den eindeutigen Bezeichner der unabgängigen Entität
 - Wähle bei Relate with <b>nicht den eindeutigen Bezeichner</b>, <b>sondern die OData Id</b>





