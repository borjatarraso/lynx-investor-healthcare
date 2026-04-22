# Lynx Healthcare Analysis -- API Reference

Public Python API for the `lynx_health` package (v2.0).

## Package Structure

```
lynx_health/
├── __init__.py          # Version, about text
├── __main__.py          # Entry point
├── cli.py               # CLI argument parser
├── display.py           # Rich console display
├── interactive.py       # Interactive REPL mode
├── easter.py            # Hidden features
├── models.py            # Data models (HealthCategory, CompanyStage, …)
├── core/
│   ├── analyzer.py      # Analysis orchestrator (healthcare sector gate)
│   ├── conclusion.py    # Verdict synthesis (healthcare-weighted)
│   ├── fetcher.py       # yfinance data fetching
│   ├── news.py          # News aggregation
│   ├── reports.py       # SEC filing fetching
│   ├── storage.py       # Cache management
│   └── ticker.py        # Ticker resolution
├── metrics/
│   ├── calculator.py    # Metric calculations (calc_health_quality, …)
│   ├── relevance.py     # Metric relevance by stage/tier
│   ├── explanations.py  # Metric educational content
│   └── sector_insights.py # Healthcare industry insights
├── export/
│   ├── __init__.py      # Export dispatcher
│   ├── txt_export.py    # Plain text export
│   ├── html_export.py   # HTML export
│   └── pdf_export.py    # PDF export
├── gui/
│   └── app.py           # Tkinter GUI
└── tui/
    ├── app.py           # Textual TUI
    └── themes.py        # TUI color themes
```

---

## Core API

### Analysis (`lynx_health.core.analyzer`)

#### `run_full_analysis`

```python
def run_full_analysis(
    identifier: str,
    download_reports: bool = True,
    download_news: bool = True,
    max_filings: int = 10,
    verbose: bool = False,
    refresh: bool = False,
) -> AnalysisReport
```

Run a complete fundamental analysis for a Healthcare company.
This is a convenience wrapper around `run_progressive_analysis` with
`on_progress=None`.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `identifier` | `str` | required | Ticker symbol (`JNJ`), ISIN (`US4781601046`), or company name (`Johnson & Johnson`). |
| `download_reports` | `bool` | `True` | Fetch SEC filings (10-K, 10-Q, 8-K). |
| `download_news` | `bool` | `True` | Fetch recent news articles. |
| `max_filings` | `int` | `10` | Maximum number of filings to download locally. |
| `verbose` | `bool` | `False` | Enable verbose console output. |
| `refresh` | `bool` | `False` | Force re-fetch from network even if cached data exists. |

**Returns:** `AnalysisReport` -- fully populated report dataclass.

**Raises:** `SectorMismatchError` if the company is not in the healthcare sector (non-healthcare sectors are routed to their matching Lynx specialist).

**Example:**

```python
from lynx_health.core.analyzer import run_full_analysis

report = run_full_analysis("JNJ")
print(report.profile.name)       # "Johnson & Johnson"
print(report.profile.tier.value) # "Mega Cap"
print(report.profile.stage.value)  # "Diversified Healthcare Franchise"
print(report.profile.health_category.value)  # "Large Pharmaceuticals"
print(report.solvency.cash_runway_years)
```

---

#### `run_progressive_analysis`

```python
def run_progressive_analysis(
    identifier: str,
    download_reports: bool = True,
    download_news: bool = True,
    max_filings: int = 10,
    verbose: bool = False,
    refresh: bool = False,
    on_progress: Optional[Callable[[str, AnalysisReport], None]] = None,
) -> AnalysisReport
```

Same as `run_full_analysis`, but accepts a progress callback that is invoked
after each analysis stage completes.  Used by the TUI and GUI interfaces to
update the display incrementally.

**Callback stages** (passed as the first `str` argument):

`"profile"` | `"financials"` | `"valuation"` | `"profitability"` |
`"solvency"` | `"growth"` | `"share_structure"` | `"health_quality"` |
`"intrinsic_value"` | `"market_intelligence"` | `"filings"` | `"news"` |
`"conclusion"` | `"complete"`

**Example:**

