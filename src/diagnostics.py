import pandas as pd


def calculate_vehicle_diagnostics(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = (
        data.groupby("veiculo_id", as_index=False)
        .agg(
            custo_total=("valor_total", "sum"),
            quantidade_transacoes=("valor_total", "count"),
        )
    )

    media_custo = result["custo_total"].mean()

    result["media_frota"] = round(media_custo, 2)

    result["desvio_percentual"] = (
        (result["custo_total"] - media_custo)
        / media_custo
        * 100
    ).round(2)

    result["acima_da_media"] = (
        result["custo_total"] > media_custo
    )

    return result.sort_values(
        by="custo_total",
        ascending=False
    ).reset_index(drop=True)


def calculate_category_diagnostics(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = (
        data.groupby("categoria", as_index=False)
        .agg(
            custo_total=("valor_total", "sum"),
            quantidade_transacoes=("valor_total", "count"),
        )
    )

    total_cost = result["custo_total"].sum()

    result["participacao_percentual"] = (
        result["custo_total"]
        / total_cost
        * 100
    ).round(2)

    result["custo_medio_transacao"] = (
        result["custo_total"]
        / result["quantidade_transacoes"]
    ).round(2)

    return result.sort_values(
        by="custo_total",
        ascending=False
    ).reset_index(drop=True)


def detect_expensive_transactions(
    data: pd.DataFrame,
    multiplier: float = 2.0
) -> pd.DataFrame:
    average_cost = data["valor_total"].mean()
    threshold = average_cost * multiplier

    result = data[
        data["valor_total"] > threshold
    ].copy()

    result["limite_anomalia"] = round(threshold, 2)

    return result.sort_values(
        by="valor_total",
        ascending=False
    ).reset_index(drop=True)


def calculate_savings_opportunities(
    data: pd.DataFrame,
    reduction_rate: float = 0.10
) -> pd.DataFrame:
    category_diagnostics = calculate_category_diagnostics(data)

    category_diagnostics["economia_estimada"] = (
        category_diagnostics["custo_total"]
        * reduction_rate
    ).round(2)

    category_diagnostics["percentual_reducao"] = (
        reduction_rate * 100
    )

    return category_diagnostics.sort_values(
        by="economia_estimada",
        ascending=False
    ).reset_index(drop=True)


def generate_recommendations(
    data: pd.DataFrame
) -> list[dict]:
    recommendations = []

    vehicle_diagnostics = calculate_vehicle_diagnostics(data)
    category_diagnostics = calculate_category_diagnostics(data)

    vehicles_above_average = vehicle_diagnostics[
        vehicle_diagnostics["acima_da_media"]
    ]

    for _, row in vehicles_above_average.iterrows():
        recommendations.append({
            "tipo": "Veículo acima da média",
            "prioridade": "Alta",
            "alvo": row["veiculo_id"],
            "recomendacao": (
                "Investigar consumo, manutenção, rotas "
                "e perfil de utilização."
            ),
            "impacto_estimado": round(
                row["custo_total"]
                - row["media_frota"],
                2
            ),
        })

    if not category_diagnostics.empty:
        largest_category = category_diagnostics.iloc[0]

        recommendations.append({
            "tipo": "Categoria de maior impacto",
            "prioridade": "Alta",
            "alvo": largest_category["categoria"],
            "recomendacao": (
                "Priorizar análise detalhada desta categoria "
                "e avaliar ações de redução."
            ),
            "impacto_estimado": round(
                largest_category["custo_total"]
                * 0.10,
                2
            ),
        })

    return recommendations