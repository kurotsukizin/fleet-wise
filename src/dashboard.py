import sys
from datetime import datetime
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
from src.reports import gerar_relatorio_excel
from src.validators import validate_data


st.set_page_config(
    page_title="FleetWise",
    page_icon="🚛",
    layout="wide",
)


with st.expander("Formato esperado dos arquivos"):
    st.markdown(
        """
        O arquivo deve conter as seguintes colunas:

        - `data`
        - `veiculo_id`
        - `categoria`
        - `descricao`
        - `quantidade`
        - `valor_total`
        - `quilometragem`

        Categorias aceitas:

        - Combustível
        - Manutenção
        - Pedágio
        - Multa
        - Impostos
        - Seguro
        - Outros
        """
    )


def format_currency(value):
    """
    Exibe valores monetários no padrão brasileiro.
    """

    value = float(value or 0)

    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X")
    formatted = formatted.replace(".", ",")
    formatted = formatted.replace("X", ".")

    return f"R$ {formatted}"


def load_uploaded_data(uploaded_file):
    """
    Lê, padroniza e valida arquivos CSV ou XLSX enviados pelo usuário.
    """

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            data = pd.read_excel(
                uploaded_file,
                engine="openpyxl"
            )

        else:
            st.error(
                "Formato não suportado. "
                "Envie um arquivo CSV ou XLSX."
            )
            return None

    except Exception as error:
        st.error(
            f"Não foi possível ler o arquivo: {error}"
        )
        return None

    try:
        data = standardize_data(data)

    except Exception as error:
        st.error(
            f"Erro ao padronizar os dados: {error}"
        )
        return None

    errors = validate_data(data)

    if errors:
        st.error("O arquivo possui problemas:")

        for error in errors:
            st.error(error)

        return None

    return data


def filter_data(data):
    """
    Aplica filtros de veículo, categoria e período na barra lateral.
    """

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
    """
    Converte um DataFrame em CSV compatível com Excel.
    """

    return data.to_csv(
        index=False,
        encoding="utf-8-sig"
    )


def build_report_metrics(data):
    """
    Cria o dicionário de métricas utilizado no relatório executivo.
    """

    total_cost = calculate_total_cost(data)
    total_vehicles = data["veiculo_id"].nunique()
    total_transactions = len(data)

    average_cost = (
        total_cost / total_vehicles
        if total_vehicles > 0
        else 0
    )

    return {
        "custo_total": total_cost,
        "total_veiculos": total_vehicles,
        "total_transacoes": total_transactions,
        "custo_medio_veiculo": average_cost,
    }


def show_kpis(data):
    """
    Exibe os quatro KPIs principais.
    """

    metrics = build_report_metrics(data)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Custo total",
        format_currency(metrics["custo_total"])
    )

    col2.metric(
        "Veículos",
        metrics["total_veiculos"]
    )

    col3.metric(
        "Transações",
        metrics["total_transacoes"]
    )

    col4.metric(
        "Custo médio por veículo",
        format_currency(
            metrics["custo_medio_veiculo"]
        )
    )


def show_cost_analysis(data):
    """
    Exibe custos e participação por categoria.
    """

    st.subheader("Custos por categoria")

    category_costs = calculate_cost_by_category(data)

    if category_costs.empty:
        st.warning(
            "Não existem dados para os filtros selecionados."
        )
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
    """
    Exibe ranking de custos por veículo.
    """

    st.subheader("Custos por veículo")

    vehicle_costs = calculate_cost_by_vehicle(data)

    if vehicle_costs.empty:
        st.warning(
            "Não existem dados para os filtros selecionados."
        )
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


def show_diagnostics(
    vehicle_diagnostics,
    category_diagnostics,
    expensive_transactions,
):
    """
    Exibe diagnósticos e anomalias já calculados.
    """

    st.subheader("Diagnóstico da frota")

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


def show_benchmarks(
    benchmark,
    cost_per_km,
    savings,
):
    """
    Exibe benchmark de custo por quilômetro e economia estimada.
    """

    st.subheader("Benchmark interno da frota")

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


def show_recommendations(
    recommendations,
    total_savings,
):
    """
    Exibe o plano de ação e disponibiliza o download em CSV.
    """

    st.subheader("Plano de ação")

    st.metric(
        "Economia potencial estimada",
        format_currency(total_savings)
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
            label="Baixar plano de ação em CSV",
            data=dataframe_to_csv(recommendations),
            file_name="plano_de_acao.csv",
            mime="text/csv",
            use_container_width=True
        )


def show_report_download(
    data,
    metrics,
    anomalies,
    benchmark_data,
    recommendations,
    total_savings,
):
    """
    Gera o relatório FleetWise em memória e exibe botão de download.
    """

    st.subheader("Relatório executivo")

    report_excel = gerar_relatorio_excel(
        dados=data,
        metricas=metrics,
        anomalias=anomalies,
        benchmark=benchmark_data,
        recomendacoes=recommendations,
        economia_potencial=total_savings,
    )

    file_name = (
        "relatorio_fleetwise_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    st.download_button(
        label="Baixar relatório executivo em Excel",
        data=report_excel,
        file_name=file_name,
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )


def main():
    st.title("🚛 FleetWise")

    st.caption(
        "Inteligência de custos para gestão de frotas"
    )

    st.sidebar.header("Fonte de dados")

    uploaded_file = st.sidebar.file_uploader(
        "Envie um arquivo CSV ou Excel",
        type=["csv", "xlsx"]
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

    metrics = build_report_metrics(filtered_data)

    vehicle_diagnostics = calculate_vehicle_diagnostics(
        filtered_data
    )

    category_diagnostics = calculate_category_diagnostics(
        filtered_data
    )

    expensive_transactions = detect_expensive_transactions(
        filtered_data
    )

    benchmark = calculate_fleet_benchmark(filtered_data)

    cost_per_km = calculate_cost_per_km(
        filtered_data
    )

    benchmark_savings = calculate_benchmark_savings(
        filtered_data
    )

    recommendations = create_recommendations(
        filtered_data
    )

    total_savings = calculate_total_savings(
        recommendations
    )

    st.download_button(
        label="Baixar dados filtrados em CSV",
        data=dataframe_to_csv(filtered_data),
        file_name="frota_filtrada.csv",
        mime="text/csv",
        use_container_width=True
    )

    show_kpis(filtered_data)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Custos",
        "Veículos",
        "Diagnóstico",
        "Benchmarks",
        "Recomendações",
        "Exportações",
    ])

    with tab1:
        show_cost_analysis(filtered_data)

    with tab2:
        show_vehicle_analysis(filtered_data)

    with tab3:
        show_diagnostics(
            vehicle_diagnostics=vehicle_diagnostics,
            category_diagnostics=category_diagnostics,
            expensive_transactions=expensive_transactions,
        )

    with tab4:
        show_benchmarks(
            benchmark=benchmark,
            cost_per_km=cost_per_km,
            savings=benchmark_savings,
        )

    with tab5:
        show_recommendations(
            recommendations=recommendations,
            total_savings=total_savings,
        )

    with tab6:
        show_report_download(
            data=filtered_data,
            metrics=metrics,
            anomalies=expensive_transactions,
            benchmark_data=cost_per_km,
            recommendations=recommendations,
            total_savings=total_savings,
        )


if __name__ == "__main__":
    main()