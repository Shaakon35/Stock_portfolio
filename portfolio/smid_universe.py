"""
~700 US small/mid-cap tickers for optimization.
Sourced from S&P 400 MidCap, S&P 600 SmallCap, Russell 2000 components.
Each ticker has a default strategy assignment based on market cap and sector.
"""

# Format: ticker -> {strategy, basket}
# strategy: hold_forever (quality compounder), cycle (cyclical), catalyst (binary event)
# We assign defaults; the optimizer will find weights per strategy anyway.

SMID_UNIVERSE = {}

def _add(tickers_dict):
    SMID_UNIVERSE.update(tickers_dict)

# --- TECHNOLOGY / SOFTWARE ---
_add({
    "TENB": {"s": "hold_forever", "b": "Cyber"}, "VRNS": {"s": "hold_forever", "b": "Cyber"},
    "RPD": {"s": "cycle", "b": "Cyber"}, "CYBR": {"s": "hold_forever", "b": "Cyber"},
    "MNDY": {"s": "hold_forever", "b": "SpecGrowth"}, "PCOR": {"s": "cycle", "b": "SpecGrowth"},
    "PAYC": {"s": "hold_forever", "b": "SpecGrowth"}, "WDAY": {"s": "hold_forever", "b": "SpecGrowth"},
    "TYL": {"s": "hold_forever", "b": "SpecGrowth"}, "DT": {"s": "hold_forever", "b": "SpecGrowth"},
    "IOT": {"s": "cycle", "b": "SpecGrowth"}, "FOUR": {"s": "cycle", "b": "SpecGrowth"},
    "RELY": {"s": "cycle", "b": "SpecGrowth"}, "GLBE": {"s": "cycle", "b": "SpecGrowth"},
    "DOMO": {"s": "catalyst", "b": "SpecGrowth"}, "LMND": {"s": "catalyst", "b": "SpecGrowth"},
    "UPST": {"s": "catalyst", "b": "SpecGrowth"}, "LC": {"s": "cycle", "b": "SpecGrowth"},
    "ALTR": {"s": "cycle", "b": "Industrial"},
    "CVLT": {"s": "hold_forever", "b": "Cyber"}, "QLYS": {"s": "hold_forever", "b": "Cyber"},
    "SAIL": {"s": "cycle", "b": "Cyber"}, "RDWR": {"s": "cycle", "b": "Cyber"},
    "VRNT": {"s": "cycle", "b": "SpecGrowth"}, "PRGS": {"s": "hold_forever", "b": "SpecGrowth"},
    "JAMF": {"s": "cycle", "b": "SpecGrowth"}, "ALRM": {"s": "hold_forever", "b": "SpecGrowth"},
    "SMAR": {"s": "cycle", "b": "SpecGrowth"}, "APPF": {"s": "cycle", "b": "SpecGrowth"},
    "NCNO": {"s": "cycle", "b": "SpecGrowth"}, "FRSH": {"s": "cycle", "b": "SpecGrowth"},
    "CWAN": {"s": "cycle", "b": "SpecGrowth"}, "QTWO": {"s": "cycle", "b": "SpecGrowth"},
    "PYCR": {"s": "cycle", "b": "SpecGrowth"}, "INTA": {"s": "cycle", "b": "SpecGrowth"},
    "SEMR": {"s": "cycle", "b": "SpecGrowth"}, "SQSP": {"s": "cycle", "b": "SpecGrowth"},
    "WEAV": {"s": "catalyst", "b": "SpecGrowth"}, "CXAI": {"s": "catalyst", "b": "SpecGrowth"},
    "BIGC": {"s": "catalyst", "b": "SpecGrowth"}, "GENI": {"s": "cycle", "b": "SpecGrowth"},
    "MAPS": {"s": "catalyst", "b": "SpecGrowth"}, "RAMP": {"s": "cycle", "b": "SpecGrowth"},
})

# --- SEMICONDUCTORS / HARDWARE ---
_add({
    "CRUS": {"s": "cycle", "b": "Industrial"}, "DIOD": {"s": "cycle", "b": "Industrial"},
    "AMBA": {"s": "cycle", "b": "Industrial"}, "SITM": {"s": "cycle", "b": "Industrial"},
    "SLAB": {"s": "cycle", "b": "Industrial"}, "SMTC": {"s": "cycle", "b": "Industrial"},
    "AOSL": {"s": "cycle", "b": "Industrial"}, "INDI": {"s": "catalyst", "b": "Industrial"},
    "MTSI": {"s": "cycle", "b": "Industrial"}, "COHR": {"s": "cycle", "b": "Industrial"},
    "IPGP": {"s": "cycle", "b": "Industrial"}, "MKSI": {"s": "cycle", "b": "Industrial"},
    "NOVT": {"s": "hold_forever", "b": "Industrial"}, "ONTO": {"s": "cycle", "b": "Industrial"},
    "FORM": {"s": "cycle", "b": "Industrial"}, "CEVA": {"s": "cycle", "b": "Industrial"},
    "PLAB": {"s": "cycle", "b": "Industrial"}, "AMKR": {"s": "cycle", "b": "Industrial"},
    "SGH": {"s": "cycle", "b": "Industrial"}, "PI": {"s": "cycle", "b": "Industrial"},
    "LFUS": {"s": "hold_forever", "b": "Industrial"}, "NXPI": {"s": "cycle", "b": "Industrial"},
    "SWKS": {"s": "cycle", "b": "Industrial"}, "QRVO": {"s": "cycle", "b": "Industrial"},
    "MCHP": {"s": "cycle", "b": "Industrial"}, "TER": {"s": "cycle", "b": "Industrial"},
    "ENTG": {"s": "hold_forever", "b": "Industrial"}, "LRCX": {"s": "cycle", "b": "Industrial"},
    "KLAC": {"s": "hold_forever", "b": "Industrial"}, "AEHR": {"s": "catalyst", "b": "Industrial"},
})

