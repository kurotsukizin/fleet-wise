from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

INPUT_FILE = DATA_DIR / "frota_simulada.csv"
OUTPUT_FILE = PROCESSED_DIR / "frota_padronizada.csv"