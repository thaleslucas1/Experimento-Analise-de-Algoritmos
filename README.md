# Cálculo da Mediana Salarial — Experimento de Análise de Algoritmos

Experimento acadêmico comparando dois algoritmos para o cálculo da mediana em vetores de salários sintéticos: **Merge Sort** (O(n log n)) e **QuickSelect** (O(n) médio), ambos implementados em Python puro.

---

## Resultado principal

Para `n = 1.000.000`, o QuickSelect foi aproximadamente **7 vezes mais rápido** que o Merge Sort:

| Algoritmo   | Tempo médio (s) |
| ----------- | --------------- |
| Merge Sort  | 4,30            |
| QuickSelect | 0,61            |

---

## Estrutura do repositório

```
algorithms/          # Implementações dos algoritmos
  median_sort.py     # Merge Sort do zero — O(n log n)
  median_quickselect.py  # QuickSelect com pivot aleatório — O(n) médio

data_gen/            # Geração de dados sintéticos
  salary_generator.py    # Salários aleatórios entre R$ 1.000 e R$ 50.000

experiments/         # Benchmark
  benchmark.py       # 30 repetições por tamanho, exporta CSV

plots/               # Gráficos gerados automaticamente
  generate_plots.py      # Script de geração
  mean_time_vs_input_size.png
  empirical_vs_theoretical.png

reports/             # Resultados
  benchmark_results.csv  # Dados do benchmark atual (Merge Sort puro)

docs/                # Relatório acadêmico
  relatorio.tex

tests/               # Suíte de testes
  test_sort_median.py
  test_quickselect_median.py
  test_consistency.py

requirements.txt
```

---

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar os testes

```bash
pytest tests/
```

Resultado esperado: **20 testes aprovados**.

### 3. Executar o benchmark

```bash
python -m experiments.benchmark
```

Os resultados são salvos em `reports/benchmark_results.csv`.

### 4. Gerar os gráficos

```bash
python plots/generate_plots.py
```

As imagens são salvas em `plots/`.

---

## Algoritmos

### Merge Sort

Ordena completamente o vetor e acessa o elemento central. Implementado do zero em Python puro — sem uso do `sorted()` nativo — para garantir paridade de implementação com o QuickSelect.

### QuickSelect

Seleciona diretamente o elemento de ordem desejada sem ordenar o vetor completo. Utiliza pivot aleatório para reduzir a probabilidade do pior caso O(n²). Para `n` par, realiza duas seleções independentes sobre cópias distintas da entrada.

---

## Metodologia

- **Tamanhos de entrada:** 100 tamanhos em escala logarítmica entre 1.000 e 1.000.000
- **Repetições:** 30 por tamanho, com seeds de 0 a 29
- **Medição:** `time.perf_counter()`
- **Validação de corretude:** `math.isclose(rel_tol=1e-12, abs_tol=1e-12)` antes de qualquer medição
- **Cópia defensiva:** realizada fora da região cronometrada

---

## Dependências

```
pytest
matplotlib
numpy
```

---

## Relatório

O relatório completo está em `docs/Experimento_de_Análise_de_Algoritmos.pdf`.
