# Development Guide

## Architecture

The application shares core architecture with other Lynx specialists (Information Technology, Basic Materials, Energy, etc.) but applies healthcare-specific domain logic end-to-end.

### Data Flow

```
User Input (ticker/ISIN/name)
    ↓
CLI/Interactive/TUI/GUI → cli.py
    ↓
analyzer.py: run_progressive_analysis()
    ↓
ticker.py: resolve_identifier() → (ticker, isin)
    ↓
storage.py: check cache → return if cached
    ↓
fetcher.py: yfinance data (profile + financials, incl. R&D, SBC, deferred revenue, goodwill)
    ↓
models.py: classify_stage / classify_category (HealthCategory) / classify_jurisdiction
    ↓
calculator.py: calc_valuation / profitability / solvency / growth / efficiency
    ↓
calculator.py: calc_share_structure + calc_health_quality
    ↓
calculator.py: calc_market_intelligence (insider, analyst, short, technicals, XLV + sub-sector ETF)
    ↓
calculator.py: calc_intrinsic_value (DCF, EV/Sales peer, Reverse DCF, cash-backing floor for biotech)
    ↓
[parallel] reports.py + news.py
    ↓
conclusion.py: generate_conclusion() → verdict + 10-point healthcare screening
    ↓
storage.py: save_analysis_report()
    ↓
display.py / tui/app.py / gui/app.py / export/* → render with severity + impact columns
```

### Key Design Decisions

1. **Stage > Tier**: Healthcare lifecycle stage (Preclinical → Clinical → Launch → Commercial → Diversified Franchise) is the primary analysis axis. The relevance system prioritizes stage overrides.

2. **R&D intensity as innovation anchor**: For pharma and biotech, R&D spending as % of revenue is the single best proxy for innovation commitment. Branded pharma runs 18-22%; mid-cap biotech 40-80%; clinical-stage biotech often >150% (R&D exceeds revenue).

3. **Cash runway as survival anchor (biotech)**: For clinical-stage biotech, cash runway years is the dominant metric. <1yr = imminent financing (dilution expected); 1-2yr = secondary offering within 12m likely; >3yr = comfortable runway to the next catalyst.

4. **Rule of 40 for digital health only**: The Rule of 40 (revenue growth % + FCF margin %) is meaningful for health-IT / digital-health SaaS peers, not for pharma or providers. The calculator computes both FCF and EBITDA variants but relevance gates where it matters.

5. **SBC as structural dilution**: Healthcare SBC is heavy in biotech (a typical clinical-stage biotech spends 15-30% of revenue on SBC). We compute SBC/Revenue and SBC/FCF to expose the "paper vs cash" gap.

6. **Gross margin = category fingerprint**: Gross margin bands classify healthcare business models — branded pharma / biologics >80%, devices 65-75%, generics 50-60%, providers 30-40%, distribution 3-5%.

7. **Severity + Impact dual-axis display**: Every metric row shows BOTH a severity tag (how bad is this reading?) and an impact column (how much does this metric matter for this stage?). The two are independent.

8. **Progressive Rendering**: The analyzer emits progress callbacks so UIs can render sections as data arrives.

9. **Reverse DCF sanity check**: We compute the growth rate implied by the current price to spot priced-in expectations.

10. **Benchmark = XLV + sub-sector ETF**: Headline benchmark is XLV (Health Care Select Sector SPDR). The sub-sector ETF rotates by detected `HealthCategory` — XBI/IBB for biotech, XPH/IHE for pharma, IHI/XHE for devices, IHF/XHS for providers and insurers, VHT for the broad default.

### Adding New Metrics

1. Add field to the appropriate dataclass in `models.py`
2. Calculate in `calculator.py` (in the relevant `calc_*` function)
3. Add relevance entry in `relevance.py` (`_STAGE_OVERRIDES` and tier tables)
4. Add explanation in `explanations.py`
5. Add display row in `display.py`, `tui/app.py`, `gui/app.py`
6. Add export row in `export/html_export.py` and `export/txt_export.py`

### Adding New Healthcare Categories

1. Add to `HealthCategory` enum in `models.py`
2. Add keywords to `_CATEGORY_KEYWORDS`
3. Add sub-sector ETFs to `_CATEGORY_ETFS` in `calculator.py`
4. Add industry insight in `sector_insights.py`

### Adding New Stages

1. Add to `CompanyStage` enum
2. Add keywords to `_STAGE_KEYWORDS` in `models.py`
3. Add weights to `_WEIGHTS` in `conclusion.py`
4. Add relevance overrides in `relevance.py`
5. Update method selection in `calc_intrinsic_value`

## Running Tests

```bash
# Python unit tests
pytest tests/ -v --tb=short

# Robot Framework (requires robotframework)
pip install robotframework
robot --outputdir results robot/

# Syntax check all files
python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('lynx_health/**/*.py', recursive=True)]"
```

## Code Style

- Python 3.10+ with type hints
- Dataclasses for all data models
- Rich for console rendering
- Textual for TUI
- Tkinter for GUI (dark theme)

## Severity & Impact System

The dual-axis display is implemented in `lynx_health/display.py`:

- `_SEVERITY_FMT` → maps `Severity.*` to `[color]***CRITICAL***[/]`, `[color]*WARNING*[/]`, `[color][WATCH][/]` etc.
- `_IMPACT_DISPLAY` → maps `Relevance.*` to `[blink bold red]Critical[/]`, `[#ff8800]Important[/]`, etc.

Both are shown as separate columns in every metric table, alongside the Value and Assessment columns.
