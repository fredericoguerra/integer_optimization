import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from numpy.ma.core import var
from mip import *

predictions = pd.read_csv('predictions.csv',delimiter=';')
predictions['seed_target_class'] = np.where(predictions['seed_target'] > 15000, 2, 1)

margin = 2.5
target = 96

df_solution = pd.DataFrame()
mdl = Model('reduction_factor')
var_indices = predictions.index.values.tolist()

num_plots_optimized_half = [mdl.add_var(var_type=INTEGER) for i in var_indices]
num_plots_optimized = [mdl.add_var(var_type=INTEGER) for i in var_indices]
seed_production_optimized = [mdl.add_var(var_type=CONTINUOUS) for i in var_indices]
metst_optimized = [mdl.add_var(var_type=BINARY) for i in var_indices]

M = 50000
for i in var_indices:
    mdl += num_plots_optimized_half[i] <= 25
    mdl += num_plots_optimized_half[i] >= 0
    mdl += num_plots_optimized[i] == 2*num_plots_optimized_half[i]
    mdl += seed_production_optimized[i] == 1.23 * num_plots_optimized[i] * predictions.loc[i, 'y_predicted']
    mdl += seed_production_optimized[i] <= predictions.loc[i,'seed_target']*margin + metst_optimized[i]*M
    mdl += seed_production_optimized[i] >= predictions.loc[i,'seed_target']*margin

mdl += xsum(metst_optimized[i] for i in var_indices)/len(predictions)*100 >= target
mdl.objective = minimize(xsum(num_plots_optimized[i] for i in var_indices))

mdl.optimize()

mdl.objective_value
df_solution = pd.DataFrame(columns=['num_plots_optimized','metst_optimized','num_plots_optimized_half','seed_production_optimized'])
num_plots_optimized_list = []
metst_optimized_list = []
num_plots_optimized_half_list = []
seed_production_optimized_list = []

for i in var_indices:
    num_plots_optimized_list.append(num_plots_optimized[i].x)
    metst_optimized_list.append(metst_optimized[i].x)
    seed_production_optimized_list.append(seed_production_optimized[i].x)
    num_plots_optimized_half_list.append(num_plots_optimized_half[i].x)

df_solution['num_plots_optimized'] = num_plots_optimized_list
df_solution['metst_optimized'] = metst_optimized_list
df_solution['num_plots_optimized_half'] = num_plots_optimized_half_list
df_solution['seed_production_optimized'] = seed_production_optimized_list

df_solution = df_solution.reset_index().rename(columns={'index':'hyb_index'})

rec = pd.merge(how='left', left=predictions, right=df_solution, on='hyb_index')
rec['Recomendacao_Planejamento'] = 24
rec.to_csv('final_recommendation.csv')
print(f"Total de área recomendada pelo time de planejamento: {sum(rec['Recomendacao_Planejamento'])} \nTotal de área recomendada pelo modelo:{rec['num_plots_optimized'].sum()} \nUnidades de área relativa reduzida: {np.round((sum(rec['Recomendacao_Planejamento'])-rec['num_plots_optimized'].sum())/sum(rec['Recomendacao_Planejamento'])*100,2)}%")