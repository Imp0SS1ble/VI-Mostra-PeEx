import matplotlib.pyplot as plt # Importando a biblioteca matplotlib.pyplot e dando o apelido de plt para a plotagem do gráfico.
from scipy.optimize import curve_fit # Importando a biblioteca scipy.optimize para o ajuste de curva e cálculo dos parâmetros fixos da curva.
import numpy as np # Importando a biblioteca numpy e dando o apelido de np, que possui várias funcionalidades matemáticas.
from sklearn.metrics import r2_score # Importando a biblioteca sklearn.metrics para calcular o R².

u0 = 4e-7*np.pi # Constante de permeabilidade magnética no vácuo, representado pela letra grega mi.
I = [] # Declarando o vetor que armazenará os dados de corrente elétrica.
ang_graus = [] # Declarando o vetor que armazenará os dados de ângulo em graus.
ang_rad = [] # Declarando o vetor que armazenará os dados ângulo em radianos.
B = [] # Declarando o vetor que armazenará os dados de campo magnético.
tan = [] # Declarando o vetor que armazenará os dados de tangente de θ.
B_ajustado = [] # Declarando o vetor que armazenará os dados calculados de campo magnético a partir dos dados de parâmetros fixos na função da linhas 25 e 26.
    
N = float(input('Informe quantas espiras possui as bobinas? ')) # Pedindo para o usuário informar quantas espiras possuem as bobinas.
R = float(input('Informe o raio das bobinas (em metros)? ')) # Pedindo para o usuário informar o raio das bobinas.
n = int(input('Qual a quantidade de medições de correntes elétricas e ângulos? ')) # Pedindo para o usuário informar a quantidade de dados medidos.

for i in range(0, n): # Loop até coletar a quantidade informada pelo usuário.
    I.append(float(input('Qual a ' +str(i+1)+ 'ª corrente elétrica medida (em ampère)? '))) # Pedindo para o usuário informar as correntes elétricas medidas.
    ang_graus.append(float(input('Qual o ' +str(i+1)+ 'º ângulo medido (em graus)? '))) # Pedindo para o usuário informar os ângulos medidos na bússola.
    ang_rad.append(ang_graus[i]*(np.pi/180)) # Convertendo os ângulos informados pelo usuário de graus para radianos.
    B.append((8.0*u0*N*I[i])/(np.sqrt(5.0**3)*R)) # Calculando o campo magnético induzido, a partir dos dados informados.
    tan.append(np.tan(ang_rad[i])) # Calculando a tangente do ângulo convertido para radianos.
    
def y(tan, a, b): # Criando uma função que retorna o valor de B(θ)=a*tan(θ)+b para análise dessa relação entre o campo magnético e a tangente do ângulo da bússola.
    return a*tan+b

fig, ax = plt.subplots(figsize = (8,5)) # Definindo o tamanho do gráfico para melhor visualização.
xData = np.array(tan) # Colocando as variáveis de elongação nos dados do eixo x.
yData = np.array(B) # Colocando as variáveis de força nos dados do eixo y.
plt.axis(ymin=0, ymax=(B[(n-1)])*1.1, xmin=0, xmax=(tan[(n-1)])*1.1) # Definindo os valores limites dos eixos do gráfico.

plt.title('Bobina de Helmholtz') # Título do gráfico
plt.plot(xData, yData, 'bo', label='Dados') # Plotando valores do eixo x e y.

popt, pcov = curve_fit(y, xData, yData)  # Calculando parâmetros fixos (a e b) por meio da função da linha 25 e 26.
xFit = np.arange(0.0, tan[n-1], 0.000001) # Definindo o tamanho e o intervalo da curva de tendência.

for i in range(0, n): # As linhas 39 e 40 serão responsáveis pelo cálculo do campo magnético com os dados dos parâmetros fixos calculados e inseridos na equação y.
    B_ajustado.append(tan[i]*popt[0] + popt[1])
    
r2 = r2_score(B_ajustado, B)  # Os valores de campo magnético que são calculados com os dados informados pelo usuário, compara-se estatisticamente com o campo magnético obtido pelos parâmetros fixos estimados pelo script, obtendo-se o R², onde 1 representa uma compatibilidade perfeita entre dados experimentais e os estimados, já 0 representa uma incompatibilidade total entre eles.

plt.plot(xFit, y(xFit, *popt), 'r', label=f'Parâmetro de ajuste: a= {popt[0]:.5e}, b= {popt[1]:.5e}\nEquação: a*tan+b\n R² = {r2:.5}') # Plotando valores calculados no ajuste de curva.
plt.xlabel('tan θ') # Título da eixo x.
plt.ylabel('B (T)') # Título da eixo y.
plt.legend() # Exibição da legenda
plt.show() # Exibição do gráfico.

# As linhas 51 e 52 abaixo realizam o calculo da componente horizontal do campo magenético terrestre, pois quando a bússola medir 45° (π/4 rad) as componentes da resultante (Campo magnético terrestre horizontal e campo magnético induzido pela bobina de Helmholtz) do campo magnético medido pela bússola seram iguais.
componente_horizontal_do_campo_magnetico_da_terra = popt[0]*np.tan((np.pi/4))+popt[1]
print(f'\nA componente horizontal do campo magenético terrestre a partir da equação e valores dos parâmetros fixos, é de: B = {componente_horizontal_do_campo_magnetico_da_terra:.5e} T \n')