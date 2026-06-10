import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

from portfolio.ranking import (
    RANKING_UNIVERSE, STRATEGY_WEIGHTS, RISK_ADJUSTMENTS,
    score_analyst_upside, score_revenue_quality, score_analyst_conviction,
    score_entry_position, score_momentum, score_valuation,
    score_long_term_health, score_cash_runway,
    score_revenue_acceleration,
    penalty_fragility, penalty_downside, bonus_profitability,
)

# =========================================================================
# EXTRA STOCKS for broader backtest validation
# =========================================================================

BACKTEST_EXTRA = {
    # --- Mid/small-cap high-growth: nuclear/energy ---
    "VST":   {"name": "Vistra",             "basket": "Nuclear",     "strategy": "cycle",        "what": "Nuclear + natural gas power generation",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "CEG":   {"name": "Constellation Energy","basket": "Nuclear",    "strategy": "hold_forever", "what": "Largest US nuclear fleet operator",
              "fragility": "none",      "downside_if_fail": "low"},
    "TLN":   {"name": "Talen Energy",       "basket": "Nuclear",     "strategy": "cycle",        "what": "Nuclear + data center power provider",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "NNE":   {"name": "Nano Nuclear",       "basket": "Nuclear",     "strategy": "catalyst",     "what": "Portable microreactor design — pre-revenue",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "DNN":   {"name": "Denison Mines",      "basket": "Nuclear",     "strategy": "cycle",        "what": "Uranium mining — ISR extraction in Canada",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "UEC":   {"name": "Uranium Energy",     "basket": "Nuclear",     "strategy": "cycle",        "what": "US uranium mining — ISR production",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # --- Mid/small-cap: quantum/computing ---
    "QUBT":  {"name": "Quantum Computing",  "basket": "Quantum",     "strategy": "catalyst",     "what": "Quantum optimization + photonic chips",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "ARQQ":  {"name": "Arqit Quantum",      "basket": "Quantum",     "strategy": "catalyst",     "what": "Quantum encryption key distribution",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- Mid/small-cap: AI/data center ---
    "APP":   {"name": "AppLovin",           "basket": "SpecGrowth",  "strategy": "cycle",        "what": "AI-powered mobile ad tech platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "SMCI":  {"name": "Super Micro",        "basket": "Industrial",  "strategy": "cycle",        "what": "AI server hardware manufacturer",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "BBAI":  {"name": "BigBear.ai",         "basket": "Defense",     "strategy": "catalyst",     "what": "AI analytics for defense + intelligence",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "SOUN":  {"name": "SoundHound AI",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Voice AI for restaurants + automotive",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "AI":    {"name": "C3.ai",              "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Enterprise AI application platform",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "ASTS":  {"name": "AST SpaceMobile",    "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Satellite-to-phone broadband — space-based cellular",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- Mid/small-cap: cyber/defense ---
    "RCAT":  {"name": "Red Cat Holdings",   "basket": "Defense",     "strategy": "catalyst",     "what": "Military drones — Teal 2 for US Army",
              "fragility": "political", "downside_if_fail": "severe"},
    "PLTR":  {"name": "Palantir",           "basket": "Defense",     "strategy": "cycle",        "what": "AI/ML data analytics for defense + enterprise",
              "fragility": "none",      "downside_if_fail": "low"},
    "FTNT":  {"name": "Fortinet",           "basket": "Cyber",       "strategy": "hold_forever", "what": "Network security appliances + SASE",
              "fragility": "none",      "downside_if_fail": "low"},
    "S":     {"name": "SentinelOne",        "basket": "Cyber",       "strategy": "cycle",        "what": "AI-powered endpoint security",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ZS":    {"name": "Zscaler",            "basket": "Cyber",       "strategy": "hold_forever", "what": "Zero-trust cloud security platform",
              "fragility": "none",      "downside_if_fail": "low"},
    # --- Mid/small-cap: space ---
    "IRDM":  {"name": "Iridium",            "basket": "Industrial",  "strategy": "hold_forever", "what": "Satellite communications — global coverage monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "RDW":   {"name": "Redwire",            "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Space infrastructure + 3D printing in orbit",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- Mid/small-cap: fintech/speculative ---
    "HOOD":  {"name": "Robinhood",          "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Commission-free trading platform",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "SOFI":  {"name": "SoFi Technologies", "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Digital banking + lending + investing",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "AFRM":  {"name": "Affirm",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Buy-now-pay-later fintech",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "COIN":  {"name": "Coinbase",           "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Crypto exchange + custody",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "MSTR":  {"name": "MicroStrategy",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Bitcoin treasury company",
              "fragility": "macro",     "downside_if_fail": "severe"},
    # --- Mid/small-cap: medtech/biotech ---
    "HIMS":  {"name": "Hims & Hers",        "basket": "MedTech",     "strategy": "cycle",        "what": "Telehealth + direct-to-consumer pharma",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "OSCR":  {"name": "Oscar Health",       "basket": "MedTech",     "strategy": "cycle",        "what": "Tech-driven health insurance",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "RXRX":  {"name": "Recursion Pharma",   "basket": "MedTech",     "strategy": "catalyst",     "what": "AI-driven drug discovery platform",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- Mid/small-cap: industrial/infra ---
    "TOST":  {"name": "Toast",              "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Restaurant management SaaS + payments",
              "fragility": "none",      "downside_if_fail": "low"},
    "RDDT":  {"name": "Reddit",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Social media + AI data licensing",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "CAVA":  {"name": "Cava Group",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Fast-casual Mediterranean restaurant chain",
              "fragility": "none",      "downside_if_fail": "low"},
    "CELH":  {"name": "Celsius",            "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Energy drink challenger brand",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "GRAB":  {"name": "Grab Holdings",      "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Southeast Asia super-app (ride/food/fintech)",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "DUOL":  {"name": "Duolingo",           "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "AI language learning platform — niche monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    # --- Mid/small-cap: EV/clean energy ---
    "QS":    {"name": "QuantumScape",       "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Solid-state EV batteries — pre-production",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "PLUG":  {"name": "Plug Power",         "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Hydrogen fuel cells — green hydrogen",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "SEDG":  {"name": "SolarEdge",          "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Solar inverters + energy storage",
              "fragility": "macro",     "downside_if_fail": "severe"},
    # --- Mid/small-cap: robotics/automation ---
    "ISRG":  {"name": "Intuitive Surgical", "basket": "MedTech",     "strategy": "hold_forever", "what": "Da Vinci surgical robots — monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "PATH":  {"name": "UiPath",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Robotic process automation (RPA) platform",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "JOBY":  {"name": "Joby Aviation",      "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "eVTOL air taxi — FAA certification pending",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- Stocks that crashed (negative control) ---
    "LCID":  {"name": "Lucid Motors",       "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Luxury EV maker — Saudi-backed",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "RIVN":  {"name": "Rivian",             "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Electric trucks + Amazon delivery vans",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "DNA":   {"name": "Ginkgo Bioworks",    "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Synthetic biology platform — cell programming",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "NKLA":  {"name": "Nikola",             "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Hydrogen fuel cell trucks",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "SPCE":  {"name": "Virgin Galactic",    "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Space tourism — suborbital flights",
              "fragility": "binary",    "downside_if_fail": "severe"},
    # --- EXPANDED UNIVERSE: small/mid-cap breadth for cross-validation ---
    # Semiconductors / hardware
    "MRVL":  {"name": "Marvell Technology","basket": "Industrial",  "strategy": "cycle",        "what": "Custom AI/cloud silicon + networking chips",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "ON":    {"name": "ON Semiconductor",  "basket": "Industrial",  "strategy": "cycle",        "what": "Power semis for EV + industrial",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "WOLF":  {"name": "Wolfspeed",         "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Silicon carbide wafers for EV power",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "MPWR":  {"name": "Monolithic Power",  "basket": "Industrial",  "strategy": "hold_forever", "what": "Power management ICs — data center + auto",
              "fragility": "none",      "downside_if_fail": "low"},
    "ALGM":  {"name": "Allegro Micro",     "basket": "Industrial",  "strategy": "cycle",        "what": "Magnetic sensor ICs for EV + industrial",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "ACLS":  {"name": "Axcelis Tech",      "basket": "Industrial",  "strategy": "cycle",        "what": "Ion implant equipment for chip fabs",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "RMBS":  {"name": "Rambus",            "basket": "Industrial",  "strategy": "hold_forever", "what": "Memory interface chips + silicon IP licensing",
              "fragility": "none",      "downside_if_fail": "low"},
    "POWI":  {"name": "Power Integrations", "basket": "Industrial", "strategy": "cycle",        "what": "High-voltage power conversion ICs",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # Software / SaaS
    "NET":   {"name": "Cloudflare",        "basket": "Cyber",       "strategy": "hold_forever", "what": "Edge network + CDN + zero-trust security",
              "fragility": "none",      "downside_if_fail": "low"},
    "DDOG":  {"name": "Datadog",           "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "Cloud monitoring + observability platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "MDB":   {"name": "MongoDB",           "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "NoSQL database platform — developer-first",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "SNOW":  {"name": "Snowflake",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Cloud data warehouse + analytics",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "CFLT":  {"name": "Confluent",         "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Data streaming platform (Apache Kafka)",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "BILL":  {"name": "Bill Holdings",     "basket": "SpecGrowth",  "strategy": "cycle",        "what": "SMB financial automation + AP/AR",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "GTLB":  {"name": "GitLab",            "basket": "SpecGrowth",  "strategy": "cycle",        "what": "DevSecOps platform — AI-powered CI/CD",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ESTC":  {"name": "Elastic",           "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Search + observability + security analytics",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "DOCN":  {"name": "DigitalOcean",      "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Cloud infrastructure for SMBs + developers",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "BRZE":  {"name": "Braze",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Customer engagement platform — marketing automation",
              "fragility": "none",      "downside_if_fail": "moderate"},
    # Biotech / pharma (small-mid)
    "EXAS":  {"name": "Exact Sciences",    "basket": "MedTech",     "strategy": "cycle",        "what": "Cancer screening — Cologuard + Oncotype",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "INSP":  {"name": "Inspire Medical",   "basket": "MedTech",     "strategy": "hold_forever", "what": "Implantable neurostimulator for sleep apnea",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "NUVB":  {"name": "Nuvation Bio",      "basket": "MedTech",     "strategy": "catalyst",     "what": "Oncology drug pipeline — pre-revenue biotech",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "PCVX":  {"name": "Vaxcyte",           "basket": "MedTech",     "strategy": "catalyst",     "what": "Next-gen pneumococcal vaccines — Phase III",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "VERA":  {"name": "Vera Therapeutics", "basket": "MedTech",     "strategy": "catalyst",     "what": "IgA nephropathy treatment — Phase III",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "KRYS":  {"name": "Krystal Biotech",   "basket": "MedTech",     "strategy": "cycle",        "what": "Gene therapy for skin diseases — Vyjuvek approved",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "GKOS":  {"name": "Glaukos",           "basket": "MedTech",     "strategy": "cycle",        "what": "Micro-invasive glaucoma surgery devices",
              "fragility": "none",      "downside_if_fail": "moderate"},
    # Industrials / infrastructure
    "AAON":  {"name": "AAON",              "basket": "Industrial",  "strategy": "hold_forever", "what": "Premium HVAC equipment — data center cooling",
              "fragility": "none",      "downside_if_fail": "low"},
    "GNRC":  {"name": "Generac",           "basket": "Industrial",  "strategy": "cycle",        "what": "Backup power generators + energy storage",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "TT":    {"name": "Trane Technologies","basket": "Industrial",  "strategy": "hold_forever", "what": "HVAC + climate solutions — data center cooling",
              "fragility": "none",      "downside_if_fail": "low"},
    "EME":   {"name": "EMCOR Group",       "basket": "Industrial",  "strategy": "hold_forever", "what": "Electrical + mechanical construction — data centers",
              "fragility": "none",      "downside_if_fail": "low"},
    "PRIM":  {"name": "Primoris Services", "basket": "Industrial",  "strategy": "cycle",        "what": "Infrastructure construction — energy + utilities",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "TTEK":  {"name": "Tetra Tech",        "basket": "Industrial",  "strategy": "hold_forever", "what": "Environmental + infrastructure consulting",
              "fragility": "none",      "downside_if_fail": "low"},
    "GVA":   {"name": "Granite Construction","basket": "Industrial","strategy": "cycle",        "what": "Heavy civil construction — infrastructure",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # Consumer / retail (small-mid)
    "BROS":  {"name": "Dutch Bros",        "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Drive-thru coffee chain — rapid expansion",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "SHAK":  {"name": "Shake Shack",       "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Fast-casual burger chain — premium positioning",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ELF":   {"name": "e.l.f. Beauty",     "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Value cosmetics brand — Gen Z market share gains",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ONON":  {"name": "On Holding",        "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Swiss performance running shoes + apparel",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "BIRK":  {"name": "Birkenstock",       "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "Heritage footwear brand — pricing power",
              "fragility": "none",      "downside_if_fail": "low"},
    "DKS":   {"name": "Dick's Sporting",   "basket": "Industrial",  "strategy": "cycle",        "what": "Sporting goods retail — market share leader",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # Defense / aerospace (small-mid)
    "AVAV":  {"name": "AeroVironment",     "basket": "Defense",     "strategy": "hold_forever", "what": "Small military drones — Switchblade + Puma",
              "fragility": "political", "downside_if_fail": "moderate"},
    "MRCY":  {"name": "Mercury Systems",   "basket": "Defense",     "strategy": "cycle",        "what": "Defense electronics — sensor processing",
              "fragility": "political", "downside_if_fail": "moderate"},
    "KTOS":  {"name": "Kratos Defense",    "basket": "Defense",     "strategy": "cycle",        "what": "Autonomous military drones + hypersonic",
              "fragility": "political", "downside_if_fail": "moderate"},
    "TDG":   {"name": "TransDigm",         "basket": "Defense",     "strategy": "hold_forever", "what": "Aerospace components — sole-source monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "HEI":   {"name": "HEICO",             "basket": "Defense",     "strategy": "hold_forever", "what": "Aerospace replacement parts — FAA-approved alt",
              "fragility": "none",      "downside_if_fail": "low"},
    # Fintech / payments
    "FOUR":  {"name": "Shift4 Payments",   "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Integrated payments — stadiums + hospitality",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "RELY":  {"name": "Remitly Global",    "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Digital remittances — cross-border payments",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "UPST":  {"name": "Upstart",           "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "AI lending platform — credit underwriting",
              "fragility": "macro",     "downside_if_fail": "severe"},
    "LC":    {"name": "LendingClub",       "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Digital marketplace bank — personal loans",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # Energy / materials
    "FSLR":  {"name": "First Solar",       "basket": "Industrial",  "strategy": "cycle",        "what": "US thin-film solar panel manufacturer",
              "fragility": "political", "downside_if_fail": "moderate"},
    "ENPH":  {"name": "Enphase Energy",    "basket": "Industrial",  "strategy": "cycle",        "what": "Solar microinverters + home batteries",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "MP":    {"name": "MP Materials",      "basket": "Industrial",  "strategy": "cycle",        "what": "Rare earth mining — only US source",
              "fragility": "political", "downside_if_fail": "moderate"},
    "LAC":   {"name": "Lithium Americas",  "basket": "Industrial",  "strategy": "catalyst",     "what": "Thacker Pass lithium mine — largest US deposit",
              "fragility": "political", "downside_if_fail": "severe"},
    "BE":    {"name": "Bloom Energy",      "basket": "Industrial",  "strategy": "cycle",        "what": "Solid oxide fuel cells for data centers",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    # Data / analytics
    "DOMO":  {"name": "Domo",              "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "Cloud BI platform — small-cap turnaround",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "ALTR":  {"name": "Altair Engineering","basket": "Industrial",  "strategy": "hold_forever", "what": "Simulation + AI-driven engineering software",
              "fragility": "none",      "downside_if_fail": "low"},
    "TYL":   {"name": "Tyler Technologies","basket": "Industrial",  "strategy": "hold_forever", "what": "Government software — courts + public safety",
              "fragility": "none",      "downside_if_fail": "low"},
    "DT":    {"name": "Dynatrace",         "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "AI-powered application performance monitoring",
              "fragility": "none",      "downside_if_fail": "low"},
    # Misc small/mid-cap
    "LMND":  {"name": "Lemonade",          "basket": "SpecGrowth",  "strategy": "catalyst",     "what": "AI-powered insurance — renters + pet + auto",
              "fragility": "binary",    "downside_if_fail": "severe"},
    "RKLB":  {"name": "Rocket Lab",        "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Rockets + space systems — Neutron pending",
              "fragility": "binary",    "downside_if_fail": "moderate"},
    "MNDY":  {"name": "monday.com",        "basket": "SpecGrowth",  "strategy": "hold_forever", "what": "Work management SaaS — CRM expansion",
              "fragility": "none",      "downside_if_fail": "low"},
    "GLBE":  {"name": "Global-e Online",   "basket": "SpecGrowth",  "strategy": "cycle",        "what": "Cross-border e-commerce platform",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "WDAY":  {"name": "Workday",           "basket": "Industrial",  "strategy": "hold_forever", "what": "Enterprise HR + finance cloud software",
              "fragility": "none",      "downside_if_fail": "low"},
    "PAYC":  {"name": "Paycom Software",   "basket": "Industrial",  "strategy": "hold_forever", "what": "Payroll + HCM SaaS — single-database platform",
              "fragility": "none",      "downside_if_fail": "low"},
    "PCOR":  {"name": "Procore Tech",      "basket": "Industrial",  "strategy": "cycle",        "what": "Construction management SaaS platform",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "IOT":   {"name": "Samsara",           "basket": "Industrial",  "strategy": "cycle",        "what": "IoT fleet management + industrial operations",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "ANET":  {"name": "Arista Networks",   "basket": "Industrial",  "strategy": "hold_forever", "what": "Data center networking switches — AI/cloud",
              "fragility": "none",      "downside_if_fail": "low"},
    "CYBR":  {"name": "CyberArk",          "basket": "Cyber",       "strategy": "hold_forever", "what": "Privileged access management — identity security",
              "fragility": "none",      "downside_if_fail": "low"},
    "TENB":  {"name": "Tenable",           "basket": "Cyber",       "strategy": "cycle",        "what": "Vulnerability management + exposure analytics",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "RPD":   {"name": "Rapid7",            "basket": "Cyber",       "strategy": "cycle",        "what": "Cloud security + threat detection platform",
              "fragility": "none",      "downside_if_fail": "moderate"},
    "VRNS":  {"name": "Varonis Systems",   "basket": "Cyber",       "strategy": "cycle",        "what": "Data security + insider threat detection",
              "fragility": "none",      "downside_if_fail": "moderate"},
    # Large-cap anchors (stable references for cross-validation calibration)
    "NVDA":  {"name": "Nvidia",            "basket": "Industrial",  "strategy": "hold_forever", "what": "GPU + AI accelerator monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "MSFT":  {"name": "Microsoft",         "basket": "Industrial",  "strategy": "hold_forever", "what": "Cloud + enterprise software + AI",
              "fragility": "none",      "downside_if_fail": "low"},
    "AAPL":  {"name": "Apple",             "basket": "Industrial",  "strategy": "hold_forever", "what": "Consumer hardware + services ecosystem",
              "fragility": "none",      "downside_if_fail": "low"},
    "GOOGL": {"name": "Alphabet",          "basket": "Industrial",  "strategy": "hold_forever", "what": "Search + cloud + AI — ad revenue monopoly",
              "fragility": "none",      "downside_if_fail": "low"},
    "AMZN":  {"name": "Amazon",            "basket": "Industrial",  "strategy": "hold_forever", "what": "E-commerce + AWS cloud + AI",
              "fragility": "none",      "downside_if_fail": "low"},
    "META":  {"name": "Meta Platforms",    "basket": "Industrial",  "strategy": "hold_forever", "what": "Social media + AI + metaverse",
              "fragility": "none",      "downside_if_fail": "low"},
    "TSLA":  {"name": "Tesla",             "basket": "SpecGrowth",  "strategy": "cycle",        "what": "EV + energy + autonomous driving",
              "fragility": "macro",     "downside_if_fail": "moderate"},
    "AMD":   {"name": "AMD",               "basket": "Industrial",  "strategy": "cycle",        "what": "CPU + GPU — AI accelerator challenger",
              "fragility": "macro",     "downside_if_fail": "moderate"},
}


# =========================================================================
# HISTORICAL ANALYST DATA — reconstructed from upgrades_downgrades
# =========================================================================

# Map the many analyst grade labels to buy/hold/sell buckets
_GRADE_MAP = {
    # Buy-equivalent
    "Buy": "buy", "Outperform": "buy", "Overweight": "buy",
    "Positive": "buy", "Market Outperform": "buy",
    "Strong Buy": "buy", "Top Pick": "buy", "Sector Outperform": "buy",
    # Hold-equivalent
    "Hold": "hold", "Neutral": "hold", "Equal-Weight": "hold",
    "Market Perform": "hold", "In-Line": "hold",
    "Sector Perform": "hold", "Sector Weight": "hold",
    "Peer Perform": "hold", "Mixed": "hold", "Fair Value": "hold",
    # Sell-equivalent
    "Sell": "sell", "Underperform": "sell", "Underweight": "sell",
    "Reduce": "sell", "Strong Sell": "sell",
}


def _reconstruct_analyst_data(ticker_obj, lookback_date, price_then):
    """Reconstruct analyst target price and consensus from upgrades_downgrades.

    Uses the ~20 most recent analyst actions before lookback_date to compute:
    - Median price target (as analysts saw it then)
    - Consensus recommendation (buy/hold/sell ratio)
    - Number of analysts with coverage

    Returns (target_price, recommendation_key, num_analysts) or (None, "none", 0).
    """
    try:
        ud = ticker_obj.upgrades_downgrades
        if ud is None or len(ud) == 0:
            return None, "none", 0

        import pandas as pd
        cutoff = pd.Timestamp(lookback_date)
        if ud.index.tz:
            cutoff = cutoff.tz_localize(ud.index.tz)

        before = ud[ud.index <= cutoff]
        if len(before) == 0:
            return None, "none", 0

        # Use the most recent 20 analyst actions (typical coverage window)
        recent = before.head(20)

        # --- Price target: median of non-zero targets ---
        targets = recent["currentPriceTarget"].dropna()
        targets = targets[targets > 0]
        target_price = float(targets.median()) if len(targets) >= 3 else None

        # --- Consensus: map grades to buy/hold/sell, take majority ---
        grades = recent["ToGrade"].dropna()
        buy_count = 0
        hold_count = 0
        sell_count = 0
        for g in grades:
            bucket = _GRADE_MAP.get(g, "hold")  # unknown → hold
            if bucket == "buy":
                buy_count += 1
            elif bucket == "sell":
                sell_count += 1
            else:
                hold_count += 1

        total = buy_count + hold_count + sell_count
        if total == 0:
            return target_price, "none", 0

        # Determine consensus from ratio
        buy_pct = buy_count / total
        sell_pct = sell_count / total
        if buy_pct >= 0.7:
            rec = "strongBuy"
        elif buy_pct >= 0.5:
            rec = "buy"
        elif sell_pct >= 0.5:
            rec = "sell"
        elif sell_pct >= 0.3:
            rec = "underperform"
        else:
            rec = "hold"

        return target_price, rec, total

    except Exception:
        return None, "none", 0


# =========================================================================
# HISTORICAL DATA FETCHING
# =========================================================================

def fetch_historical_data(ticker, lookback_date):
    """Fetch stock data as it would have appeared on lookback_date.

    Reconstructs historical fundamentals:
    - Revenue growth + acceleration: from annual income statements (quarterly
      if 8+ quarters available, else annual FY data going back 5 years)
    - EPS, FCF, cash: from quarterly financials available at lookback_date
    - Market cap: price_then × current shares (approximation)
    - SMAs, 52w range: from historical price data
    - 2y high + history_years: from 4-year price window (so LT health works)
    - Analyst targets/consensus: ALWAYS neutralized — Yahoo only has current
      targets, using them on old prices is look-ahead bias

    Args:
        ticker: stock ticker
        lookback_date: datetime — the "as of" date for the backtest

    Returns:
        dict with same keys as ranking.fetch_stock_data, plus 'price_now'
    """
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}

        # --- Historical price on lookback_date ---
        # Fetch a window around the lookback date to ensure we get a trading day
        start = lookback_date - timedelta(days=10)
        end = lookback_date + timedelta(days=5)
        hist_window = t.history(start=start, end=end)
        if hist_window.empty:
            return {"error": f"no price data around {lookback_date.date()}"}

        close = hist_window["Close"].dropna()
        if close.empty:
            return {"error": "no close prices"}

        # Get the last price on or before lookback_date
        mask = close.index <= lookback_date.strftime("%Y-%m-%d 23:59:59")
        if hasattr(close.index, 'tz') and close.index.tz is not None:
            from pandas import Timestamp
            cutoff = Timestamp(lookback_date).tz_localize(close.index.tz)
            mask = close.index <= cutoff
        prices_before = close[mask]
        if prices_before.empty:
            price_then = float(close.iloc[0])
        else:
            price_then = float(prices_before.iloc[-1])

        # --- Current price (for return calculation) ---
        hist_now = t.history(period="5d")
        close_now = hist_now["Close"].dropna()
        price_now = float(close_now.iloc[-1]) if not close_now.empty else None

        # --- Historical SMAs (need 4+ years so history_years >= 3 for LT health) ---
        hist_start = lookback_date - timedelta(days=1500)
        hist_2y = t.history(start=hist_start, end=lookback_date + timedelta(days=1))
        hist_close = hist_2y["Close"].dropna() if not hist_2y.empty else None

        sma_50 = None
        sma_200 = None
        high_2y = None
        history_years = None
        if hist_close is not None and len(hist_close) > 0:
            if len(hist_close) >= 50:
                sma_50 = float(hist_close.rolling(50).mean().iloc[-1])
            if len(hist_close) >= 200:
                sma_200 = float(hist_close.rolling(200).mean().iloc[-1])
            high_2y = float(hist_close.max())
            history_years = len(hist_close) / 252.0

        # --- Historical 52w range ---
        hist_52w = hist_close.iloc[-252:] if hist_close is not None and len(hist_close) >= 252 else hist_close
        high_52w = float(hist_52w.max()) if hist_52w is not None and len(hist_52w) > 0 else None
        low_52w = float(hist_52w.min()) if hist_52w is not None and len(hist_52w) > 0 else None

        # --- Revenue growth from financials ---
        # Try quarterly first (TTM), fall back to annual statements.
        # yfinance only returns ~5 quarters, so for lookbacks > a few months
        # quarterly data is usually insufficient. Annual data goes back 5 years.
        rev_growth = None
        prior_rev_growth = None
        total_revenue = None
        try:
            # --- Attempt 1: quarterly TTM (needs 8 quarters) ---
            qf = t.quarterly_income_stmt
            if qf is not None and "Total Revenue" in qf.index:
                avail_cols = [c for c in qf.columns if c <= lookback_date + timedelta(days=45)]
                if len(avail_cols) >= 8:
                    recent_4 = sum(qf.loc["Total Revenue", avail_cols[:4]])
                    prior_4 = sum(qf.loc["Total Revenue", avail_cols[4:8]])
                    if prior_4 and prior_4 > 0 and recent_4 and recent_4 > 0:
                        rev_growth = ((recent_4 - prior_4) / prior_4) * 100
                        total_revenue = recent_4
                if len(avail_cols) >= 12:
                    prev_4 = sum(qf.loc["Total Revenue", avail_cols[4:8]])
                    prev_prior_4 = sum(qf.loc["Total Revenue", avail_cols[8:12]])
                    if prev_prior_4 and prev_prior_4 > 0 and prev_4 and prev_4 > 0:
                        prior_rev_growth = ((prev_4 - prev_prior_4) / prev_prior_4) * 100

            # --- Attempt 2: annual statements (needs 2-3 fiscal years) ---
            if rev_growth is None:
                af = t.income_stmt
                if af is not None and "Total Revenue" in af.index:
                    # Annual reports available ~90 days after fiscal year end
                    avail_annual = [c for c in af.columns
                                    if c <= lookback_date + timedelta(days=90)]
                    if len(avail_annual) >= 2:
                        r_recent = af.loc["Total Revenue", avail_annual[0]]
                        r_prior = af.loc["Total Revenue", avail_annual[1]]
                        if (r_prior and r_prior > 0 and r_recent and r_recent > 0
                                and not np.isnan(r_recent) and not np.isnan(r_prior)):
                            rev_growth = ((r_recent - r_prior) / r_prior) * 100
                            total_revenue = float(r_recent)
                    # Acceleration: prior year vs year before that
                    if len(avail_annual) >= 3 and prior_rev_growth is None:
                        r_mid = af.loc["Total Revenue", avail_annual[1]]
                        r_old = af.loc["Total Revenue", avail_annual[2]]
                        if (r_old and r_old > 0 and r_mid and r_mid > 0
                                and not np.isnan(r_mid) and not np.isnan(r_old)):
                            prior_rev_growth = ((r_mid - r_old) / r_old) * 100
        except Exception:
            pass

        # Fall back to info only for recent lookbacks (≤18 months)
        months_ago = (datetime.now() - lookback_date).days / 30
        is_recent = months_ago <= 18

        if rev_growth is None and is_recent:
            rg = info.get("revenueGrowth")
            rev_growth = (rg * 100) if rg is not None else None
            if not total_revenue:
                total_revenue = info.get("totalRevenue", 0)

        # --- Valuation: compute historical P/S ---
        shares = info.get("sharesOutstanding")
        ps_ratio = None
        if total_revenue and total_revenue > 0 and shares and shares > 0:
            ps_ratio = (price_then * shares) / total_revenue

        # Fall back to current P/S only for recent lookbacks
        if ps_ratio is None and is_recent:
            ps_ratio = info.get("priceToSalesTrailing12Months")

        # --- Historical market cap (price_then × shares) ---
        market_cap = None
        if shares and shares > 0:
            market_cap = price_then * shares
        elif is_recent:
            market_cap = info.get("marketCap")

        # --- Cash and profitability ---
        # Try to reconstruct from quarterly financials
        eps = None
        free_cash_flow = None
        total_cash = None
        try:
            # EPS from quarterly income statement
            qf = t.quarterly_income_stmt
            if qf is not None:
                avail_cols = [c for c in qf.columns if c <= lookback_date + timedelta(days=45)]
                if len(avail_cols) >= 4:
                    # Net income TTM / shares = approximate EPS
                    if "Net Income" in qf.index and shares and shares > 0:
                        net_income_ttm = sum(qf.loc["Net Income", avail_cols[:4]])
                        if net_income_ttm is not None:
                            eps = net_income_ttm / shares

            # FCF from quarterly cash flow statement
            qcf = t.quarterly_cashflow
            if qcf is not None:
                avail_cols = [c for c in qcf.columns if c <= lookback_date + timedelta(days=45)]
                if len(avail_cols) >= 4:
                    if "Free Cash Flow" in qcf.index:
                        free_cash_flow = sum(qcf.loc["Free Cash Flow", avail_cols[:4]])

            # Cash from balance sheet (most recent quarter before lookback)
            qbs = t.quarterly_balance_sheet
            if qbs is not None:
                avail_cols = [c for c in qbs.columns if c <= lookback_date + timedelta(days=45)]
                if len(avail_cols) >= 1:
                    if "Cash And Cash Equivalents" in qbs.index:
                        total_cash = qbs.loc["Cash And Cash Equivalents", avail_cols[0]]
                        if total_cash is not None:
                            total_cash = float(total_cash)
        except Exception:
            pass

        # Fall back to current values only for recent lookbacks
        if is_recent:
            if eps is None:
                eps = info.get("trailingEps")
            if free_cash_flow is None:
                free_cash_flow = info.get("freeCashflow")
            if total_cash is None:
                total_cash = info.get("totalCash")

        # --- Analyst data (reconstructed from historical upgrades/downgrades) ---
        # Yahoo's info.targetMeanPrice is today's target — using it on old
        # prices is look-ahead bias. Instead, reconstruct from the dated
        # upgrades_downgrades table which has per-analyst price targets and
        # grades going back years.
        target, rec, num_analysts = _reconstruct_analyst_data(
            t, lookback_date, price_then
        )

        return {
            "price": price_then,
            "price_now": price_now,
            "target": target,
            "recommendation": rec,
            "num_analysts": num_analysts or 0,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "market_cap": market_cap,
            "total_revenue": total_revenue,
            "rev_growth_pct": rev_growth,
            "prior_rev_growth_pct": prior_rev_growth,
            "eps": eps,
            "free_cash_flow": free_cash_flow,
            "ps_ratio": ps_ratio,
            "total_cash": total_cash,
            "high_2y": high_2y,
            "history_years": round(history_years, 1) if history_years else None,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "error": None,
        }

    except Exception as e:
        return {"error": str(e)}


# =========================================================================
# BACKTEST ENGINE
# =========================================================================

def compute_backtest_score(data, meta):
    """Same as compute_composite but works with historical data."""
    if data.get("error"):
        return 0, {}

    price = data["price"]
    strategy = meta.get("strategy", "hold_forever")
    w = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["hold_forever"])

    s_upside = score_analyst_upside(price, data["target"])
    s_growth = score_revenue_quality(
        data["rev_growth_pct"], data.get("total_revenue", 0)
    )
    s_accel = score_revenue_acceleration(
        data.get("rev_growth_pct"), data.get("prior_rev_growth_pct")
    )
    s_valuation = score_valuation(data.get("ps_ratio"))
    s_long_term = score_long_term_health(
        price, data.get("high_2y"), data.get("history_years")
    )
    s_cash = score_cash_runway(
        data.get("total_cash"), data.get("free_cash_flow"), data.get("eps")
    )
    s_conviction = score_analyst_conviction(
        data["recommendation"], data["num_analysts"]
    )
    s_entry = score_entry_position(price, data["high_52w"], data["low_52w"])
    s_momentum = score_momentum(price, data["sma_50"], data["sma_200"])

    base_score = (
        s_upside * w["upside"]
        + s_growth * w["growth"]
        + s_accel * w["accel"]
        + s_valuation * w["valuation"]
        + s_long_term * w["long_term"]
        + s_cash * w["cash_runway"]
        + s_conviction * w["conviction"]
        + s_entry * w["entry"]
        + s_momentum * w["momentum"]
    )

    p_fragility = penalty_fragility(meta.get("fragility", "none"))
    p_downside = penalty_downside(meta.get("downside_if_fail", "low"))
    b_profit = bonus_profitability(
        data.get("eps"), data.get("free_cash_flow"), data.get("market_cap")
    )

    composite = base_score + b_profit + p_fragility + p_downside
    composite = max(0, min(100, composite))

    breakdown = {
        "upside": round(s_upside, 1),
        "growth": round(s_growth, 1),
        "accel": round(s_accel, 1),
        "valuation": round(s_valuation, 1),
        "long_term": round(s_long_term, 1),
        "cash_runway": round(s_cash, 1),
        "conviction": round(s_conviction, 1),
        "entry": round(s_entry, 1),
        "momentum": round(s_momentum, 1),
        "profitability": b_profit,
        "fragility": p_fragility,
        "downside": p_downside,
    }

    return round(composite, 1), breakdown


def run_backtest(lookback_months=12):
    """Run the ranking model on historical data and compare with actual returns.

    Args:
        lookback_months: how many months ago to simulate (default 12)

    Returns:
        list of dicts with ranking, score, actual return, sorted by score desc
    """
    lookback_date = datetime.now() - timedelta(days=lookback_months * 30)

    # Combine ranking universe + extra stocks
    universe = {}
    universe.update(RANKING_UNIVERSE)
    universe.update(BACKTEST_EXTRA)

    results = []

    for ticker, meta in universe.items():
        data = fetch_historical_data(ticker, lookback_date)

        if data.get("error"):
            print(f"  ⚠️ {ticker}: {data['error']}")
            continue

        score, breakdown = compute_backtest_score(data, meta)

        # Actual return
        price_then = data["price"]
        price_now = data.get("price_now")
        if price_then and price_now and price_then > 0:
            actual_return = ((price_now - price_then) / price_then) * 100
        else:
            actual_return = None

        results.append({
            "ticker": ticker,
            "name": meta["name"],
            "basket": meta["basket"],
            "strategy": meta["strategy"],
            "what": meta["what"],
            "price_then": round(price_then, 2),
            "price_now": round(price_now, 2) if price_now else None,
            "actual_return_pct": round(actual_return, 1) if actual_return is not None else None,
            "score": score,
            "breakdown": breakdown,
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    # Assign ranks
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


def compute_validation_stats(results):
    """Compute validation metrics from backtest results.

    Returns dict with:
    - quintile_returns: avg return per quintile (top 20%, next 20%, etc.)
    - top5_avg, top10_avg, bottom10_avg: avg returns for key groups
    - correlation: rank correlation between score and return
    - hit_rate: % of top-half stocks that beat bottom-half average
    """
    # Filter out stocks with no return data
    valid = [r for r in results if r["actual_return_pct"] is not None]
    if len(valid) < 10:
        return {"error": "Not enough data for validation"}

    n = len(valid)

    # Quintile analysis (5 groups)
    q_size = n // 5
    quintiles = {}
    for i in range(5):
        start = i * q_size
        end = start + q_size if i < 4 else n
        group = valid[start:end]
        avg_ret = np.mean([r["actual_return_pct"] for r in group])
        avg_score = np.mean([r["score"] for r in group])
        quintiles[f"Q{i+1}"] = {
            "label": ["Top 20%", "20-40%", "40-60%", "60-80%", "Bottom 20%"][i],
            "avg_return": round(avg_ret, 1),
            "avg_score": round(avg_score, 1),
            "stocks": [r["ticker"] for r in group],
        }

    # Key group averages
    top5 = valid[:5]
    top10 = valid[:10]
    bottom10 = valid[-10:]

    top5_avg = round(np.mean([r["actual_return_pct"] for r in top5]), 1)
    top10_avg = round(np.mean([r["actual_return_pct"] for r in top10]), 1)
    bottom10_avg = round(np.mean([r["actual_return_pct"] for r in bottom10]), 1)

    # Rank correlation (Spearman)
    scores = [r["score"] for r in valid]
    returns = [r["actual_return_pct"] for r in valid]
    # Simple rank correlation
    score_ranks = np.argsort(np.argsort([-s for s in scores])) + 1
    return_ranks = np.argsort(np.argsort([-r for r in returns])) + 1
    n_v = len(valid)
    d_sq = sum((sr - rr) ** 2 for sr, rr in zip(score_ranks, return_ranks))
    spearman = 1 - (6 * d_sq) / (n_v * (n_v ** 2 - 1))

    # Hit rate: % of top-half that beat median return
    median_return = np.median(returns)
    top_half = valid[:n // 2]
    hits = sum(1 for r in top_half if r["actual_return_pct"] > median_return)
    hit_rate = round((hits / len(top_half)) * 100, 1)

    # Win rate: % of top 10 that had positive returns
    top10_positive = sum(1 for r in top10 if r["actual_return_pct"] > 0)
    win_rate = round((top10_positive / len(top10)) * 100, 1)

    return {
        "quintiles": quintiles,
        "top5_avg_return": top5_avg,
        "top10_avg_return": top10_avg,
        "bottom10_avg_return": bottom10_avg,
        "spearman_correlation": round(spearman, 3),
        "hit_rate": hit_rate,
        "win_rate_top10": win_rate,
        "total_stocks": n,
    }