# --- BIOTECH / MEDTECH ---
_add({
    "AXSM": {"s": "catalyst", "b": "MedTech"}, "CORT": {"s": "cycle", "b": "MedTech"},
    "FOLD": {"s": "catalyst", "b": "MedTech"}, "GERN": {"s": "catalyst", "b": "MedTech"},
    "HALO": {"s": "cycle", "b": "MedTech"}, "IOVA": {"s": "catalyst", "b": "MedTech"},
    "LEGN": {"s": "catalyst", "b": "MedTech"}, "MGNX": {"s": "catalyst", "b": "MedTech"},
    "NTRA": {"s": "hold_forever", "b": "MedTech"}, "RARE": {"s": "catalyst", "b": "MedTech"},
    "RGEN": {"s": "cycle", "b": "MedTech"}, "SGEN": {"s": "catalyst", "b": "MedTech"},
    "TWST": {"s": "catalyst", "b": "MedTech"}, "XNCR": {"s": "catalyst", "b": "MedTech"},
    "ARWR": {"s": "catalyst", "b": "MedTech"}, "BEAM": {"s": "catalyst", "b": "MedTech"},
    "CRSP": {"s": "catalyst", "b": "MedTech"}, "NTLA": {"s": "catalyst", "b": "MedTech"},
    "EDIT": {"s": "catalyst", "b": "MedTech"}, "FATE": {"s": "catalyst", "b": "MedTech"},
    "IONS": {"s": "hold_forever", "b": "MedTech"}, "NBIX": {"s": "hold_forever", "b": "MedTech"},
    "PTCT": {"s": "cycle", "b": "MedTech"}, "SRPT": {"s": "catalyst", "b": "MedTech"},
    "UTHR": {"s": "hold_forever", "b": "MedTech"}, "XENE": {"s": "catalyst", "b": "MedTech"},
    "CYTK": {"s": "catalyst", "b": "MedTech"}, "ARVN": {"s": "catalyst", "b": "MedTech"},
    "RCKT": {"s": "catalyst", "b": "MedTech"}, "DNLI": {"s": "catalyst", "b": "MedTech"},
    "PRCT": {"s": "cycle", "b": "MedTech"}, "RVMD": {"s": "cycle", "b": "MedTech"},
    "MDGL": {"s": "catalyst", "b": "MedTech"}, "ITCI": {"s": "cycle", "b": "MedTech"},
    "CRNX": {"s": "catalyst", "b": "MedTech"}, "APLS": {"s": "catalyst", "b": "MedTech"},
    "ACLX": {"s": "catalyst", "b": "MedTech"}, "KYMR": {"s": "catalyst", "b": "MedTech"},
    "IMVT": {"s": "catalyst", "b": "MedTech"}, "TGTX": {"s": "cycle", "b": "MedTech"},
    "ROIV": {"s": "catalyst", "b": "MedTech"}, "INSM": {"s": "cycle", "b": "MedTech"},
    "PODD": {"s": "hold_forever", "b": "MedTech"}, "DXCM": {"s": "hold_forever", "b": "MedTech"},
    "ALGN": {"s": "cycle", "b": "MedTech"}, "HOLX": {"s": "hold_forever", "b": "MedTech"},
    "NVCR": {"s": "catalyst", "b": "MedTech"}, "AZTA": {"s": "cycle", "b": "MedTech"},
    "NEOG": {"s": "cycle", "b": "MedTech"}, "OLINK": {"s": "cycle", "b": "MedTech"},
})

# --- INDUSTRIALS / INFRASTRUCTURE ---
_add({
    "ATKR": {"s": "cycle", "b": "Industrial"}, "AZEK": {"s": "cycle", "b": "Industrial"},
    "BLDR": {"s": "cycle", "b": "Industrial"}, "CALX": {"s": "cycle", "b": "Industrial"},
    "CSWI": {"s": "hold_forever", "b": "Industrial"}, "EXP": {"s": "cycle", "b": "Industrial"},
    "FBIN": {"s": "cycle", "b": "Industrial"}, "GTLS": {"s": "cycle", "b": "Industrial"},
    "IESC": {"s": "hold_forever", "b": "Industrial"}, "LNTH": {"s": "cycle", "b": "Industrial"},
    "MATX": {"s": "cycle", "b": "Industrial"}, "MIDD": {"s": "cycle", "b": "Industrial"},
    "SITE": {"s": "cycle", "b": "Industrial"}, "SPSC": {"s": "hold_forever", "b": "Industrial"},
    "TREX": {"s": "cycle", "b": "Industrial"}, "WMS": {"s": "cycle", "b": "Industrial"},
    "WDFC": {"s": "hold_forever", "b": "Industrial"}, "ZWS": {"s": "cycle", "b": "Industrial"},
    "ROAD": {"s": "cycle", "b": "Industrial"}, "STRL": {"s": "cycle", "b": "Industrial"},
    "EXPO": {"s": "hold_forever", "b": "Industrial"}, "ESAB": {"s": "cycle", "b": "Industrial"},
    "KRNT": {"s": "cycle", "b": "Industrial"}, "REZI": {"s": "cycle", "b": "Industrial"},
    "ASPN": {"s": "cycle", "b": "Industrial"}, "ROCK": {"s": "hold_forever", "b": "Industrial"},
    "SPXC": {"s": "hold_forever", "b": "Industrial"}, "RBC": {"s": "hold_forever", "b": "Industrial"},
    "PIPR": {"s": "cycle", "b": "Industrial"}, "CWST": {"s": "hold_forever", "b": "Industrial"},
    "TNET": {"s": "cycle", "b": "Industrial"}, "ASGN": {"s": "cycle", "b": "Industrial"},
    "BFAM": {"s": "hold_forever", "b": "Industrial"}, "ENSG": {"s": "hold_forever", "b": "Industrial"},
    "LSTR": {"s": "cycle", "b": "Industrial"}, "SAIA": {"s": "cycle", "b": "Industrial"},
    "ODFL": {"s": "hold_forever", "b": "Industrial"}, "XPO": {"s": "cycle", "b": "Industrial"},
    "ARCB": {"s": "cycle", "b": "Industrial"}, "HUBG": {"s": "cycle", "b": "Industrial"},
    "SNDR": {"s": "cycle", "b": "Industrial"}, "WERN": {"s": "cycle", "b": "Industrial"},
    "JBHT": {"s": "hold_forever", "b": "Industrial"}, "SKYW": {"s": "cycle", "b": "Industrial"},
    "ALG": {"s": "hold_forever", "b": "Industrial"}, "EPAC": {"s": "hold_forever", "b": "Industrial"},
    "FSS": {"s": "cycle", "b": "Industrial"}, "HAYW": {"s": "cycle", "b": "Industrial"},
    "MBC": {"s": "cycle", "b": "Industrial"}, "PRLB": {"s": "cycle", "b": "Industrial"},
})

