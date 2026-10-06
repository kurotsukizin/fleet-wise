import pandas as pd

from src.benchmarks import (
    calculate_benchmark_savings,
    calculate_cost_per_km,
    calculate_distance_by_vehicle,
    calculate_fleet_benchmark,
    classify_vehicle_performance,
)


def create_sample_data():
    return pd.DataFrame({
        "data": pd.to_datetime([
            "2026-08-01",
            "2026-08-05",
            "2026-08-10",
            "2026-08-15",
            "2026-08-20",
            "2026-08-25",
        ]),
        "veiculo_id": [
            "V001",
            "V001",
            "V002",
            "V002",
            "V003",
            "V003",
        ],
        "categoria": [
            "Combustível",
            "Pedágio",
            "Combustível",
            "Manutenção",
            "Combustível",
            "Multa",
        ],
        "descricao": [
            "Diesel",
            "Rodovia",
            "Diesel",
            "Troca de óleo",
            "Gasolina",
            "Infração",
        ],
        "quantidade": [
            180,
            1,
            160,
            1,
            50,
            1,
        ],
        "valor_total": [
            1080.00,
            20.00,
            960.00,
            400.00,
            300.00,
            195.23,
        ],
        "quilometragem": [
            45000,
            45400,
            30000,
            30500,
            20000,
            20500,
        ],
    })


def test_calculate_distance_by_vehicle():
    data = create_sample_data()

    result = calculate_distance_by_vehicle(data)

    v001 = result[
        result["veiculo_id"] == "V001"
    ].iloc[0]

    assert v001["km_percorridos"] == 400


def test_calculate_cost_per_km():
    data = create_sample_data()

    result = calculate_cost_per_km(data)

    assert "custo_por_km" in result.columns
    assert (result["custo_por_km"] > 0).all()


def test_calculate_fleet_benchmark():
    data = create_sample_data()

    result = calculate_fleet_benchmark(data)

    assert result > 0


def test_classify_vehicle_performance():
    data = create_sample_data()

    result = classify_vehicle_performance(data)

    assert "classificacao" in result.columns
    assert len(result) == 3


def test_calculate_benchmark_savings():
    data = create_sample_data()

    result = calculate_benchmark_savings(data)

    assert "economia_potencial" in result.columns
    assert (result["economia_potencial"] >= 0).all()