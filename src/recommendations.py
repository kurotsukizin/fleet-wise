import pandas as pd


def create_recommendations(
    data: pd.DataFrame
) -> pd.DataFrame:
    recommendations = []

    total_cost = data["valor_total"].sum()

    if total_cost <= 0:
        return pd.DataFrame(
            columns=[
                "prioridade",
                "categoria",
                "diagnostico",
                "acao_recomendada",
                "solucao_relacionada",
                "economia_estimada",
            ]
        )

    category_costs = (
        data.groupby("categoria", as_index=False)
        ["valor_total"]
        .sum()
        .rename(columns={"valor_total": "custo_total"})
    )

    category_costs["participacao"] = (
        category_costs["custo_total"]
        / total_cost
        * 100
    )

    for _, row in category_costs.iterrows():
        category = row["categoria"]
        cost = row["custo_total"]
        participation = row["participacao"]

        if category == "Combustível":
            recommendations.append({
                "prioridade": (
                    "Alta"
                    if participation >= 30
                    else "Média"
                ),
                "categoria": category,
                "diagnostico": (
                    f"Combustível representa "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Analisar consumo, preços, rotas "
                    "e comportamento de abastecimento."
                ),
                "solucao_relacionada": "Multiabastece",
                "economia_estimada": round(
                    cost * 0.10,
                    2
                ),
            })

        elif category == "Manutenção":
            recommendations.append({
                "prioridade": (
                    "Alta"
                    if participation >= 25
                    else "Média"
                ),
                "categoria": category,
                "diagnostico": (
                    f"Manutenção representa "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Priorizar manutenção preventiva "
                    "e acompanhar veículos parados."
                ),
                "solucao_relacionada": (
                    "Gestão de Manutenção"
                ),
                "economia_estimada": round(
                    cost * 0.12,
                    2
                ),
            })

        elif category == "Pedágio":
            recommendations.append({
                "prioridade": (
                    "Alta"
                    if participation >= 20
                    else "Baixa"
                ),
                "categoria": category,
                "diagnostico": (
                    f"Pedágio representa "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Analisar rotas e centralizar "
                    "o controle das passagens."
                ),
                "solucao_relacionada": (
                    "Tag Sem Parar / Vale-Pedágio"
                ),
                "economia_estimada": round(
                    cost * 0.08,
                    2
                ),
            })

        elif category == "Multa":
            recommendations.append({
                "prioridade": "Alta",
                "categoria": category,
                "diagnostico": (
                    f"Multas representam "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Investigar recorrência por veículo "
                    "e condutor."
                ),
                "solucao_relacionada": (
                    "Gestor de Multas"
                ),
                "economia_estimada": round(
                    cost * 0.20,
                    2
                ),
            })

        elif category == "Impostos":
            recommendations.append({
                "prioridade": "Média",
                "categoria": category,
                "diagnostico": (
                    f"Impostos representam "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Criar calendário de vencimentos "
                    "e acompanhar pagamentos."
                ),
                "solucao_relacionada": (
                    "Gestão financeira da frota"
                ),
                "economia_estimada": round(
                    cost * 0.03,
                    2
                ),
            })

        else:
            recommendations.append({
                "prioridade": "Baixa",
                "categoria": category,
                "diagnostico": (
                    f"{category} representa "
                    f"{participation:.2f}% dos custos."
                ),
                "acao_recomendada": (
                    "Avaliar detalhadamente a composição "
                    "dessa categoria."
                ),
                "solucao_relacionada": (
                    "Análise personalizada"
                ),
                "economia_estimada": round(
                    cost * 0.05,
                    2
                ),
            })

    result = pd.DataFrame(recommendations)

    priority_order = {
        "Alta": 1,
        "Média": 2,
        "Baixa": 3,
    }

    result["ordem_prioridade"] = (
        result["prioridade"].map(priority_order)
    )

    result = result.sort_values(
        by=["ordem_prioridade", "economia_estimada"],
        ascending=[True, False]
    )

    result = result.drop(
        columns=["ordem_prioridade"]
    )

    return result.reset_index(drop=True)


def calculate_total_savings(
    recommendations: pd.DataFrame
) -> float:
    if recommendations.empty:
        return 0.0

    return round(
        recommendations["economia_estimada"].sum(),
        2
    )