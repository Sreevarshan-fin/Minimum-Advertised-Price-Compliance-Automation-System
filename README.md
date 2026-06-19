<h1 align="center">MAP Compliance Automation System</h1>

<p align="center"><b>Automated Price Monitoring & Violation Detection Across Multi-Marketplaces</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Core-Python-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Database-MySQL-orange?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Orchestration-Airflow-red?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/Visualization-Power%20BI-yellow?style=for-the-badge&logo=powerbi&logoColor=black"/>
</p>

----

![workflow](assets/MAP_workflow.jpg)

---

## 🔹 Overview

An end-to-end automated MAP compliance monitoring system that processes **150K+ product listings** from **901 sellers across 5 marketplaces**, detects pricing violations, resolves seller identities, and triggers enforcement actions — replacing fragmented manual tracking with consistent, near real-time surveillance.

---

## 🔹 Business Problem

Brands enforce **Minimum Advertised Price (MAP)** policies to protect **brand value** and maintain **pricing consistency** across resellers. However, monitoring compliance across **5 online marketplaces** is challenging due to **frequent price changes**, **seller aliases**, **fragmented data sources**, and the lack of a **centralized audit trail**. These challenges lead to **missed violations**, **inconsistent enforcement**, **price erosion**, and potential **revenue loss**. The objective was to build an **automated MAP compliance system** that could **detect violations**, **identify repeat offenders**, and provide a **unified compliance dashboard** for efficient monitoring and enforcement.


---

## 🔹 System Architecture


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

## 🔹 How It Works (Execution)

The system runs as an automated workflow:

- **Ingestion:** CSV/Excel files are periodically loaded  
- **Processing:** Data is cleaned and deduplicated using Python  
- **Storage:** Data is stored in MySQL (sellers, products, pricing)  
- **Detection:** SQL identifies violations (**SAP < LPP**)  
- **Tracking:** Violations are logged for audit and monitoring  
- **Enforcement:** Automated PDF warnings and reports generated  
- **Orchestration:** Apache Airflow manages scheduling and dependencies  

👉 Runs every **12 minutes** for near real-time monitoring

---------------

## 🔹 Business Impact

→ Continuously monitored **1,500+ product listings** and tracked **150K+ pricing records** from **901 sellers** across **5 marketplaces** through an automated MAP compliance pipeline running every **12 minutes**.

→ Replaced fragmented manual reviews with **near real-time violation detection**, **seller tracking**, and **automated compliance reporting**, improving compliance visibility and audit readiness.

→ Estimated a **30% reduction in manual compliance review effort** by automating repetitive monitoring, tracking, and reporting activities, enabling compliance teams to focus on enforcement actions and high-priority investigations.


---

## 🔹 Key Concepts & Example

| Term          | Definition                                        | Example     |
| ------------- | ------------------------------------------------- | ----------- |
| **MAP**       | Minimum Advertised Price set by the brand         | $100        |
| **LPP**       | Lowest Possible Price derived from MAP            | $95         |
| **SAP**       | Seller Advertised Price listed on the marketplace | $90         |
| **Violation** | Occurs when **SAP < LPP**                         | $90 < $95 ✅ |

### Example Violation

**Seller:** 7-Eleven
**Alias:** Smart Place Store
**SKU:** GT53XL

**System Workflow:**

1. Detects **SAP ($90) < LPP ($95)** → MAP violation flagged.
2. Uses **fuzzy matching** to map **"Smart Place Store"** to **"7-Eleven"**.
3. Records the violation in the compliance database.
4. Generates an automated PDF warning notification.
5. Tracks repeat violations and triggers enforcement actions when thresholds are exceeded.


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
