import pandas as pd

from src.reports import gerar_relatorio_excel


dados = pd.DataFrame(
    {
        "data": [
            "2026-01-10",
            "2026-01-11",
            "2026-01-12"
        ],
        "veiculo": [
            "ABC-1234",
            "ABC-1234",
            "XYZ-5678"
        ],
        "categoria": [
            "Combustível",
            "Pedágio",
            "Manutenção"
        ],
        "valor": [
            500.00,
            85.90,
            1200.00
        ]
    }
)

anomalias = pd.DataFrame(
    {
        "veiculo": ["XYZ-5678"],
        "categoria": ["Manutenção"],
        "valor": [1200.00],
        "prioridade": ["Alta"],
        "motivo": [
            "Valor acima do padrão histórico."
        ]
    }
)

recomendacoes = pd.DataFrame(
    {
        "prioridade": ["Alta"],
        "acao_recomendada": [
            "Validar a manutenção do veículo XYZ-5678."
        ],
        "economia_estimada": [300.00]
    }
)

arquivo = gerar_relatorio_excel(
    dados=dados,
    metricas={
        "custo_total": 1785.90,
        "total_veiculos": 2,
        "total_transacoes": 3
    },
    anomalias=anomalias,
    recomendacoes=recomendacoes,
    economia_potencial=300.00
)

with open("relatorio_teste_fleetwise.xlsx", "wb") as arquivo_excel:
    arquivo_excel.write(arquivo)