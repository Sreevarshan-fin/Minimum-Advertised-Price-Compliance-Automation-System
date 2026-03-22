
# Minimum Advertised Price (MAP) Compliance Automation System

## 🔹 Project Overview

This project implements an automated MAP compliance monitoring system to track reseller pricing across multiple marketplaces and enforce pricing policies.

The system processes 150K+ product listings from 901 sellers across 5 marketplaces, detects MAP/LPP violations, resolves reseller identities, and triggers enforcement actions such as warning notifications and category suspension..


---

## 🔹 Business Problem

Brands enforce **Minimum Advertised Price (MAP)** policies to protect product value and maintain consistent pricing across resellers.

However, monitoring reseller compliance across multiple marketplaces is challenging due to the following factors:

* A Large volume of product listings.
* Sellers operating under multiple storefront aliases.
* Frequent price updates.
* Manual monitoring limitations.

Without automated monitoring, brands risk:

* Market price erosion.
* Brand devaluation.
* Unfair reseller competition.

---

## 🔹 Key Concepts

👉 Minimum Advertised Price (MAP)

The minimum price at which resellers are allowed to advertise a product.

👉 Lowest Possible Price (LPP)

The lowest acceptable selling price derived from MAP.

Violation rule:

```
Seller Advertised Price (SAP) < LPP
```

**Seller Advertised Price (SAP):** The price at which a reseller lists a product on a marketplace.

👉 Seller Identity Resolution

Resellers may operate under multiple storefront names across marketplaces.
The system uses **fuzzy matching and lookup mapping** to consolidate aliases into a single seller identity.

---

##  🔹 Project Architecture