# --- DEFENSE / AEROSPACE ---
_add({
    "HEI": {"s": "hold_forever", "b": "Defense"}, "TDG": {"s": "hold_forever", "b": "Defense"},
    "AJRD": {"s": "cycle", "b": "Defense"}, "MRCY": {"s": "cycle", "b": "Defense"},
    "AVAV": {"s": "hold_forever", "b": "Defense"}, "CACI": {"s": "hold_forever", "b": "Defense"},
    "LDOS": {"s": "hold_forever", "b": "Defense"}, "SAIC": {"s": "cycle", "b": "Defense"},
    "BWXT": {"s": "hold_forever", "b": "Defense"}, "KTOS": {"s": "cycle", "b": "Defense"},
    "RKLB": {"s": "cycle", "b": "Defense"}, "LUNR": {"s": "catalyst", "b": "Defense"},
    "ERII": {"s": "cycle", "b": "Defense"}, "SWBI": {"s": "cycle", "b": "Defense"},
    "RGR": {"s": "cycle", "b": "Defense"}, "VSAT": {"s": "cycle", "b": "Defense"},
    "SPIR": {"s": "catalyst", "b": "Defense"}, "MNTS": {"s": "catalyst", "b": "Defense"},
    "MAXR": {"s": "cycle", "b": "Defense"}, "PSN": {"s": "hold_forever", "b": "Defense"},
})

# --- ENERGY / CLEAN ENERGY / MINING ---
_add({
    "ARRY": {"s": "cycle", "b": "Industrial"}, "FLNC": {"s": "cycle", "b": "Industrial"},
    "RUN": {"s": "catalyst", "b": "SpecGrowth"}, "NOVA": {"s": "cycle", "b": "SpecGrowth"},
    "SHLS": {"s": "cycle", "b": "Industrial"}, "STEM": {"s": "catalyst", "b": "SpecGrowth"},
    "CHPT": {"s": "catalyst", "b": "SpecGrowth"}, "BLNK": {"s": "catalyst", "b": "SpecGrowth"},
    "EVGO": {"s": "catalyst", "b": "SpecGrowth"}, "CLSK": {"s": "cycle", "b": "Industrial"},
    "MARA": {"s": "cycle", "b": "Industrial"}, "RIOT": {"s": "cycle", "b": "Industrial"},
    "WULF": {"s": "cycle", "b": "Industrial"}, "BTBT": {"s": "cycle", "b": "Industrial"},
    "CORZ": {"s": "cycle", "b": "Industrial"}, "HUT": {"s": "cycle", "b": "Industrial"},
    "BITF": {"s": "cycle", "b": "Industrial"}, "BTDR": {"s": "cycle", "b": "Industrial"},
    "CEIX": {"s": "cycle", "b": "Industrial"}, "ARCH": {"s": "cycle", "b": "Industrial"},
    "BTU": {"s": "cycle", "b": "Industrial"}, "NRP": {"s": "cycle", "b": "Industrial"},
    "TALO": {"s": "cycle", "b": "Industrial"}, "SM": {"s": "cycle", "b": "Industrial"},
    "MTDR": {"s": "cycle", "b": "Industrial"}, "CHRD": {"s": "cycle", "b": "Industrial"},
    "GPOR": {"s": "cycle", "b": "Industrial"}, "CTRA": {"s": "cycle", "b": "Industrial"},
    "RRC": {"s": "cycle", "b": "Industrial"}, "AR": {"s": "cycle", "b": "Industrial"},
    "EQT": {"s": "cycle", "b": "Industrial"}, "CNX": {"s": "cycle", "b": "Industrial"},
    "PTEN": {"s": "cycle", "b": "Industrial"}, "LBRT": {"s": "cycle", "b": "Industrial"},
    "NEX": {"s": "cycle", "b": "Industrial"}, "PUMP": {"s": "cycle", "b": "Industrial"},
})

# --- CONSUMER / RETAIL / RESTAURANTS ---
_add({
    "WING": {"s": "hold_forever", "b": "SpecGrowth"}, "TXRH": {"s": "hold_forever", "b": "SpecGrowth"},
    "DNUT": {"s": "cycle", "b": "SpecGrowth"}, "JACK": {"s": "cycle", "b": "SpecGrowth"},
    "PLAY": {"s": "cycle", "b": "SpecGrowth"}, "CAKE": {"s": "cycle", "b": "SpecGrowth"},
    "LULU": {"s": "hold_forever", "b": "SpecGrowth"}, "DECK": {"s": "hold_forever", "b": "SpecGrowth"},
    "CROX": {"s": "cycle", "b": "SpecGrowth"}, "SKX": {"s": "cycle", "b": "SpecGrowth"},
    "FOXF": {"s": "cycle", "b": "SpecGrowth"}, "YETI": {"s": "cycle", "b": "SpecGrowth"},
    "FIVE": {"s": "cycle", "b": "SpecGrowth"}, "OLPX": {"s": "cycle", "b": "SpecGrowth"},
    "WRBY": {"s": "cycle", "b": "SpecGrowth"}, "FIGS": {"s": "catalyst", "b": "SpecGrowth"},
    "XPOF": {"s": "cycle", "b": "SpecGrowth"}, "ARKO": {"s": "cycle", "b": "SpecGrowth"},
    "PRPL": {"s": "catalyst", "b": "SpecGrowth"}, "LOVE": {"s": "cycle", "b": "SpecGrowth"},
    "PLBY": {"s": "catalyst", "b": "SpecGrowth"}, "RVLV": {"s": "cycle", "b": "SpecGrowth"},
    "MNST": {"s": "hold_forever", "b": "SpecGrowth"}, "FIZZ": {"s": "cycle", "b": "SpecGrowth"},
    "SAM": {"s": "cycle", "b": "SpecGrowth"}, "FRPT": {"s": "hold_forever", "b": "SpecGrowth"},
    "SMPL": {"s": "cycle", "b": "SpecGrowth"}, "VITL": {"s": "cycle", "b": "SpecGrowth"},
    "HAIN": {"s": "cycle", "b": "SpecGrowth"}, "LANC": {"s": "hold_forever", "b": "SpecGrowth"},
    "JJSF": {"s": "cycle", "b": "SpecGrowth"}, "MGPI": {"s": "cycle", "b": "SpecGrowth"},
})

