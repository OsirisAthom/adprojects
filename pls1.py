"""
Programa para realizar Partial Least Square Regression
Utilizado para analizar todos las longitudes de onda a minuto 10
21/08/2024 : Adler
"""

# Aquí estamos midiendo solamente las mediciones de t=10min
"""
Realizar las importaciones pertinentes
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.integrate import simpson
from scipy import stats
from sklearn.linear_model import LinearRegression
"""
Realizar la preparación necesaria
"""
# Fibra a utilizar
fibra = 'F1'
# Formato de las imágenes a guardar
image_format='png'
# Ruta donde se extraerán los archivos
directoriod = '$HOME/Documents/datos_csv/'
# Los siguientes valores serán referenciados a lo largo del programa, alterar dado el caso
# Lista para referir al volumen
volumen = [0,1,2,3,4,5,6,7,8,9,10]
# Preasignar matriz de datos: NOTA: alterar la siguiente matriz a conveniencia
# col1 = Volumen col2:: = Transmitancia
MD = np.ones((11,1001))
# Preasignar matriz centrada por columnas
MDC = np.ones((11,1001))
"""
Funciones utilizadas para construir la tabla de datos MD
"""
# Función para abrir los archivos *.csv y sacar el área
def abrir(volumen,tiempo,matrizd):
    # Cambiar valores requeridos a strings
    tiempostr = str(tiempo)
    # Hacer un ifelse para la variable volumen
    if volumen == 0:
        volumenstr = '0'
    elif volumen == 10:
        volumenstr = '1'
    else:
        volumenstr = '0_'+str(volumen)
    # Ruta del archivo
    # Si quiere cambiar de fibra, cambie el número en F1 a F2 en la línea de abajo
    archivo = directoriod+fibra+'-'+volumenstr+'-'+tiempostr+'minutos.csv'
    # Leer el archivo
    informacion = pd.read_csv(archivo)
    # Exportar los valores del archivo
    transmitancia = informacion[['Respuesta']].values
    matrizd[volumen,:] = np.transpose(transmitancia[:,0])
"""
Matriz de datos
"""
# Ciclo for para contruir matriz de datos
for i in volumen:
    abrir(i,10,MD)

"""
Centrar los datos
"""
def centrar(matrizd,c,matrizc):
    col = matrizd[:,c]
    prom = np.mean(col)
    col = (col - prom)
    matrizc[:,c] = col
# Ciclo para centrar
for j in range(1001):
    centrar(MD,j,MDC)

"""
Aplicar PLS
"""
# Realizar otras importaciones
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error
# Preparar vector volumen
vol = np.transpose(np.array(volumen)/10)
X = MDC
y = vol
pls1 = PLSRegression(n_components=2,scale=False)
pls1.fit(X,y)
print(pls1.coef_,pls1.intercept_)
Ypred = pls1.predict(X)
mse = mean_squared_error(y,Ypred)
print(f"Datos PLSR lambdat10{fibra}")
print(f"Mean squared error 2 components:{mse}")
print(f"LoD = {np.sqrt(mse)*332}ppm")
"""
Graficar el predicho contra lo puesto.
"""
# Nota se utilizan todas las áreas y todos los tiempos
fig = plt.figure()
plt.scatter(y,Ypred, c='blue', label='Actual vs Predicted')
plt.plot([min(y),max(y)],[min(y),max(y)], '--r',label='Perfect prediction')
plt.xlabel("Actual Volume")
plt.ylabel("Predicted Volume")
plt.legend()
plt.title(f"{fibra} PLS on the spectre")
plt.grid(True)
image_name = 'plslambdat10'+fibra+'.png'
#fig.savefig(image_name,format = image_format,dpi = 1200)
plt.show()