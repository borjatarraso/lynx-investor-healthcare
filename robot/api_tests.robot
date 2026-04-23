*** Settings ***
Documentation    Python API tests for Lynx Healthcare — exercises the core functions directly.
Library          Process
Library          BuiltIn
Library          Collections
Suite Setup      Log    Starting API Tests


*** Keywords ***
I Run Python Code
    [Arguments]    ${code}
    ${result}=    Run Process    python3    -c    ${code}    stderr=STDOUT    timeout=30s
    Set Test Variable    ${PY_OUTPUT}    ${result.stdout}
    Set Test Variable    ${PY_RC}    ${result.rc}

The Output Should Contain
    [Arguments]    ${snippet}
    Should Contain    ${PY_OUTPUT}    ${snippet}

The Process Should Succeed
    Should Be Equal As Integers    ${PY_RC}    0    msg=Expected success but got ${PY_RC}: ${PY_OUTPUT}


*** Test Cases ***
Package Imports Successfully
    [Documentation]    GIVEN the package WHEN I import core classes THEN they load
    When I Run Python Code    from lynx_health.models import AnalysisReport, CompanyProfile, CompanyStage, CompanyTier, HealthCategory, JurisdictionTier, Relevance, Severity, MarketIntelligence, InsiderTransaction; print('OK')
    Then The Output Should Contain    OK
    And The Process Should Succeed

Classify Tier Mega Cap
    [Documentation]    GIVEN a 300B market cap WHEN I classify THEN Mega Cap
    When I Run Python Code    from lynx_health.models import classify_tier; print(classify_tier(300_000_000_000).value)
    Then The Output Should Contain    Mega Cap

Classify Tier Micro Cap
    [Documentation]    GIVEN 100M market cap WHEN I classify THEN Micro Cap
    When I Run Python Code    from lynx_health.models import classify_tier; print(classify_tier(100_000_000).value)
    Then The Output Should Contain    Micro Cap

Classify Stage Platform
    [Documentation]    GIVEN a diversified pharma description WHEN I classify THEN Diversified Franchise
    When I Run Python Code    from lynx_health.models import classify_stage; print(classify_stage('diversified pharmaceutical blockbuster franchise', 50_000_000_000, {'marketCap': 200_000_000_000}).value)
    Then The Output Should Contain    Diversified

Classify Stage Mature
    [Documentation]    GIVEN profitable commercial pharma WHEN I classify THEN Commercial
    When I Run Python Code    from lynx_health.models import classify_stage; print(classify_stage('established commercial pharmaceutical with approved products', 10_000_000_000, {'marketCap': 50_000_000_000, 'profitMargins': 0.25}).value)
    Then The Output Should Contain    Commercial

Classify Stage Growth
    [Documentation]    GIVEN late-stage clinical biotech WHEN I classify THEN Clinical Hyper-Growth
    When I Run Python Code    from lynx_health.models import classify_stage; print(classify_stage('phase 3 pivotal trial clinical-stage biotechnology', 100_000_000, {'revenueGrowth': 0.40}).value)
    Then The Output Should Contain    Clinical

Classify Stage Startup
    [Documentation]    GIVEN preclinical biotech WHEN I classify THEN Preclinical / Early-Stage Biotech
    When I Run Python Code    from lynx_health.models import classify_stage; print(classify_stage('preclinical biotechnology investigational therapy', 0).value)
    Then The Output Should Contain    Preclinical

Classify Category Biotech
    [Documentation]    GIVEN biotech description WHEN I classify THEN Biotechnology
    When I Run Python Code    from lynx_health.models import classify_category; print(classify_category('clinical-stage biotechnology monoclonal antibody', 'Biotechnology').value)
    Then The Output Should Contain    Biotech

Classify Category Medical Devices
    [Documentation]    GIVEN medical device description WHEN I classify THEN Medical Devices
    When I Run Python Code    from lynx_health.models import classify_category; print(classify_category('minimally invasive surgical instruments and orthopedic implants', 'Medical Devices').value)
    Then The Output Should Contain    Medical Devices

Classify Jurisdiction Tier 1 US
    [Documentation]    GIVEN United States WHEN I classify THEN Tier 1
    When I Run Python Code    from lynx_health.models import classify_jurisdiction; print(classify_jurisdiction('United States').value)
    Then The Output Should Contain    Tier 1

Classify Jurisdiction Tier 2 India
    [Documentation]    GIVEN India WHEN I classify THEN Tier 2
    When I Run Python Code    from lynx_health.models import classify_jurisdiction; print(classify_jurisdiction('India').value)
    Then The Output Should Contain    Tier 2

Relevance Startup PE Irrelevant
    [Documentation]    GIVEN startup stage WHEN I check P/E THEN irrelevant
    When I Run Python Code    from lynx_health.metrics.relevance import get_relevance; from lynx_health.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('pe_trailing', CompanyTier.MICRO, 'valuation', CompanyStage.STARTUP) == Relevance.IRRELEVANT)
    Then The Output Should Contain    True

