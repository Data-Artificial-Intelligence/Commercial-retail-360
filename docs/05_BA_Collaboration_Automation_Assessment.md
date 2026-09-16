# Process Automation Opportunity Assessment
**Collaboration Partner:** Lead Business Analyst, Retail Operations  
**Date:** August 12, 2026  

## 1. Identified Business Problem
During a sync with the Business Analysis team, it was identified that the Operations team spends 12 hours per week manually exporting CSVs from the legacy CRM, running VLOOKUPs in Excel to match customer IDs, and formatting the data for the weekly steering committee. 

## 2. Data & Process Limitations
* Manual extraction is prone to human error (resulting in the duplicate records found in AUD-001).
* The process is not scalable; as order volume increases by 15% in Q4, the manual process will break.
* No automated lineage or audit trail exists for the weekly report.

## 3. Proposed Automation Solution
* **ETL Pipeline:** Develop a Python-based automated pipeline (using Pandas and SQLAlchemy) to extract, deduplicate, and load data directly into the PostgreSQL reporting schema nightly.
* **Semantic Layer:** Shift the VLOOKUP logic from Excel into the Power BI Star Schema using DAX relationships, ensuring a single source of truth.

## 4. Expected ROI & Impact
* **Time Savings:** Reclaims ~600 hours annually for the Operations team.
* **Accuracy:** Reduces data mismatch errors by an estimated 95%.
* **Strategic Shift:** Allows the Business Analysts to focus on strategic process mapping rather than manual data wrangling.