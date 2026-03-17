
# Minimum Advertised Price (MAP) Compliance Automation System

## Project Overview

This project implements an **automated MAP (Minimum Advertised Price) compliance monitoring system** that tracks reseller pricing across multiple marketplaces and enforces pricing policies.

The system monitors **150K+ product listings from 901 sellers across 5 marketplaces**, detects **MAP/LPP violations**, resolves reseller identities, and automatically triggers enforcement actions such as **warning notifications and category suspension**.

I automated the end-to-end pipeline using **Windows Task Scheduler**, enabling the system to run every 12 minutes. The pipeline dynamically checks for new files, processes violations, generates PDF warning letters, and updates a MySQL history table to prevent duplicate processing.

The goal is to help brands **maintain price integrity, prevent price erosion, and ensure fair reseller competition**.

---

# Business Problem

Brands enforce **Minimum Advertised Price (MAP)** policies to protect product value and maintain consistent pricing across resellers.

However, monitoring reseller compliance across multiple marketplaces is challenging due to:

* Large volume of product listings
* Sellers operating under multiple storefront aliases
* Frequent price updates
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




# System Architecture

The MAP compliance system automates pricing monitoring, violation detection, and enforcement across marketplaces.

### System Workflow

```
CSV / Excel
   ↓
Data Ingestion
(scan, deduplicate)
   ↓
Seller Identity Resolution
(fuzzy alias mapping)
   ↓
Compliance Database (MySQL)
(products / sellers / listings)
   ↓
MAP Compliance Engine
(SAP vs LPP violation detection)
   ↓
Violation Table
   ↓
Enforcement Engine
(rule-based actions)
   ↓
PDF Warning Generator
```

## SQL Violation Queries

Violation Recording Query**

When a MAP violation is detected, the system records the violation in a dedicated violation tracking table. This enables enforcement rules, audit tracking, and compliance monitoring.

```
INSERT INTO violation_table (
    sku,
    seller_name,
    homologated_sellers,
    region,
    advertised_price,
    LLP,
    promotional_price,
    season,
    violation_flag,
    violation_date,
    marketplace
)
SELECT
    sku,
    seller_name,
    homologated_sellers,
    region,
    advertised_price,
    LLP,
    promotional_price,
    season,
    violation_flag,
    violation_date,
    marketplace
FROM price_monitoring
WHERE violation_flag = 'VIOLATION';
```
 
**Repeat MAP Violations by Seller, SKU, and Category**

Explanation: Identifies seller–product combinations where MAP violations occurred more than three times, helping detect repeat offenders and high-risk SKUs.

```
SELECT
    seller_name,
    sku,
    category,
    COUNT(*) AS violation_count
FROM violation_table
GROUP BY seller_name, sku, category
HAVING COUNT(*) > 3
ORDER BY violation_count DESC;
```

---

# Workflow Components

### 1. Price Monitoring

* Ingest marketplace price listings
* Compare **SAP vs LPP** thresholds
* Detect potential MAP violations

### 2. Seller Identity Mapping

* Apply **fuzzy/partial matching**
* Map seller aliases to master reseller identity
* Consolidate violations across marketplaces

### 3. Automated Enforcement

* First violation → Warning notification
* Repeated violations → Category suspension
* Maintain violation history for audit tracking

### 4. Reporting & Insights

* Violation dashboards
* Seller compliance tracking
* Marketplace compliance summaries

---

# Example Scenario

**Reseller:** 7-Eleven
**Alias:** Smart Place Store
**SKU:** GT53XL

| Metric           | Value |
| ---------------- | ----- |
| MAP              | $100  |
| LPP              | $95   |
| Advertised Price | $90   |

### System Response

1. System detects **SAP ($90) < LPP ($95)**
2. Fuzzy matching maps **Smart Place Store → 7-Eleven**
3. Violation recorded in compliance database
4. **Warning notification automatically generated**
5. Repeated violations trigger **category suspension**

---

# Business Impact

* Monitored **150K+ product listings** from **901 sellers across 5 marketplaces**
* Enabled scalable **cross-marketplace MAP compliance monitoring**
* Reduced duplicate seller identities by **~25%** through seller entity resolution
* Decreased manual compliance review time by **~40%** through automated violation detection
* Improved pricing policy enforcement with **full audit traceability**

---

# Tech Stack

* **Python** — Data processing and automation
* **SQL (MySQL)** — Compliance data storage and monitoring logic
* **Pandas / NumPy** — Data cleaning and transformation
* **Fuzzy Matching** — Seller identity resolution
* **ReportLab** — Automated warning letter generation

---

# Future Enhancements

* Real-time marketplace price scraping
* ML-based seller identity resolution
* Automated email notification system
* Seller risk scoring model
* Near real-time monitoring pipeline

---

