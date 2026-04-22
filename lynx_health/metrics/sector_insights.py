"""Healthcare-focused sector and industry insights."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SectorInsight:
    sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

@dataclass
class IndustryInsight:
    industry: str; sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

_SECTORS: dict[str, SectorInsight] = {}
_INDUSTRIES: dict[str, IndustryInsight] = {}

def _add_sector(sector, overview, cm, kr, wtw, tv):
    _SECTORS[sector.lower()] = SectorInsight(sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)

def _add_industry(industry, sector, overview, cm, kr, wtw, tv):
    _INDUSTRIES[industry.lower()] = IndustryInsight(industry=industry, sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)


_add_sector("Healthcare",
    "Healthcare is a defensive, long-duration sector driven by demographics (aging populations), scientific innovation, and regulatory/reimbursement dynamics rather than macro cyclicality. It spans extremes: profitable, cash-rich Big Pharma and integrated insurers on one side; pre-revenue biotechs where a single Phase III readout can double or destroy equity value on the other. Valuation discipline must therefore be stage-aware — DCF works for commercial-stage pharma; risk-adjusted pipeline NPV and cash runway dominate for biotech. Regulatory risk (FDA/EMA approval probability, drug-pricing legislation, reimbursement codes, 340B / IRA exposure) is first-order alongside patent-cliff and biosimilar/generic erosion.",
    ["R&D intensity (R&D/Revenue)", "Gross margin (moat proxy, drug vs services)", "Cash runway (biotech survival)", "Operating margin (commercial ops)", "Patent cliff exposure", "Medical Loss Ratio (insurers)", "Pipeline count & phase mix"],
    ["Patent cliff & loss of exclusivity (LOE) on key franchises", "Clinical-trial failures (Phase III) destroying pipeline value", "Drug-pricing legislation (IRA negotiation, 340B expansion)", "Payer denials & reimbursement code changes", "FDA regulatory delays / CRLs (Complete Response Letters)", "Biosimilar / generic erosion accelerating", "Integration risk on large biopharma M&A", "Utilization spikes or declines hitting insurer MLRs"],
    ["Phase III / FDA calendar for near-term catalysts", "Biosimilar launch timing vs reference franchises", "Payer formulary & CMS reimbursement decisions", "IRA price-negotiation list updates", "Hospital utilization trends (inpatient admissions, procedures)", "M&A cadence (pharma pipeline replenishment)"],
    "EV/EBITDA 10-16x for Big Pharma; 18-30x for med-devices & life-sciences tools; P/E 10-14x for managed-care. Biotech is valued on risk-adjusted NPV of pipeline + cash per share, not near-term earnings.")

# ── Large Pharma ──────────────────────────────────────────────────
_add_industry("Drug Manufacturers - General", "Healthcare",
    "Large / diversified pharmaceutical manufacturers (Pfizer, Merck, Johnson & Johnson, Novartis, AstraZeneca). High-margin, cash-generative, acquisition-active. Value comes from a balanced portfolio of blockbuster drugs offsetting patent cliffs with a replenished pipeline. Share of GLP-1, oncology, immunology, and rare-disease franchises drives next-decade valuation.",
    ["R&D Intensity (typical 18-22%)", "Operating Margin (target >25%)", "Free Cash Flow Margin (>25%)", "Patent Cliff % of revenue in 5 years", "Pipeline Phase III count", "ROIC (>12% for quality)"],
    ["Patent expirations & biosimilar entry on blockbusters", "Clinical trial setbacks in lead pipeline assets", "US drug-pricing pressure (Medicare Part D negotiation)", "FX exposure for multinational revenue", "Pipeline productivity dilution from M&A goodwill"],
    ["Pipeline readouts (Phase II/III)", "Biosimilar launch calendar", "R&D productivity (peak sales / $ spent)", "Dividend coverage & buyback pace", "M&A cadence in oncology/obesity/immunology"],
    "EV/EBITDA 10-14x; P/E 12-18x; 2-4% dividend yield. Premium for GLP-1 / oncology exposure.")

# ── Biotech ───────────────────────────────────────────────────────
_add_industry("Biotechnology", "Healthcare",
    "Clinical-stage & early-commercial biotechs. Binary outcome franchises — a Phase III result or FDA decision can move equity 50-200%. Value is driven by risk-adjusted NPV of pipeline assets, cash runway to next catalyst, and quality of the science (MoA novelty, biomarker selection, trial design). Preclinical platforms trade on technology moat and TAM optionality.",
    ["Cash Runway (months to next catalyst)", "Burn Rate (quarterly)", "R&D Intensity (often >80% of opex)", "Pipeline count by Phase", "Lead asset probability of technical success (PTS)", "Insider/VC ownership"],
    ["Phase III clinical failure (~35% fail at Phase III)", "FDA Complete Response Letter or refuse-to-file", "Dilutive equity / convertible financing at market bottoms", "Platform-level safety signals (gene/cell-therapy class-effect risk)", "Milestone/royalty-partner renegotiation", "IP challenges (IPR / Paragraph IV)"],
    ["Quarterly burn vs cash runway", "Catalyst calendar (next 6-12 months)", "Insider transactions around readouts", "Peer-asset readouts (class-effect read-through)", "Institutional accumulation ahead of catalysts"],
    "Pre-revenue: cash-backing floor + risk-adjusted pipeline NPV. Commercial biotechs: EV/Sales 5-15x at launch, compressing to 3-6x at peak. Avoid P/E until mature.")

_add_industry("Drug Manufacturers - Specialty & Generic", "Healthcare",
    "Generic pharmaceutical, specialty pharma, and biosimilar manufacturers (Teva, Viatris, Sandoz, Fresenius Kabi). Lower margins (55-65% gross) and valuations than branded pharma. Economics depend on launch cadence of first-to-file generics, biosimilar manufacturing scale, and working-capital turnover. Political pressure (rebate reform, PBM changes) drives earnings volatility.",
    ["Gross Margin (55-65% typical)", "Revenue Growth (2-6%)", "Leverage (Net Debt / EBITDA <3x)", "First-to-file generic launches", "Biosimilar manufacturing scale"],
    ["Price deflation in core generics (-5 to -10%/yr)", "PBM pricing pressure / formulary exclusions", "Biosimilar competitive erosion (more players per molecule)", "FDA CGMP remediation risk for legacy plants", "High leverage from prior M&A"],
    ["New ANDA approvals & exclusivity periods", "Biosimilar market share trajectory vs reference drug", "FDA inspection outcomes on legacy facilities", "Litigation reserves (opioid, antitrust)"],
    "EV/EBITDA 6-9x; P/E 8-12x; dividend yields 3-6% for mature names.")

# ── Medical Devices ───────────────────────────────────────────────
_add_industry("Medical Devices", "Healthcare",
    "Medical-device manufacturers (Medtronic, Stryker, Boston Scientific, Edwards Lifesciences, Intuitive Surgical). High gross margins (65-75%), strong mid-single-digit organic growth, and predictable procedure-volume leverage. Approval pathways shorter than drugs (510(k), PMA) but require recurring capex, robust post-market surveillance, and FDA MDR/EU MDR compliance.",
    ["Organic Revenue Growth (target 4-8%)", "Gross Margin (65-75%)", "Operating Margin (>20%)", "FCF Conversion (>80%)", "New-product revenue %"],
    ["Procedure-volume shocks (COVID-style deferrals)", "FDA inspection / MDR / UDI compliance gaps", "Category disruption from AI-enabled or robotic competitors", "Reimbursement code downgrades (CMS)", "Tariff / supply-chain disruption on components"],
    ["Hospital capex indicators", "Procedure-volume trends (elective vs emergent)", "FDA clearances (510(k)) & MDR progress in EU", "New-launch adoption curves", "M&A to refresh portfolio"],
    "EV/EBITDA 15-22x; P/E 18-28x; dividend yields 1-3% for mature platforms.")

_add_industry("Medical Instruments & Supplies", "Healthcare",
    "Durable medical equipment, single-use consumables, surgical instruments, and hospital supplies (Becton Dickinson, Baxter, Cardinal Health's medical segment). Lower margins than high-tech devices but very recurring revenue (consumable / razor-blade models).",
    ["Consumables Mix (higher = better)", "Gross Margin (40-55%)", "Operating Margin (15-22%)", "Inventory Turns", "Days Sales Outstanding"],
    ["Commoditization in disposables", "Distributor consolidation compressing margin", "Raw-material inflation (resin, metals)", "FDA quality-system warnings"],
    ["Hospital capex & procedure trends", "Distributor inventory de-stocking cycles", "Input-cost trends"],
    "EV/EBITDA 10-14x; P/E 15-20x.")

# ── Healthcare Providers ──────────────────────────────────────────
_add_industry("Medical Care Facilities", "Healthcare",
    "Hospitals, health systems, dialysis chains, surgical centers, outpatient clinics (HCA, Tenet, DaVita, Fresenius, Encompass). Volume × price business. Payer mix (commercial vs Medicare vs Medicaid) drives profitability. Labor is the largest cost line — wage inflation flows through instantly.",
    ["Admissions / Procedure Volume Growth", "Revenue per Adjusted Admission", "Payer Mix %", "Salaries/Wages as % of Revenue", "Days Cash on Hand", "Occupancy / Utilization"],
    ["Wage inflation (travel nurses, RN shortages)", "Medicare/Medicaid reimbursement cuts", "Payer denials / billing disputes", "340B program changes", "Cybersecurity incidents on EHR / systems", "Uncompensated-care growth during downturns"],
    ["Same-facility admissions growth", "Labor costs / contract labor trends", "Payer mix shifts (commercial vs government)", "CMS reimbursement updates", "Capex plans for capacity"],
    "EV/EBITDA 8-12x; P/E 10-16x; highly leverage-sensitive. Watch interest-coverage.")

# ── Healthcare Insurance / Managed Care ───────────────────────────
_add_industry("Healthcare Plans", "Healthcare",
    "Managed-care organizations and health insurers (UnitedHealth, Elevance, Humana, CVS/Aetna, Cigna, Molina, Centene). Revenue is premiums plus PBM services. Profitability hinges on medical loss ratio (MLR) — the % of premiums spent on claims — and utilization trends. Medicare Advantage growth is the single biggest multi-year driver; regulatory scrutiny on MA coding and Star Ratings is elevated.",
    ["Medical Loss Ratio (target 80-87%)", "Member Growth (MA, Commercial, Medicaid)", "Operating Margin (4-8%)", "PBM Scripts Growth", "Medical Cost Trend", "Star Ratings (Medicare Advantage)"],
    ["Utilization spikes (COVID-tail, elective demand) lifting MLR", "Medicare Advantage Star Rating downgrades", "CMS rate cuts on MA payments", "Risk-adjustment audit / RADV clawbacks", "PBM regulatory reform (rebate rule, pass-through)", "State Medicaid redeterminations reducing membership"],
    ["MLR trajectory quarter-over-quarter", "Medicare Advantage enrollment growth", "Star Ratings for next bid cycle", "PBM client retention & new wins", "Regulatory updates (CMS, state DOIs)"],
    "P/E 10-14x; EV/EBITDA 7-10x; dividend yields 1-2%. Sensitive to MLR surprises.")

# ── Life Sciences Tools ───────────────────────────────────────────
_add_industry("Medical Devices - Life Sciences Tools", "Healthcare",
    "Research instruments, bioprocessing, diagnostics and tools suppliers (Thermo Fisher, Danaher, Agilent, Waters, Bio-Techne, Illumina, Bio-Rad). Picks-and-shovels to pharma/biotech R&D plus clinical labs. High quality franchises with 55-65% gross margin, 20-30% operating margin, and significant consumables recurring revenue.",
    ["Organic Revenue Growth (target 5-9%)", "Gross Margin (55-65%)", "Operating Margin (20-30%)", "Consumables Mix (target >60%)", "Bioprocessing Orders Growth"],
    ["Biotech funding cycle → tools demand compression", "China stimulus / anti-corruption affecting lab demand", "Customer concentration in top-20 pharma", "FX translation on Europe-heavy revenue bases"],
    ["Biotech IPO & VC funding trends", "Bioprocessing order books (multi-year backlog)", "China stimulus program funding", "Diagnostics volume normalization post-COVID"],
    "EV/EBITDA 15-22x; P/E 20-30x for highest-quality franchises.")

_add_industry("Diagnostics & Research", "Healthcare",
    "Clinical laboratories, reference labs, specialty-diagnostic firms (LabCorp, Quest, Natera, Exact Sciences, Guardant, Myriad). Revenue driven by test volumes + reimbursement per test. Many rely on concentrated payer mix and CMS reimbursement codes. Genetic testing and liquid-biopsy franchises have high growth but capital-intensive commercial ramps.",
    ["Test Volume Growth", "Price per Test (PAMA sensitivity)", "Gross Margin (35-50%)", "FCF margin", "Cash runway for specialty diagnostics"],
    ["PAMA reimbursement cuts on routine tests", "Payer denial rates on specialty tests", "Specialty-diagnostic cash burn ahead of breakeven", "Medicare coverage determinations (LCD/NCD)"],
    ["Molecular / specialty-test volume growth", "Payer mix for new tests", "CMS / MAC coverage decisions", "Insurance coverage progress for liquid-biopsy panels"],
    "Reference labs: EV/EBITDA 9-12x. Specialty diagnostics: EV/Revenue 5-12x until breakeven.")

# ── Drug Distribution ─────────────────────────────────────────────
_add_industry("Medical Distribution", "Healthcare",
    "Drug & medical distributors (McKesson, Cencora/AmerisourceBergen, Cardinal Health). Large-scale, low-margin (gross ~3-5%), operating margin ~1.5-2.5%, but enormous working-capital efficiency and recurring volumes. Upside from specialty-pharmacy and GLP-1 distribution mix. Opioid-litigation overhang is largely resolved but ongoing.",
    ["Revenue Growth (3-6%)", "Operating Margin (1.5-2.5%)", "Cash Conversion Cycle", "Generic launch cadence (margin driver)", "Specialty Drug Mix"],
    ["Generic deflation beyond historical -3%", "Contract losses to retail consolidations", "Residual opioid-litigation reserves", "Specialty-biosimilar deflation"],
    ["Specialty-pharmacy volume growth", "GLP-1 distribution margin contribution", "Generic launch calendar", "Retail pharmacy consolidation"],
    "EV/EBITDA 9-12x; P/E 13-17x; 1-2% dividend yield.")

# ── Health IT / Digital Health ────────────────────────────────────
_add_industry("Health Information Services", "Healthcare",
    "Health IT, EHR vendors, digital health platforms, revenue-cycle management (Veeva, Oracle Health / Cerner, Doximity, Evolent, HealthEquity). SaaS economics applied to healthcare verticals. Rule-of-40 and NRR matter; regulatory (HIPAA, interoperability rules) and hospital IT-budget cycles shape demand.",
    ["ARR Growth (15-25%)", "Gross Margin (65-75%)", "Rule of 40", "NRR (target >110%)", "Customer retention (logos)"],
    ["Hospital IT budget compression during margin pressure", "EHR consolidation pressure (Epic dominance)", "Regulatory interoperability delays", "SBC dilution typical of SaaS"],
    ["Net ARR adds quarter-over-quarter", "Hospital margin / capex trends", "Interoperability rule progress (ONC, CMS)"],
    "EV/ARR 6-12x at high growth; EV/EBITDA 15-25x for mature platforms.")

# ── Retail Pharmacy ────────────────────────────────────────────────
_add_industry("Pharmaceutical Retailers", "Healthcare",
    "Retail pharmacy chains & PBM-adjacent retail (CVS Health's retail segment, Walgreens Boots Alliance). Thin margins, store-footprint rationalization, and a shift into healthcare services (MinuteClinic, primary-care acquisitions). Not to be confused with drug distribution.",
    ["Comparable Sales Growth", "Prescription Volume Growth", "Front-end Margin", "Store-Level ROIC", "Services Revenue Mix"],
    ["Rite-aid-style bankruptcy cascade among smaller chains", "GLP-1 Rx margin compression", "Foot-traffic decline (e-comm substitution)", "PBM reimbursement / DIR fee pressure"],
    ["Prescription volume, especially GLP-1 share", "Store closures / rationalization pace", "Primary-care M&A progress"],
    "P/E 8-12x; EV/EBITDA 7-9x; dividend yields 4-6%.")


def get_sector_insight(sector: str | None) -> SectorInsight | None:
    return _SECTORS.get(sector.lower()) if sector else None

def get_industry_insight(industry: str | None) -> IndustryInsight | None:
    return _INDUSTRIES.get(industry.lower()) if industry else None

def list_sectors() -> list[str]:
    return sorted(s.sector for s in _SECTORS.values())

def list_industries() -> list[str]:
    return sorted(i.industry for i in _INDUSTRIES.values())