# --- FINTECH / FINANCIAL SERVICES ---
_add({
    "LPRO": {"s": "catalyst", "b": "SpecGrowth"}, "OPEN": {"s": "catalyst", "b": "SpecGrowth"},
    "TREE": {"s": "cycle", "b": "SpecGrowth"}, "MKTX": {"s": "hold_forever", "b": "SpecGrowth"},
    "VIRT": {"s": "cycle", "b": "SpecGrowth"}, "IBKR": {"s": "hold_forever", "b": "SpecGrowth"},
    "LPLA": {"s": "hold_forever", "b": "SpecGrowth"}, "STEP": {"s": "cycle", "b": "SpecGrowth"},
    "HLNE": {"s": "hold_forever", "b": "SpecGrowth"}, "ARES": {"s": "hold_forever", "b": "SpecGrowth"},
    "OWL": {"s": "cycle", "b": "SpecGrowth"}, "TBBK": {"s": "cycle", "b": "SpecGrowth"},
    "CUBI": {"s": "cycle", "b": "SpecGrowth"}, "SBCF": {"s": "cycle", "b": "SpecGrowth"},
    "FFIN": {"s": "hold_forever", "b": "SpecGrowth"}, "GBCI": {"s": "cycle", "b": "SpecGrowth"},
    "PNFP": {"s": "cycle", "b": "SpecGrowth"}, "SFBS": {"s": "cycle", "b": "SpecGrowth"},
    "CADE": {"s": "cycle", "b": "SpecGrowth"}, "HWC": {"s": "cycle", "b": "SpecGrowth"},
    "BANF": {"s": "hold_forever", "b": "SpecGrowth"}, "CASH": {"s": "cycle", "b": "SpecGrowth"},
    "EVTC": {"s": "cycle", "b": "SpecGrowth"}, "PRFT": {"s": "hold_forever", "b": "SpecGrowth"},
    "TASK": {"s": "cycle", "b": "SpecGrowth"}, "HASI": {"s": "cycle", "b": "SpecGrowth"},
    "KNSL": {"s": "hold_forever", "b": "SpecGrowth"}, "RYAN": {"s": "hold_forever", "b": "SpecGrowth"},
    "PLMR": {"s": "cycle", "b": "SpecGrowth"}, "ROOT": {"s": "catalyst", "b": "SpecGrowth"},
    "LMND": {"s": "catalyst", "b": "SpecGrowth"}, "OSCR": {"s": "cycle", "b": "SpecGrowth"},
})

# --- EV / AUTOMOTIVE / MOBILITY ---
_add({
    "RIVN": {"s": "catalyst", "b": "SpecGrowth"}, "LCID": {"s": "catalyst", "b": "SpecGrowth"},
    "JOBY": {"s": "catalyst", "b": "SpecGrowth"}, "ACHR": {"s": "catalyst", "b": "SpecGrowth"},
    "LILM": {"s": "catalyst", "b": "SpecGrowth"}, "GOEV": {"s": "catalyst", "b": "SpecGrowth"},
    "XPEV": {"s": "cycle", "b": "SpecGrowth"}, "NIO": {"s": "catalyst", "b": "SpecGrowth"},
    "LI": {"s": "cycle", "b": "SpecGrowth"}, "PSNY": {"s": "catalyst", "b": "SpecGrowth"},
    "LAZR": {"s": "catalyst", "b": "SpecGrowth"}, "INVZ": {"s": "catalyst", "b": "SpecGrowth"},
    "OUST": {"s": "catalyst", "b": "SpecGrowth"}, "AEVA": {"s": "catalyst", "b": "SpecGrowth"},
    "NNOX": {"s": "catalyst", "b": "MedTech"}, "GNTX": {"s": "hold_forever", "b": "Industrial"},
    "THRM": {"s": "cycle", "b": "Industrial"}, "DORM": {"s": "cycle", "b": "Industrial"},
    "SRI": {"s": "cycle", "b": "Industrial"}, "LCII": {"s": "cycle", "b": "Industrial"},
    "FOXF": {"s": "cycle", "b": "Industrial"}, "ALV": {"s": "cycle", "b": "Industrial"},
    "LEA": {"s": "cycle", "b": "Industrial"}, "BWA": {"s": "cycle", "b": "Industrial"},
    "APTV": {"s": "cycle", "b": "Industrial"}, "VC": {"s": "cycle", "b": "Industrial"},
})

# --- REAL ESTATE / REITS (small-mid) ---
_add({
    "IIPR": {"s": "cycle", "b": "Industrial"}, "REXR": {"s": "cycle", "b": "Industrial"},
    "STAG": {"s": "hold_forever", "b": "Industrial"}, "TRNO": {"s": "hold_forever", "b": "Industrial"},
    "FR": {"s": "cycle", "b": "Industrial"}, "EGP": {"s": "hold_forever", "b": "Industrial"},
    "COLD": {"s": "cycle", "b": "Industrial"}, "CUBE": {"s": "cycle", "b": "Industrial"},
    "LSI": {"s": "cycle", "b": "Industrial"}, "NSA": {"s": "cycle", "b": "Industrial"},
    "INVH": {"s": "hold_forever", "b": "Industrial"}, "AMH": {"s": "hold_forever", "b": "Industrial"},
    "SUI": {"s": "cycle", "b": "Industrial"}, "ELS": {"s": "hold_forever", "b": "Industrial"},
    "GLPI": {"s": "hold_forever", "b": "Industrial"}, "VICI": {"s": "hold_forever", "b": "Industrial"},
})

