"""Unit tests for data models and classification functions (Healthcare)."""

import pytest
from lynx_health.models import (
    CompanyProfile, CompanyStage, CompanyTier, HealthCategory,
    JurisdictionTier, Relevance, Severity, AnalysisReport,
    ValuationMetrics, SolvencyMetrics, GrowthMetrics,
    HealthQualityIndicators, ShareStructure, MarketIntelligence,
    FinancialStatement, AnalysisConclusion,
    classify_tier, classify_stage, classify_category, classify_jurisdiction,
    format_severity, format_impact, SEVERITY_STYLE, IMPACT_STYLE,
)


class TestClassifyTier:
    def test_mega_cap(self):
        assert classify_tier(300_000_000_000) == CompanyTier.MEGA

    def test_large_cap(self):
        assert classify_tier(50_000_000_000) == CompanyTier.LARGE

    def test_mid_cap(self):
        assert classify_tier(5_000_000_000) == CompanyTier.MID

    def test_small_cap(self):
        assert classify_tier(1_000_000_000) == CompanyTier.SMALL

    def test_micro_cap(self):
        assert classify_tier(100_000_000) == CompanyTier.MICRO

    def test_nano_cap(self):
        assert classify_tier(10_000_000) == CompanyTier.NANO

    def test_none_returns_nano(self):
        assert classify_tier(None) == CompanyTier.NANO

    def test_zero_returns_nano(self):
        assert classify_tier(0) == CompanyTier.NANO

    def test_negative_returns_nano(self):
        assert classify_tier(-100) == CompanyTier.NANO


class TestClassifyStage:
    def test_platform_from_description(self):
        assert classify_stage("diversified pharmaceutical franchise with blockbuster portfolio",
                              50_000_000_000, {"marketCap": 200_000_000_000}) == CompanyStage.PLATFORM

    def test_mature_by_profit_margin(self):
        assert classify_stage("established commercial pharmaceutical with approved products", 10_000_000_000,
                              {"marketCap": 50_000_000_000, "profitMargins": 0.25}) == CompanyStage.MATURE

    def test_growth_hyper(self):
        assert classify_stage("pivotal trial phase 3 biotechnology", 100_000_000,
                              {"revenueGrowth": 0.40}) == CompanyStage.GROWTH

    def test_scale_by_revenue(self):
        assert classify_stage("medical devices manufacturer", 800_000_000,
                              {"revenueGrowth": 0.15}) == CompanyStage.SCALE

    def test_startup_low_revenue(self):
        assert classify_stage("preclinical biotech with investigational therapy", 0) == CompanyStage.STARTUP

    def test_none_description(self):
        assert classify_stage(None, None) == CompanyStage.STARTUP

    def test_empty_description(self):
        assert classify_stage("", 0) == CompanyStage.STARTUP


class TestClassifyCategory:
    def test_biotech(self):
        assert classify_category("clinical-stage biotechnology developing mrna gene therapy",
                                 "Biotechnology") == HealthCategory.BIOTECH

    def test_big_pharma(self):
        assert classify_category("multinational pharmaceutical company with branded drug portfolio",
                                 "Drug Manufacturers - General") == HealthCategory.BIG_PHARMA

    def test_medical_devices(self):
        assert classify_category("minimally invasive surgical instruments and orthopedic implants",
                                 "Medical Devices") == HealthCategory.MEDICAL_DEVICES

    def test_health_insurance(self):
        assert classify_category("managed care medicare advantage health insurer",
                                 "Healthcare Plans") == HealthCategory.HEALTH_INSURANCE

    def test_health_providers(self):
        assert classify_category("hospital health system with outpatient services",
                                 "Medical Care Facilities") == HealthCategory.HEALTH_PROVIDERS

    def test_life_sciences_tools(self):
        assert classify_category("life sciences tools bioprocessing genomic sequencing instruments",
                                 None) == HealthCategory.LIFE_SCIENCES_TOOLS

    def test_generic_pharma(self):
        assert classify_category("generic pharmaceutical and biosimilar manufacturer",
                                 None) == HealthCategory.GENERIC_PHARMA

    def test_distribution(self):
        assert classify_category("pharmaceutical distribution and specialty pharmacy",
                                 None) == HealthCategory.HEALTH_DISTRIBUTION

    def test_health_it(self):
        assert classify_category("electronic health record and telehealth digital health platform",
                                 None) == HealthCategory.HEALTH_IT

    def test_cro(self):
        assert classify_category("contract research organization cro clinical trial services",
                                 None) == HealthCategory.CRO_CDMO

    def test_other_when_no_match(self):
        assert classify_category("generic company", None) == HealthCategory.OTHER

    def test_none_inputs(self):
        assert classify_category(None, None) == HealthCategory.OTHER


