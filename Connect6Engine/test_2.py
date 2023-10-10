import numpy as np
import matplotlib.pyplot as plt


media = np.array([0, 0])
covarianza = np.array([[1, 0.5], [0.5, 1]])

#Numero de muestras a generar
num_muestras = 1000

#PASO 1: Inicializar las variables de interes con valores iniciales
x = 0
y = 0
muestras = []

#Realizar el muestreo de Gibbs
for _ in range(num_muestras): 

    x = np.random.normal(media[0] + covarianza[0, 1] * (y - media[1]) / covarianza[1, 1], np.sqrt(covarianza[0, 0] - covarianza[0, 1]**2 / covarianza[1, 1]))


    y = np.random.normal(media[1] + covarianza[0, 1] * (x - media[0])/ covarianza[0, 0], np.sqrt(covarianza[1, 1] - covarianza[0, 1]**2 / covarianza[0, 0]))

    muestras.append([x, y])



#Visualizar las muestras generadas
plt.hist(muestras, bins=50, density=True, alpha=0.6)
x = np.linspace(-5, 15, 100)

plt.xlabel("Muestra")
plt.ylabel("Densidad")
plt.title("M")
plt.show()