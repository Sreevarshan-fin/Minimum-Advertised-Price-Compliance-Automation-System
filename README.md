# Minimum-Advertised-Price-Compliance-Automation-System


## 🧭 Project Overview

This project focuses on building an automated **MAP (Minimum Advertised Price) compliance monitoring system** that helps brands ensure their resellers do not advertise products below approved pricing thresholds.

The solution continuously monitors marketplace prices, maps reseller identities across platforms, and triggers automated enforcement actions such as warning notifications and category suspension.

---

## 🎯 Objective

To design and implement a scalable system that:

* Tracks reseller advertised prices across marketplaces
* Detects violations of MAP/LPP policies
* Automatically issues warning letters
* Enforces category suspension for repeated violations
* Maintains brand price integrity and fair competition

---

## 🚨 Business Problem

Brands rely on MAP policies to protect product value and prevent price wars among resellers. However, manual monitoring is:

* ❌ Time-consuming
* ❌ Error-prone
* ❌ Difficult across multiple marketplaces
* ❌ Complicated when sellers use different store names

Non-compliance leads to:

* Market price erosion
* Brand devaluation
* Unfair reseller competition
* Loss of customer trust

👉 The client needed an **automated, production-style monitoring system**.

---

## 🧩 Key Concepts

### 🔹 Minimum Advertised Price (MAP)

The minimum price set by the brand that resellers are allowed to advertise.

### 🔹 Lowest Possible Price (LPP)

The lowest acceptable selling price derived from MAP.
Violations are typically flagged when:

> **Seller Advertised Price (SAP) < LPP**

### 🔹 Seller Advertised Price (SAP)

The price at which a reseller lists the product on a marketplace.

### 🔹 Reseller Mapping

Resellers may operate under different storefront names.
This project uses **fuzzy matching and lookup techniques** to map aliases to a single homologated seller.

### 🔹 Product Line

Hierarchical grouping of products into categories and subcategories for enforcement actions.

---


##  ⚙️ Project Architecture


![Credit Risk Flow](https://raw.githubusercontent.com/Sreevarshan-fin/Sreevarshan-fin/main/assets/mapproject.svg)

--------


## ⚙️ System Workflow

![Credit Risk Flow](https://raw.githubusercontent.com/Sreevarshan-fin/Sreevarshan-fin/main/assets/mappipeline.svg)


### 1️⃣ Price Monitoring

* Ingest marketplace price data
* Compare SAP vs LPP
* Flag potential violations

### 2️⃣ Seller Identity Mapping

* Apply fuzzy/partial matching
* Map marketplace seller names to master reseller
* Consolidate violation counts

### 3️⃣ Automated Enforcement

* First violations → Warning letters
* Repeated violations → Category suspension
* Maintain violation history

### 4️⃣ Reporting & Insights

* Violation dashboards
* Seller risk tracking
* Compliance summaries

---

## 🧪 Example Scenario

**Reseller:** 7-Eleven
**Alias:** Smart Place Store
**SKU:** GT53XL

| Metric           | Value |
| ---------------- | ----- |
| MAP              | $100  |
| LPP              | $95   |
| Advertised Price | $90   |

### 🔍 What Happens

1. System detects SAP ($90) < LPP ($95)
2. Fuzzy mapping links *Smart Place Store* → *7-Eleven*
3. Warning letter automatically generated
4. Continued violations → Category suspension

---

## 🏆 Business Impact

- Protects brand price integrity
- Prevents marketplace price erosion
- Creates fair reseller competition
- Reduces manual monitoring effort
- Enables scalable compliance enforcement
- Improves reseller accountability

---

## 🛠️ Tech Stack (Customize if needed)

* **Python** — Data processing & automation
* **SQL (MySQL)** — Data storage & monitoring logic
* **Pandas / NumPy** — Data cleaning & analysis
* **Fuzzy Matching** — Reseller mapping
* **ReportLab** — Automated warning letters

---

## 🚀 Future Enhancements

* Real-time price scraping
* ML-based seller identity resolution
* Automated email notification system
* Risk scoring for resellers
* Near real-time monitoring pipeline

---





