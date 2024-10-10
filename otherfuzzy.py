import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Definição das variáveis de entrada e saída
rentabilidade = ctrl.Antecedent(np.arange(0, 11, 1), 'rentabilidade')
risco = ctrl.Antecedent(np.arange(0, 11, 1), 'risco')
investimento = ctrl.Consequent(np.arange(0, 101, 1), 'investimento')

# 2. Definindo as funções de pertinência (fuzzyfication)
rentabilidade['baixa'] = fuzz.trapmf(rentabilidade.universe, [0, 0, 2, 4])
rentabilidade['moderada'] = fuzz.trimf(rentabilidade.universe, [3, 5, 7])
rentabilidade['alta'] = fuzz.trapmf(rentabilidade.universe, [6, 8, 10, 10])

risco['baixo'] = fuzz.trapmf(risco.universe, [0, 0, 2, 3])
risco['moderado'] = fuzz.trimf(risco.universe, [2, 5, 7])
risco['alto'] = fuzz.trapmf(risco.universe, [6, 8, 10, 10])

investimento['baixo'] = fuzz.trimf(investimento.universe, [0, 25, 50])
investimento['moderado'] = fuzz.trimf(investimento.universe, [25, 50, 75])
investimento['alto'] = fuzz.trimf(investimento.universe, [75, 100, 100])

# 3. Definindo as regras fuzzy
regra1 = ctrl.Rule(rentabilidade['baixa'] & risco['alto'], investimento['baixo'])
regra2 = ctrl.Rule(rentabilidade['alta'] & risco['baixo'], investimento['alto'])
regra3 = ctrl.Rule(rentabilidade['moderada'] & risco['moderado'], investimento['moderado'])
regra4 = ctrl.Rule(rentabilidade['alta'] & risco['moderado'], investimento['moderado'])
regra5 = ctrl.Rule(rentabilidade['baixa'] & risco['baixo'], investimento['moderado'])

# 4. Criando o sistema de controle
investimento_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
sistema = ctrl.ControlSystemSimulation(investimento_ctrl)

# 5. Inserindo valores para as entradas
sistema.input['rentabilidade'] = 7  # Rentabilidade alta
sistema.input['risco'] = 6     # Risco moderado

# 6. Computando o resultado
sistema.compute()

# 7. Resultado final
print(f"O investimento recomendado é: {sistema.output['investimento']}% do capital disponível")

rentabilidade.view(sim=sistema)
risco.view(sim=sistema)
investimento.view(sim=sistema)

plt.show()