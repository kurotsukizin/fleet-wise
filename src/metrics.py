import pandas as pd


def calculate_total_cost(data: pd.DataFrame) -> float:
    return round(data["valor_total"].sum(), 2)


def calculate_cost_by_category(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = (
        data.groupby("categoria", as_index=False)
        ["valor_total"]
        .sum()
        .rename(columns={"valor_total": "custo_total"})
    )

    result["custo_total"] = result["custo_total"].round(2)

    return result.sort_values(
        by="custo_total",
        ascending=False
    ).reset_index(drop=True)


def calculate_cost_by_vehicle(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = (
        data.groupby("veiculo_id", as_index=False)
        ["valor_total"]
        .sum()
        .rename(columns={"valor_total": "custo_total"})
    )

    result["custo_total"] = result["custo_total"].round(2)

    return result.sort_values(
        by="custo_total",
        ascending=False
    ).reset_index(drop=True)


def calculate_category_percentage(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = calculate_cost_by_category(data)
    total_cost = result["custo_total"].sum()

    if total_cost == 0:
        result["percentual"] = 0.0
    else:
        result["percentual"] = (
            result["custo_total"] / total_cost * 100
        ).round(2)

    return result


def get_largest_cost_category(
    data: pd.DataFrame
) -> str:
    category_costs = calculate_cost_by_category(data)

    if category_costs.empty:
        return ""

    return category_costs.iloc[0]["categoria"]