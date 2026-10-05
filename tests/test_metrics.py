import pandas as pd

from src.metrics import (
    calculate_category_percentage,
    calculate_cost_by_category,
    calculate_cost_by_vehicle,
    calculate_total_cost,
    get_largest_cost_category,
)


def create_sample_data():
    return pd.DataFrame({
        "data": pd.to_datetime([
            "2026-08-01",
            "2026-08-03",
            "2026-08-05",
            "2026-08-08",
        ]),
        "veiculo_id": [
            "V001",
            "V001",
            "V002",
            "V003",
        ],
        "categoria": [
            "Combustível",
            "Pedágio",
            "Manutenção",
            "Multa",
        ],
        "descricao": [
            "Diesel",
            "Rodovia Anhanguera",
            "Troca de óleo",
            "Excesso de velocidade",
        ],
        "quantidade": [
            180,
            1,
            1,
            1,
        ],
        "valor_total": [
            1080.00,
            18.50,
            420.00,
            195.23,
        ],
        "quilometragem": [
            45200,
            45410,
            31800,
            27650,
        ],
    })


def test_calculate_total_cost():
    data = create_sample_data()

    result = calculate_total_cost(data)

    assert result == 1713.73


def test_calculate_cost_by_category():
    data = create_sample_data()

    result = calculate_cost_by_category(data)

    assert result.iloc[0]["categoria"] == "Combustível"
    assert result.iloc[0]["custo_total"] == 1080.00


def test_calculate_cost_by_vehicle():
    data = create_sample_data()

    result = calculate_cost_by_vehicle(data)

    assert result.iloc[0]["veiculo_id"] == "V001"
    assert result.iloc[0]["custo_total"] == 1098.50


def test_calculate_category_percentage():
    data = create_sample_data()

    result = calculate_category_percentage(data)

    total_percentage = result["percentual"].sum()

    assert round(total_percentage, 2) == 100.00


def test_get_largest_cost_category():
    data = create_sample_data()

    result = get_largest_cost_category(data)

    assert result == "Combustível"