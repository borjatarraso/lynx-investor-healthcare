# Changelog

All notable changes to Lynx Healthcare Analysis are documented here.

## [3.0] - 2026-04-22

Part of **Lince Investor Suite v3.0** coordinated release.

### Added
- Uniform PageUp / PageDown navigation across every UI mode (GUI, TUI,
  interactive, console). Scrolling never goes above the current output
  in interactive and console mode; Shift+PageUp / Shift+PageDown remain
  reserved for the terminal emulator's own scrollback.
- Sector-mismatch warning now appends a `Suggestion: use
  'lynx-investor-<other>' instead.` line sourced from
  `lynx_investor_core.sector_registry`. The original warning text is
  preserved as-is.

### Changed
- TUI wires `lynx_investor_core.pager.PagingAppMixin` and
  `tui_paging_bindings()` into the main application.
- Graphical mode binds `<Prior>` / `<Next>` / `<Control-Home>` /
  `<Control-End>` via `bind_tk_paging()`.
- Interactive mode pages long output through `console_pager()` /
  `paged_print()`.
- Depends on `lynx-investor-core>=2.0`.

## [2.0] - 2026-04-22

Initial release of **Lynx Healthcare Analysis**, part of the **Lince Investor Suite v2.0**.

### Added
- **Healthcare-specific lifecycle stages**: Preclinical / Early-Stage Biotech, Clinical / Hyper-Growth, Launch / Scale-Up, Commercial / Cash-Generative, Diversified Healthcare Franchise
- **Healthcare sub-category classification**: Large Pharmaceuticals, Biotechnology, Generic & Specialty Pharma, Medical Devices, Healthcare Equipment & Supplies, Healthcare Providers & Services, Managed Care / Health Insurance, Life Sciences Tools & Diagnostics, Healthcare Distribution, Health IT / Digital Health, CRO / CDMO
- **Healthcare-specific valuation metrics**: EV/Gross-Profit, EV/ARR (for health IT), EV/Employee, Rule-of-40-Adjusted EV/Revenue
- **Healthcare-specific profitability metrics**: Rule of 40 (FCF & EBITDA variants — for digital-health SaaS peers), Magic Number (sales efficiency for health IT), SBC/Revenue, SBC/FCF, GAAP-vs-Adjusted gap
- **Healthcare-specific growth & pipeline signals**: R&D intensity (the primary pharma/biotech innovation metric), R&D growth, SG&A intensity, Revenue per Employee, ARR growth (approx via deferred revenue), slots for NRR and GRR for health-IT names
- **Healthcare-specific solvency metrics**: Cash runway & burn rate (critical for clinical-stage biotech), Capex/Revenue, Deferred Revenue / RPO Coverage, Goodwill-to-Assets (post-M&A impairment risk), Cash Coverage (months)
- **Healthcare-specific efficiency metrics**: Rule of X (Altimeter), CAC Payback Months (for health IT), FCF Conversion
- **Healthcare Quality scoring**: Moat/Gross-Margin calibrated to healthcare bands (20pts), Rule-of-40 (20pts), Financial Position / Runway (15pts), Dilution+SBC (15pts), R&D Efficiency (10pts), Unit Economics (10pts), Revenue Predictability (10pts)
- **Severity system with 5 levels**: `***CRITICAL***` (red uppercase), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Impact column** on every metric table: Critical (blinking red), Important (orange), Relevant (yellow), Informational (green), Irrelevant (silver)
- **Healthcare sector validation gate**: refuses to analyze non-healthcare companies with prominent red-blinking warning and routing hint to sibling Lynx specialists
- **Healthcare benchmark context**: **XLV (Health Care Select Sector SPDR)** headline benchmark + sub-sector ETFs (XBI, IBB, XPH, IHE, IHI, XHE, IHF, XHS, VHT) based on detected healthcare category
- **Healthcare investment disclaimers**: FDA / payer catalyst risk, Phase III failure rates, IRA price-negotiation exposure, patent-cliff / biosimilar erosion, MLR sensitivity for insurers, binary biotech valuations
- **Intrinsic value adapted per stage**: DCF for platform/commercial, EV/Gross-Profit for scale-up/launch, Reverse DCF for all, Cash-backing floor + option value for preclinical biotech
- **Healthcare-specific test fixtures** (Pharmaceuticals Corp, Biotech profile, Clinical-stage Hyper-Growth)

### Changed (vs Information Technology predecessor)
- Package renamed `lynx_tech` → `lynx_health`
- CLI command renamed `lynx-tech` → `lynx-health`
- `CompanyStage` values retuned to healthcare lifecycle (Preclinical / Clinical / Launch / Commercial / Diversified Franchise)
- `TechCategory` enum replaced with `HealthCategory` (Big Pharma, Biotech, Generic Pharma, Medical Devices, Health Equipment, Health Providers, Health Insurance, Life Sciences Tools, Health Distribution, Health IT, CRO/CDMO)
- `TechQualityIndicators` dataclass renamed to `HealthQualityIndicators`
- `tech_category` field renamed to `health_category`
- Jurisdiction tiers adapted to healthcare lens (FDA / EMA / PMDA approval quality, drug-pricing stability, reimbursement predictability, IP protection)
- Tech-specific benchmark (QQQ) replaced with Healthcare Benchmark (XLV) and category-specific ETFs (XBI/IBB for biotech, XPH/IHE for pharma, IHI/XHE for devices, IHF/XHS for services/insurers)
- Sector-validation gate retargeted from IT to Healthcare (biotech/pharma/devices/providers/insurers/tools/distribution/health IT/CROs/CDMOs)
- Sector & industry insights rewritten for healthcare peers (Big Pharma, Biotech, Generic Pharma, Medical Devices, Medical Instruments, Medical Care Facilities, Healthcare Plans, Life Sciences Tools, Diagnostics & Research, Medical Distribution, Health Information Services, Pharmaceutical Retailers)

### Retained (from common architecture)
- Progressive rendering across four UI modes (Console, Interactive REPL, Textual TUI, Tkinter GUI)
- Rich-powered tables with relevance-based styling
- TXT / HTML / PDF export (with healthcare-adapted tables and sections)
- Local caching (production mode) and isolated testing mode (`data/` vs `data_test/`)
- SEC filings fetcher
- News fetcher (Yahoo Finance + Google News RSS)
- ISIN resolution, exchange-suffix search, and ticker validation
- BSD-3-Clause license, suite branding, ASCII logo support