```python
from lynx_health.core.analyzer import run_progressive_analysis

def on_progress(stage: str, report):
    print(f"Stage complete: {stage}")

report = run_progressive_analysis("MRNA", on_progress=on_progress)
```

---

### Conclusion (`lynx_health.core.conclusion`)

#### `generate_conclusion`

```python
def generate_conclusion(report: AnalysisReport) -> AnalysisConclusion
```

Synthesize a scored verdict from a completed `AnalysisReport`.

Scoring weights are determined by the company's `(stage, tier)` combination.
For example, solvency (runway) and healthcare quality are weighted much more heavily for
clinical-stage biotech than for Diversified Healthcare Franchises.

**Returns:** `AnalysisConclusion` with:

- `overall_score` -- 0-100 composite score.
- `verdict` -- one of `"Strong Buy"`, `"Buy"`, `"Hold"`, `"Caution"`, `"Avoid"`.
- `summary` -- one-paragraph narrative.
- `category_scores` -- dict with scores for `valuation`, `profitability`, `solvency`, `growth`, `health_quality`.
- `category_summaries` -- dict with human-readable summary per category.
- `strengths` / `risks` -- lists of up to 6 key points each.
- `tier_note` / `stage_note` -- explanations of why certain metrics matter for this company.
- `screening_checklist` -- dict of boolean pass/fail/None checks (e.g. `cash_runway_18m`, `low_dilution`, `healthy_rd_spend`, `moat_gross_margin`).

**Example:**

```python
from lynx_health.core.conclusion import generate_conclusion

conclusion = generate_conclusion(report)
print(conclusion.verdict)          # "Buy"
print(conclusion.overall_score)    # 68.4
print(conclusion.strengths)        # ["Rule-of-40 of 62% — strong growth + profitability trade-off", ...]
print(conclusion.screening_checklist)
```

---

## Data Models (`lynx_health.models`)

All models are Python `dataclasses`.  Every numeric field defaults to `None`
(meaning "not available") unless otherwise noted.

### Enums

| Enum | Values |
|---|---|
| `CompanyTier` | `MEGA`, `LARGE`, `MID`, `SMALL`, `MICRO`, `NANO` |
| `CompanyStage` | `STARTUP` (Preclinical / Early-Stage Biotech), `GROWTH` (Clinical / Hyper-Growth), `SCALE` (Launch / Scale-Up), `MATURE` (Commercial / Cash-Generative), `PLATFORM` (Diversified Healthcare Franchise) |
| `HealthCategory` | `BIG_PHARMA`, `BIOTECH`, `GENERIC_PHARMA`, `MEDICAL_DEVICES`, `HEALTH_EQUIPMENT`, `HEALTH_PROVIDERS`, `HEALTH_INSURANCE`, `LIFE_SCIENCES_TOOLS`, `HEALTH_DISTRIBUTION`, `HEALTH_IT`, `CRO_CDMO`, `OTHER` |
| `JurisdictionTier` | `TIER_1` (FDA/EMA/PMDA stable regulation), `TIER_2` (Moderate regulatory & reimbursement risk), `TIER_3` (High regulatory, pricing or geopolitical risk), `UNKNOWN` |
| `Relevance` | `CRITICAL`, `IMPORTANT`, `RELEVANT`, `CONTEXTUAL`, `IRRELEVANT` |
| `Severity` | `CRITICAL`, `WARNING`, `WATCH`, `OK`, `STRONG`, `NA` |

### Core Dataclasses

#### `CompanyProfile`

Company identity and classification.

