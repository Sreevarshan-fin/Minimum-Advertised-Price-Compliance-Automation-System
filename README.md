# Minimum-Advertised-Price-Compliance-Automation-System


## Project Overview

This project implements an automated **MAP (Minimum Advertised Price) compliance monitoring system** that tracks reseller pricing across marketplaces and enforces pricing policies.

The system monitors **150K+ product listings from 901 sellers across 5 marketplaces**, detects MAP/LPP violations, resolves reseller identities, and automatically triggers enforcement actions such as warning notifications and category suspension.

The goal is to help brands maintain **price integrity, prevent price erosion, and enforce fair reseller competition**.

---

# Business Problem

Brands enforce **Minimum Advertised Price (MAP)** policies to protect product value.
However, monitoring reseller compliance across multiple marketplaces is difficult due to:

* Large number of product listings
* Sellers using **different storefront aliases**
* Constant price updates
* Manual monitoring limitations

Without automated monitoring, brands risk:

* Market price erosion
* Brand devaluation
* Unfair reseller competition

---

# Key Concepts

### Minimum Advertised Price (MAP)

The minimum price that resellers are allowed to advertise for a product.

### Lowest Possible Price (LPP)

The lowest acceptable selling price derived from MAP.

Violation rule:

```
Seller Advertised Price (SAP) < LPP
```

### Seller Advertised Price (SAP)

The price at which a reseller lists a product on a marketplace.

### Seller Identity Resolution

Resellers may operate under multiple storefront names across marketplaces.
The system uses **fuzzy matching and lookup mapping** to consolidate aliases into a single seller identity.



---


##  Project Architecture


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





