"""Metric explanations for Lynx Healthcare Analysis."""

from __future__ import annotations
from lynx_health.models import MetricExplanation

METRIC_EXPLANATIONS: dict[str, MetricExplanation] = {}

def _add(key, full_name, description, why_used, formula, category):
    METRIC_EXPLANATIONS[key] = MetricExplanation(key=key, full_name=full_name, description=description,
                                                  why_used=why_used, formula=formula, category=category)

# ── Valuation ──────────────────────────────────────────────────────
_add("pe_trailing", "Price-to-Earnings (TTM)", "Compares stock price to trailing 12-month earnings per share.", "Primary anchor for mature / commercial pharma & managed-care. Meaningless for pre-revenue biotech and highly misleading right after a large acquisition.", "P/E = Price / EPS (TTM)", "valuation")
_add("pe_forward", "Forward P/E", "Forward P/E based on next-year analyst EPS estimates.", "Useful when a drug launch or biosimilar wave is visibly shifting earnings. Healthcare forward estimates are often more reliable than tech because payer dynamics are modelable.", "Fwd P/E = Price / Est. EPS (next FY)", "valuation")
_add("pb_ratio", "Price-to-Book", "Compares stock price to book value per share.", "Weak anchor for IP-heavy pharma (intangibles dominate). Most useful for hospitals / providers where tangible assets matter.", "P/B = Price / Book Value per Share", "valuation")
_add("ps_ratio", "Price-to-Sales", "Compares market cap to revenue.", "Used for scale-up biotech post-launch and specialty diagnostics. Benchmarks: biotech pre-peak 5-15x, devices 4-8x, distributors 0.1-0.3x.", "P/S = Market Cap / Revenue", "valuation")
_add("p_fcf", "Price-to-Free-Cash-Flow", "Compares market cap to free cash flow.", "Best cash-economics anchor for commercial-stage pharma, devices, insurers, and mature health IT.", "P/FCF = Market Cap / FCF", "valuation")
_add("ev_ebitda", "Enterprise Value / EBITDA", "Capital-structure-neutral earnings multiple.", "Cross-company comparison for pharma (10-14x), devices (15-22x), managed-care (7-10x), and distributors (9-12x).", "EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA", "valuation")
_add("ev_revenue", "Enterprise Value / Revenue", "EV divided by revenue.", "Key multiple for growth biotech & life-sciences tools. Typical bands: Big Pharma 3-5x, devices 4-7x, biotech launch 5-15x, distributors 0.15-0.25x.", "EV/Revenue = EV / Revenue", "valuation")
_add("ev_gross_profit", "EV / Gross Profit", "EV divided by gross profit — a margin-adjusted variant of EV/Sales.", "Strips out cost-of-goods differences between branded pharma (80%+ GM), specialty devices (65-75%), and distributors (3-5%). Apples-to-apples scale comparison.", "EV / GP = EV / (Revenue - COGS)", "valuation")
_add("ev_to_arr", "EV / ARR", "Enterprise value divided by Annual Recurring Revenue (approximated when not disclosed).", "Relevant for health IT, Veeva-style vertical SaaS, digital-health platforms. Growth-adjusted benchmarks: 8-15x at 30%+ ARR growth.", "EV/ARR = EV / ARR  (approx: revenue + Δdeferred rev)", "valuation")
_add("ev_per_employee", "EV per Employee", "Enterprise value divided by full-time employees.", "Healthcare bands: pharma $2-5M/emp, biotech $5-15M/emp, devices $1-2M/emp, providers $0.2-0.4M/emp, insurers $1-3M/emp.", "EV / Employees", "valuation")
_add("rule_of_40_adj_multiple", "R40-Adjusted EV/Revenue", "EV/Revenue divided by Rule-of-40 sum normalized to 40.", "Normalizes valuation by quality of growth + profitability — useful specifically for digital-health & life-sciences-tools SaaS peers.", "EV/Rev / (Rule40 / 40)", "valuation")
_add("peg_ratio", "PEG Ratio", "P/E adjusted by growth rate.", "Useful for mid-cap devices and specialty pharma with durable growth. PEG <1 suggests undervaluation vs earnings trajectory.", "PEG = P/E / Annual EPS growth rate", "valuation")
_add("cash_to_market_cap", "Cash / Market Cap", "How much of market cap is backed by cash on the balance sheet.", "CRITICAL for clinical-stage biotech — often 50-100%+ before a key readout. A >30% ratio is a meaningful downside cushion.", "Cash / Market Cap", "valuation")

