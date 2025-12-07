# Strategic Marketing Insights & Data Analysis

## Overview

This project performs an end-to-end analysis of marketing campaign performance. It involves cleaning a raw, messy dataset, performing exploratory data analysis (EDA), and generating a professional PDF report with strategic recommendations.

**Key Objectives:**

- Clean and standardize messy marketing data.
- Analyze channel efficiency (CPA, ROI) and trends.
- Generate a "Board-Ready" PDF report.

## Project Structure

```
├── data/
│   ├── raw/                  # Original messy dataset
│   └── processed/            # Cleaned CSV ready for analysis
├── scripts/
│   ├── clean_data.py         # Data cleaning logic
│   ├── eda_analysis.py       # Basic EDA and visualization generation
│   ├── deep_dive_analysis.py # Advanced metrics (ROI, Correlations)
│   └── create_professional_report.py # PDF Report generation
└── reports/
    ├── Strategic_Marketing_Insights_Report.pdf # Final Output
    └── figures/              # Generated plots and charts
```

## Setup & Usage

### 1. Prerequisites

Ensure you have Python installed with the following libraries:

```bash
pip install pandas numpy matplotlib seaborn
```

### 2. Run the Pipeline

Execute the scripts in the following order:

**Step 1: Clean the Data**

```bash
python scripts/clean_data.py
```

**Step 2: Generate Visualizations**

```bash
python scripts/eda_analysis.py
```

**Step 3: Generate the Report**

```bash
python scripts/create_professional_report.py
```

## Key Findings

- **Most Efficient Channel**: Instagram & Google Ads (Lowest CPA).
- **Highest Volume**: Email (but with high CPA).
- **Seasonality**: Strong spikes in Q4, but with diminishing returns on spend.

## License

Confidential - Internal Use Only.
