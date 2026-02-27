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







## Data Pipeline Workflow

<img width="1536" height="1024" alt="MAP Compliance Data Pipeline stages" src="https://github.com/user-attachments/assets/cc332c41-960e-4bdc-b797-543e0ca609f8" />


-------------------

## 🛠️ Tech Stack

Python • Pandas • MySQL • SQLAlchemy • ReportLab • Logging

---

##  Business Impact

- Significantly reduced manual monitoring effort through automation

- Improved reliability of violation detection using rule-based validation

- Ensured safe pipeline re-runs with incremental processing design

- Accelerated enforcement workflow via automated letter generation

- Built scalable foundation for enterprise MAP compliance monitoring

---

