from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT_DIR / "data" / "frota_simulada.csv"
OUTPUT_FILE = ROOT_DIR / "data" / "frota_simulada.xlsx"


def main():
    data = pd.read_csv(INPUT_FILE)
    data.to_excel(
        OUTPUT_FILE,
        index=False,
        engine="openpyxl"
    )

    print(
        f"Arquivo Excel gerado em: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()