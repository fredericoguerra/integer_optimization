import pandas as pd
import numpy as np
from docplex.mp.model import Model
import matplotlib.pyplot as plt
import json
from numpy.ma.core import var

#Utilizar o pythonMIP - CBC

predictions = pd.read_csv('./data/predictions.csv',delimiter=';')
predictions = predictions.head(150)
predictions['seed_target_class'] = np.where(predictions['seed_target'] > 15000, 2, 1)

margin = 2.5
target = 96

df_solution = pd.DataFrame()
mdl = Model('reduction_factor')

var_indices = predictions.index.values.tolist()
num_plots_optimized_half = mdl.integer_var_dict(var_indices, name='NumPlotsOptimizedHalf')
num_plots_optimized = mdl.integer_var_dict(var_indices, name = 'NumPlotsOptimized')
seed_production_optimized = mdl.continuous_var_dict(var_indices, name='SeedProductionOptimized')
metst_optimized = mdl.binary_var_dict(var_indices, name='MetstOptimized')

M = 50000

mdl.add_constraints(num_plots_optimized_half[i] <= 25 for i in var_indices)
mdl.add_constraints(num_plots_optimized_half[i] >= 0 for i in var_indices)
mdl.add_constraints(num_plots_optimized[i] == 2*num_plots_optimized_half[i] for i in var_indices)##
mdl.add_constraints(seed_production_optimized[i] == 1.23 * num_plots_optimized[i] * predictions.loc[i, 'y_predicted'] for i in var_indices)##
mdl.add_constraints(seed_production_optimized[i] <= predictions.loc[i,'seed_target']*margin + metst_optimized[i]*M for i in var_indices)##
mdl.add_constraints(seed_production_optimized[i] >= predictions.loc[i,'seed_target']*margin for i in var_indices)##
mdl.add_constraint(mdl.sum(metst_optimized[i] for i in var_indices)/len(predictions)*100 >= target)##

area_planted = 1.23*(mdl.sum(num_plots_optimized[i] for i in var_indices)) ##
hybrids_met_target = (mdl.sum(metst_optimized[i] for i in var_indices)/len(var_indices)*100)

mdl.minimize(area_planted)
mdl.solve()
mdl.solution.export('./data/results.json')

df_solution = pd.DataFrame()
with open('./data/results.json','r') as results:
    data = json.load(results)
    for i in data['CPLEXSolution']['variables']:
        df_solution = df_solution.append(i,ignore_index=True)

df_solution = df_solution.loc[df_solution['name'].str.find('factor_')==-1]
df_solution['hyb_index'] = df_solution['name'].str.split('_',expand=True)[1]
df_solution['parameter'] = df_solution['name'].str.split('_',expand=True)[0]
df_pivot = df_solution.pivot(index="hyb_index", columns="parameter", values="value")
df_pivot = df_pivot.fillna(0)
df_pivot = df_pivot.reset_index()
df_pivot['hyb_index'] = df_pivot['hyb_index'].astype(int)
df_pivot.to_csv('results.csv')
recommendation = pd.merge(how='left', left=predictions, right=df_pivot[['hyb_index','MetstOptimized','NumPlotsOptimized','NumPlotsOptimizedHalf','SeedProductionOptimized']], on='hyb_index', )
recommendation['Recomendacao_Planejamento'] = 24
recommendation['SeedProductionOptimized'] = np.round(recommendation['SeedProductionOptimized'].astype(float),0)
recommendation = recommendation.fillna(0)
recommendation['SeedProductionOptimized'] = recommendation['SeedProductionOptimized'].astype(int)
recommendation['NumPlotsOptimized'] = recommendation['NumPlotsOptimized'].astype(float)
recommendation.to_csv('./data/final_recommendation.csv')

print(f"Total de área recomendada pelo time de planejamento: {sum(recommendation['Recomendacao_Planejamento'])} \nTotal de área recomendada pelo modelo:{sum(recommendation['NumPlotsOptimized'])} \nUnidades de área relativa reduzida: {np.round((sum(recommendation['Recomendacao_Planejamento'])-sum(recommendation['NumPlotsOptimized']))/sum(recommendation['Recomendacao_Planejamento'])*100,2)}%")