# ── Profitability ──────────────────────────────────────────────────
_add("roe", "Return on Equity", "Profit per dollar of equity.", "For mature pharma & devices, ROE >20% signals strong profitability. Insurers typically 15-25%.", "ROE = Net Income / Equity", "profitability")
_add("roic", "Return on Invested Capital", "Return on all invested capital.", "Best moat evidence for diversified pharma & devices — >12% ROIC compound over years is a quality hallmark.", "ROIC = NOPAT / Invested Capital", "profitability")
_add("gross_margin", "Gross Margin", "Revenue remaining after cost of revenue.", "Huge dispersion in healthcare: branded pharma/biologics 80%+, devices 65-75%, generics 50-60%, providers 30-40%, distribution 3-5%.", "Gross Margin = (Revenue - COGS) / Revenue", "profitability")
_add("operating_margin", "Operating Margin", "Revenue remaining after all operating expenses.", "Benchmarks: Big Pharma 25-35%, devices 20-28%, biotech often negative pre-launch, managed-care 4-8%, distributors 1.5-2.5%.", "Operating Margin = Operating Income / Revenue", "profitability")
_add("net_margin", "Net Margin", "Bottom-line profitability.", "Traditional profitability anchor; distorted for pharma by one-time R&D charges and M&A write-downs.", "Net Margin = Net Income / Revenue", "profitability")
_add("fcf_margin", "FCF Margin", "Free cash flow as % of revenue.", "Best-in-class commercial pharma >25%; devices 18-25%; insurers 2-5% (premium inflows distort); biotech often negative.", "FCF Margin = FCF / Revenue", "profitability")
_add("ebitda_margin", "EBITDA Margin", "EBITDA / revenue.", "Cyclicality-adjusted operating profit. Branded pharma 35-45%; medtech 25-35%; hospitals 10-15%; distribution 2-3%.", "EBITDA Margin = EBITDA / Revenue", "profitability")
_add("rule_of_40", "Rule of 40 (FCF variant)", "Revenue growth % + FCF margin %.", "Applied to health IT / digital-health SaaS peers. >40% passing, >60% best-in-class. Not meaningful for branded pharma or hospitals.", "Rule40 = Rev Growth % + FCF Margin %", "profitability")
_add("rule_of_40_ebitda", "Rule of 40 (EBITDA variant)", "Revenue growth % + EBITDA margin %.", "Useful for pre-FCF-positive health IT and launch-stage biopharma that have EBITDA but are reinvesting heavily.", "Rule40(EBITDA) = Rev Growth % + EBITDA Margin %", "profitability")
_add("magic_number", "Magic Number", "Sales efficiency: (ΔARR × 4) / S&M spend.", "Only meaningful for health IT / digital-health SaaS. Irrelevant for pharma (where S&M buys physician detailing, not logo acquisition).", "Magic Number = (ΔARR × 4) / S&M", "profitability")
_add("sbc_to_revenue", "SBC / Revenue", "Stock-Based Compensation as % of revenue.", "Critical for biotech: clinical-stage names often spend 15-30% of revenue on SBC, creating material dilution.", "SBC / Revenue", "profitability")
_add("sbc_to_fcf", "SBC / FCF", "Stock-Based Compensation as % of free cash flow.", "If SBC > FCF, reported cash economics are partly paper — common in mid-cap biopharma.", "SBC / FCF", "profitability")
_add("gaap_vs_adj_gap", "GAAP vs Adjusted Gap", "Spread between GAAP and non-GAAP (adjusted) operating income.", "Wider gaps in healthcare typically flag R&D in-process write-offs, acquisition amortization, or legal charges (opioid/antitrust).", "(Adj Op Inc - GAAP Op Inc) / Revenue", "profitability")

