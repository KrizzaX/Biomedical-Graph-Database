KUZU_DB_PATH = "hetio.kuzu"
ROCKS_DB_PATH = "hetio_rocks"


NODE_TYPES = {"Anatomy", "Compound", "Disease", "Gene"}

EDGE_TYPES = {
    "AdG": ["Anatomy", "Gene"],
    "AeG": ["Anatomy", "Gene"],
    "AuG": ["Anatomy", "Gene"],
    "CbG": ["Compound", "Gene"],
    "CdG": ["Compound", "Gene"],
    "CuG": ["Compound", "Gene"],
    "CpD": ["Compound", "Disease"],
    "CtD": ["Compound", "Disease"],
    "DaG": ["Disease", "Gene"],
    "DdG": ["Disease", "Gene"],
    "DuG": ["Disease", "Gene"],
    "DlA": ["Disease", "Anatomy"],
}


QUERY2_KEY = "query2"