Relevance Growth Cash Runway Critical
    [Documentation]    GIVEN clinical-stage biotech WHEN I check cash runway THEN critical
    When I Run Python Code    from lynx_health.metrics.relevance import get_relevance; from lynx_health.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('cash_runway_years', CompanyTier.MID, 'solvency', CompanyStage.GROWTH) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Relevance Growth SBC To Revenue Critical
    [Documentation]    GIVEN clinical-stage biotech WHEN I check SBC/Rev THEN critical
    When I Run Python Code    from lynx_health.metrics.relevance import get_relevance; from lynx_health.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('sbc_to_revenue', CompanyTier.MID, 'profitability', CompanyStage.GROWTH) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Relevance Mature ROIC Critical
    [Documentation]    GIVEN mature stage WHEN I check ROIC THEN critical
    When I Run Python Code    from lynx_health.metrics.relevance import get_relevance; from lynx_health.models import CompanyTier, CompanyStage, Relevance; print(get_relevance('roic', CompanyTier.MID, 'profitability', CompanyStage.MATURE) == Relevance.CRITICAL)
    Then The Output Should Contain    True

Explanations Rule Of 40 Metric Present
    [Documentation]    GIVEN explanations WHEN I look up Rule of 40 THEN it exists
    When I Run Python Code    from lynx_health.metrics.explanations import get_explanation; e = get_explanation('rule_of_40'); print(e.category if e else 'NONE')
    Then The Output Should Contain    profitability

Explanations SBC Metric Present
    [Documentation]    GIVEN explanations WHEN I look up sbc_to_revenue THEN it exists
    When I Run Python Code    from lynx_health.metrics.explanations import get_explanation; e = get_explanation('sbc_to_revenue'); print(e.category if e else 'NONE')
    Then The Output Should Contain    profitability

Severity Format Critical Red Bold
    [Documentation]    GIVEN CRITICAL severity WHEN I format THEN red + bold + triple stars
    When I Run Python Code    from lynx_health.models import format_severity, Severity; s = format_severity(Severity.CRITICAL); assert '***CRITICAL***' in s and 'bold red' in s; print('OK')
    Then The Output Should Contain    OK

Severity Format Strong Silver
    [Documentation]    GIVEN STRONG severity WHEN I format THEN silver/grey
    When I Run Python Code    from lynx_health.models import format_severity, Severity; s = format_severity(Severity.STRONG); assert '[STRONG]' in s and 'grey' in s; print('OK')
    Then The Output Should Contain    OK

Impact Format Critical Blinks Red
    [Documentation]    GIVEN CRITICAL relevance WHEN I format impact THEN blink + red
    When I Run Python Code    from lynx_health.models import format_impact, Relevance; s = format_impact(Relevance.CRITICAL); assert 'blink' in s and 'red' in s; print('OK')
    Then The Output Should Contain    OK

Impact Format Irrelevant Silver
    [Documentation]    GIVEN IRRELEVANT relevance WHEN I format impact THEN silver/grey
    When I Run Python Code    from lynx_health.models import format_impact, Relevance; s = format_impact(Relevance.IRRELEVANT); assert 'grey' in s; print('OK')
    Then The Output Should Contain    OK

Sector Validation Allows Healthcare
    [Documentation]    GIVEN a biotech company WHEN I validate THEN allowed
    When I Run Python Code    from lynx_health.core.analyzer import _validate_sector; from lynx_health.models import CompanyProfile; p = CompanyProfile(ticker='MRNA', name='Moderna', sector='Healthcare', industry='Biotechnology'); _validate_sector(p); print('ALLOWED')
    Then The Output Should Contain    ALLOWED

Conclusion Generation Returns Verdict
    [Documentation]    GIVEN a minimal report WHEN I generate conclusion THEN verdict is present
    When I Run Python Code    from lynx_health.models import AnalysisReport, CompanyProfile; from lynx_health.core.conclusion import generate_conclusion; r = AnalysisReport(profile=CompanyProfile(ticker='T', name='T')); c = generate_conclusion(r); print(c.verdict)
    Then The Output Should Contain    Caution

Healthcare Screening Checklist Present
    [Documentation]    GIVEN a report WHEN I screen THEN rule_of_40_pass key exists
    When I Run Python Code    from lynx_health.models import AnalysisReport, CompanyProfile; from lynx_health.core.conclusion import generate_conclusion; r = AnalysisReport(profile=CompanyProfile(ticker='T', name='T')); c = generate_conclusion(r); print('rule_of_40_pass' in c.screening_checklist)
    Then The Output Should Contain    True

Metric Explanations Healthcare Specific
    [Documentation]    GIVEN explanations WHEN I list THEN healthcare metrics present
    When I Run Python Code    from lynx_health.metrics.explanations import list_metrics; keys = [m.key for m in list_metrics()]; print('rd_intensity' in keys and 'sbc_to_revenue' in keys and 'cash_runway_years' in keys and 'cash_to_market_cap' in keys)
    Then The Output Should Contain    True
