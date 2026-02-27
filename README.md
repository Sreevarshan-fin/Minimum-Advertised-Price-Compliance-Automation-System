# Minimum-Advertised-Price-Compliance-Automation-System



## Problem Statement

The client faced significant challenges in manually monitoring Minimum Advertised Price (MAP) compliance across multiple marketplaces. Resellers often operated under different storefront names, making it difficult to identify repeat violations and enforce pricing policies consistently. This manual process increased the risk of price erosion, delayed enforcement, and potential brand value dilution.

---

## Approach

* Designed an **idempotent, incremental data pipeline** to process seller files reliably
* Standardized global pricing through **currency normalization**
* Implemented **reseller identity mapping** using lookup and fuzzy matching techniques
* Built a rule-based engine to evaluate **SAP vs MAP/LLP** compliance
* Ensured safe re-runs using **processed flags and batch tracking**
* Automated violation communication via **PDF letter generation**


**Example**

If Smart Place Store lists SKU GT53XL at $90 (< LPP $95), the system maps it to 7-Eleven, sends a warning, and escalates on repeat violations.

---

## ⚙️ Solution

* Automatically ingests only new seller files and prevents duplicate loads
* Enriches seller observations with product and promotional data
* Detects MAP violations using structured business rules
* Maintains historical monitoring in the `price_monitoring` fact table
* Populates a dedicated violations table for enforcement workflows
* Generates and logs violation letters exactly once per violation

---

## Project Architecture


![Credit Risk Flow](https://raw.githubusercontent.com/Sreevarshan-fin/Sreevarshan-fin/main/assets/mapproject.svg)


## Data Pipeline Workflow


![Credit Risk Flow](https://raw.githubusercontent.com/Sreevarshan-fin/Sreevarshan-fin/main/assets/mappipeline.svg)



-------------------

## 🛠️ Tech Stack

Python • Pandas • MySQL • SQLAlchemy • ReportLab • Logging

---



##  Business Impact

* Enabled automated monitoring and enforcement of MAP compliance across marketplaces
* Strengthened brand price integrity and reduced risk of market price erosion
* Created a level playing field for authorized resellers
* Improved visibility into reseller pricing behavior
* Accelerated detection and response to pricing violations
* Enhanced customer trust through consistent market pricing
* Provided a scalable foundation for proactive compliance management

---


