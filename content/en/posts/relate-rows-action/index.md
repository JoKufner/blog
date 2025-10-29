---
title: "Relate Rows in Power Automate – Easily Link Dataverse Rows"
slug: "relate-rows-power-automate"
date: "2025-10-29T10:00:00+01:00"
description: "Learn how to correctly link Dataverse rows using the Power Automate 'Relate rows' action – explained step by step with an example of songs and albums."
draft: true
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
  - dataverse relate rows example
  - dataverse link rows
  - power automate dataverse lookup
  - relate rows explanation
  - power automate tutorial dataverse
translationKey: "relate-rows-power-automate"
cover:
  image: "/images/relate-rows-cover.webp"
  alt: "Ticket system built with Microsoft 365 and Power Automate."
  caption: "Tutorial for creating a simple ticket system with Microsoft 365 and Power Automate"
  relative: true
author: "Jonas Kufner"
---

## The Example

I want to demonstrate how **Relate Rows** works with a small example:

There are two tables: **Albums** and **Songs**, where *Songs* has a lookup to the *Albums* table.

{{< figure src="/images/album-song-relation.webp" alt="Microsoft Planner - Der Aufgabenplan für das M365 Ticketsystem" caption="The relationship between Album and Song" >}}

## The Flow

{{< figure src="/images/relate-rows-flow.webp" alt="Flow to link Album and Song" caption="The flow linking Album and Song" >}}

In the flow, the album and then the song are first loaded using their respective IDs.

After that, the link is created using the **Relate rows** action.

### Action: Relate Rows

The **Relate Rows** action has three parameters:

- **Table name:** Select the *independent* entity here — in our example, *Album*.  
- **Row ID:** Here, choose the ID of the row from the first table. The ID (or unique identifier) is usually named after the table. For example: *Album* (unique identifier). In the background, it’s exactly the Row ID shown above (“c44db2ac...b1b1”).  
- **Relationship:** Choose the relationship that was automatically created when the lookup column was added. Example: *Songs - jk_songs_Album_jk_album* (“jk” refers to the publisher in my development environment).  
- **Relate with:** Enter the **OData Id** (not the Id) of the dependent entity (in this example: *Songs*).  

With this approach, the linking works reliably. Important points to remember:

- Always select the *independent entity first* (for a 1:n relationship, that’s the “1”).  
- For **Row ID**, use the *unique identifier* of the independent entity.  
- For **Relate with**, use the **OData Id**, **not** the unique identifier.
