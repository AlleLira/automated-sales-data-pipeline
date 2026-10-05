# Pipeline Automatizado de Dados de Vendas

🇧🇷 **Português** | [🇺🇸 English](README_EN.md)

## Sobre o projeto

Este é um mini pipeline de ETL desenvolvido em Python para validar, tratar,
padronizar e consolidar planilhas de vendas recebidas de diferentes lojas.

O projeto utiliza dados totalmente fictícios e demonstra publicamente um tipo
de automação que pode reduzir tarefas repetitivas antes da análise dos dados.

## Problema de negócio

Imagine uma empresa que recebe periodicamente arquivos de vendas de várias
lojas. Antes da análise, uma pessoa precisa abrir cada planilha, conferir as
colunas, localizar dados inválidos, padronizar as categorias e reunir todas as
informações em um único arquivo.

Além de consumir tempo, esse processo manual aumenta o risco de inconsistências.
Este projeto automatiza o fluxo:

```text
Planilhas Excel → Extração → Validação → Limpeza e padronização
                 → Consolidação → Excel final + rejeições + log
```

## Objetivos

- Automatizar a leitura de vários arquivos de vendas.
- Validar a estrutura das planilhas antes do processamento.
- Identificar registros inconsistentes e explicar cada rejeição.
- Padronizar categorias e campos de texto.
- Calcular automaticamente o valor total de cada venda.
- Consolidar apenas registros válidos.
- Manter rastreabilidade por arquivo e linha de origem.
- Gerar um resumo da execução e um arquivo de log.

## Tecnologias utilizadas

- Python 3.10+
- pandas
- openpyxl
- Excel
- logging

## Estrutura do projeto

```text
automated-sales-data-pipeline/
├── data/
│   ├── input/
│   │   ├── sales_store_101.xlsx
│   │   ├── sales_store_102.xlsx
│   │   └── sales_store_103.xlsx
│   └── output/
├── logs/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── main.py
│   ├── transform.py
│   └── validate.py
├── .gitignore
├── generate_sample_data.py
├── README.md
├── README_EN.md
└── requirements.txt
```

## Regras de validação

O pipeline verifica:

- presença das oito colunas obrigatórias;
- existência de colunas inesperadas;
- valores obrigatórios vazios;
- identificadores de venda duplicados no mesmo arquivo;
- identificadores duplicados entre arquivos diferentes;
- tipo e integridade do identificador da loja;
- quantidade inteira e maior que zero;
- preço unitário numérico e maior que zero;
- data de venda válida e não futura;
- categoria pertencente ao dicionário configurado.

Variações como `ELECTRONICS`, `electronics` e `Eletrônicos` são convertidas
para o padrão `Electronics`. Categorias desconhecidas não são corrigidas
silenciosamente: o registro é rejeitado e recebe a justificativa correspondente.

## Transformações realizadas

Depois das validações, o pipeline:

- remove espaços desnecessários dos campos de texto;
- padroniza as categorias;
- converte quantidades e códigos de loja para números inteiros;
- converte preços para valores numéricos com duas casas decimais;
- normaliza as datas;
- cria a coluna `total_sale` utilizando:

```text
total_sale = quantity × unit_price
```

## Como executar

### 1. Criar o ambiente virtual

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual no Windows

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Prompt de Comando:

```bat
.venv\Scripts\activate.bat
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o pipeline

```bash
python -m src.main
```

## Arquivos gerados

O resultado principal é salvo em:

```text
data/output/sales_consolidated.xlsx
```

Essa planilha contém três abas:

1. **Valid Sales** — registros válidos, tratados e consolidados.
2. **Rejected Rows** — registros inválidos e o motivo de cada rejeição.
3. **Processing Summary** — quantidade de linhas processadas por arquivo.

O histórico técnico da execução é salvo em `logs/processing.log`.

## Resultado com os dados de demonstração

Os arquivos fictícios incluídos no projeto possuem 13 registros:

| Indicador | Resultado |
|---|---:|
| Arquivos processados | 3 |
| Registros analisados | 13 |
| Registros válidos | 9 |
| Registros rejeitados | 4 |

Os quatro erros intencionais são:

- categoria desconhecida;
- quantidade igual a zero;
- preço unitário negativo;
- data de venda futura.

Esses erros demonstram tanto o fluxo de sucesso quanto o tratamento de
inconsistências.

## Recriar os dados fictícios

```bash
python generate_sample_data.py
```

## Competências demonstradas

- automação com Python;
- manipulação de dados com pandas;
- construção de pipeline ETL;
- Data Quality;
- validação de regras de negócio;
- tratamento de erros;
- logging e rastreabilidade;
- geração automatizada de relatórios em Excel;
- organização modular de código;
- documentação técnica.

## Privacidade

Todos os dados utilizados são fictícios. O projeto demonstra uma lógica geral
de automação sem expor dados empresariais, códigos internos ou regras de negócio
confidenciais.

## Autora

**Alessandra Lira**  
Ciência da Computação | Business Intelligence | Análise de Dados

- [LinkedIn](https://www.linkedin.com/in/alessandra-lira-oliveira/)
- [GitHub](https://github.com/AlleLira)