| Field | Type | Description |
|---|---|---|
| `ticker` | `str` | Resolved ticker symbol. |
| `name` | `str` | Company name. |
| `isin` | `Optional[str]` | ISIN code if resolved. |
| `sector` | `Optional[str]` | Sector (expected: `"Healthcare"`). |
| `industry` | `Optional[str]` | Industry (e.g. `"Biotechnology"`, `"Drug Manufacturers - General"`, `"Medical Devices"`). |
| `country` | `Optional[str]` | Country of domicile. |
| `exchange` | `Optional[str]` | Primary exchange. |
| `currency` | `Optional[str]` | Reporting currency. |
| `market_cap` | `Optional[float]` | Market capitalization. |
| `description` | `Optional[str]` | Company description. |
| `website` | `Optional[str]` | Corporate website. |
| `employees` | `Optional[int]` | Number of employees. |
| `tier` | `CompanyTier` | Market-cap tier (default `NANO`). |
| `stage` | `CompanyStage` | Healthcare lifecycle stage (default `STARTUP`). |
| `health_category` | `HealthCategory` | Healthcare sub-category (default `OTHER`). |
| `jurisdiction_tier` | `JurisdictionTier` | Jurisdiction risk tier (default `UNKNOWN`). |
| `jurisdiction_country` | `Optional[str]` | Country used for jurisdiction classification. |

#### `ValuationMetrics`

Traditional and healthcare-specific valuation ratios.

Key fields: `pe_trailing`, `pe_forward`, `pb_ratio`, `ps_ratio`, `p_fcf`,
`ev_ebitda`, `ev_revenue`, `ev_gross_profit`, `ev_to_arr`, `ev_per_employee`,
`rule_of_40_adj_multiple`, `peg_ratio`, `dividend_yield`, `earnings_yield`,
`enterprise_value`, `market_cap`, `price_to_tangible_book`, `price_to_ncav`,
`cash_to_market_cap`.

#### `ProfitabilityMetrics`

Margins and returns, plus healthcare-specific profitability metrics.

Key fields: `roe`, `roa`, `roic`, `gross_margin`, `operating_margin`,
`net_margin`, `fcf_margin`, `ebitda_margin`, `rule_of_40`, `rule_of_40_ebitda`,
`magic_number`, `gaap_vs_adj_gap`, `sbc_to_revenue`, `sbc_to_fcf`.

#### `SolvencyMetrics`

Balance sheet health and cash survival metrics (crucial for clinical-stage biotech).

Key fields: `debt_to_equity`, `debt_to_ebitda`, `current_ratio`, `quick_ratio`,
`interest_coverage`, `altman_z_score`, `net_debt`, `total_debt`, `total_cash`,
`cash_burn_rate`, `cash_runway_years`, `working_capital`, `cash_per_share`,
`tangible_book_value`, `ncav`, `ncav_per_share`, `quarterly_burn_rate`,
`burn_as_pct_of_market_cap`, `cash_coverage_months`, `capex_to_revenue`,
`rpo_coverage`, `goodwill_to_assets`, `deferred_revenue_ratio`.

#### `GrowthMetrics`

Revenue, earnings, dilution, and healthcare-specific pipeline/innovation signals.

Key fields: `revenue_growth_yoy`, `revenue_cagr_3y`, `revenue_cagr_5y`,
`earnings_growth_yoy`, `earnings_cagr_3y`, `earnings_cagr_5y`,
`fcf_growth_yoy`, `book_value_growth_yoy`, `dividend_growth_5y`,
`shares_growth_yoy`, `shares_growth_3y_cagr`, `fully_diluted_shares`,
`dilution_ratio`, `arr_growth_yoy`, `net_revenue_retention`,
`gross_revenue_retention`, `rd_intensity`, `rd_growth_yoy`,
`sales_marketing_intensity`, `employee_growth_yoy`, `revenue_per_employee`,
`operating_leverage`.

#### `EfficiencyMetrics`

Operational efficiency ratios.

Key fields: `asset_turnover`, `inventory_turnover`, `receivables_turnover`,
`days_sales_outstanding`, `days_inventory`, `cash_conversion_cycle`,
`rule_of_x_score`, `cac_payback_months`, `fcf_conversion`.

#### `HealthQualityIndicators`

Composite quality score and qualitative assessments.

Key fields: `quality_score` (0-100), `management_quality`,
`insider_ownership_pct`, `founder_led`, `moat_assessment`, `moat_type`,
`competitive_position`, `rd_efficiency_assessment`, `unit_economics`,
`platform_position`, `financial_position`, `dilution_risk`,
`rule_of_40_assessment`, `sbc_risk_assessment`, `catalyst_density`,
`near_term_catalysts` (list), `revenue_predictability`,
`roic_history` (list), `gross_margin_history` (list).