![Credit Risk Flow](https://raw.githubusercontent.com/Sreevarshan-fin/Sreevarshan-fin/main/assets/mapproject.svg)




# System Architecture

The MAP compliance system automates pricing monitoring, violation detection, and enforcement across marketplaces.

👉 System Workflow:

```
CSV / Excel
   ↓
Data Ingestion
(scanning, deduplication)
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

## 🔹 SQL Violation Queries

👉 **Violation Recording Query**

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
 
👉 **Repeat MAP Violations by Seller, SKU, and Category**

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

## 🔹 Pipeline & Automation

* Designed an Airflow DAG to define task dependencies, including::

  * Data ingestion
  * Price monitoring
  * Violation detection
  * Letter generation

* Implemented execution using Windows Task Scheduler, running every 12 minutes.

* Handles:

  * New file detection
  * Violation processing
  * PDF generation (ReportLab)
  * MySQL history tracking (prevents duplicates)
    
## Workflow Components

 👉 **1. Price Monitoring**

* Ingest marketplace price listings
* Compare **SAP vs LPP** thresholds
* Detect potential MAP violations

👉 **2. Seller Identity Mapping**

* Unified multiple seller name variations into a single identity  
* Map seller aliases to master reseller identity
* Consolidate violations across marketplaces

👉 **3. Automated Enforcement**

* First violation → Warning notification
* Repeated violations → Category suspension
* Maintain violation history for audit tracking

👉 **4. Reporting & Insights**

* Violation dashboards
* Seller compliance tracking
* Marketplace compliance summaries

---

## 🔹Example Scenario

**Reseller:** 7-Eleven
**Alias:** Smart Place Store
**SKU:** GT53XL

| Metric           | Value |
| ---------------- | ----- |
| MAP              | $100  |
| LPP              | $95   |
| Advertised Price | $90   |

**System Response**

1. The system detects that SAP ($90) is less than LPP ($95).
2. Fuzzy matching maps **Smart Place Store → 7-Eleven**
3. Violation recorded in compliance database
4. **Warning notification automatically generated**
5. Repeated violations trigger **category suspension**

---

## 🔹 Business Impact

* Monitored **150K+ product listings** from **901 sellers across 5 marketplaces**
* Enabled scalable MAP compliance monitoring across multiple marketplaces.
* Reduced duplicate seller identities by **~25%** through seller entity resolution
* Decreased manual compliance review time by **~40%** through automated violation detection
* Improved pricing policy enforcement with **full audit traceability.**

---

## 🔹 Tech Stack

* **Python** – Data processing and automation
* **MySQL** – Data storage & compliance logic
* **Pandas / NumPy** – Data transformation
* **ReportLab** – PDF generation
* **Airflow (Design)** – Pipeline orchestration
* **Task Scheduler** – Automation execution

---
  
## 🔹 Future Enhancements

* Real-time marketplace price scraping
* ML-based seller identity resolution
* Automated email notification system
* Seller risk scoring model
* Near real-time monitoring pipeline

---

# MAP Compliance Automation System

![Python](https://img.shields.io/badge/Python-3.11-black)
![MySQL](https://img.shields.io/badge/MySQL-black)
![Pandas](https://img.shields.io/badge/Pandas-black)
![Airflow](https://img.shields.io/badge/Apache_Airflow-black)
![ReportLab](https://img.shields.io/badge/ReportLab-black)
![Task Scheduler](https://img.shields.io/badge/Task_Scheduler-black)

---

## 🔹 Overview

An end-to-end automated MAP compliance monitoring system that processes **150K+ product listings** from **901 sellers across 5 marketplaces**, detects pricing violations, resolves seller identities, and triggers enforcement actions — replacing fragmented manual tracking with consistent, near real-time surveillance.

---

## 🔹 Business Problem

Brands enforce Minimum Advertised Price (MAP) policies to protect product value and maintain consistent pricing across resellers. Manual monitoring at scale fails due to:

| Challenge | Impact |
|---|---|
| 150K+ listings updated frequently | Manual review impossible |
| Sellers operating under multiple aliases | Duplicate violations, missed offenders |
| Multi-marketplace spread | No unified compliance view |
| No audit trail | Enforcement decisions unverifiable |

Without automation, brands risk **price erosion**, **brand devaluation**, and **unfair reseller competition**.

---

## 🔹 Key Concepts

| Term | Definition |
|---|---|
| MAP | Minimum Advertised Price — the floor price resellers can advertise |
| LPP | Lowest Possible Price — derived from MAP |
| SAP | Seller Advertised Price — actual listed price |
| Violation | SAP < LPP |

---

## 🔹 System Architecture

![Architecture](images/architecture.png)

**Pipeline flow:**
```
CSV / Excel Input
      ↓
Data Ingestion — scanning, deduplication
      ↓
Seller Identity Resolution — fuzzy alias mapping
      ↓
Compliance Database (MySQL) — products, sellers, listings
      ↓
MAP Compliance Engine — SAP vs LPP detection
      ↓
Violation Table
      ↓
Enforcement Engine — rule-based actions
      ↓
PDF Warning Generator
```

---

## 🔹 Results

| Metric | Value |
|---|---|
| Listings monitored | 150K+ |
| Sellers tracked | 901 across 5 marketplaces |
| Duplicate seller identities reduced | ~25% |
| Manual compliance review time reduced | ~40% |
| Monitoring frequency | Every 12 minutes |

---

## 🔹 Real-World Example

**Reseller:** 7-Eleven · **Alias:** Smart Place Store · **SKU:** GT53XL

| Metric | Value |
|---|---|
| MAP | $100 |
| LPP | $95 |
| Advertised Price | $90 |

**System response:**
1. Detects SAP ($90) < LPP ($95) → violation flagged
2. Fuzzy matching maps `Smart Place Store` → `7-Eleven`
3. Violation recorded in compliance database
4. PDF warning notification auto-generated
5. Repeated violations → category suspension triggered

---

## 🔹 SQL Queries

<details>
<summary><b>Violation recording query</b></summary>
   
```sql
INSERT INTO violation_table (
    sku, seller_name, homologated_sellers,
    region, advertised_price, LLP,
    promotional_price, season,
    violation_flag, violation_date, marketplace
)
SELECT
    sku, seller_name, homologated_sellers,
    region, advertised_price, LLP,
    promotional_price, season,
    violation_flag, violation_date, marketplace
FROM price_monitoring
WHERE violation_flag = 'VIOLATION';
```

</details>

<details>
<summary><b>Repeat offender detection</b></summary>
```sql
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

</details>

---

## 🔹 Pipeline & Automation

<details>
<summary><b>Airflow DAG — task dependencies</b></summary>
```
data_ingestion
      ↓
price_monitoring
      ↓
violation_detection
      ↓
letter_generation
```

- Designed in **Apache Airflow** for dependency management
- Executed via **Windows Task Scheduler** every 12 minutes
- Handles new file detection, violation processing, PDF generation, MySQL deduplication

</details>

<details>
<summary><b>Enforcement logic</b></summary>

| Violation Count | Action |
|---|---|
| First violation | PDF warning notification sent |
| Repeated violations | Category suspension triggered |
| All violations | Logged to audit trail |

</details>

---

## 🔹 Project Structure
```
map-compliance/
│
├── pipeline/
│   ├── ingestion.py           # Data ingestion & deduplication
│   ├── identity_resolution.py # Fuzzy seller alias mapping
│   ├── compliance_engine.py   # SAP vs LPP violation detection
│   └── enforcement.py         # Warning & suspension logic
│
├── sql/
│   ├── violation_insert.sql
│   └── repeat_offenders.sql
│
├── reports/
│   └── warning_template.py    # ReportLab PDF generator
│
├── dags/
│   └── map_dag.py             # Airflow DAG definition
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔹 Challenges

- **Seller alias explosion** — same reseller operating under 10+ storefronts required fuzzy matching + manual lookup tables to consolidate accurately
- **Idempotency** — pipeline runs every 12 minutes, so duplicate violation inserts had to be prevented via MySQL deduplication logic
- **Scale** — 150K+ listings per run required efficient batch processing to avoid memory issues

---

## 🔹 Future Enhancements

- Real-time marketplace price scraping
- ML-based seller identity resolution
- Automated email notification system
- Seller risk scoring model
- Near real-time monitoring pipeline