# ── Solvency ───────────────────────────────────────────────────────
_add("debt_to_equity", "Debt / Equity", "Debt financing vs equity financing.", "Big Pharma & devices often run moderate leverage for M&A (0.5-1.5x). Hospitals & insurers higher. Biotech should be near 0 or fully cash-backed.", "D/E = Total Debt / Equity", "solvency")
_add("current_ratio", "Current Ratio", "Short-term asset coverage.", ">2 healthy for pharma/devices; <1 critical for biotech and concerning for providers.", "Current Ratio = Current Assets / Current Liabilities", "solvency")
_add("interest_coverage", "Interest Coverage", "Ability to pay interest from operating income.", ">6 comfortable, <2 dangerous. Watch for leveraged hospital operators and generic pharma rolled up by PE.", "Operating Income / Interest Expense", "solvency")
_add("altman_z_score", "Altman Z-Score", "Bankruptcy probability predictor.", "Z >2.99 safe. 1.81-2.99 grey. <1.81 distress. Less meaningful for pre-revenue biotech (use cash runway instead).", "Z = 1.2(WC/TA) + 1.4(RE/TA) + 3.3(EBIT/TA) + 0.6(MV/TL) + 1.0(Sales/TA)", "solvency")
_add("cash_burn_rate", "Cash Burn Rate", "Annual rate of cash consumption.", "THE survival metric for clinical-stage biotech. Negative OCF compared to cash balance tells you how close the next dilution round is.", "Operating Cash Flow (negative)", "solvency")
_add("cash_runway_years", "Cash Runway", "Years of operation at current burn rate.", "<1yr = imminent financing (expect dilution). 1-2yr = secondary within 12m likely. >3yr = comfortable to the next catalyst.", "Total Cash / Annual Burn", "solvency")
_add("burn_as_pct_of_market_cap", "Burn % of Market Cap", "How fast the company burns shareholder value.", "<5%/yr healthy. >10%/yr is a dilution setup. Common in clinical-stage biotech.", "|Burn| / Market Cap", "solvency")
_add("capex_to_revenue", "Capex / Revenue", "Capital intensity.", "Branded pharma 4-7%; devices 4-6%; biotech <2% (except manufacturing-owning biologics); hospitals & dialysis 5-10%; insurers <1%.", "Capex / Revenue", "solvency")
_add("rpo_coverage", "RPO / Revenue Coverage", "Remaining Performance Obligations vs annual revenue.", "Forward-visibility proxy for health IT SaaS and CRO/CDMO backlog. >100% means >1 year of booked revenue.", "Deferred Revenue / Revenue", "solvency")
_add("deferred_revenue_ratio", "Deferred Revenue Ratio", "Deferred revenue vs annual revenue.", "Subscription / milestone billing strength. Strong predictor for CROs, health IT vendors, and subscription diagnostics.", "Deferred Revenue / Revenue", "solvency")
_add("goodwill_to_assets", "Goodwill / Total Assets", "Goodwill from acquisitions as share of assets.", ">40% is impairment-risk territory. Big Pharma M&A rolls — watch post-close writedowns in the 3-5 year window.", "Goodwill / Total Assets", "solvency")