#### `IntrinsicValue`

Intrinsic value estimates using multiple methods, adapted by stage.

Key fields: `dcf_value`, `graham_number`, `lynch_fair_value`, `ncav_value`,
`asset_based_value`, `ev_sales_implied_price`, `reverse_dcf_growth`,
`current_price`, `margin_of_safety_dcf`, `margin_of_safety_graham`,
`margin_of_safety_ncav`, `margin_of_safety_asset`, `margin_of_safety_ev_sales`,
`primary_method`, `secondary_method`.

The `primary_method` and `secondary_method` fields indicate which valuation
approach is most appropriate for the company's stage (e.g. `"DCF"` for
commercial-stage franchises, `"Cash Backing + Option Value"` for preclinical biotech).

#### `ShareStructure`

Share count, dilution, and ownership breakdown.

Key fields: `shares_outstanding`, `fully_diluted_shares`,
`warrants_outstanding`, `options_outstanding`, `rsu_outstanding`,
`insider_ownership_pct`, `institutional_ownership_pct`, `float_shares`,
`dual_class_structure`, `share_structure_assessment`, `sbc_overhang_risk`.

#### `MarketIntelligence`

Market sentiment, insider activity, institutional holdings, technicals,
projected dilution, and healthcare benchmark context (XLV + category ETF).

Key fields: `insider_transactions`, `net_insider_shares_3m`,
`insider_buy_signal`, `top_holders`, `institutions_count`,
`analyst_count`, `recommendation`, `target_high`, `target_low`,
`target_mean`, `target_upside_pct`, `shares_short`, `short_pct_of_float`,
`short_ratio_days`, `short_squeeze_risk`, `price_current`,
`price_52w_high`, `price_52w_low`, `sma_50`, `sma_200`, `beta`,
`projected_dilution_annual_pct`, `projected_shares_in_2y`,
`financing_warning`, `benchmark_name` (= `"Health Care Select Sector (XLV)"`),
`benchmark_ticker` (= `"XLV"`), `sector_etf_name`, `sector_etf_ticker`,
`peer_etf_name`, `peer_etf_ticker`, `risk_warnings`, `disclaimers`.

#### `FinancialStatement`

One annual fiscal period.

Key fields: `period`, `revenue`, `cost_of_revenue`, `gross_profit`,
`operating_income`, `net_income`, `ebitda`, `interest_expense`,
`total_assets`, `total_liabilities`, `total_equity`, `total_debt`,
`total_cash`, `current_assets`, `current_liabilities`,
`operating_cash_flow`, `capital_expenditure`, `free_cash_flow`,
`dividends_paid`, `shares_outstanding`, `eps`, `book_value_per_share`,
`research_development`, `selling_general_admin`, `stock_based_compensation`,
`deferred_revenue`, `goodwill`, `intangibles`.

#### `AnalysisConclusion`

Scored verdict produced by `generate_conclusion`.

Fields: `overall_score`, `verdict`, `summary`, `category_scores`,
`category_summaries`, `strengths`, `risks`, `tier_note`, `stage_note`,
`screening_checklist`.

#### `AnalysisReport`

The main container returned by analysis functions.

| Field | Type | Description |
|---|---|---|
| `profile` | `CompanyProfile` | Always populated. |
| `valuation` | `Optional[ValuationMetrics]` | Valuation ratios. |
| `profitability` | `Optional[ProfitabilityMetrics]` | Margin and return metrics. |
| `solvency` | `Optional[SolvencyMetrics]` | Balance sheet health. |
| `growth` | `Optional[GrowthMetrics]` | Growth rates, dilution, R&D intensity. |
| `efficiency` | `Optional[EfficiencyMetrics]` | Operational efficiency. |
| `health_quality` | `Optional[HealthQualityIndicators]` | Composite quality score. |
| `intrinsic_value` | `Optional[IntrinsicValue]` | Intrinsic value estimates. |
| `share_structure` | `Optional[ShareStructure]` | Share count and ownership. |
| `market_intelligence` | `Optional[MarketIntelligence]` | Sentiment, technicals, XLV benchmark. |
| `financials` | `list[FinancialStatement]` | Annual financial statements. |
| `filings` | `list[Filing]` | SEC filings. |
| `news` | `list[NewsArticle]` | Recent news articles. |
| `fetched_at` | `str` | ISO timestamp of when data was fetched. |

