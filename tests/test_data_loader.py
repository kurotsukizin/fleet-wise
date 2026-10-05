import pandas as pd

from src.data_loader import standardize_data


def test_standardize_data_converts_types():
    data = pd.DataFrame({
        "data": ["2026-08-01"],
        "veiculo_id": [" v001 "],
        "categoria": [" combustível "],
        "descricao": [" Diesel "],
        "quantidade": ["180"],
        "valor_total": ["1080.00"],
        "quilometragem": ["45200"],
    })

    result = standardize_data(data)

    assert result.loc[0, "veiculo_id"] == "V001"
    assert result.loc[0, "categoria"] == "Combustível"
    assert result.loc[0, "valor_total"] == 1080.00
    assert pd.api.types.is_datetime64_any_dtype(
        result["data"]
    )