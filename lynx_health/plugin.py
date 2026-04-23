"""Entry-point registration for the Lince Investor Suite plugin system.

Exposed via ``pyproject.toml`` under the ``lynx_investor_suite.agents``
entry-point group. See :mod:`lynx_investor_core.plugins` for the
discovery contract.

The lynx_health package does not (yet) expose APP_TAGLINE / PROG_NAME
at module level, so the plugin encodes them here directly. This keeps
imports lazy and avoids modifying the package surface.
"""

from __future__ import annotations

from lynx_investor_core.plugins import SectorAgent

from lynx_health import __version__


def register() -> SectorAgent:
    """Return this agent's descriptor for the plugin registry."""
    return SectorAgent(
        name="lynx-investor-healthcare",
        short_name="healthcare",
        sector="Healthcare",
        tagline="Pharma, Biotech, Devices & Healthcare Services",
        prog_name="lynx-health",
        version=__version__,
        package_module="lynx_health",
        entry_point_module="lynx_health.__main__",
        entry_point_function="main",
        icon="\u2695",  # medical symbol / staff of Aesculapius
    )
