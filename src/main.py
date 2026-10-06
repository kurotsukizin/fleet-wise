from .config import INPUT_FILE, OUTPUT_FILE, PROCESSED_DIR
from .data_loader import load_data, standardize_data
from .metrics import (
    calculate_category_percentage,
    calculate_cost_by_category,
    calculate_cost_by_vehicle,
    calculate_total_cost,
    get_largest_cost_category,
)
from .validators import validate_data
from .diagnostics import (
    calculate_category_diagnostics,
    calculate_savings_opportunities,
    calculate_vehicle_diagnostics,
    detect_expensive_transactions,
    generate_recommendations,
)
from .benchmarks import (
    calculate_benchmark_savings,
    calculate_cost_per_km,
    calculate_fleet_benchmark,
    classify_vehicle_performance,
)


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
    recommendations = generate_recommendations(data)

    cost_per_km = calculate_cost_per_km(data)
    fleet_benchmark = calculate_fleet_benchmark(data)
    performance = classify_vehicle_performance(data)
    benchmark_savings = calculate_benchmark_savings(data)

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

    print(
        f"\nArquivo tratado gerado em: "
        f"{OUTPUT_FILE}"
    )

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

    print("\nRecomendações:")

    for recommendation in recommendations:
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

if __name__ == "__main__":
    main()