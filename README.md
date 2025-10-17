# BankPulse: An End-to-End Data Analytics Platform

### 🧠 Overview

BankPulse is a comprehensive data engineering and analytics platform designed to ingest, validate, store, and analyze real-world financial and economic data. This project demonstrates a full data lifecycle, from raw API extraction to an interactive, AI-powered chatbot for natural language querying.

The architecture combines a modern cloud data warehouse (**Snowflake**), a powerful data virtualization layer (**Denodo Express**), and a polished BI dashboard (**Tableau Public**). A key feature is the custom-built validation framework using **Pydantic** within Python scripts, ensuring high-quality data before it enters the warehouse. The project culminates in a **Streamlit** web application powered by **Google's Gemini** model, allowing for intuitive, conversational data exploration.

<img width="1920" height="1080" alt="Screenshot (291)" src="https://github.com/user-attachments/assets/810cd98c-3794-488c-a3b9-6900e53efe50" />


### 🎯 Key Accomplishments

* **Ingested and integrated** real-world data from public APIs (Frankfurter, World Bank) and Kaggle datasets.
* **Built a robust, in-script validation framework** using Pydantic to enforce strict data schemas, types, and quality rules during ingestion.
* **Stored and managed** clean, structured data in a **Snowflake** cloud data warehouse.
* **Developed a unified virtual data layer** in **Denodo Express**, joining disparate datasets without data replication.
* **Created an interactive, multi-part dashboard** in **Tableau Public** to visualize macroeconomic trends and credit risk factors.
* **Implemented an AI-powered Chatbot** using Streamlit, LangChain, and **Google's Gemini model** to query the Snowflake warehouse in natural language.
* **Automated data pipeline tasks** by creating scheduled cache-refreshing jobs in the **Denodo Scheduler**.

### 🏗️ Architecture

```
       External Sources (APIs, Kaggle)
               │
               ▼
       Python Ingestion & Validation Scripts
       (fetch → clean → validate with Pydantic → load)
               │
               ▼
       Snowflake Cloud Data Warehouse
       (STAGING Schema)
               │
               ▼
       Denodo Express Virtualization Layer
       (Base Views → Derived Views)
               │
          ┌────┴────┐
          │         │
          ▼         ▼
   Tableau Public    Chatbot (Streamlit + LangChain)
   (Dashboards)       (Natural Language Querying)
```

---

### 📦 Tech Stack

| Layer                    | Tool                  | Purpose                        |
| ------------------------ | --------------------- | ------------------------------ |
| Data Ingestion           | Python                | Collect API & CSV data         |
| Data Validation          | Pydantic              | In-script data validation.     |
| Data Warehouse           | Snowflake             | Centralized clean data storage |
| Virtualization           | Denodo Express        | Data federation and modeling   |
| Orchestration            | Denodo Scheduler      | Job automation & refreshes     |
| Visualization            | Tableau Public        | Dashboarding and reporting     |
| Conversational Analytics | Streamlit + LangChain | Natural language data querying |
| Version Control          | GitHub                | Code and documentation hosting |

---

### 🌍 Data Sources

* **World Bank API** – GDP, inflation, interest rate, and macro indicators.
* **Frankfurter API** – Historical and live FX rates (USD, EGP, EUR, etc.).
* **Kaggle Credit Risk Dataset** – Real loan and repayment data for risk analytics.

---
### 🚀 Setup & Running the Project

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/amrabdallah187/BankPulse.git](https://github.com/amrabdallah187/BankPulse.git)
    cd BankPulse
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Credentials:**
    This project requires API keys and credentials for Snowflake and Google AI. Set them as environment variables in your terminal session.
    **Required Variables:**
    ```
    SNOWFLAKE_USER
    SNOWFLAKE_PASSWORD
    SNOWFLAKE_ACCOUNT
    SNOWFLAKE_WAREHOUSE
    SNOWFLAKE_DATABASE
    SNOWFLAKE_SCHEMA
    GOOGLE_API_KEY
    ```

5.  **Run the Chatbot Application:**
    ```bash
    streamlit run scripts/app.py
    ```

### 📁 Repository Structure

```
BankPulse/
├── data/
│   └── raw/                # Holds the raw CSV files after ingestion
├── scripts/                # All Python scripts for the project
│   ├── fetch_fx_data.py
│   ├── fetch_worldbank_data.py
│   ├── fetch_kaggle_data.py
│   ├── validate_fx.py
│   ├── validate_worldbank.py
│   ├── validate_credit_risk.py
│   ├── load_to_snowflake.py
│   └── app.py              # The Streamlit chatbot application
├── docs/                     # Tableau dashboard screenshots
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

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