# --- ADDITIONAL SMID GROWTH / MISC ---
_add({
    "DKNG": {"s": "cycle", "b": "SpecGrowth"}, "PENN": {"s": "cycle", "b": "SpecGrowth"},
    "RSI": {"s": "catalyst", "b": "SpecGrowth"}, "GNOG": {"s": "catalyst", "b": "SpecGrowth"},
    "CHGG": {"s": "catalyst", "b": "SpecGrowth"}, "ASAN": {"s": "cycle", "b": "SpecGrowth"},
    "ZI": {"s": "cycle", "b": "SpecGrowth"}, "FVRR": {"s": "cycle", "b": "SpecGrowth"},
    "UPWK": {"s": "cycle", "b": "SpecGrowth"}, "ETSY": {"s": "cycle", "b": "SpecGrowth"},
    "W": {"s": "cycle", "b": "SpecGrowth"}, "CHWY": {"s": "cycle", "b": "SpecGrowth"},
    "CVNA": {"s": "cycle", "b": "SpecGrowth"}, "RDFN": {"s": "catalyst", "b": "SpecGrowth"},
    "OPEN": {"s": "catalyst", "b": "SpecGrowth"}, "REAL": {"s": "catalyst", "b": "SpecGrowth"},
    "DOCS": {"s": "cycle", "b": "MedTech"}, "GDRX": {"s": "cycle", "b": "MedTech"},
    "SDGR": {"s": "catalyst", "b": "MedTech"}, "VEEV": {"s": "hold_forever", "b": "MedTech"},
    "CERT": {"s": "cycle", "b": "MedTech"}, "MDXH": {"s": "cycle", "b": "MedTech"},
    "PHR": {"s": "cycle", "b": "MedTech"}, "TALK": {"s": "catalyst", "b": "MedTech"},
    "AMWL": {"s": "catalyst", "b": "MedTech"}, "TDOC": {"s": "cycle", "b": "MedTech"},
    "IRTC": {"s": "cycle", "b": "MedTech"}, "NVST": {"s": "cycle", "b": "MedTech"},
    "SWAV": {"s": "cycle", "b": "MedTech"}, "SILK": {"s": "catalyst", "b": "MedTech"},
    "AXNX": {"s": "cycle", "b": "MedTech"}, "ATEC": {"s": "cycle", "b": "MedTech"},
})

# --- MORE INDUSTRIALS / SPECIALTY ---
_add({
    "POOL": {"s": "hold_forever", "b": "Industrial"}, "WSO": {"s": "hold_forever", "b": "Industrial"},
    "SSD": {"s": "hold_forever", "b": "Industrial"}, "SITE": {"s": "cycle", "b": "Industrial"},
    "BECN": {"s": "cycle", "b": "Industrial"}, "GMS": {"s": "cycle", "b": "Industrial"},
    "TILE": {"s": "cycle", "b": "Industrial"}, "FLOR": {"s": "cycle", "b": "Industrial"},
    "IBP": {"s": "cycle", "b": "Industrial"}, "BLD": {"s": "cycle", "b": "Industrial"},
    "UFPI": {"s": "cycle", "b": "Industrial"}, "APOG": {"s": "cycle", "b": "Industrial"},
    "AWI": {"s": "hold_forever", "b": "Industrial"}, "DOOR": {"s": "cycle", "b": "Industrial"},
    "JELD": {"s": "cycle", "b": "Industrial"}, "MHK": {"s": "cycle", "b": "Industrial"},
    "FND": {"s": "cycle", "b": "Industrial"}, "LL": {"s": "catalyst", "b": "Industrial"},
    "LESL": {"s": "catalyst", "b": "Industrial"}, "CTOS": {"s": "cycle", "b": "Industrial"},
    "TGLS": {"s": "cycle", "b": "Industrial"}, "WIRE": {"s": "cycle", "b": "Industrial"},
    "ASTE": {"s": "cycle", "b": "Industrial"}, "POWI": {"s": "cycle", "b": "Industrial"},
    "AAON": {"s": "hold_forever", "b": "Industrial"}, "WFRD": {"s": "cycle", "b": "Industrial"},
    "CHX": {"s": "cycle", "b": "Industrial"}, "GATX": {"s": "hold_forever", "b": "Industrial"},
    "TNC": {"s": "hold_forever", "b": "Industrial"}, "RXO": {"s": "cycle", "b": "Industrial"},
    "GXO": {"s": "cycle", "b": "Industrial"}, "FWRD": {"s": "cycle", "b": "Industrial"},
})

# --- ADDITIONAL TECH / AI / CLOUD ---
_add({
    "CRWD": {"s": "hold_forever", "b": "Cyber"}, "PANW": {"s": "hold_forever", "b": "Cyber"},
    "OKTA": {"s": "cycle", "b": "Cyber"}, "ABNB": {"s": "cycle", "b": "SpecGrowth"},
    "DASH": {"s": "cycle", "b": "SpecGrowth"}, "UBER": {"s": "hold_forever", "b": "SpecGrowth"},
    "LYFT": {"s": "cycle", "b": "SpecGrowth"}, "PINS": {"s": "cycle", "b": "SpecGrowth"},
    "SNAP": {"s": "catalyst", "b": "SpecGrowth"}, "TTD": {"s": "hold_forever", "b": "SpecGrowth"},
    "MGNI": {"s": "cycle", "b": "SpecGrowth"}, "DSP": {"s": "cycle", "b": "SpecGrowth"},
    "PUBM": {"s": "cycle", "b": "SpecGrowth"}, "IAS": {"s": "cycle", "b": "SpecGrowth"},
    "DV": {"s": "cycle", "b": "SpecGrowth"}, "ZETA": {"s": "cycle", "b": "SpecGrowth"},
    "BRZE": {"s": "cycle", "b": "SpecGrowth"}, "KARO": {"s": "cycle", "b": "SpecGrowth"},
    "TWLO": {"s": "cycle", "b": "SpecGrowth"}, "BAND": {"s": "cycle", "b": "SpecGrowth"},
    "RNG": {"s": "cycle", "b": "SpecGrowth"}, "FIVN": {"s": "cycle", "b": "SpecGrowth"},
    "TALKW": {"s": "catalyst", "b": "SpecGrowth"}, "ZM": {"s": "cycle", "b": "SpecGrowth"},
    "DOCU": {"s": "cycle", "b": "SpecGrowth"}, "BOX": {"s": "cycle", "b": "SpecGrowth"},
    "SUMO": {"s": "catalyst", "b": "SpecGrowth"}, "NEWR": {"s": "cycle", "b": "SpecGrowth"},
    "ESTC": {"s": "cycle", "b": "SpecGrowth"}, "CLDR": {"s": "catalyst", "b": "SpecGrowth"},
    "PLAN": {"s": "cycle", "b": "SpecGrowth"}, "COUP": {"s": "cycle", "b": "SpecGrowth"},
})