---

## Classification Helpers (`lynx_health.models`)

#### `classify_tier`

```python
def classify_tier(market_cap: Optional[float]) -> CompanyTier
```

Classify by market capitalization:

| Threshold | Tier |
|---|---|
| >= $200B | Mega Cap |
| >= $10B | Large Cap |
| >= $2B | Mid Cap |
| >= $300M | Small Cap |
| >= $50M | Micro Cap |
| < $50M or None | Nano Cap |

#### `classify_stage`

```python
def classify_stage(
    description: Optional[str],
    revenue: Optional[float],
    info: Optional[dict] = None,
) -> CompanyStage
```

Classify healthcare lifecycle stage by keyword matching (preclinical, Phase I-III,
commercial launch, diversified pharma, etc.) against the company description,
with fallback to market-cap and profit-margin heuristics.

#### `classify_category`

```python
def classify_category(
    description: Optional[str],
    industry: Optional[str] = None,
) -> HealthCategory
```

Identify primary healthcare sub-category (Big Pharma, Biotech, Medical Devices,
Health Providers, Health Insurance, Life Sciences Tools, Distribution,
Health IT, CRO/CDMO, Generic Pharma, Health Equipment) from description and
industry text using keyword frequency scoring.

#### `classify_jurisdiction`

```python
def classify_jurisdiction(
    country: Optional[str],
    description: Optional[str] = None,
) -> JurisdictionTier
```

Classify jurisdiction risk using a healthcare lens (FDA / EMA / PMDA approval
quality, drug-pricing stability, reimbursement predictability, IP protection):

- **Tier 1:** USA, Canada, UK, Ireland, Germany, France, Netherlands, Switzerland, Japan, South Korea, Singapore, Israel, Australia, New Zealand, Nordics.
- **Tier 2:** Spain, Portugal, Italy, Hong Kong, Taiwan, India, Brazil, Mexico, South Africa, Chile, Uruguay, Turkey, Eastern European EU members.
- **Tier 3:** Everything else.

---

## Metrics Calculator (`lynx_health.metrics.calculator`)

All `calc_*` functions accept `info` (yfinance info dict), `statements`
(list of `FinancialStatement`), and tier/stage classification.  They return
the corresponding metrics dataclass with all fields computed from available
data.

| Function | Returns | Description |
|---|---|---|
| `calc_valuation(info, statements, tier, stage)` | `ValuationMetrics` | P/E, P/B, EV/EBITDA, P/FCF, EV/GP, EV/ARR, EV/Employee, R40-adjusted EV/Rev. |
| `calc_profitability(info, statements, tier, stage)` | `ProfitabilityMetrics` | ROE, ROA, ROIC, margins, Rule-of-40 (FCF & EBITDA), Magic Number, SBC ratios. |
| `calc_solvency(info, statements, tier, stage)` | `SolvencyMetrics` | D/E, current/quick ratios, Altman Z, **cash burn rate, cash runway**, goodwill-to-assets, deferred revenue / RPO coverage, capex intensity. |
| `calc_growth(statements, tier, stage, info)` | `GrowthMetrics` | Revenue/earnings/FCF growth YoY and CAGR (3y, 5y). Share dilution. **R&D intensity** (the healthcare innovation metric). Revenue/employee. |
| `calc_efficiency(info, statements, tier)` | `EfficiencyMetrics` | Asset turnover, Rule-of-X, CAC payback (health IT), FCF conversion. |
| `calc_share_structure(info, statements, growth, tier, stage)` | `ShareStructure` | Outstanding/fully-diluted shares, insider/institutional ownership %, SBC overhang risk. |
| `calc_health_quality(profitability, growth, solvency, share_structure, statements, info, tier, stage)` | `HealthQualityIndicators` | Composite quality score (0-100) on 7 axes: moat/gross-margin (20pts), Rule-of-40 (20pts), financial position (15pts), dilution/SBC (15pts), R&D efficiency (10pts), unit economics (10pts), revenue predictability (10pts). |
| `calc_intrinsic_value(info, statements, growth, solvency, tier, stage)` | `IntrinsicValue` | DCF, Graham number, Lynch fair value, NCAV, asset-based value, EV/Sales implied, Reverse DCF. Method selection is stage-aware. |
| `calc_market_intelligence(info, ticker_obj, solvency, share_structure, growth, tier, stage)` | `MarketIntelligence` | Insider transactions, institutional holders, analyst consensus, short interest, price technicals, projected dilution, **XLV + sub-sector ETF (XBI / IBB / XPH / IHE / IHI / XHE / IHF / XHS / VHT)** benchmark context. |