class TestClassifyJurisdiction:
    def test_us_tier1(self):
        assert classify_jurisdiction("United States") == JurisdictionTier.TIER_1

    def test_ireland_tier1(self):
        assert classify_jurisdiction("Ireland") == JurisdictionTier.TIER_1

    def test_switzerland_tier1(self):
        assert classify_jurisdiction("Switzerland") == JurisdictionTier.TIER_1

    def test_japan_tier1(self):
        assert classify_jurisdiction("Japan") == JurisdictionTier.TIER_1

    def test_india_tier2(self):
        assert classify_jurisdiction("India") == JurisdictionTier.TIER_2

    def test_spain_tier2(self):
        assert classify_jurisdiction("Spain") == JurisdictionTier.TIER_2

    def test_unknown_country_tier3(self):
        assert classify_jurisdiction("SomeCountry") == JurisdictionTier.TIER_3

    def test_none_unknown(self):
        assert classify_jurisdiction(None) == JurisdictionTier.UNKNOWN


class TestDataModels:
    def test_analysis_report_defaults(self):
        r = AnalysisReport(profile=CompanyProfile(ticker="TEST", name="Test"))
        assert r.valuation is None
        assert r.market_intelligence is None
        assert r.financials == []
        assert r.fetched_at != ""

    def test_company_profile_defaults(self):
        p = CompanyProfile(ticker="X", name="X Corp")
        assert p.tier == CompanyTier.NANO
        assert p.stage == CompanyStage.STARTUP
        assert p.health_category == HealthCategory.OTHER
        assert p.jurisdiction_tier == JurisdictionTier.UNKNOWN

    def test_solvency_metrics_defaults(self):
        s = SolvencyMetrics()
        assert s.cash_runway_years is None
        assert s.burn_as_pct_of_market_cap is None
        assert s.goodwill_to_assets is None
        assert s.deferred_revenue_ratio is None

    def test_market_intelligence_defaults(self):
        mi = MarketIntelligence()
        assert mi.insider_transactions == []
        assert mi.risk_warnings == []
        assert mi.disclaimers == []

    def test_health_quality_defaults(self):
        tq = HealthQualityIndicators()
        assert tq.quality_score is None
        assert tq.moat_assessment is None
        assert tq.rule_of_40_assessment is None


class TestSeverityFormatting:
    def test_critical_severity_format(self):
        s = format_severity(Severity.CRITICAL)
        assert "***CRITICAL***" in s
        assert "bold red" in s

    def test_warning_severity_format(self):
        s = format_severity(Severity.WARNING)
        assert "*WARNING*" in s
        assert "#ff8800" in s

    def test_watch_severity_format(self):
        s = format_severity(Severity.WATCH)
        assert "[WATCH]" in s
        assert "yellow" in s

    def test_ok_severity_format(self):
        s = format_severity(Severity.OK)
        assert "[OK]" in s
        assert "green" in s

    def test_strong_severity_format(self):
        s = format_severity(Severity.STRONG)
        assert "[STRONG]" in s
        assert "grey" in s or "silver" in s.lower()


class TestImpactFormatting:
    def test_critical_impact_blinks(self):
        s = format_impact(Relevance.CRITICAL)
        assert "Critical" in s
        assert "blink" in s

    def test_important_impact_orange(self):
        s = format_impact(Relevance.IMPORTANT)
        assert "Important" in s
        assert "#ff8800" in s

    def test_relevant_impact_yellow(self):
        s = format_impact(Relevance.RELEVANT)
        assert "Relevant" in s
        assert "yellow" in s

    def test_contextual_impact_green(self):
        s = format_impact(Relevance.CONTEXTUAL)
        assert "Informational" in s
        assert "green" in s

    def test_irrelevant_impact_silver(self):
        s = format_impact(Relevance.IRRELEVANT)
        assert "Irrelevant" in s
        assert "grey" in s or "silver" in s.lower()
