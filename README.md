# Lynx Healthcare Analysis

> Fundamental analysis specialized for large pharmaceuticals, biotech, medical devices, healthcare services, managed care / health insurance, life-sciences tools, drug distribution, and health IT.

Part of the **Lince Investor Suite**.

## Overview

Lynx Healthcare is a comprehensive fundamental analysis tool built specifically for healthcare investors. It evaluates companies across the full lifecycle — from preclinical biotech to diversified Big Pharma and integrated managed-care franchises — using healthcare-specific metrics, valuation methods, and risk assessments.

### Key Features

- **Stage-Aware Analysis**: Automatically classifies companies as Preclinical / Early-Stage Biotech, Clinical / Hyper-Growth, Launch / Scale-Up, Commercial / Cash-Generative, or Diversified Healthcare Franchise — and adapts all metrics and scoring accordingly
- **Healthcare-Specific Metrics**: R&D Intensity (pharma/biotech innovation signal), Rule of 40 (for digital-health SaaS), Cash Runway & Burn (biotech survival), SBC/Revenue & SBC/FCF (dilution), Revenue/Employee, CAC Payback (health IT), FCF Conversion, EV/Gross-Profit, EV/ARR (for health IT)
- **Healthcare Sub-Category Detection**: Automatic identification of Big Pharma, Biotechnology, Generic & Specialty Pharma, Medical Devices, Healthcare Equipment & Supplies, Healthcare Providers, Managed Care / Insurance, Life Sciences Tools & Diagnostics, Healthcare Distribution, Health IT / Digital Health, or CRO / CDMO
- **5-Level Relevance System**: Critical, Important, Relevant, Informational, Irrelevant — plus an **Impact column** with colored labels (blinking red / orange / yellow / green / silver)
- **5-Level Severity System**: `***CRITICAL***` (red), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Market Intelligence**: Insider transactions (with 10b5-1 plan awareness), institutional holders, analyst consensus, short interest, price technicals with golden/death cross detection, **XLV (Health Care Select Sector SPDR)** + healthcare sub-sector ETF comparison (XBI, IBB, XPH, IHE, IHI, XHE, IHF, XHS)
- **10-Point Healthcare Screening Checklist**: Rule-of-40 pass (digital health), moat gross margin, SBC contained, dilution, cash runway, R&D intensity, debt, insider/founder alignment, revenue growth, jurisdiction
- **Jurisdiction Risk Classification**: Tier 1/2/3 based on FDA / EMA / PMDA approval quality, drug-pricing stability, reimbursement predictability, and IP protection
- **Multiple Interface Modes**: Console CLI, Interactive REPL, Textual TUI, Tkinter GUI
- **Export**: TXT, HTML, and PDF report generation
- **Sector & Industry Insights**: Deep context for Big Pharma, Biotech, Generic / Specialty Pharma, Medical Devices, Medical Instruments & Supplies, Medical Care Facilities, Healthcare Plans, Life Sciences Tools, Diagnostics & Research, Medical Distribution, Health Information Services, and Pharmaceutical Retailers

### Target Companies

Designed for analyzing companies like:
- **Diversified Franchises / Big Pharma**: Johnson & Johnson (JNJ), Pfizer (PFE), Merck (MRK), AbbVie (ABBV), Novartis (NVS), Roche (ROG.SW), AstraZeneca (AZN), Eli Lilly (LLY)
- **Biotech**: Vertex (VRTX), Regeneron (REGN), Moderna (MRNA), BioNTech (BNTX), Beam Therapeutics (BEAM), CRISPR Therapeutics (CRSP), Arcus Biosciences (RCUS), plus clinical-stage names
- **Medical Devices**: Medtronic (MDT), Stryker (SYK), Boston Scientific (BSX), Edwards Lifesciences (EW), Intuitive Surgical (ISRG), Dexcom (DXCM)
- **Managed Care**: UnitedHealth (UNH), Elevance (ELV), Humana (HUM), Cigna (CI), Molina (MOH), Centene (CNC)
- **Life Sciences Tools**: Thermo Fisher (TMO), Danaher (DHR), Agilent (A), Waters (WAT), Bio-Techne (TECH), Illumina (ILMN)
- **Providers / Hospitals**: HCA Healthcare (HCA), Tenet (THC), DaVita (DVA), Encompass Health (EHC)
- **Distributors**: McKesson (MCK), Cencora (COR), Cardinal Health (CAH)

