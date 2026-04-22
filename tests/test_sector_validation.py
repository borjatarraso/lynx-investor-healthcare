"""Tests for the sector validation gate (Healthcare)."""

import pytest
from lynx_health.core.analyzer import _validate_sector, SectorMismatchError
from lynx_health.models import CompanyProfile


class TestSectorValidation:
    """Sector validation blocks non-healthcare companies."""

    def _profile(self, ticker="T", sector=None, industry=None, desc=None):
        return CompanyProfile(ticker=ticker, name=f"{ticker} Corp",
                              sector=sector, industry=industry, description=desc)

    # --- Should ALLOW ---
    def test_healthcare_sector_general_pharma(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Drug Manufacturers - General"))

    def test_healthcare_sector_specialty_pharma(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Drug Manufacturers - Specialty & Generic"))

    def test_healthcare_sector_biotechnology(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Biotechnology"))

    def test_healthcare_sector_medical_devices(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Medical Devices"))

    def test_healthcare_sector_medical_instruments(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Medical Instruments & Supplies"))

    def test_healthcare_sector_medical_care(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Medical Care Facilities"))

    def test_healthcare_sector_healthcare_plans(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Healthcare Plans"))

    def test_healthcare_sector_diagnostics(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Diagnostics & Research"))

    def test_healthcare_sector_distribution(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Medical Distribution"))

    def test_healthcare_sector_health_it(self):
        _validate_sector(self._profile(sector="Healthcare", industry="Health Information Services"))

    def test_biotech_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Clinical-stage biotechnology developing novel mrna therapies"))

    def test_medical_device_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Manufacturer of medical devices for cardiovascular procedures"))

    def test_phase3_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Conducting phase 3 pivotal trials for oncology therapy"))

    # --- Should BLOCK ---
    def test_basic_materials_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_energy_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Energy", industry="Uranium"))

    def test_financial_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Financial Services", industry="Banks"))

    def test_technology_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Technology", industry="Software - Application"))

    def test_consumer_cyclical_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Consumer Cyclical", industry="Auto Manufacturers"))

    def test_real_estate_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Real Estate", industry="REIT"))

    def test_all_none_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile())

    def test_empty_strings_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="", industry="", desc=""))

    def test_mining_company_blocked(self):
        """A mining company with vague 'Other' sector should be blocked."""
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(
                sector="Basic Materials", industry="Gold",
                desc="Gold mining exploration and drill program"))

    def test_error_message_content(self):
        with pytest.raises(SectorMismatchError, match="outside the scope"):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_error_suggests_another_agent(self):
        """Wrong-sector warning appends a 'use lynx-investor-*' line."""
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Energy", industry="Oil & Gas E&P"))
        message = str(exc.value)
        assert "Suggestion" in message
        assert "lynx-investor-energy" in message

    def test_error_never_suggests_self(self):
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Utilities", industry="Utilities—Regulated Electric"))
        message = str(exc.value)
        assert "use 'lynx-investor-healthcare'" not in message
