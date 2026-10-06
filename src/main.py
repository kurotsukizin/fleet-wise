from .benchmarks import (
    calculate_benchmark_savings,
    calculate_cost_per_km,
    calculate_fleet_benchmark,
    classify_vehicle_performance,
)
from .config import INPUT_FILE, OUTPUT_FILE, PROCESSED_DIR
from .data_loader import load_data, standardize_data
from .diagnostics import (
    calculate_category_diagnostics,
    calculate_savings_opportunities,
    calculate_vehicle_diagnostics,
    detect_expensive_transactions,
    generate_recommendations as generate_diagnostic_recommendations,
)
from .metrics import (
    calculate_category_percentage,
    calculate_cost_by_category,
    calculate_cost_by_vehicle,
    calculate_total_cost,
    get_largest_cost_category,
)
from .recommendations import (
    calculate_total_savings,
    create_recommendations,
)
from .validators import validate_data


def main():
    data = load_data(INPUT_FILE)
    data = standardize_data(data)

    errors = validate_data(data)

    if errors:
        print("Foram encontrados problemas:")

        for error in errors:
            print(f"- {error}")

        return

    total_cost = calculate_total_cost(data)
    cost_by_category = calculate_cost_by_category(data)
    cost_by_vehicle = calculate_cost_by_vehicle(data)
    category_percentage = calculate_category_percentage(data)
    largest_category = get_largest_cost_category(data)

    vehicle_diagnostics = calculate_vehicle_diagnostics(data)
    category_diagnostics = calculate_category_diagnostics(data)
    expensive_transactions = detect_expensive_transactions(data)
    savings_opportunities = calculate_savings_opportunities(data)

    diagnostic_recommendations = (
        generate_diagnostic_recommendations(data)
    )

    cost_per_km = calculate_cost_per_km(data)
    fleet_benchmark = calculate_fleet_benchmark(data)
    performance = classify_vehicle_performance(data)
    benchmark_savings = calculate_benchmark_savings(data)

    recommendations = create_recommendations(data)
    total_savings = calculate_total_savings(recommendations)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\n========== FleetWise ==========")
    print(f"Custo total da frota: R$ {total_cost:.2f}")
    print(
        f"Maior categoria de custo: "
        f"{largest_category}"
    )

    print("\nCusto por categoria:")
    print(cost_by_category.to_string(index=False))

    print("\nCusto por veículo:")
    print(cost_by_vehicle.to_string(index=False))

    print("\nParticipação por categoria:")
    print(category_percentage.to_string(index=False))

    print("\nDiagnóstico por veículo:")
    print(vehicle_diagnostics.to_string(index=False))

    print("\nDiagnóstico por categoria:")
    print(category_diagnostics.to_string(index=False))

    print("\nTransações potencialmente anômalas:")

    if expensive_transactions.empty:
        print("Nenhuma transação fora do padrão encontrada.")
    else:
        print(expensive_transactions.to_string(index=False))

    print("\nOportunidades de economia:")
    print(savings_opportunities.to_string(index=False))

    print("\nRecomendações do diagnóstico:")

    if not diagnostic_recommendations:
        print("Nenhuma recomendação diagnóstica foi gerada.")
    else:
        for recommendation in diagnostic_recommendations:
            print(
                f"- [{recommendation['prioridade']}] "
                f"{recommendation['tipo']} — "
                f"{recommendation['alvo']}: "
                f"{recommendation['recomendacao']} "
                f"Economia estimada: "
                f"R$ {recommendation['impacto_estimado']:.2f}"
            )

    print("\nCusto por quilômetro:")
    print(cost_per_km.to_string(index=False))

    print(
        f"\nBenchmark médio da frota: "
        f"R$ {fleet_benchmark:.4f} por km"
    )

    print("\nClassificação de desempenho:")
    print(performance.to_string(index=False))

    print("\nEconomia potencial por benchmark:")
    print(benchmark_savings.to_string(index=False))

    print("\nPlano de ação:")

    if recommendations.empty:
        print("Nenhuma recomendação foi gerada.")
    else:
        print(
            recommendations.to_string(
                index=False
            )
        )

        for _, recommendation in recommendations.iterrows():
            print(
                f"- [{recommendation['prioridade']}] "
                f"{recommendation['categoria']}: "
                f"{recommendation['acao_recomendada']} "
                f"Economia estimada: "
                f"R$ {recommendation['economia_estimada']:.2f}"
            )

    print(
        f"\nEconomia potencial total: "
        f"R$ {total_savings:.2f}"
    )

    recommendations_file = (
        PROCESSED_DIR / "plano_de_acao.csv"
    )

    recommendations.to_csv(
        recommendations_file,
        index=False,
        encoding="utf-8"
    )

    print(
        f"\nArquivo tratado gerado em: "
        f"{OUTPUT_FILE}"
    )

    print(
        f"Plano de ação exportado para: "
        f"{recommendations_file}"
    )


if __name__ == "__main__":
    main()