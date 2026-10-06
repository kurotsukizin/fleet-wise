import pandas as pd

from src.recommendations import (
    calculate_total_savings,
    create_recommendations,
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


def test_create_recommendations():
    data = create_sample_data()

    result = create_recommendations(data)

    assert not result.empty
    assert "prioridade" in result.columns
    assert "economia_estimada" in result.columns
    assert "acao_recomendada" in result.columns


def test_recommendations_are_sorted_by_priority():
    data = create_sample_data()

    result = create_recommendations(data)

    priorities = result["prioridade"].tolist()

    priority_values = {
        "Alta": 1,
        "Média": 2,
        "Baixa": 3,
    }

    numeric_priorities = [
        priority_values[priority]
        for priority in priorities
    ]

    assert numeric_priorities == sorted(numeric_priorities)


def test_calculate_total_savings():
    data = create_sample_data()
    recommendations = create_recommendations(data)

    total = calculate_total_savings(recommendations)

    assert total > 0