## Installation

```bash
# Clone the repository
git clone https://github.com/borjatarraso/lynx-investor-healthcare.git
cd lynx-investor-healthcare

# Install in editable mode (creates the `lynx-health` command)
pip install -e .
```

### Dependencies

| Package        | Purpose                              |
|----------------|--------------------------------------|
| yfinance       | Financial data from Yahoo Finance    |
| requests       | HTTP calls (OpenFIGI, EDGAR, etc.)   |
| beautifulsoup4 | HTML parsing for SEC filings         |
| rich           | Terminal tables and formatting       |
| textual        | Full-screen TUI framework            |
| feedparser     | News RSS feed parsing                |
| pandas         | Data analysis                        |
| numpy          | Numerical computing                  |

All dependencies are installed automatically via `pip install -e .`.

## Usage

### Direct Execution
```bash
# Via the runner script
./lynx-investor-healthcare.py -p JNJ

# Via Python
python3 lynx-investor-healthcare.py -p LLY

# Via pip-installed command
lynx-health -p MRK
```

### Execution Modes

| Flag | Mode | Description |
|------|------|-------------|
| `-p` | Production | Uses `data/` for persistent cache |
| `-t` | Testing | Uses `data_test/` (isolated, always fresh) |

### Interface Modes

| Flag | Interface | Description |
|------|-----------|-------------|
| (none) | Console | Progressive CLI output |
| `-i` | Interactive | REPL with commands |
| `-tui` | TUI | Textual terminal UI with themes |
| `-x` | GUI | Tkinter graphical interface |

### Examples

```bash
# Analyze a diversified Big Pharma franchise
lynx-health -p JNJ

# Force fresh data download
lynx-health -p LLY --refresh

# Search by company name
lynx-health -p "Vertex Pharmaceuticals"

# Clinical-stage biotech — runway dominates
lynx-health -p MRNA

# Managed-care insurer — MLR-driven profitability
lynx-health -p UNH

# Medical devices
lynx-health -p ISRG

# Interactive mode
lynx-health -p -i

# Export HTML report
lynx-health -p PFE --export html

# Explain a metric
lynx-health --explain rd_intensity

# Skip filings and news for faster analysis
lynx-health -t MRK --no-reports --no-news
```

## Severity & Impact System

Every metric displays a **Severity tag** and an **Impact column**.

### Severity Levels

| Severity        | Marker          | Color           | Meaning                  |
|-----------------|-----------------|-----------------|--------------------------|
| `***CRITICAL***` | uppercase, red bold | Red             | Urgent red flag          |
| `*WARNING*`     | italic          | Orange          | Significant concern      |
| `[WATCH]`       | bracketed       | Yellow          | Needs monitoring         |
| `[OK]`          | bracketed       | Green           | Normal range             |
| `[STRONG]`      | bracketed       | Silver / Grey   | Excellent signal         |

### Impact Column

| Impact          | Color (text)      |
|-----------------|-------------------|
| Critical        | Blinking red      |
| Important       | Orange            |
| Relevant        | Yellow            |
| Informational   | Green             |
| Irrelevant      | Grey / Silver     |

## Analysis Sections

