# Estrutura de Dados — FleetWise

## Visão geral

O FleetWise trabalha com dados de custos operacionais de frota, organizados em categorias padronizadas para permitir análise consolidada e identificação de ineficiências.

---

## Categorias de custo

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| **Combustível** | Gastos com abastecimento | Diesel, gasolina, etanol, GNV |
| **Manutenção** | Reparos e prevenção | Troca de óleo, pneus, freios |
| **Pedágio** | Tarifas de rodovias | Praças de pedágio |
| **Multas** | Infrações de trânsito | Excesso de velocidade, estacionamento |
| **Impostos** | Tributos obrigatórios | IPVA, licenciamento |
| **Seguros** | Apólices e coberturas | Seguro de frota |
| **Outros** | Despesas operacionais diversas | Lavagem, acessórios |

---

## Estrutura do dataset

### Arquivo: `frota_simulada.csv`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `data` | Date | Data da despesa (YYYY-MM-DD) |
| `veiculo_id` | String | Identificador único do veículo |
| `categoria` | String | Categoria da despesa |
| `descricao` | String | Detalhe da despesa |
| `quantidade` | Integer | Quantidade (litros, unidades, etc.) |
| `valor_total` | Float | Valor total em reais |
| `quilometragem` | Integer | Quilometragem do veículo |

---

## Exemplo de registros

```csv
data,veiculo_id,categoria,descricao,quantidade,valor_total,quilometragem
2026-08-01,V001,Combustível,Diesel,180,1080.00,45200
2026-08-03,V001,Pedágio,Rodovia Anhanguera,1,18.50,45410
2026-08-05,V002,Manutenção,Troca de óleo,1,420.00,31800
```

---

## Regras de validação

- `data`: formato YYYY-MM-DD, não pode ser futura.
- `veiculo_id`: não vazio, padrão VXNN.
- `categoria`: deve pertencer às categorias definidas.
- `valor_total`: maior que zero.
- `quilometragem`: maior que zero, crescente por veículo.

---

## Dados futuros (Sprints seguintes)

- Cadastro de veículos (marca, modelo, ano, tipo).
- Condutores (nome, CNH, histórico).
- Rotas (origem, destino, distância).
- Centros de custo (departamento, filial).
