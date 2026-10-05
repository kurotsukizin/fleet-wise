import pandas as pd


VALID_CATEGORIES = {
    "Combustível",
    "Manutenção",
    "Pedágio",
    "Multa",
    "Impostos",
    "Seguro",
    "Outros",
}


def validate_data(data: pd.DataFrame) -> list[str]:
    errors = []

    if data.empty:
        errors.append("A base de dados está vazia.")

    if data["data"].isna().any():
        errors.append("Existem datas inválidas.")

    if data["veiculo_id"].isna().any():
        errors.append("Existem veículos sem identificador.")

    invalid_categories = set(data["categoria"]) - VALID_CATEGORIES

    if invalid_categories:
        errors.append(
            "Categorias inválidas: "
            + ", ".join(sorted(invalid_categories))
        )

    if data["quantidade"].isna().any():
        errors.append("Existem quantidades inválidas.")

    if (data["quantidade"] <= 0).any():
        errors.append(
            "A quantidade deve ser maior que zero."
        )

    if data["valor_total"].isna().any():
        errors.append(
            "Existem valores financeiros inválidos."
        )

    if (data["valor_total"] < 0).any():
        errors.append(
            "O valor total não pode ser negativo."
        )

    if data["quilometragem"].isna().any():
        errors.append(
            "Existem quilometragens inválidas."
        )

    if (data["quilometragem"] < 0).any():
        errors.append(
            "A quilometragem não pode ser negativa."
        )

    return errors