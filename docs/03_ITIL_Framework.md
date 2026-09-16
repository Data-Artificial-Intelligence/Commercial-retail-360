# ITIL Service Management Framework

## Incident Management
* **Trigger:** Python ETL pipeline fails or Power BI dataset refresh fails.
* **Process:** 
  1. Automated alert sent to Data Analyst (me) via email/Slack.
  2. Incident logged in Jira/ServiceNow with Severity classification.
  3. Root cause analysis performed.
  4. Resolution applied and incident closed within 24 hours.

## Change Management
* **Trigger:** Updates to Power BI DAX measures or SQL schema changes.
* **Process:**
  1. Submit Request for Change (RFC) detailing impact.
  2. Deploy changes to a "Dev" Power BI workspace first.
  3. UAT (User Acceptance Testing) with Head of Analytics.
  4. Promote to "Prod" workspace during off-peak hours.