---
title: "Custom Connector for OpenWeatherMap in the Power Platform (Power Apps & Power Automate)"
slug: "custom-connector-openweathermap-power-platform"
date: 2025-10-02T09:00:00+02:00
draft: false
description: "Step-by-step guide: Create a custom connector for the OpenWeatherMap API, test it with Postman, and use it in Power Automate and Power Apps (Canvas)."
tags: ["Power Platform", "Power Apps", "Power Automate", "Custom Connector", "API", "OpenWeatherMap", "Power FX", "Postman"]
categories: ["Tutorial"]
keywords: ["custom connector", "Custom Connector Power Apps", "Power Automate Weather", "OpenWeatherMap API Key", "Postman Test", "Swagger", "Canvas App", "Dataverse"]
toc: true
canonicalURL: "https://jonaskufner.com/posts/custom-connector-openweathermap-power-platform/"
cover:
  image: "/images/custom-connector-cover.webp"
  alt: "Custom OpenWeatherMap Connector in the Microsoft Power Platform"
  caption: "From practice: Weather data via Custom Connector in Power Automate & Power Apps"
  relative: true
translationKey: "custom-connector-openweathermap-power-platform"
---

> **Video for this blog post:** 👉 [Watch the YouTube tutorial](https://www.youtube.com/watch?v=SPGXvE3D4cs)

## Overview

In this post, I’ll show you how to create a **custom connector** for the **OpenWeatherMap API** and then use it in **Power Automate** and **Power Apps (Canvas)**.  
We’ll go step by step: **Test the API (Postman)** → **Create the connector** → **Define the action** → **Test the connection** → **Use it in flows and apps**.

---

## Why a Custom Connector?

The Microsoft Power Platform includes many **out-of-the-box connectors**. But if *your* system or *your* API isn’t among them, you need a flexible solution.  
With a **custom connector**, you can integrate **any REST API** — such as project management, accounting, or AI services. For this tutorial, we’ll use **OpenWeatherMap** as a simple, practical example.

---

## Prerequisites

- Access to Microsoft Power Platform (Power Apps / Power Automate)  
- A **free OpenWeatherMap account** including an **API key**  
- **Postman** for quick API testing (free)

---

## Step 1: Test the API Call with Postman

Before actually creating the custom connector, it makes sense to test the API call with Postman. This is optional but helps for the next steps.

1. **Create a new request** (GET).  
2. Use the URL from the OWM documentation, e.g.:  
   https://api.openweathermap.org/data/2.5/weather?lat=48.17&lon=11.61&units=metric&appid=YOUR_API_KEY  
3. Click **Send** — if successful, you’ll receive **status code 200** and a **JSON response** with weather data.

{{< figure src="/images/postman-test.webp" alt="Postman Test: GET /data/2.5/weather" caption="Postman: Successful GET call with status 200 and JSON response." >}}

**Typical response fields (shortened):**
```json
{
"weather":[{"main":"Clear","description":"clear sky"}],
"main":{"temp":21.3,"feels_like":21.0,"humidity":45},
"wind":{"speed":3.6},
"name":"Munich",
"coord":{"lat":48.17,"lon":11.61}
}
```

---

## Step 2: Create the Custom Connector in Power Apps

Go to make.powerapps.com → Custom Connectors.

### 2.1 General

- Name: e.g. OpenWeather Connector  
- Host: api.openweathermap.org  
- Base URL: /data/2.5/  
- Description (example):  
  “The custom connector provides the ‘Current Weather’ action, which returns weather information for a defined location. The data source is openweathermap.org.”  

Optional: Add an icon & color for better recognition.

{{< figure src="/images/connector-general.webp" alt="Connector General: Host & Base URL" caption="Power Apps: General section with host api.openweathermap.org and base URL /data/2.5/." >}}

### 2.2 Security

- Authentication type: “API Key”  
- Parameter label: any (e.g. “OpenWeather API Key”)  
- Parameter name: appid (must match the API)  
- Parameter location: Query (as in the Postman test)

{{< figure src="/images/connector-security.webp" alt="Connector Security: API Key in Query" caption="Power Apps: Security section – authentication type API Key, parameter name appid, location Query." >}}

### 2.3 Definition (Actions)

- Add a new action  
- Summary: Current Weather  
- Description: Returns current weather for a given position (lat/lon).  
- Operation ID: CurrentWeatherForLocation (unique, no spaces)  

**Request:**  
Import the example request (e.g., from Postman or as a sample URL).  
Remove *appid* from the parameters because the value is provided via the connection.  
Keep *lat* and *lon* as query parameters.

{{< figure src="/images/connector-definition.webp" alt="Connector Definition: Action Current Weather" caption="Power Apps: Definition section – action Current Weather with query parameters lat & lon." >}}

### 2.4 Code (optional)

Here, you could transform API responses (e.g., forward only selected fields). For the first setup, we’ll skip this part.

### 2.5 Test

Save the connector → then, under the “Test” tab, create a new connection.  
Enter your API key (appid).  
Enter lat/lon, e.g. 48.17 and 11.61 (English Garden, Munich).  
Run the test – you should see the JSON response.

{{< figure src="/images/connector-test.webp" alt="Connector Test: Connection & Request" caption="Power Apps: Test section – connection with API key and test call using lat=48.17, lon=11.61." >}}

---

## Step 3: Use in Power Automate

Create a new flow (e.g., “Manually triggered”).  
Action → Custom → select your OpenWeather Connector.  
Pass parameters: lat & lon.  
Save and test the flow.  

The output contains all weather data, which you can further process (e.g., condition, message, Teams post, email).

{{< figure src="/images/flow-action.webp" alt="Power Automate: Action from Custom Connector" caption="Power Automate: Flow action from the custom connector showing weather data output." >}}

**Example: Use fields from the response**

```
body('CurrentWeatherForLocation')?['main']?['temp']
body('CurrentWeatherForLocation')?['weather']?[0]?['description']
```

---

## Step 4: Use in Power Apps (Canvas)

Add a data source → select your OpenWeather Connector.  
In Power FX, call the action and pass parameters as a record.  

**Example (OnSelect of a button):**
```powerfx
Set(
    gblWeather,
    OpenWeatherConnector.CurrentWeatherForLocation(
        { lat: 48.17, lon: 11.61 }
    )
)
```

**Example (Text label):**
```powerfx
"Temp: " & Round(gblWeather.main.temp, 1) & " °C — " & 
First(gblWeather.weather).description
```

{{< figure src="/images/tests-powerapps.webp" alt="Power Apps Canvas: Weather data output" caption="Power Apps (Canvas): Label showing temperature & description from gblWeather." >}}

Tip: Define `units=metric` in the action or as an optional query parameter to return temperatures in °C.

---

## Summary

- **What?** Custom connector for OpenWeatherMap  
- **Why?** Use any REST API in the Power Platform  
- **How?** Test in Postman → define connector → use in Flows & Apps  
- **Code?** Power FX for calling & displaying results  
- **Next step:** Package as a solution & connect more business APIs  

**Video:** Step-by-step walkthrough  

👉 Watch the tutorial here:  
Custom Connector – OpenWeatherMap (YouTube)

{{< figure
    src="/images/YouTube-Link-image.webp"
    alt="Preview: Connect any API with the Power Platform 🚀 | Custom Connector Tutorial"
    caption="Video tutorial for the blog post (YouTube | external link)"
    link="https://www.youtube.com/watch?v=SPGXvE3D4cs"
    target="_blank"
    rel="external noopener nofollow"
    title="YouTube: Connect any API with the Power Platform 🚀 | Custom Connector Tutorial"
>}}

I plan to build my own interfaces between business applications next (e.g., project management, accounting, AI services).  
Which applications would you like to connect? Let me know in the comments!