# ── Growth ─────────────────────────────────────────────────────────
_add("revenue_growth_yoy", "Revenue Growth (YoY)", "Annual revenue change.", "Core growth metric. Bands: Big Pharma 2-6%, devices 4-8%, biotech launch >100%, insurers 6-12%, distributors 3-6%.", "(Rev - Rev_Prior) / |Rev_Prior|", "growth")
_add("revenue_cagr_3y", "Revenue CAGR (3Y)", "3-year compound revenue growth.", "Smooths drug launches / biosimilar cliffs. >20% is hyper-growth for healthcare; <3% suggests franchise erosion.", "CAGR = (End / Start)^(1/3) - 1", "growth")
_add("earnings_growth_yoy", "Earnings Growth (YoY)", "Annual net income change.", "Drives Big Pharma / devices / insurer valuation. Distorted by IPR&D charges and one-time legal reserves.", "(NI - NI_Prior) / |NI_Prior|", "growth")
_add("shares_growth_yoy", "Share Dilution (YoY)", "Annual change in shares outstanding.", "Biotech dilutes aggressively to fund trials — 10-25%/yr is common. Mature pharma usually buys back (negative growth).", "(Shares - Shares_Prior) / Shares_Prior", "growth")
_add("arr_growth_yoy", "ARR Growth (YoY)", "Annual Recurring Revenue growth.", "Growth signal for health IT / digital-health SaaS. Approximated here as revenue + deferred-revenue growth.", "(ARR - ARR_Prior) / ARR_Prior", "growth")
_add("net_revenue_retention", "Net Revenue Retention", "% of cohort revenue retained after expansion & churn.", "Top signal for health IT SaaS. >120% = expansion economy. Not applicable to pharma (patent-driven).", "NRR = (Starting ARR + Expansion - Contraction - Churn) / Starting ARR", "growth")
_add("gross_revenue_retention", "Gross Revenue Retention", "% of cohort revenue retained before expansion.", "Pure stickiness — vital for health IT logos. >90% = embedded product; <80% = fragile.", "GRR = (Starting ARR - Contraction - Churn) / Starting ARR", "growth")
_add("rd_intensity", "R&D Intensity", "R&D as % of revenue.", "THE innovation metric for healthcare. Big Pharma 18-22%, mid-cap biotech 40-80%, clinical-stage often 150%+ (R&D > revenue), devices 6-10%, life-sciences tools 7-10%.", "R&D / Revenue", "growth")
_add("rd_growth_yoy", "R&D Growth (YoY)", "Year-over-year R&D spending change.", "Pipeline investment pace. Sustained high R&D growth with flat revenue is a setup for future reinvestment returns.", "(R&D - R&D_Prior) / R&D_Prior", "growth")
_add("sales_marketing_intensity", "SG&A / S&M Intensity", "Sales, general & admin as % of revenue.", "Big Pharma 25-35% (physician detailing), devices 30-40% (rep-driven), biotech launches 40-60% (build commercial infra), mature insurers 8-12%.", "SG&A / Revenue", "growth")
_add("employee_growth_yoy", "Employee Growth (YoY)", "Headcount change.", "Biotech typically scales headcount ahead of revenue (trial & manufacturing build). Watch productivity once commercial.", "(Emp - Emp_Prior) / Emp_Prior", "growth")
_add("revenue_per_employee", "Revenue per Employee", "Productivity metric.", "Wide range: big pharma $1.2-1.6M/emp, devices $0.5-0.8M/emp, biotech $0.1-0.4M pre-commercial, distributors $2-3M, insurers $0.8-1.5M.", "Revenue / Employees", "growth")