# --- NUCLEAR / URANIUM EXPANDED ---
_add({
    "CCJ": {"s": "cycle", "b": "Nuclear"}, "LEU": {"s": "cycle", "b": "Nuclear"},
    "NXE": {"s": "cycle", "b": "Nuclear"}, "UUUU": {"s": "cycle", "b": "Nuclear"},
    "URG": {"s": "catalyst", "b": "Nuclear"}, "EU": {"s": "cycle", "b": "Nuclear"},
    "BWXT": {"s": "hold_forever", "b": "Nuclear"}, "GEV": {"s": "hold_forever", "b": "Nuclear"},
    "SMR": {"s": "catalyst", "b": "Nuclear"}, "OKLO": {"s": "catalyst", "b": "Nuclear"},
    "NNE": {"s": "catalyst", "b": "Nuclear"}, "DNN": {"s": "cycle", "b": "Nuclear"},
    "UEC": {"s": "cycle", "b": "Nuclear"}, "VST": {"s": "cycle", "b": "Nuclear"},
    "CEG": {"s": "hold_forever", "b": "Nuclear"}, "TLN": {"s": "cycle", "b": "Nuclear"},
})

# --- QUANTUM EXPANDED ---
_add({
    "IONQ": {"s": "cycle", "b": "Quantum"}, "QBTS": {"s": "catalyst", "b": "Quantum"},
    "RGTI": {"s": "catalyst", "b": "Quantum"}, "QUBT": {"s": "catalyst", "b": "Quantum"},
    "ARQQ": {"s": "catalyst", "b": "Quantum"}, "QNT": {"s": "catalyst", "b": "Quantum"},
})

# --- ADDITIONAL SMID TO REACH ~700 ---
_add({
    # Healthcare services
    "ENSG": {"s": "hold_forever", "b": "MedTech"}, "AMED": {"s": "hold_forever", "b": "MedTech"},
    "ACHC": {"s": "cycle", "b": "MedTech"}, "SGRY": {"s": "cycle", "b": "MedTech"},
    "USPH": {"s": "hold_forever", "b": "MedTech"}, "CCRN": {"s": "cycle", "b": "MedTech"},
    "AMN": {"s": "cycle", "b": "MedTech"}, "HCAT": {"s": "cycle", "b": "MedTech"},
    "OMCL": {"s": "hold_forever", "b": "MedTech"}, "PINC": {"s": "cycle", "b": "MedTech"},
    # More industrials
    "POWL": {"s": "cycle", "b": "Industrial"}, "FIX": {"s": "hold_forever", "b": "Industrial"},
    "VRT": {"s": "cycle", "b": "Industrial"}, "EME": {"s": "hold_forever", "b": "Industrial"},
    "GNRC": {"s": "cycle", "b": "Industrial"}, "TT": {"s": "hold_forever", "b": "Industrial"},
    "TTEK": {"s": "hold_forever", "b": "Industrial"}, "GVA": {"s": "cycle", "b": "Industrial"},
    "PRIM": {"s": "cycle", "b": "Industrial"}, "IESC": {"s": "hold_forever", "b": "Industrial"},
    # Specialty chemicals / materials
    "AXTA": {"s": "cycle", "b": "Industrial"}, "CBT": {"s": "cycle", "b": "Industrial"},
    "HWKN": {"s": "hold_forever", "b": "Industrial"}, "KWR": {"s": "hold_forever", "b": "Industrial"},
    "IOSP": {"s": "hold_forever", "b": "Industrial"}, "BCPC": {"s": "hold_forever", "b": "Industrial"},
    "HXL": {"s": "cycle", "b": "Industrial"}, "CRS": {"s": "cycle", "b": "Industrial"},
    "ATI": {"s": "cycle", "b": "Industrial"}, "HAYN": {"s": "cycle", "b": "Industrial"},
    "KALU": {"s": "cycle", "b": "Industrial"}, "CENX": {"s": "cycle", "b": "Industrial"},
    "STLD": {"s": "cycle", "b": "Industrial"}, "CMC": {"s": "cycle", "b": "Industrial"},
    "RS": {"s": "hold_forever", "b": "Industrial"}, "ZEUS": {"s": "cycle", "b": "Industrial"},
    # More software / data
    "HUBS": {"s": "hold_forever", "b": "SpecGrowth"}, "PCTY": {"s": "hold_forever", "b": "SpecGrowth"},
    "PAYC": {"s": "hold_forever", "b": "SpecGrowth"}, "WK": {"s": "cycle", "b": "SpecGrowth"},
    "ALKT": {"s": "cycle", "b": "SpecGrowth"}, "CCCS": {"s": "cycle", "b": "SpecGrowth"},
    "ENV": {"s": "hold_forever", "b": "SpecGrowth"}, "SPNS": {"s": "cycle", "b": "SpecGrowth"},
    "VERX": {"s": "cycle", "b": "SpecGrowth"}, "CARG": {"s": "cycle", "b": "SpecGrowth"},
    # Gaming / entertainment
    "RBLX": {"s": "cycle", "b": "SpecGrowth"}, "U": {"s": "catalyst", "b": "SpecGrowth"},
    "SKLZ": {"s": "catalyst", "b": "SpecGrowth"}, "PLTK": {"s": "cycle", "b": "SpecGrowth"},
    "ZNGA": {"s": "cycle", "b": "SpecGrowth"}, "TTWO": {"s": "hold_forever", "b": "SpecGrowth"},
    "EA": {"s": "hold_forever", "b": "SpecGrowth"}, "MTCH": {"s": "cycle", "b": "SpecGrowth"},
    "BMBL": {"s": "catalyst", "b": "SpecGrowth"}, "SPOT": {"s": "hold_forever", "b": "SpecGrowth"},
    # More fintech / payments
    "SQ": {"s": "cycle", "b": "SpecGrowth"}, "AFRM": {"s": "catalyst", "b": "SpecGrowth"},
    "SOFI": {"s": "cycle", "b": "SpecGrowth"}, "COIN": {"s": "cycle", "b": "SpecGrowth"},
    "HOOD": {"s": "cycle", "b": "SpecGrowth"}, "MSTR": {"s": "catalyst", "b": "SpecGrowth"},
    "BILL": {"s": "cycle", "b": "SpecGrowth"}, "TOST": {"s": "cycle", "b": "SpecGrowth"},
    "RDDT": {"s": "cycle", "b": "SpecGrowth"}, "CAVA": {"s": "cycle", "b": "SpecGrowth"},
    # Misc small-cap
    "YELP": {"s": "cycle", "b": "SpecGrowth"}, "ANGI": {"s": "catalyst", "b": "SpecGrowth"},
    "COUR": {"s": "cycle", "b": "SpecGrowth"}, "SKIL": {"s": "catalyst", "b": "SpecGrowth"},
    "UDMY": {"s": "cycle", "b": "SpecGrowth"}, "INST": {"s": "cycle", "b": "SpecGrowth"},
    "NTNX": {"s": "cycle", "b": "SpecGrowth"}, "PSTG": {"s": "cycle", "b": "SpecGrowth"},
    "SMCI": {"s": "cycle", "b": "Industrial"}, "ANET": {"s": "hold_forever", "b": "Industrial"},
    "CALX": {"s": "cycle", "b": "Industrial"}, "LITE": {"s": "cycle", "b": "Industrial"},
    "VIAV": {"s": "cycle", "b": "Industrial"}, "COMM": {"s": "cycle", "b": "Industrial"},
    "INFN": {"s": "catalyst", "b": "Industrial"}, "AAOI": {"s": "catalyst", "b": "Industrial"},
    "CIEN": {"s": "cycle", "b": "Industrial"}, "EXTR": {"s": "cycle", "b": "Industrial"},
})

