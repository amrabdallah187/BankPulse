# BankPulse: Real-Time Economic & Banking Data Platform

### 🧠 Overview

BankPulse is an end-to-end **data engineering and analytics platform** designed to integrate, validate, and analyze real-world **banking and economic data** using modern enterprise tools. The project combines **Snowflake**, **Denodo Express**, **Great Expectations**, and **Tableau Public** to build a scalable data infrastructure, while an **AI-powered chatbot** enables natural-language data exploration.

This project demonstrates how to unify **data engineering**, **data quality**, and **data science** concepts into one professional-grade system — using only **free tools** and **public datasets**.

---

### 🎯 Objectives

* Ingest and integrate real macroeconomic and financial data from **public APIs and Kaggle datasets**.
* Enforce **data validation** and quality assurance using **Great Expectations**.
* Store and process clean data in **Snowflake**.
* Build a **virtualized data layer** in **Denodo Express** for unified semantic access.
* Create **interactive dashboards** in **Tableau Public** to visualize key indicators.
* Implement an **AI Chatbot Data Detective** (LangChain + Streamlit) to query the data in natural language.
* Automate the entire workflow with **Denodo Scheduler**.

---

### 🏗️ Architecture

```
  External APIs (World Bank, IMF, ExchangeRate.host, Yahoo Finance, Kaggle)
             │
             ▼
     Python Ingestion Scripts
     (fetch → clean → validate → load)
             │
             ▼
     Great Expectations Validation
             │
             ▼
     Snowflake Warehouse
     (Raw → Clean → Aggregated Tables)
             │
             ▼
     Denodo Express Virtualization Layer
     (Wrappers → Base Views → Derived Views)
             │
        ┌────┴────┐
        │         │
        ▼         ▼
   Tableau Public   Chatbot (Streamlit + LangChain)
   (Dashboards)     (Natural-Language Querying)
```

---

### 📦 Tech Stack

| Layer                    | Tool                  | Purpose                        |
| ------------------------ | --------------------- | ------------------------------ |
| Data Ingestion           | Python                | Collect API & CSV data         |
| Data Validation          | Great Expectations    | Ensure data quality            |
| Data Warehouse           | Snowflake             | Centralized clean data storage |
| Virtualization           | Denodo Express        | Data federation and modeling   |
| Orchestration            | Denodo Scheduler      | Job automation & refreshes     |
| Visualization            | Tableau Public        | Dashboarding and reporting     |
| Conversational Analytics | Streamlit + LangChain | Natural language data querying |
| Version Control          | GitHub                | Code and documentation hosting |

---

### 🌍 Data Sources

* **World Bank API** – GDP, inflation, interest rate, and macro indicators.
* **ExchangeRate.host API** – Historical and live FX rates (USD, EGP, EUR, etc.).
* **Kaggle Credit Risk Dataset** – Real loan and repayment data for risk analytics.
* **Yahoo Finance API** – Historical stock and market data.
* **IMF API** – Banking and monetary statistics.

---

### 📊 Key Features

* **Data Virtualization:** Unify multiple APIs and warehouse tables via Denodo.
* **Data Quality Layer:** Implement automated validation checkpoints with Great Expectations.
* **Scalable Cloud Warehouse:** Store curated, queryable datasets in Snowflake.
* **Interactive Analytics:** Build dashboards tracking GDP, inflation, FX volatility, and credit risk.
* **AI-Powered Exploration:** Ask questions like *“Show Egypt’s inflation trend from 2015–2024”* or *“Compare USD/EGP volatility with GDP growth.”*
* **Automated Refresh:** Schedule recurring data pulls, validations, and cache refreshes.

---

### 📁 Repository Structure

```
BankPulse/
├─ data/                    # Sample CSVs & API extracts
├─ scripts/                 # Python ingestion & loading scripts
│   ├─ fetch_fx_data.py
│   ├─ fetch_worldbank_data.py
│   ├─ load_to_snowflake.py
│   └─ run_validation.py
├─ denodo/                  # View definitions & connection configs
│   ├─ base_views.sql
│   ├─ derived_views.sql
│   └─ scheduler_jobs.md
├─ chatbot_app/             # Streamlit/FastAPI chatbot
│   ├─ app.py
│   └─ utils/
├─ docs/                    # Architecture diagrams & Tableau screenshots
│   ├─ architecture.png
│   └─ tableau_dashboards/
├─ requirements.txt         # Python dependencies
└─ README.md                # Project documentation
```

---

### 🧠 Learning Focus

This project is built to strengthen your hands-on understanding of:

* **Data pipelines** and **ETL orchestration**
* **Data virtualization & modeling** using enterprise tools
* **Data quality frameworks** (Great Expectations)
* **Cloud data engineering** with Snowflake
* **BI & storytelling** through Tableau
* **Natural language interfaces** for data analytics

---

### 📜 License

This project is open-source and intended for educational and portfolio use.

---

### 👤 Author

**Amr Abdallah**
Data Engineer | Cloud & Analytics Enthusiast
[LinkedIn](https://www.linkedin.com/in/amr-abdallah-64144b248/) | [GitHub](https://github.com/amrabdallah187)

---

**⭐ If you find this useful, star the repo and share your feedback!**
