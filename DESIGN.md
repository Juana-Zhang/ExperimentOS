# ExperimentOS: Technical Design Document

## 1. Strategic Rationale
Modern product teams run A/B tests constantly, yet most lack a centralized system for experimentation governance[cite: 4, 18]. Without ExperimentOS, organizations face several critical issues[cite: 12]:
* **Inconsistent Metrics**: Different teams defining success in different ways[cite: 14].
* **Poor Statistical Rigor**: Lack of guardrails leads to invalid conclusions[cite: 15].
* **No Institutional Memory**: Valuable experiment results are lost in spreadsheets and Slack[cite: 11, 17].

ExperimentOS acts as a lightweight experimentation operating system to standardize the full lifecycle of an experiment[cite: 18, 27].

---

## 2. Product Scope (MVP)Final Polish & Portfolio Positioning.
The platform is built around five core modules[cite: 33]:

### 2.1 Experiment Registry
A centralized database to track every test from proposal to completion[cite: 34, 42].
* **Metadata**: Name, Owner, Hypothesis, and Target Segment[cite: 36, 37, 40].
* **Tracking**: Monitoring start/end dates and sample sizes[cite: 39, 41].

### 2.2 Statistical Engine
Automates complex calculations to ensure scientific accuracy[cite: 43].
* **Tests**: Support for Two-sample t-tests and Proportion tests[cite: 45, 46].
* **Metrics**: Automated Lift calculation and Confidence Intervals[cite: 47, 48].
* **Planning**: MDE and Power calculators for pre-experiment setup[cite: 49, 50].

### 2.3 KPI Tracking & Dashboard
Visualizing experiment performance for stakeholders[cite: 51].
* Control vs. Treatment comparison and lift visualization[cite: 54].
* Automatic significance flagging to prevent "peeking" errors[cite: 55].

### 2.4 Prioritization Framework
Using the **RICE (Reach, Impact, Confidence, Effort)** scoring system to manage the experiment backlog and maximize ROI[cite: 56, 57, 60].

### 2.5 Automated Report Generator
One-click generation of PDF summaries including executive summaries and risk flags[cite: 62, 65, 68, 69].

---

## 3. Technical Architecture
The system is designed for high performance and scalability[cite: 71].

* **Backend**: **FastAPI** (Python) for rapid, documented API development[cite: 73, 74].
* **Database**: **PostgreSQL** (AWS RDS) for robust relational data storage[cite: 75, 76].
* **Pipeline**: **Apache Airflow** for orchestrating daily metric ingestion and statistical triggers[cite: 77, 78, 150].
* **Cloud**: **AWS EC2** for deployment and **S3** for storing experiment artifacts[cite: 81, 82, 83].
* **Frontend**: **Streamlit** for a lightweight, data-centric user interface[cite: 84, 85].



---

## 4. Experiment Data Model
Below is the core schema for the `experiments` registry[cite: 92, 93]:

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
* **Week 1**: Product Design & Architecture (Current)[cite: 90].
* **Week 2**: Backend Infrastructure & CRUD APIs[cite: 97, 100].
* **Week 3**: Statistical Engine (t-tests, lift, power)[cite: 108, 110].
* **Week 4**: Frontend MVP development[cite: 122].
* **Week 5**: Cloud Deployment (AWS).
* **Week 6**: Airflow Pipeline Integration.
* **Week 7**: Automated Report Generator.
* **Week 8**: Final Polish & Portfolio Positioning.


