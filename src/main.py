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


if __name__ == "__main__":
    main()