# --- BATCH TO REACH ~700 ---
_add({
    # More small-cap biotech
    "ALNY": {"s": "hold_forever", "b": "MedTech"}, "BMRN": {"s": "hold_forever", "b": "MedTech"},
    "HZNP": {"s": "cycle", "b": "MedTech"}, "MRNA": {"s": "cycle", "b": "MedTech"},
    "BNTX": {"s": "cycle", "b": "MedTech"}, "SRRK": {"s": "catalyst", "b": "MedTech"},
    "ACAD": {"s": "cycle", "b": "MedTech"}, "PTGX": {"s": "catalyst", "b": "MedTech"},
    "CPRX": {"s": "cycle", "b": "MedTech"}, "DVAX": {"s": "cycle", "b": "MedTech"},
    "VCEL": {"s": "cycle", "b": "MedTech"}, "SUPN": {"s": "cycle", "b": "MedTech"},
    "PCRX": {"s": "cycle", "b": "MedTech"}, "LNSR": {"s": "catalyst", "b": "MedTech"},
    "DAWN": {"s": "catalyst", "b": "MedTech"}, "IRON": {"s": "catalyst", "b": "MedTech"},
    # More small-cap tech
    "ARLO": {"s": "cycle", "b": "SpecGrowth"}, "LPSN": {"s": "catalyst", "b": "SpecGrowth"},
    "AGYS": {"s": "cycle", "b": "SpecGrowth"}, "CSGS": {"s": "hold_forever", "b": "SpecGrowth"},
    "EVBG": {"s": "cycle", "b": "SpecGrowth"}, "OSPN": {"s": "cycle", "b": "SpecGrowth"},
    "SCWX": {"s": "cycle", "b": "Cyber"}, "FSLY": {"s": "catalyst", "b": "SpecGrowth"},
    "GDYN": {"s": "cycle", "b": "SpecGrowth"}, "TASK": {"s": "cycle", "b": "SpecGrowth"},
    "TTGT": {"s": "cycle", "b": "SpecGrowth"}, "YEXT": {"s": "catalyst", "b": "SpecGrowth"},
    "ZUOR": {"s": "catalyst", "b": "SpecGrowth"}, "AVLR": {"s": "cycle", "b": "SpecGrowth"},
    # More small-cap industrial
    "AIMC": {"s": "cycle", "b": "Industrial"}, "DNOW": {"s": "cycle", "b": "Industrial"},
    "GTES": {"s": "cycle", "b": "Industrial"}, "HI": {"s": "cycle", "b": "Industrial"},
    "JBT": {"s": "hold_forever", "b": "Industrial"}, "KBAL": {"s": "cycle", "b": "Industrial"},
    "LNN": {"s": "hold_forever", "b": "Industrial"}, "MWA": {"s": "cycle", "b": "Industrial"},
    "NVT": {"s": "cycle", "b": "Industrial"}, "REXR": {"s": "cycle", "b": "Industrial"},
    "SPXC": {"s": "hold_forever", "b": "Industrial"}, "WTS": {"s": "hold_forever", "b": "Industrial"},
    "XPEL": {"s": "cycle", "b": "Industrial"}, "ZWS": {"s": "cycle", "b": "Industrial"},
    # More consumer / services
    "BROS": {"s": "cycle", "b": "SpecGrowth"}, "SHAK": {"s": "cycle", "b": "SpecGrowth"},
    "ELF": {"s": "cycle", "b": "SpecGrowth"}, "ONON": {"s": "cycle", "b": "SpecGrowth"},
    "BIRK": {"s": "hold_forever", "b": "SpecGrowth"}, "DKS": {"s": "cycle", "b": "SpecGrowth"},
    "CELH": {"s": "cycle", "b": "SpecGrowth"}, "DUOL": {"s": "hold_forever", "b": "SpecGrowth"},
    "GRAB": {"s": "cycle", "b": "SpecGrowth"}, "HIMS": {"s": "cycle", "b": "MedTech"},
    # More energy / utilities
    "NOVA": {"s": "cycle", "b": "Industrial"}, "MAXN": {"s": "catalyst", "b": "Industrial"},
    "SPWR": {"s": "catalyst", "b": "Industrial"}, "CSIQ": {"s": "cycle", "b": "Industrial"},
    "JKS": {"s": "cycle", "b": "Industrial"}, "DQ": {"s": "cycle", "b": "Industrial"},
    "ENPH": {"s": "cycle", "b": "Industrial"}, "FSLR": {"s": "cycle", "b": "Industrial"},
    "BE": {"s": "cycle", "b": "Industrial"}, "BLDP": {"s": "catalyst", "b": "Industrial"},
    "FCEL": {"s": "catalyst", "b": "Industrial"}, "PLUG": {"s": "catalyst", "b": "Industrial"},
    # More defense
    "PLTR": {"s": "cycle", "b": "Defense"}, "AXON": {"s": "hold_forever", "b": "Defense"},
    "RCAT": {"s": "catalyst", "b": "Defense"}, "BBAI": {"s": "catalyst", "b": "Defense"},
    # More fintech
    "PYPL": {"s": "cycle", "b": "SpecGrowth"}, "FIS": {"s": "cycle", "b": "SpecGrowth"},
    "GPN": {"s": "cycle", "b": "SpecGrowth"}, "WEX": {"s": "cycle", "b": "SpecGrowth"},
    "NDAQ": {"s": "hold_forever", "b": "SpecGrowth"}, "CBOE": {"s": "hold_forever", "b": "SpecGrowth"},
    "MKTX": {"s": "hold_forever", "b": "SpecGrowth"}, "VIRT": {"s": "cycle", "b": "SpecGrowth"},
    # Misc remaining
    "APPN": {"s": "catalyst", "b": "SpecGrowth"}, "CRCT": {"s": "cycle", "b": "SpecGrowth"},
    "DLO": {"s": "cycle", "b": "SpecGrowth"}, "FLYW": {"s": "cycle", "b": "SpecGrowth"},
    "GOCO": {"s": "catalyst", "b": "SpecGrowth"}, "INTA": {"s": "cycle", "b": "SpecGrowth"},
    "KD": {"s": "cycle", "b": "SpecGrowth"}, "OLO": {"s": "catalyst", "b": "SpecGrowth"},
    "PAX": {"s": "cycle", "b": "SpecGrowth"}, "PGNY": {"s": "cycle", "b": "MedTech"},
    "RXST": {"s": "catalyst", "b": "MedTech"}, "SOUN": {"s": "catalyst", "b": "SpecGrowth"},
    "ASTS": {"s": "catalyst", "b": "SpecGrowth"}, "SERV": {"s": "catalyst", "b": "SpecGrowth"},
    "ENVX": {"s": "catalyst", "b": "SpecGrowth"}, "APLD": {"s": "cycle", "b": "Industrial"},
    "IREN": {"s": "cycle", "b": "Industrial"}, "CIFR": {"s": "cycle", "b": "Industrial"},
})

