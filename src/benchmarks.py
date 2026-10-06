import pandas as pd


def calculate_distance_by_vehicle(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = (
        data.sort_values(
            by=["veiculo_id", "data"]
        )
        .groupby("veiculo_id", as_index=False)
        .agg(
            quilometragem_inicial=(
                "quilometragem",
                "first"
            ),
            quilometragem_final=(
                "quilometragem",
                "last"
            ),
        )
    )

    result["km_percorridos"] = (
        result["quilometragem_final"]
        - result["quilometragem_inicial"]
    )

    result["km_percorridos"] = result[
        "km_percorridos"
    ].clip(lower=0)

    return result


def calculate_cost_per_km(
    data: pd.DataFrame
) -> pd.DataFrame:
    cost_by_vehicle = (
        data.groupby("veiculo_id", as_index=False)
        .agg(custo_total=("valor_total", "sum"))
    )

    distance = calculate_distance_by_vehicle(data)

    result = cost_by_vehicle.merge(
        distance,
        on="veiculo_id",
        how="left"
    )

    result["custo_por_km"] = 0.0

    valid_distance = result["km_percorridos"] > 0

    result.loc[valid_distance, "custo_por_km"] = (
        result.loc[valid_distance, "custo_total"]
        / result.loc[valid_distance, "km_percorridos"]
    ).round(4)

    return result.sort_values(
        by="custo_por_km",
        ascending=False
    ).reset_index(drop=True)


def calculate_fleet_benchmark(
    data: pd.DataFrame
) -> float:
    cost_by_km = calculate_cost_per_km(data)

    valid_values = cost_by_km[
        cost_by_km["custo_por_km"] > 0
    ]["custo_por_km"]

    if valid_values.empty:
        return 0.0

    return round(valid_values.mean(), 4)


def classify_vehicle_performance(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = calculate_cost_per_km(data)
    benchmark = calculate_fleet_benchmark(data)

    result["benchmark_custo_por_km"] = benchmark

    if benchmark == 0:
        result["desvio_benchmark_percentual"] = 0.0
        result["classificacao"] = "Sem referência"
        return result

    result["desvio_benchmark_percentual"] = (
        (
            result["custo_por_km"] - benchmark
        )
        / benchmark
        * 100
    ).round(2)

    result["classificacao"] = "Dentro da média"

    result.loc[
        result["custo_por_km"] > benchmark * 1.10,
        "classificacao"
    ] = "Acima da média"

    result.loc[
        result["custo_por_km"] < benchmark * 0.90,
        "classificacao"
    ] = "Abaixo da média"

    return result


def calculate_benchmark_savings(
    data: pd.DataFrame
) -> pd.DataFrame:
    result = classify_vehicle_performance(data)

    result["economia_potencial"] = 0.0

    above_benchmark = (
        result["custo_por_km"]
        > result["benchmark_custo_por_km"]
    )

    result.loc[above_benchmark, "economia_potencial"] = (
        (
            result.loc[above_benchmark, "custo_por_km"]
            - result.loc[
                above_benchmark,
                "benchmark_custo_por_km"
            ]
        )
        * result.loc[above_benchmark, "km_percorridos"]
    ).round(2)

    return result.sort_values(
        by="economia_potencial",
        ascending=False
    ).reset_index(drop=True)