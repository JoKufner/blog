---
title: "Digital Vacation Planning with SharePoint, Power Apps & Power Automate – Complete Approval Process Step by Step"
date: 2025-11-20T09:00:00+02:00
draft: false
slug: "digital-vacation-planning-sharepoint-powerapps-approval-process"
description: "Create a complete digital vacation planning solution, including approval workflow, using SharePoint, Power Apps, and Power Automate. Includes vacation overview, day calculation, calendar views, and automated approvals – ideal for IT departments and management."
categories: ["Power Platform", "Microsoft 365", "Tutorials"]
tags: ["Power Apps", "Power Automate", "SharePoint", "Vacation Planning", "Approval Process", "Approval", "Workflow", "Microsoft 365", "Business Apps"]
keywords:
  [
    "digital vacation planning sharepoint",
    "power apps vacation planner",
    "power automate vacation workflow",
    "vacation request approval process microsoft 365",
    "sharepoint vacation planner template",
    "vacation workflow power automate tutorial",
    "vacation calculation power automate",
    "vacation calendar sharepoint",
    "microsoft 365 vacation request"
  ]
cover:
  image: "/images/blogBanner.webp"
  alt: "Digital vacation planning with approval process in SharePoint, Power Apps, and Power Automate."
  caption: "Complete approval process for vacation requests in Microsoft 365 using Power Apps and automation."
  relative: true
translationKey: "digitale-urlaubsplanung-sharepoint-powerapps-genehmigungsprozess"
---

# Digital Vacation Planning with Approval Workflow – Efficient, Transparent, and License-Free

If vacation planning in your company still happens in Excel or on paper, now is the perfect time to switch to a modern, digital solution.  
In this post, I’ll show you step by step how to build a complete vacation planning and approval workflow using SharePoint, Power Apps, and Power Automate.

The best part:  
You’ll be able to download the finished solution from my blog later (under Downloads).

This solution is particularly suitable for IT departments, HR teams, and managers who need a structured, traceable, and scalable vacation management system.

---

# Components of the Solution

The solution consists of three core components:

1. SharePoint lists as the data model  
2. Power App as the user interface  
3. Power Automate flow for calculation and approval process

---

# SharePoint Lists

## 1. List “Vacation” (Employee Overview)

This list manages:

- Employees  
- Contractual vacation days  
- Planned vacation  
- Approved vacation  

**Fields:**

- Employee (Person – unique values recommended)  
- Workdays (Number)

{{< figure src="/images/urlaubsplanung-sharepoint-liste-urlaub.webp" alt="Vacation list" caption="The SharePoint list 'Vacation'" >}}

---

## 2. List “Vacation Planning” (Requests)

This list stores individual vacation requests.

**Fields:**

- Title  
- Start Date  
- End Date  
- Optional: Status  

{{< figure src="/images/urlaubsplanung.webp" alt="Vacation planning list" caption="The SharePoint list 'Vacation Planning'" >}}

---

# Create the Power App

The app is generated directly from the SharePoint list.

**Menu:**  
Integrate → Power Apps → Create an app

{{< figure src="/images/urlaubsplanung-powerapp-erstellen.webp" alt="Create Power App from SharePoint list" caption="Creating the Power App directly from the SharePoint list" >}}

---

# Customizing the Power App

## 1. Default Status “Requested”

In the Status dropdown control, set the **DefaultSelectedItems** property to:

```powerfx
[ { Value: "beantragt" } ]
```

---

## 2. Automatically Fill the Employee Field

Set a user object as the default for the Employee field:

```json
{
  '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
  Claims: "i:0#.f|membership|" & User().Email,
  DisplayName: User().FullName,
  Email: User().Email
}
```

{{< figure src="/images/urlaubsplanung-powerapp-mitarbeiter-default.webp" alt="Default user object" caption="User object in DefaultSelectedItems" >}}

---

## 3. Automatic Title

Example:

```powerfx
"Vacation " & User().FullName
```

---

## 4. Remove Attachments

The “Attachments” field is removed entirely from the form.

---

## 5. Hide Unnecessary Fields

Use the **Visible** property to hide fields that are not needed for submitting a vacation request.

---

## 6. Display Status in Browse Screen

Add a text field in the gallery that displays:

```powerfx
ThisItem.Status.Value
```

{{< figure src="/images/urlaubsplanung-powerapp-gallery-status.webp" alt="New text field" caption="New text field for Status in the Browse Gallery" >}}

---

# Power Automate Flow

The flow handles:

1. Calculating vacation days  
2. Manager approval process  
3. Updating the vacation list  

{{< figure src="/images/urlaubsplanung-flow-uebersicht.webp" alt="Vacation approval flow" caption="Power Automate flow for vacation planning and approval" >}}

---

## Trigger

The flow is triggered when an item is created in the **Vacation Planning** list.

---

## Step 1: Retrieve Employee Data

The matching row from the Vacation list is filtered using an OData query:

```
Mitarbeiter/Email eq '@{triggerOutputs()?['body/Author/Email']}'
```

{{< figure src="/images/urlaubsplanung-flow-getitem.webp" alt="Action Get Employee Vacation" caption="Action to retrieve employee vacation data" >}}

---

## Step 2: Store Employee Object in Variable

The retrieved row is stored in an object variable for easier access later.

---

## Step 3: Calculate Number of Vacation Days

Formula for calculating vacation days:

```
div( sub( ticks(outputs('Begin')), ticks(outputs('Ende')) ), 864000000000 )
```

{{< figure src="/images/urlaubsplanung-flow-compose-urlaubstage.webp" alt="Compose action vacation days" caption="Calculation of vacation days between start and end dates" >}}

---

## Step 4: Update Planned Vacation

New planned vacation value:

```
add( variables('MitarbeiterObjekt')?['geplanterUrlaub'], outputs('Compose_Urlaubstage') )
```

---

## Step 5: Determine Manager

Use the “Get Manager (V2)” action to retrieve the requester’s manager.

---

## Step 6: Send Approval Request

Use “Start and wait for an approval” to notify the supervisor.

Approval check:

```
@if(equals(outputs('Approval')?['outcome'], 'Approve'), true, false)
```

{{< figure src="/images/urlaubsplanung-flow-approval.webp" alt="Start and wait for an approval action" caption="Action to send vacation approval request" >}}

---

## Step 7: Update SharePoint (on Approval)

Depending on the approval result:

**If approved:**  
- Status → approved  
- Planned vacation decreases  
- Approved vacation increases  
- Remaining vacation recalculated  

**If rejected:**  
- Status → rejected  

---

# SharePoint Calendar View

For the best overview, set up a calendar view.

Settings:

- Start date: Start  
- End date: End  
- Subtitle: Status  

{{< figure src="/images/urlaubsplanung-sharepoint-kalender.webp" alt="Calendar view vacation overview" caption="Calendar overview for planned and approved vacation days" >}}

---

# Conditional Formatting

Under “Format current view,” you can add visual formatting:

- Requested → Yellow  
- Approved → Green  
- Rejected → Red  

---

# Testing & Useful Extensions

Additional optimization options:

- Secure SharePoint list permissions  
- Automatically exclude weekends and holidays  
- Integrate with HR/payroll systems  
- Support individual work schedules  

---

# ⬇ Download the Finished Solution

The complete import package can be found at:  
jonaskufner.com → Downloads → Vacation Planner

The download links to the corresponding GitHub repository.

---

# Thanks for Reading!

If you have any questions about the implementation or need support for Power Platform projects, feel free to get in touch.

{{< confirmed_youtube id="FkT7il9dYpg" >}}
