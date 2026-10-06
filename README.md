# 🚛 FleetWise

> Plataforma inteligente para consolidar custos de frota, identificar ineficiências e recomendar ações de redução de despesas.

## 🎯 Problema

Os custos de frota (combustível, manutenção, pedágio, multas, impostos e outras despesas) frequentemente estão distribuídos em diferentes sistemas, planilhas, PDFs, imagens e extratos. Essa fragmentação dificulta a visão consolidada da operação e torna a análise manual, demorada e pouco eficiente.

## 👥 Usuários

- **Gestor de Frota:** compreender custos e ineficiências operacionais.
- **CFO/Liderança:** visualizar impacto financeiro e oportunidades de economia.
- **Sem Parar Empresas:** identificar clientes com oportunidades relevantes e relacionar soluções do portfólio.

## 📋 User Stories selecionadas

| ID | User Story | Como a solução responde |
|---|---|---|
| US01 | Consolidar custos | Receber diferentes formatos e organizar em categorias padronizadas |
| US02 | Identificar ineficiências | Calcular indicadores e destacar situações críticas |
| US03 | Estimar economia | Comparar custo atual com referência e apresentar valor em reais |
| US04 | Receber recomendações | Apresentar ações priorizadas por impacto financeiro |
| US05 | Trabalhar com dados incompletos | Gerar estimativa parcial e indicar dados faltantes |
| US06 | Acompanhar evolução | Armazenar históricos e gerar comparações temporais |

## 💡 Solução proposta

O FleetWise receberá informações de combustível, manutenção, pedágios, multas, impostos e demais despesas, mesmo quando estiverem em formatos distintos. Após o tratamento, a solução consolidará os custos, identificará ineficiências, estimará a economia potencial em reais e apresentará recomendações práticas.

## 🗂️ Dados utilizados

A solução trabalhará com:

- Cadastro de veículos.
- Abastecimentos.
- Manutenções.
- Pedágios.
- Multas e impostos.
- Outras despesas operacionais.

Exemplo de estrutura:

```csv
data,veiculo_id,categoria,descricao,quantidade,valor_total,quilometragem
2026-08-01,V001,Combustível,Diesel,180,1080.00,45200
2026-08-03,V001,Pedágio,Rodovia Anhanguera,1,18.50,45410
```

## 🏗️ Arquitetura inicial

![Arquitetura do FleetWise](diagrams/arquitetura-geral.png)

## 🖥️ Dashboard

O FleetWise possui um dashboard desenvolvido com Streamlit para visualização dos custos, diagnósticos, benchmarks e recomendações.

Para executar:

```bash
python -m streamlit run src/dashboard.py
```

Após a execução, acesse:

```text
http://localhost:8501
```

O usuário deve enviar um arquivo CSV da operação para iniciar a análise.

## 🎥 Vídeo demonstrativo

**Link do vídeo:** (inserir após publicação como "não listado")

```text
```
