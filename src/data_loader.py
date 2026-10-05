from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "data",
    "veiculo_id",
    "categoria",
    "descricao",
    "quantidade",
    "valor_total",
    "quilometragem",
]


def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )

    data = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Colunas obrigatórias ausentes: "
            + ", ".join(missing_columns)
        )

    return data


def standardize_data(data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()

    result.columns = (
        result.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    result["data"] = pd.to_datetime(
        result["data"],
        errors="coerce"
    )

    result["veiculo_id"] = (
        result["veiculo_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    result["categoria"] = (
        result["categoria"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    result["descricao"] = (
        result["descricao"]
        .astype(str)
        .str.strip()
    )

    numeric_columns = [
        "quantidade",
        "valor_total",
        "quilometragem",
    ]

    for column in numeric_columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce"
        )

    result["valor_total"] = result["valor_total"].round(2)

    return result