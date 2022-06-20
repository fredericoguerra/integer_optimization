## Descrição do Problema

Uma empresa de pesquisa em biotecnologia aplicada na agricultura planta diferentes populações genéticas de um determinada cultivar objetivando desenvolver os melhores produtos para o agricultor. Para isso, durante duas safras ao ano o time de planejamento precisa tomar a decisão de quantas unidades de área plantar a fim de garantir que, durante o processo, os times operacionais tenham plantas suficientes no campo para cultivar e alcançar o número de sementes necessário ($T_{i}$) para produção de cada material ($A_{i}$).

No entanto, após uma análise detalhada dos dados históricos, a equipe encontrou uma alta taxa de excesso de sementes produzidas - o que indica uma utilização ineficiente dos recursos (pessoas, água, fertilizantes, área, sementes, etc.) necessários durante cada cultivo. Nesse cenário, o presente trabalho propõe um modelo de otimização em programação inteira a fim de minimizar a área planejada de plantio para um conjunto de 150 materiais e dadas alguns restrições requeridas pelo negócio.

O arquivo *predictions.csv* é a entrada para o modelo proposto, *results.csv* contém as saídas do modelo desenvolvido utilizando a biblioteca CPLEX e o *final_recommendations.csv* apresenta a prescrição final de unidades de área de plantio por cada material.

## Modelagem

### Variáveis de decisão:

$A_{i}$: Quantidade de unidades de área plantada do material $i$.

$y_{i}$: Variável binária indicando se o material $i$ atingiu o volume de sementes esperado.

$T_{i}$: Volume de sementes esperado para o material $i$

$P_{i}$: Volume de sementes predito

### Restrições:

$ \frac{\sum_{i=0}^{n} y_{i}}{n} \ge 0.96$

$ 1.23 * A_{i} * P_{i} \ge 2.5*T_{i}$

$1.23 * A_{i} * P_{i} \le 2.5*T_{i} + 50000$

$A_{i} \ge 0$

$A_{i} \le 50$

$y_{i} \in \{0,1\}$

### Função Objetivo:

$ Min f(A) = 1.23 * \sum_{i=0}^{n} A_{i}$

## Resultados

* Total de área recomendada pelo time de planejamento: 8160
* Total de área recomendada pelo modelo:7658.0
* Unidades de área relativa reduzida: 6.15%

### Python MIP output

Welcome to the CBC MILP Solver
Version: Trunk
Build Date: Oct 28 2021

Starting solution of the Linear programming relaxation problem using Dual Simplex

Coin0506I Presolve 0 (-2041) rows, 0 (-1360) columns and 0 (-3400) elements
Clp0000I Optimal - objective value 7331.9982
Coin0511I After Postsolve, objective 7331.9982, infeasibilities - dual 0 (0), primal 0 (0)
Clp0032I Optimal objective 7331.998196 - 0 iterations time 0.022, Presolve 0.02

Starting MIP optimization
Cgl0004I processed model has 0 rows, 0 columns (0 integer (0 of which binary)) and 0 elements
Cgl0015I Clique Strengthening extended 0 cliques, 0 were dominated
Cbc3007W No integer variables
Total time (CPU seconds):       0.03   (Wallclock seconds):       0.03

Total de área recomendada pelo time de planejamento: 8160
Total de área recomendada pelo modelo:7658.0
Unidades de área relativa reduzida: 6.15%