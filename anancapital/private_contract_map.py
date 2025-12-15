# /Users/nanthawat/PycharmProjects/bc-utils/anancapital/private_contract_map.py

CONTRACT_MAP_OVERRIDES = {
    "AUD_micro": {"code": "MG", "cycle": "HMUZ", "exchange": "CME"},
    "CAD_micro": {"code": "WK", "cycle": "HMUZ", "exchange": "CME"},
    "CORN_mini": {"code": "XN", "cycle": "HKNUZ", "exchange": "CBOT"},
    "CRUDE_W_micro": {"code": "CY", "cycle": "FGHJKMNQUVXZ", "exchange": "NYMEX"},
    "ETHER-micro": {"code": "TA", "cycle": "FGHJKMNQUVXZ", "exchange": "CME"},
    "EUR_micro": {"code": "MF", "cycle": "HMUZ", "exchange": "CME"},
    "KRWUSD_mini": {"code": "K9", "cycle": "FGHJKMNQUVXZ", "exchange": "SGX"},
    "VIX_mini": {"code": "VJ", "cycle": "FGHJKMNQUVXZ", "exchange": "CFE"},
    "WHEAT_mini": {"code": "XW", "cycle": "HKNUZ", "exchange": "CBOT"},

}

EXCHANGES_OVERRIDES = {
    # e.g. "TMX": {"tick_date": "2010-04-05", "eod_date": "1993-04-22"},
}

CONTRACT_MAP_REMOVALS = set([
    "MSCIEMASIA", # Mismatch
    "INR", # Mismatch
    "KRWUSD", # Mismatch; change exchange from cme to sgx

])

EXCHANGES_REMOVALS = set([
    # "SOME_EXCHANGE",
])
