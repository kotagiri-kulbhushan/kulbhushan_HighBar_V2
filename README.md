# HighBar Marketing Intelligence Pipeline — V2  
A fully automated pipeline for transforming raw marketing data into insights, evaluations, creative recommendations, and final reports.

---

## Overview
HighBar V2 is an end-to-end AI-driven marketing analytics system designed to analyze Meta advertising performance. It processes campaign data, computes KPIs, evaluates performance trends, generates creative recommendations when needed, and saves structured reports.

This version is a production-focused upgrade over V1, offering:

- Cleaner modular architecture  
- Standardized and minimal logging  
- Automated insights and report generation  
- Better scalability for large datasets  
- More structured agent-to-agent interactions  

---

## Expected Pipeline Output
The orchestrator prints the following sequence each time it runs:

```
Data Loaded  
Tasks Planned  
Processing...  
KPIs computed  
Evaluation done  
Creatives generated  
Reports saved  
Pipeline Completed Successfully  
```

This consistent output format aligns with common expectations for automated analytics workflows in industry environments.

---

## Architecture (Comparison: V1 vs V2)

### Key Improvements in V2
| Component | V1 | V2 |
|----------|----|----|
| Pipeline Flow | Linear, less modular | Fully modular and agent-driven |
| Agents | Logic mixed across modules | Dedicated Planner, Insight, Evaluation, Creative, and Reporting agents |
| Orchestrator | Hard-coded and rigid | Clean execution pipeline with clear responsibilities |
| Campaign Planning | Simple grouping | Smart name normalization and flexible task planning |
| Insights | Limited KPI support | Comprehensive KPI engine (CTR, CPC, ROAS, Purchase Value, etc.) |
| Evaluation | Static checks | Delta-based scoring with severity levels |
| Creative Generation | Always triggered | Only triggered on Medium or High performance impact |
| Reporting | Basic JSON | JSON + markdown report with clear summaries |
| Scalability | Harder to extend | Fully modular and designed for growth |

---

## Folder Structure

```
kasparro-v2/

│

├── src/

│   ├── orchestrator_v2.py

│   ├── run.py

│   ├── utils/

│   ├── agents/

│   │   ├── planner_v2.py

│   │   ├── insight_agent_v2.py

│   │   ├── evaluation_agent_v2.py

│   │   ├── creative_agent_v2.py

│   │   └── report_agent_v2.py

│

├── data/

│   └── synthetic_fb_ads_undergarments.csv

│

├── reports/

│   ├── insights_*.json

│   ├── creatives_*.json

│   └── report_*.md

│

├── README.md

└── requirements.txt

```

---

## Pipeline Components

### 1. Data Loader
Responsible for loading campaign data from CSV, validating fields, and displaying a small preview for traceability.

### 2. Planner Agent
Handles campaign normalization, task identification, and filtering out campaigns with insufficient data.

### 3. Insight Agent
Calculates key performance indicators, including:
- Click-through rate (CTR)
- Cost per click (CPC)
- Return on ad spend (ROAS)
- Purchase value and related metrics

### 4. Evaluation Agent
Evaluates each campaign based on KPI deltas:
```
ctr_delta  
roas_delta  
cpc_delta  
```
The output includes:
- Performance impact (Low, Medium, High)  
- Severity score  
- Reasoning and evidence  

### 5. Creative Agent
Activated only when the impact is Medium or High.  
Produces targeted creative recommendations based on detected performance issues.

### 6. Report Agent
Exports:
- Insights JSON  
- Creative suggestions JSON  
- A clean markdown report summarizing the entire run  

---

## Running the Pipeline

### Install dependencies:
```
pip install -r requirements.txt
```

### Execute the system:
```
python -m src.run
```

### Generated output files:
```
/reports/*.json  
/reports/*.md
```

---

## Environment Requirements
- Python 3.10 or above  
- Pandas  
- NumPy  
- Rich (for clean console formatting)  
- Markdown and JSON support  

---

## Sample Execution Log
```
Data Loaded  
Tasks Planned  
Processing...  
KPIs computed  
Evaluation done  
Creatives generated  
Reports saved  
Pipeline Completed Successfully  
```

---

## Why V2 Meets Professional Standards
- Strong modular architecture suitable for team-based development  
- Clear separation of concerns using specialized agents  
- Automated KPI analysis and evaluation logic  
- Intelligent creative generation triggered only when needed  
- Robust reporting layer for internal reviews or client delivery  
- Scalable for large data volumes and multi-campaign pipelines  

---

If you would like, I can also prepare:
- A GitHub banner  
- API-style documentation  
- A Dockerfile for deployment  
- A quickstart notebook for demos  
- A flow diagram for the pipeline  

Just let me know.
