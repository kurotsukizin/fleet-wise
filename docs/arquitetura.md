# Arquitetura da Solução — FleetWise

## Visão geral

O FleetWise segue uma arquitetura modular que separa entrada de dados, processamento, análise e apresentação.

---

## Diagrama de fluxo

┌─────────────────────┐
│ Entrada de dados │
│ CSV, Excel, PDF, │
│ imagem, texto │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Extração e ETL │
│ Validação, limpeza, │
│ padronização │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Banco de dados │
│ CSV / PostgreSQL │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Análise e KPIs │
│ Custo/km, consumo, │
│ manutenção/veículo │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Diagnóstico │
│ Ineficiências, │
│ alertas, outliers │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Benchmark │
│ Comparação com │
│ referências │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Recomendações │
│ Ações, prioridade, │
│ economia em R$ │
└──────────┬──────────┘
↓
┌─────────────────────┐
│ Dashboard e Reports │
│ Gestor, CFO, Sem │
│ Parar │
└─────────────────────┘

---

## Componentes

### 1. Entrada de dados

- Upload de arquivos CSV e Excel.
- Processamento de PDFs e imagens (OCR).
- Formulários manuais.

### 2. ETL (Extract, Transform, Load)

- Leitura e validação.
- Padronização de datas e valores.
- Classificação de categorias.
- Tratamento de dados ausentes.

### 3. Banco de dados

- Armazenamento estruturado.
- Histórico de análises.
- Controle de versões dos dados.

### 4. Análise e KPIs

- Custo total por categoria.
- Custo por veículo.
- Custo por quilômetro.
- Consumo médio.

### 5. Diagnóstico

- Identificação de outliers.
- Detecção de anomalias.
- Alertas de custos elevados.

### 6. Benchmark

- Comparação com médias de mercado.
- Percentis de desempenho.
- Metas de redução.

### 7. Recomendações

- Ações priorizadas.
- Economia estimada.
- Relacionamento com soluções Sem Parar.

### 8. Dashboard e Reports

- Visualização de indicadores.
- Gráficos e tabelas.
- Exportação em PDF/Excel.

---

## Tecnologias previstas

| Camada | Tecnologia |
|--------|------------|
| Backend | Python, Pandas |
| Banco de dados | CSV, PostgreSQL |
| IA/ML | OCR, classificação |
| Frontend | Streamlit, Power BI |
| Versionamento | Git, GitHub |
