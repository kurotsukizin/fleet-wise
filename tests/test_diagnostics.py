import pandas as pd

from src.diagnostics import (
    calculate_category_diagnostics,
    calculate_savings_opportunities,
    calculate_vehicle_diagnostics,
    detect_expensive_transactions,
    generate_recommendations,
)


def create_sample_data():
    return pd.DataFrame({
        "data": pd.to_datetime([
            "2026-08-01",
            "2026-08-03",
            "2026-08-05",
            "2026-08-08",
            "2026-08-10",
        ]),
        "veiculo_id": [
            "V001",
            "V001",
            "V002",
            "V003",
            "V003",
        ],
        "categoria": [
            "Combustível",
            "Pedágio",
            "Manutenção",
            "Multa",
            "Combustível",
        ],
        "descricao": [
            "Diesel",
            "Rodovia Anhanguera",
            "Troca de óleo",
            "Excesso de velocidade",
            "Gasolina",
        ],
        "quantidade": [
            180,
            1,
            1,
            1,
            50,
        ],
        "valor_total": [
            1080.00,
            18.50,
            420.00,
            195.23,
            300.00,
        ],
        "quilometragem": [
            45200,
            45410,
            31800,
            27650,
            28100,
        ],
    })


def test_vehicle_diagnostics():
    data = create_sample_data()

    result = calculate_vehicle_diagnostics(data)

    assert "acima_da_media" in result.columns
    assert result.iloc[0]["veiculo_id"] == "V001"


def test_category_diagnostics():
    data = create_sample_data()

    result = calculate_category_diagnostics(data)

    assert "participacao_percentual" in result.columns
    assert result["participacao_percentual"].sum() == 100.0


def test_detect_expensive_transactions():
    data = create_sample_data()

    result = detect_expensive_transactions(
        data,
        multiplier=2.0
    )

    assert not result.empty
    assert result.iloc[0]["valor_total"] == 1080.00


def test_savings_opportunities():
    data = create_sample_data()

    result = calculate_savings_opportunities(data)

    assert "economia_estimada" in result.columns
    assert result["economia_estimada"].sum() > 0


def test_generate_recommendations():
    data = create_sample_data()

    result = generate_recommendations(data)

    assert isinstance(result, list)
    assert len(result) > 0