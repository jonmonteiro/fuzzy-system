import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

#Definição das variáveis de entrada e saída
rentabilidade = ctrl.Antecedent(np.arange(0, 11, 1), 'rentabilidade')
risco = ctrl.Antecedent(np.arange(0, 11, 1), 'risco')
tempo = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo')
investimento = ctrl.Consequent(np.arange(0, 101, 1), 'investimento')

#Definindo as funções de pertinência (fuzzyfication)
rentabilidade['baixa'] = fuzz.trapmf(rentabilidade.universe, [0, 0, 2, 4])
rentabilidade['moderada'] = fuzz.trimf(rentabilidade.universe, [3, 5, 7])
rentabilidade['alta'] = fuzz.trapmf(rentabilidade.universe, [6, 8, 10, 10])

risco['baixo'] = fuzz.trapmf(risco.universe, [0, 0, 2, 3])
risco['moderado'] = fuzz.trimf(risco.universe, [2, 5, 7])
risco['alto'] = fuzz.trapmf(risco.universe, [6, 8, 10, 10])

tempo['curto'] = fuzz.trapmf(tempo.universe, [0, 0, 3, 5])
tempo['medio'] = fuzz.trimf(tempo.universe, [4, 5, 7])
tempo['longo'] = fuzz.trapmf(tempo.universe, [6, 8, 10, 10])

investimento['baixo'] = fuzz.trimf(investimento.universe, [0, 25, 50])
investimento['moderado'] = fuzz.trimf(investimento.universe, [25, 50, 75])
investimento['alto'] = fuzz.trimf(investimento.universe, [75, 100, 100])

#Definindo todas as combinações de regras fuzzy (27 regras)
regras = [
    ctrl.Rule(rentabilidade['baixa'] & risco['baixo'] & tempo['curto'], investimento['moderado']),
    ctrl.Rule(rentabilidade['baixa'] & risco['baixo'] & tempo['medio'], investimento['moderado']),
    ctrl.Rule(rentabilidade['baixa'] & risco['baixo'] & tempo['longo'], investimento['alto']),

    ctrl.Rule(rentabilidade['baixa'] & risco['moderado'] & tempo['curto'], investimento['baixo']),
    ctrl.Rule(rentabilidade['baixa'] & risco['moderado'] & tempo['medio'], investimento['baixo']),
    ctrl.Rule(rentabilidade['baixa'] & risco['moderado'] & tempo['longo'], investimento['moderado']),

    ctrl.Rule(rentabilidade['baixa'] & risco['alto'] & tempo['curto'], investimento['baixo']),
    ctrl.Rule(rentabilidade['baixa'] & risco['alto'] & tempo['medio'], investimento['baixo']),
    ctrl.Rule(rentabilidade['baixa'] & risco['alto'] & tempo['longo'], investimento['baixo']),

    ctrl.Rule(rentabilidade['moderada'] & risco['baixo'] & tempo['curto'], investimento['moderado']),
    ctrl.Rule(rentabilidade['moderada'] & risco['baixo'] & tempo['medio'], investimento['alto']),
    ctrl.Rule(rentabilidade['moderada'] & risco['baixo'] & tempo['longo'], investimento['alto']),

    ctrl.Rule(rentabilidade['moderada'] & risco['moderado'] & tempo['curto'], investimento['moderado']),
    ctrl.Rule(rentabilidade['moderada'] & risco['moderado'] & tempo['medio'], investimento['moderado']),
    ctrl.Rule(rentabilidade['moderada'] & risco['moderado'] & tempo['longo'], investimento['moderado']),

    ctrl.Rule(rentabilidade['moderada'] & risco['alto'] & tempo['curto'], investimento['baixo']),
    ctrl.Rule(rentabilidade['moderada'] & risco['alto'] & tempo['medio'], investimento['baixo']),
    ctrl.Rule(rentabilidade['moderada'] & risco['alto'] & tempo['longo'], investimento['moderado']),

    ctrl.Rule(rentabilidade['alta'] & risco['baixo'] & tempo['curto'], investimento['alto']),
    ctrl.Rule(rentabilidade['alta'] & risco['baixo'] & tempo['medio'], investimento['alto']),
    ctrl.Rule(rentabilidade['alta'] & risco['baixo'] & tempo['longo'], investimento['alto']),

    ctrl.Rule(rentabilidade['alta'] & risco['moderado'] & tempo['curto'], investimento['moderado']),
    ctrl.Rule(rentabilidade['alta'] & risco['moderado'] & tempo['medio'], investimento['alto']),
    ctrl.Rule(rentabilidade['alta'] & risco['moderado'] & tempo['longo'], investimento['alto']),

    ctrl.Rule(rentabilidade['alta'] & risco['alto'] & tempo['curto'], investimento['baixo']),
    ctrl.Rule(rentabilidade['alta'] & risco['alto'] & tempo['medio'], investimento['moderado']),
    ctrl.Rule(rentabilidade['alta'] & risco['alto'] & tempo['longo'], investimento['moderado'])
]

#Criando o sistema de controle
investimento_ctrl = ctrl.ControlSystem(regras)
sistema = ctrl.ControlSystemSimulation(investimento_ctrl)

rentabilidade_input = float(input("Informe a rentabilidade: "))
risco_input = float(input("Informe o risco: "))
tempo_input = float(input("Informe o tempo: "))

#Inserindo valores para as entradas
sistema.input['rentabilidade'] = rentabilidade_input  
sistema.input['risco'] = risco_input          
sistema.input['tempo'] = tempo_input          

sistema.compute()

print(f"O investimento recomendado é: {sistema.output['investimento']}% do capital disponível")

rentabilidade.view(sim=sistema)
risco.view(sim=sistema)
tempo.view(sim=sistema)
investimento.view(sim=sistema)

plt.show()
