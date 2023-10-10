import numpy as np
import matplotlib.pyplot as plt


#Funcion objetivo: Distribucion normal con media desconocida
def objetivo(x, media):
    return np.exp(-(x - media) ** 2 / 2)

#Algoritmo de Metropolis-Hastings
def metropolis_hastings(iteraciones, media_propuesta, desviacion_estandar_propuesta, muestra_inicial):

    muestra_actual = muestra_inicial 
    muestras = [muestra_actual]

    for _ in range(iteraciones): 
        candidato = np.random.normal(muestra_actual,
        desviacion_estandar_propuesta)

        ratio_aceptacion = objetivo(candidato, media_propuesta) / objetivo(muestra_actual, media_propuesta)


        if np.random.rand() < ratio_aceptacion:
            muestra_actual = candidato




        muestras.append(muestra_actual)

    return muestras

#Parametros del problema
media_real = 7.0
desviacion_estandar_propuesta = 1.0
iteraciones = 100000

#Ejecutar el algoritmo de Metropolis-Hastings
muestra_inicial = 0.0 #Punto de inicio arbitrario
muestras = metropolis_hastings(iteraciones, media_real,
desviacion_estandar_propuesta,
muestra_inicial)

#Visualizar las muestras generadas
plt.hist(muestras, bins=50, density=True, alpha=0.6, color="b")
x = np.linspace(-5, 15, 100)
plt.plot(x, objetivo(x, media_real), "r-", lw=2)
plt.xlabel("Muestra")
plt.ylabel("Densidad")
plt.title("M")
plt.show()