---

## Relevance System (`lynx_health.metrics.relevance`)

#### `get_relevance`

```python
def get_relevance(
    metric_key: str,
    tier: CompanyTier,
    category: str = "valuation",
    stage: CompanyStage = CompanyStage.GROWTH,
) -> Relevance
```

Look up the relevance level of a metric given the company's tier and stage.

**Stage overrides take precedence** over tier-based lookups, because
lifecycle stage is the primary analytical axis for Healthcare companies.

**Stage-driven examples:**

- `cash_runway_years` is `CRITICAL` for clinical-stage biotech (`STARTUP`, `GROWTH`); `CONTEXTUAL` for Commercial; `IRRELEVANT` for Diversified Franchise.
- `pe_trailing` is `IRRELEVANT` for preclinical / clinical-stage biotech; `CRITICAL` for Commercial and Diversified Franchise.
- `shares_growth_yoy` is `CRITICAL` for clinical biotech (heavy dilution); `IMPORTANT` for Diversified Franchise (buybacks).
- `rd_intensity` is `IMPORTANT` across every stage — it is the healthcare innovation signal.

---

## Storage (`lynx_health.core.storage`)

Two isolated data directories: `data/` (production) and `data_test/` (testing).

#### `set_mode`

```python
def set_mode(mode: str) -> None
```

Set the storage mode.  `mode` must be `"production"` or `"testing"`.

In testing mode, cache reads are disabled (always returns `None`/`False`)
to ensure fresh data.

#### `has_cache` / `load_cached_report` / `save_analysis_report` / `list_cached_tickers` / `drop_cache_ticker` / `drop_cache_all`

Standard cache management helpers — same API as in other Lynx sector kits.

---

## Ticker Resolution (`lynx_health.core.ticker`)

#### `resolve_identifier`

```python
def resolve_identifier(identifier: str) -> tuple[str, str | None]
```

Resolve a user-provided identifier to a `(ticker, isin)` tuple.

Accepts:
- **Ticker symbols:** `JNJ`, `MRNA`, `RHHBY`, `NVS`
- **ISIN codes:** `US4781601046` (Johnson & Johnson), `US60770K1079` (Moderna)
- **Company names:** `"Johnson & Johnson"`, `"Vertex Pharmaceuticals"`, `"Medtronic"`

Resolution strategy:
1. ISIN -- search via yfinance, return best equity match.
2. Company name (contains spaces or > 12 chars) -- search.
3. Direct ticker probe -- check if the symbol has price data.
4. Suffix scan -- try common exchange suffixes (`.L`, `.SW`, `.DE`, etc. for European pharma).
5. Broadened search -- append "stock" or "corp" to query.

Raises `ValueError` if no match is found.

---

## Export (`lynx_health.export`)

#### `export_report`

```python
def export_report(
    report: AnalysisReport,
    fmt: ExportFormat,
    output_path: Optional[Path] = None,
) -> Path
```

Export an analysis report to TXT, HTML or PDF.

```python
from lynx_health.export import ExportFormat
```

---

## Sector Insights (`lynx_health.metrics.sector_insights`)

#### `get_sector_insight`

Returns sector-level analysis guidance.  Available sector: `"Healthcare"`.

#### `get_industry_insight`

