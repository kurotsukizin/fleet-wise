import sys
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.benchmarks import (
    calculate_benchmark_savings,
    calculate_cost_per_km,
    calculate_fleet_benchmark,
)
from src.data_loader import standardize_data
from src.diagnostics import (
    calculate_category_diagnostics,
    calculate_vehicle_diagnostics,
    detect_expensive_transactions,
)
from src.metrics import (
    calculate_category_percentage,
    calculate_cost_by_category,
    calculate_cost_by_vehicle,
    calculate_total_cost,
)
from src.recommendations import (
    calculate_total_savings,
    create_recommendations,
)
from src.validators import validate_data


st.set_page_config(
    page_title="FleetWise",
    page_icon="🚛",
    layout="wide",
)


def load_uploaded_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data = standardize_data(data)

    errors = validate_data(data)

    if errors:
        for error in errors:
            st.error(error)

        return None

    return data


def filter_data(data):
    st.sidebar.header("Filtros")

    vehicles = sorted(
        data["veiculo_id"].dropna().unique()
    )

    categories = sorted(
        data["categoria"].dropna().unique()
    )

    selected_vehicles = st.sidebar.multiselect(
        "Veículos",
        options=vehicles,
        default=vehicles
    )

    selected_categories = st.sidebar.multiselect(
        "Categorias",
        options=categories,
        default=categories
    )

    min_date = data["data"].min().date()
    max_date = data["data"].max().date()

    selected_dates = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    filtered = data[
        data["veiculo_id"].isin(selected_vehicles)
        & data["categoria"].isin(selected_categories)
    ].copy()

    if isinstance(selected_dates, tuple):
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates

            filtered = filtered[
                (filtered["data"].dt.date >= start_date)
                & (filtered["data"].dt.date <= end_date)
            ]

    return filtered


def dataframe_to_csv(data):
    return data.to_csv(
        index=False,
        encoding="utf-8-sig"
    )


def show_kpis(data):
    total_cost = calculate_total_cost(data)
    total_vehicles = data["veiculo_id"].nunique()
    total_transactions = len(data)

    if total_vehicles > 0:
        average_cost = total_cost / total_vehicles
    else:
        average_cost = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Custo total",
        f"R$ {total_cost:,.2f}"
    )

    col2.metric(
        "Veículos",
        total_vehicles
    )

    col3.metric(
        "Transações",
        total_transactions
    )

    col4.metric(
        "Custo médio por veículo",
        f"R$ {average_cost:,.2f}"
    )


def show_cost_analysis(data):
    st.subheader("Custos por categoria")

    category_costs = calculate_cost_by_category(data)

    if category_costs.empty:
        st.warning("Não existem dados para os filtros selecionados.")
        return

    st.bar_chart(
        category_costs.set_index("categoria")[
            "custo_total"
        ]
    )

    st.dataframe(
        calculate_category_percentage(data),
        use_container_width=True,
        hide_index=True
    )


def show_vehicle_analysis(data):
    st.subheader("Custos por veículo")

    vehicle_costs = calculate_cost_by_vehicle(data)

    if vehicle_costs.empty:
        st.warning("Não existem dados para os filtros selecionados.")
        return

    st.bar_chart(
        vehicle_costs.set_index("veiculo_id")[
            "custo_total"
        ]
    )

    st.dataframe(
        vehicle_costs,
        use_container_width=True,
        hide_index=True
    )


def show_diagnostics(data):
    st.subheader("Diagnóstico da frota")

    vehicle_diagnostics = calculate_vehicle_diagnostics(data)
    category_diagnostics = calculate_category_diagnostics(data)
    expensive_transactions = detect_expensive_transactions(data)

    tab1, tab2, tab3 = st.tabs([
        "Veículos",
        "Categorias",
        "Anomalias",
    ])

    with tab1:
        st.dataframe(
            vehicle_diagnostics,
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.dataframe(
            category_diagnostics,
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        if expensive_transactions.empty:
            st.success(
                "Nenhuma transação potencialmente anômala."
            )
        else:
            st.warning(
                "Transações acima do limite configurado."
            )

            st.dataframe(
                expensive_transactions,
                use_container_width=True,
                hide_index=True
            )


def show_benchmarks(data):
    st.subheader("Benchmark interno da frota")

    if data.empty:
        st.warning("Não existem dados para análise.")
        return

    benchmark = calculate_fleet_benchmark(data)
    cost_per_km = calculate_cost_per_km(data)
    savings = calculate_benchmark_savings(data)

    st.metric(
        "Custo médio por quilômetro",
        f"R$ {benchmark:.4f}"
    )

    st.dataframe(
        cost_per_km,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Economia potencial por benchmark")

    st.dataframe(
        savings,
        use_container_width=True,
        hide_index=True
    )


def show_recommendations(data):
    st.subheader("Plano de ação")

    recommendations = create_recommendations(data)
    total_savings = calculate_total_savings(
        recommendations
    )

    st.metric(
        "Economia potencial estimada",
        f"R$ {total_savings:,.2f}"
    )

    if recommendations.empty:
        st.info("Nenhuma recomendação foi gerada.")
    else:
        st.dataframe(
            recommendations,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="Baixar plano de ação",
            data=dataframe_to_csv(recommendations),
            file_name="plano_de_acao.csv",
            mime="text/csv"
        )


def main():
    st.title("🚛 FleetWise")
    st.caption(
        "Inteligência de custos para gestão de frotas"
    )

    st.sidebar.header("Fonte de dados")

    uploaded_file = st.sidebar.file_uploader(
        "Envie um arquivo CSV",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info(
            "Envie o arquivo frota_simulada.csv "
            "na barra lateral para iniciar a análise."
        )
        return

    data = load_uploaded_data(uploaded_file)

    if data is None:
        return

    filtered_data = filter_data(data)

    if filtered_data.empty:
        st.warning(
            "Nenhum registro corresponde aos filtros."
        )
        return

    st.success(
        f"{len(filtered_data)} registros carregados "
        "após aplicação dos filtros."
    )

    st.download_button(
        label="Baixar dados filtrados",
        data=dataframe_to_csv(filtered_data),
        file_name="frota_filtrada.csv",
        mime="text/csv"
    )

    show_kpis(filtered_data)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Custos",
        "Veículos",
        "Diagnóstico",
        "Benchmarks",
        "Recomendações",
    ])

    with tab1:
        show_cost_analysis(filtered_data)

    with tab2:
        show_vehicle_analysis(filtered_data)

    with tab3:
        show_diagnostics(filtered_data)

    with tab4:
        show_benchmarks(filtered_data)

    with tab5:
        show_recommendations(filtered_data)


if __name__ == "__main__":
    main()