1. **Company Profile** — Tier, lifecycle stage, healthcare category, jurisdiction classification
2. **Sector & Industry Insights** — Healthcare-specific context and benchmarks
3. **Valuation Metrics** — Traditional + healthcare-specific (EV/GP, EV/ARR for health IT, EV/Employee, R40-Adj EV/Rev)
4. **Profitability Metrics** — ROE/ROIC/margins + Rule of 40 (digital health), Magic Number (health IT), SBC/Revenue, SBC/FCF, GAAP-vs-Adjusted gap
5. **Solvency & Survival** — Cash runway (critical for biotech), burn rate, Capex/Revenue, Deferred Rev / RPO, Goodwill/Assets
6. **Growth & Pipeline Signals** — Revenue/ARR growth, **R&D Intensity** (the healthcare innovation metric), SG&A intensity, Revenue/Employee, NRR/GRR for health-IT names
7. **Share Structure** — Outstanding/diluted shares, insider/institutional ownership, SBC Overhang Risk, Dual-Class flag
8. **Healthcare Quality** — Moat, Rule-of-40 verdict, Unit Economics, R&D Efficiency, Franchise Position, Founder/Scientist-Led Signal
9. **Intrinsic Value** — DCF, Graham Number, EV/Sales Implied, Reverse DCF (method selection by stage; cash-backing floor for clinical biotech)
10. **Market Intelligence** — Analysts, short interest, technicals, insider trades, healthcare benchmark (XLV + sub-sector ETF)
11. **Financial Statements** — 5-year annual summary with R&D, SBC, deferred revenue
12. **SEC Filings** — Downloadable regulatory filings
13. **News** — Yahoo Finance + Google News RSS
14. **Assessment Conclusion** — Weighted score, verdict, strengths/risks, 10-point healthcare screening checklist
15. **Healthcare Disclaimers** — Stage-specific and category-specific risk disclosures (patent cliff, biosimilar erosion, MLR for insurers, Phase III failure rates for biotech, etc.)

## Relevance System

Each metric is classified by importance for the company's lifecycle stage:

| Level | Prefix | Impact Column    | Meaning |
|-------|--------|------------------|---------|
| **Critical**    | `*`      | Blinking Red    | Must-check for this stage |
| **Important**   | `!`      | Orange          | Primary metric |
| **Relevant**    | normal   | Yellow          | Important context |
| **Informational** (Contextual) | dimmed | Green | Background only |
| **Irrelevant**  | hidden   | Silver          | Not meaningful for this stage |

Example: For a clinical-stage biotech, **cash runway** and **burn rate** are **Critical** while traditional **P/E** is **Irrelevant**. For a diversified Big Pharma franchise, **ROIC** and **EV/EBITDA** are **Critical** while **Magic Number** is **Irrelevant**.

## Scoring Methodology

The overall score (0-100) is a weighted average of 5 categories, with weights adapted by both company tier AND lifecycle stage:

| Stage | Valuation | Profitability | Solvency | Growth | Healthcare Quality |
|-------|-----------|---------------|----------|--------|--------------------|
| Preclinical / Early-Stage Biotech | 5-10% | 5% | 35-40% | 15-20% | 30-35% |
| Clinical / Hyper-Growth | 10-15% | 10-15% | 15-25% | 30% | 25% |
| Launch / Scale-Up | 15-20% | 15-20% | 15-20% | 20-25% | 25% |
| Commercial / Cash-Generative | 20-25% | 20-25% | 10-15% | 15-20% | 25% |
| Diversified Healthcare Franchise | 25% | 25% | 10% | 15% | 25% |

Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30).

## Project Structure

```
lynx-investor-healthcare/
├── lynx-investor-healthcare.py   # Runner script
├── pyproject.toml                # Build configuration
├── requirements.txt              # Dependencies
├── img/                          # Logo images
├── data/                         # Production cache
├── data_test/                    # Testing cache
├── docs/                         # Documentation
│   └── API.md                    # API reference
├── robot/                        # Robot Framework tests
│   ├── cli_tests.robot
│   ├── api_tests.robot
│   └── export_tests.robot
├── tests/                        # Unit tests
└── lynx_health/                  # Main package
```

## Testing

```bash
# Unit tests
pytest tests/ -v

# Robot Framework acceptance tests
robot robot/
```

## License

BSD 3-Clause License. See LICENSE in source.

## Author

**Borja Tarraso** — borja.tarraso@member.fsf.org