Returns industry-level analysis guidance.  Available industries:
`"Drug Manufacturers - General"` (Big Pharma), `"Biotechnology"`,
`"Drug Manufacturers - Specialty & Generic"`, `"Medical Devices"`,
`"Medical Instruments & Supplies"`, `"Medical Care Facilities"`,
`"Healthcare Plans"` (managed care / insurance),
`"Medical Devices - Life Sciences Tools"`, `"Diagnostics & Research"`,
`"Medical Distribution"`, `"Health Information Services"`,
`"Pharmaceutical Retailers"`.

---

## Usage Examples

### 1. Basic Analysis

```python
from lynx_health.core.analyzer import run_full_analysis
from lynx_health.core.conclusion import generate_conclusion

report = run_full_analysis("JNJ")

print(f"{report.profile.name} ({report.profile.ticker})")
print(f"Tier: {report.profile.tier.value}")
print(f"Stage: {report.profile.stage.value}")
print(f"Healthcare Category: {report.profile.health_category.value}")
print(f"Jurisdiction: {report.profile.jurisdiction_tier.value}")

conclusion = generate_conclusion(report)
print(f"Score: {conclusion.overall_score}/100 -- {conclusion.verdict}")
```

### 2. Progressive Analysis with Callback

```python
from lynx_health.core.analyzer import run_progressive_analysis

def progress_handler(stage: str, report):
    if stage == "profile":
        print(f"Analyzing: {report.profile.name}")
    elif stage == "solvency":
        runway = report.solvency.cash_runway_years
        if runway is not None:
            print(f"Cash runway: {runway:.1f} years")
    elif stage == "complete":
        print("Analysis complete.")

report = run_progressive_analysis("MRNA", on_progress=progress_handler)
```

### 3. Accessing Specific Metrics

```python
report = run_full_analysis("PFE")

# Profitability — key anchors for commercial pharma
if report.profitability:
    print(f"Gross margin: {report.profitability.gross_margin:.1%}")
    print(f"Operating margin: {report.profitability.operating_margin:.1%}")
    print(f"FCF margin: {report.profitability.fcf_margin:.1%}")

# Growth — R&D intensity is the healthcare innovation signal
if report.growth:
    rd = report.growth.rd_intensity
    print(f"R&D intensity: {rd:.1%}")  # 18-22% typical for Big Pharma

# Solvency — crucial for biotech
report_bio = run_full_analysis("BEAM")
if report_bio.solvency:
    print(f"Cash: ${report_bio.solvency.total_cash:,.0f}")
    print(f"Burn rate: ${report_bio.solvency.cash_burn_rate:,.0f}/yr")
    print(f"Runway: {report_bio.solvency.cash_runway_years:.1f} years")

# Market intelligence
if report.market_intelligence:
    mi = report.market_intelligence
    print(f"Benchmark: {mi.benchmark_name}")  # "Health Care Select Sector (XLV)"
    print(f"Sub-sector ETF: {mi.sector_etf_name} ({mi.sector_etf_ticker})")
```

### 4. Checking Metric Relevance

```python
from lynx_health.metrics.relevance import get_relevance
from lynx_health.models import CompanyTier, CompanyStage, Relevance

# Clinical-stage biotech — runway is critical, P/E is irrelevant
tier = CompanyTier.SMALL
stage = CompanyStage.STARTUP

rel = get_relevance("cash_runway_years", tier, "solvency", stage)
assert rel == Relevance.CRITICAL

rel = get_relevance("pe_trailing", tier, "valuation", stage)
assert rel == Relevance.IRRELEVANT

rel = get_relevance("rd_intensity", tier, "growth", stage)
assert rel == Relevance.IMPORTANT
```

### 5. Exporting Reports

```python
from pathlib import Path
from lynx_health.core.analyzer import run_full_analysis
from lynx_health.export import ExportFormat, export_report

report = run_full_analysis("LLY")

# Export as HTML (default path: data/LLY/report_<timestamp>.html)
html_path = export_report(report, ExportFormat.HTML)
print(f"HTML report: {html_path}")

# Export as plain text to a custom path
txt_path = export_report(report, ExportFormat.TXT, Path("./lly_report.txt"))
print(f"Text report: {txt_path}")

# Export as PDF
pdf_path = export_report(report, ExportFormat.PDF)
print(f"PDF report: {pdf_path}")
```