# --- FINAL BATCH TO HIT ~700 ---
_add({
    "ACIW": {"s": "hold_forever", "b": "SpecGrowth"}, "ALRM": {"s": "hold_forever", "b": "SpecGrowth"},
    "AVPT": {"s": "cycle", "b": "SpecGrowth"}, "BRSP": {"s": "cycle", "b": "Industrial"},
    "CARG": {"s": "cycle", "b": "SpecGrowth"}, "CGNX": {"s": "cycle", "b": "Industrial"},
    "CMPR": {"s": "cycle", "b": "SpecGrowth"}, "CORT": {"s": "cycle", "b": "MedTech"},
    "CRVL": {"s": "hold_forever", "b": "MedTech"}, "CYBR": {"s": "hold_forever", "b": "Cyber"},
    "DSGX": {"s": "cycle", "b": "Industrial"}, "EEFT": {"s": "hold_forever", "b": "SpecGrowth"},
    "ENOV": {"s": "cycle", "b": "MedTech"}, "EPAM": {"s": "cycle", "b": "SpecGrowth"},
    "EXLS": {"s": "hold_forever", "b": "SpecGrowth"}, "GLOB": {"s": "cycle", "b": "SpecGrowth"},
    "GSHD": {"s": "cycle", "b": "SpecGrowth"}, "IDCC": {"s": "hold_forever", "b": "Industrial"},
    "INFA": {"s": "cycle", "b": "SpecGrowth"}, "ITRI": {"s": "hold_forever", "b": "Industrial"},
    "MANH": {"s": "hold_forever", "b": "SpecGrowth"}, "MEDP": {"s": "hold_forever", "b": "MedTech"},
    "MASI": {"s": "hold_forever", "b": "MedTech"}, "NATI": {"s": "cycle", "b": "Industrial"},
    "NEWR": {"s": "cycle", "b": "SpecGrowth"}, "OLED": {"s": "hold_forever", "b": "Industrial"},
    "PCVX": {"s": "catalyst", "b": "MedTech"}, "QLYS": {"s": "hold_forever", "b": "Cyber"},
    "SLAB": {"s": "cycle", "b": "Industrial"}, "TECH": {"s": "hold_forever", "b": "MedTech"},
    "TMDX": {"s": "hold_forever", "b": "MedTech"}, "VRNS": {"s": "hold_forever", "b": "Cyber"},
    "WFRD": {"s": "cycle", "b": "Industrial"}, "XRAY": {"s": "cycle", "b": "MedTech"},
    "ZBRA": {"s": "cycle", "b": "Industrial"},
})


def get_full_universe():
    """Merge SMID_UNIVERSE with existing RANKING_UNIVERSE and BACKTEST_EXTRA.

    Returns dict: ticker -> {"strategy": str, "basket": str, "name": ticker,
                              "fragility": "none", "downside_if_fail": "moderate"}
    """
    from portfolio.ranking import RANKING_UNIVERSE
    from portfolio.validation import BACKTEST_EXTRA

    full = {}

    # Add existing universes first (they have richer metadata)
    for ticker, meta in {**RANKING_UNIVERSE, **BACKTEST_EXTRA}.items():
        full[ticker] = meta

    # Add SMID tickers that aren't already present
    for ticker, meta in SMID_UNIVERSE.items():
        if ticker not in full:
            full[ticker] = {
                "name": ticker,
                "basket": meta["b"],
                "strategy": meta["s"],
                "what": "",
                "fragility": "none",
                "downside_if_fail": "moderate",
            }

    return full
