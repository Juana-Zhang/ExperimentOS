# ExperimentOS: Technical Design Document

## 1. Strategic Rationale
Modern product teams run A/B tests constantly, yet most lack a centralized system for experimentation governance. Without ExperimentOS, organizations face several critical issues:
* **Inconsistent Metrics**: Different teams defining success in different ways.
* **Poor Statistical Rigor**: Lack of guardrails leads to invalid conclusions.
* **No Institutional Memory**: Valuable experiment results are lost in spreadsheets and Slack.

ExperimentOS acts as a lightweight experimentation operating system to standardize the full lifecycle of an experiment.

---

## 2. Product Scope (MVP)Final Polish & Portfolio Positioning.
The platform is built around five core modules:

### 2.1 Experiment Registry
A centralized database to track every test from proposal to completion.
* **Metadata**: Name, Owner, Hypothesis, and Target Segment.
* **Tracking**: Monitoring start/end dates and sample sizes.

### 2.2 Statistical Engine
Automates complex calculations to ensure scientific accuracy.
* **Tests**: Support for Two-sample t-tests and Proportion tests.
* **Metrics**: Automated Lift calculation and Confidence Intervals.
* **Planning**: MDE and Power calculators for pre-experiment setup.

### 2.3 KPI Tracking & Dashboard
Visualizing experiment performance for stakeholders.
* Control vs. Treatment comparison and lift visualization.
* Automatic significance flagging to prevent "peeking" errors.

### 2.4 Prioritization Framework
Using the **RICE (Reach, Impact, Confidence, Effort)** scoring system to manage the experiment backlog and maximize ROI.

### 2.5 Automated Report Generator
One-click generation of PDF summaries including executive summaries and risk flags.

---

## 3. Technical Architecture
The system is designed for high performance and scalability.

* **Backend**: **FastAPI** (Python) for rapid, documented API development.
* **Database**: **PostgreSQL** (AWS RDS) for robust relational data storage.
* **Pipeline**: **Apache Airflow** for orchestrating daily metric ingestion and statistical triggers.
* **Cloud**: **AWS EC2** for deployment and **S3** for storing experiment artifacts.
* **Frontend**: **Streamlit** for a lightweight, data-centric user interface.



---

## 4. Experiment Data Model
Below is the core schema for the `experiments` registry:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | SERIAL | Primary Key |
| `name` | VARCHAR | Name of the experiment |
| `hypothesis` | TEXT | If-Then statement for the test |
| `status` | VARCHAR | Proposed, Running, or Completed |
| `primary_metric`| VARCHAR | The main KPI being measured |
| `sample_size` | INTEGER | Required users per variant |
| `rice_score` | FLOAT | (Impact * Confidence) / Effort |

---

## 5. Implementation Roadmap
* **Week 1**: Product Design & Architecture (Current).
* **Week 2**: Backend Infrastructure & CRUD APIs.
* **Week 3**: Statistical Engine (t-tests, lift, power).
* **Week 4**: Frontend MVP development.
* **Week 5**: Cloud Deployment (AWS).
* **Week 6**: Airflow Pipeline Integration.
* **Week 7**: Automated Report Generator.
* **Week 8**: Final Polish & Portfolio Positioning.