# ── Healthcare Quality ─────────────────────────────────────────────
_add("quality_score", "Healthcare Quality Score", "Composite healthcare-quality score (0-100).", "Weighted: Moat / Gross Margin (20), Rule-of-40 (20), Financial Position / Runway (15), Dilution / SBC (15), R&D Efficiency (10), Unit Economics (10), Revenue Predictability (10). >75 elite franchise; <30 weak / speculative.", "Weighted sum of 7 healthcare-specific axes", "health_quality")
_add("moat_assessment", "Moat Assessment", "Qualitative moat classification tied to gross margin + category.", "Healthcare moats: IP (patents, data exclusivity), switching costs (EHR, medical-device training), regulatory barriers (FDA approval timelines), scale (distribution, payer networks).", "Derived from GM %, category, franchise depth", "health_quality")
_add("rule_of_40_assessment", "Rule-of-40 Verdict", "Assessment of Rule-of-40 score.", "Meaningful for health IT / digital-health peers; contextual elsewhere in healthcare. Pass/fail grade used by SaaS-style healthcare investors.", "Rule40 band", "health_quality")
_add("unit_economics", "Unit Economics", "Summary of magic number, CAC payback, NRR (health IT).", "Evaluates whether growth is economically sustainable, not just fueled by burn. Particularly relevant for digital health and specialty-diagnostics commercial ramps.", "Magic#, CAC payback, NRR", "health_quality")
_add("sbc_risk_assessment", "SBC Risk", "Stock-based compensation risk framing.", "Healthcare dilution risk category: Contained / Moderate / High / Severe. Biotech routinely Severe through Phase II/III.", "SBC / Revenue band", "health_quality")
_add("platform_position", "Platform Position", "Scale/franchise/pipeline breadth.", "A diversified Big Pharma or integrated managed-care compounds for decades; a single-asset biotech is binary.", "Tier + category analysis", "health_quality")
_add("founder_led", "Founder / Scientist-Led Signal", "Founder or strong insider control (often scientific founder for biotech).", "Founder/scientist-led biotech and device companies historically outperform. >10% insider ownership is meaningful alignment.", "Insider ownership % band", "health_quality")

# ── Share Structure ────────────────────────────────────────────────
_add("shares_outstanding", "Shares Outstanding", "Basic shares currently issued.", "Baseline for per-share metrics.", "—", "share_structure")
_add("fully_diluted_shares", "Fully Diluted Shares", "Shares + RSUs + options + warrants + convertibles.", "True dilution floor — essential for biotech where convertibles and warrant overhangs are heavy.", "Basic + RSUs + Options + Warrants + Convertibles", "share_structure")
_add("insider_ownership_pct", "Insider Ownership %", "% of shares held by insiders/founders/scientists.", ">10% is meaningful alignment. Scientific founders often hold 15-30% post-IPO.", "Insider Shares / Total Shares", "share_structure")
_add("dual_class_structure", "Dual-Class Structure", "Whether insiders hold super-voting shares.", "Less common in healthcare than in tech. Where present (some device / health IT), locks in founder control.", "Voting class structure", "share_structure")
_add("sbc_overhang_risk", "SBC Overhang Risk", "Forward dilution pressure from future equity comp grants.", "Large overhangs depress per-share economics — common in pre-profit biotech and launch-stage med-devices.", "Cumulative SBC run-rate vs float", "share_structure")

# ── Efficiency ─────────────────────────────────────────────────────
_add("rule_of_x_score", "Rule of X (Altimeter)", "Revenue growth × (1 + FCF margin).", "Altimeter's multiplicative refinement of Rule-of-40 — useful for health IT and launch-stage biopharma that compound growth × profitability.", "Growth × (1 + FCF margin)", "efficiency")
_add("cac_payback_months", "CAC Payback (months)", "Months to recover customer acquisition cost via gross profit.", "For health IT / subscription diagnostics: <18 months best-in-class; >36 months = fix the motion.", "S&M / (Quarterly GP Delta × 3)", "efficiency")
_add("fcf_conversion", "FCF Conversion", "FCF divided by net income.", ">1 = high-quality earnings (mature pharma / devices); <0.8 = earnings may overstate cash (common in biotech with heavy SBC addback).", "FCF / Net Income", "efficiency")

SECTION_EXPLANATIONS = {
    "profile": {"title": "Company Profile", "description": "Company identification, market cap tier, healthcare lifecycle stage, healthcare sub-category (Big Pharma / Biotech / Devices / Providers / Insurers / Tools / Distribution / Health IT / CRO-CDMO), and jurisdiction risk."},
    "valuation": {"title": "Valuation Metrics", "description": "Traditional + healthcare-specific valuation ratios. EV/EBITDA, P/FCF, and P/E dominate commercial-stage. Cash-to-Market-Cap and EV/Sales dominate clinical-stage biotech. EV/ARR for digital-health SaaS."},
    "profitability": {"title": "Profitability Metrics", "description": "Margin analysis plus healthcare-specific: Rule-of-40 for digital health, Magic Number for SaaS peers, SBC/Revenue and SBC/FCF for biotech dilution pressure, GAAP-vs-Adjusted gap for acquisition-heavy pharma."},
    "solvency": {"title": "Solvency & Survival", "description": "Balance sheet strength, cash runway (CRITICAL for clinical-stage biotech), burn rate, deferred revenue / RPO coverage (CROs, health IT), goodwill-to-assets (post-M&A impairment risk), capex intensity."},
    "growth": {"title": "Growth & Pipeline Signals", "description": "Revenue + ARR growth, R&D intensity & growth (THE healthcare innovation metric), SG&A intensity, employee & productivity trends. NRR and GRR slots reserved for health-IT names."},
    "share_structure": {"title": "Share Structure", "description": "Basic/fully-diluted shares, insider & institutional ownership, dual-class flag, SBC overhang risk — dilution concerns are particularly heavy in clinical-stage biotech."},
    "health_quality": {"title": "Healthcare Quality Assessment", "description": "Healthcare-specialized scoring. Evaluates moat quality (patents, switching costs), Rule-of-40 for digital health, unit economics, financial position (runway), R&D efficiency, dilution/SBC risk, and revenue predictability."},
    "intrinsic_value": {"title": "Intrinsic Value Estimates", "description": "Multiple methods adapted by stage. Diversified pharma / managed-care: DCF. Mature commercial: DCF + P/FCF. Launch/scale: EV/Gross-Profit peer multiples. Clinical biotech: cash-backing floor + risk-adjusted pipeline NPV (proxied)."},
    "conclusion": {"title": "Assessment Conclusion", "description": "Weighted scoring across 5 categories with weights adapted by tier AND healthcare lifecycle stage. Includes a 10-point healthcare screening checklist evaluating the key quality criteria."},
}

CONCLUSION_METHODOLOGY = {
    "overall": {"title": "Conclusion Methodology", "description": "Score is a weighted average of 5 categories (valuation, profitability, solvency, growth, healthcare quality). Weights vary by company tier AND healthcare lifecycle stage. Clinical-stage biotech weights solvency at 35-40% (runway) and quality at 30%. Diversified franchises use balanced weights. Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30)."},
    "valuation": {"title": "Valuation Score", "description": "Starts at 50. Adjusted by EV/Gross-Profit, P/FCF, Rule-of-40-adjusted EV/Revenue (digital health), cash-to-market-cap (bonus for clinical biotech), and P/E where applicable."},
    "profitability": {"title": "Profitability Score", "description": "Starts at 50. Rule-of-40 (health IT), gross margin vs category benchmark, FCF margin, SBC penalty. Clinical-stage biotech is not penalized for lack of profit — quality-weighted instead."},
    "solvency": {"title": "Solvency Score", "description": "Starts at 50. Debt/equity, current ratio, cash runway (crucial for biotech), burn rate, goodwill-to-assets. Biotech is penalized heavily for debt on a pre-revenue book. Cash runway <1 year = -25 points."},
    "health_quality": {"title": "Healthcare Quality Score", "description": "Composite of moat/gross-margin (20pts), Rule-of-40 / growth-quality (20pts), financial position (15pts), dilution/SBC risk (15pts), R&D efficiency (10pts), unit economics (10pts), revenue predictability (10pts)."},
}

def get_explanation(key): return METRIC_EXPLANATIONS.get(key)
def get_section_explanation(section): return SECTION_EXPLANATIONS.get(section)
def get_conclusion_explanation(category=None): return CONCLUSION_METHODOLOGY.get(category or "overall")
def list_metrics(category=None):
    metrics = list(METRIC_EXPLANATIONS.values())
    return [m for m in metrics if m.category == category] if category else metrics
