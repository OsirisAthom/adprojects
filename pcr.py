"""
Programa para realizar Regresión de componentes principales
para predecir el volumen medido por un sensor de fibra óptica
con rejilla de periodo largo
Actualizado 16/08/2024
Adler
"""
# Aquí estamos midiendo las áreas con los tiempos
"""
Realizar las importaciones pertinentes
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.integrate import simpson
from scipy import stats
"""
Realizar la preparación necesaria
"""
# Fibra a utilizar
fibra = 'F1'
# Ruta donde se extraerán los archivos
directoriod = '$HOME/Documents/datos_csv/'
# Los siguientes valores serán referenciados a lo largo del programa, alterar dado el caso
# Lista para referir al tiempo
tiempo = [1,2,3,4,5,6,7,8,9,10]
# Lista para referir al volumen
volumen = [0,1,2,3,4,5,6,7,8,9,10]
# Preasignar matriz de datos: NOTA: alterar la siguiente matriz a conveniencia
# col1 = Volumen, col2 = Tiempo, col3 = Área
MD = np.zeros((110,3))
# Preasignar matriz de datos estandarizada
MDE = np.zeros((110,3))
# Preasignar matriz varianza covarianza para PCR
MVC = np.zeros((2,2))
"""
Funciones utilizadas para construir la tabla de datos MD
"""
# Función para abrir los archivos *.csv y sacar el área
def abrir(volumen,tiempo):
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
    global areas
    # Obtener el área bajo la curva
    areas = simpson(transmitancia[:,0],dx=0.2)
# Función para poner el área en su lugar designado
def asignar(volumen,tiempo,matrizd):
    desp = volumen*10 # Valor de desplazamiento
    t = tiempo-1
    matrizd[desp+t,2] = areas
# Función para colocar los valores correctos en el resto de la patriz
def rell(v,t,matrizd):
    # v = vector volumen
    # t = int con las repeticiones de volumen por medición
    # NOTA: colocar los valores de volumen deseados, alterar esta función de ser necesario
    vo = np.repeat(v,t)
    # Colocar la col volumenes
    matrizd[:,0] = np.transpose(vo/10)
    # Colocar la col tiempo
    p = len(volumen)
    ti = np.transpose(np.tile(tiempo,p))
    matrizd[:,1] = ti
"""
Construir la tabla de datos
"""
# Poner las columnas volumen y tiempo
rell(volumen,10,MD)
# Ciclo for para colocar las áreas
for i in volumen:
    for j in tiempo:
        abrir(i,j)
        asignar(i,j,MD)
# Guardar tabla
# ### np.savetxt('tablaf1.csv', MD, delimiter=",",header='volumen,tiempo,area')
"""
Estandarizar los datos
"""
# Función para estandarizar columnas deseadas
def est(matriz,c,matest):
    col = matriz[:,c]
    # Pomedio col
    pr = np.mean(col)
    # Estandarizar y sustituir
    res = (col-pr)/np.std(col,ddof=1)
    matest[:,c] = res
# Aplicar est en siclo for
for k in range(3):
    est(MD,k,MDE)
"""
Funciones para Matriz Varianza Covarianza
"""
# Funcion para obtener la covarianza
def covarianza(MA):
    MAT = np.transpose(MA)
    global MVC
    MVC = MAT@MA
# Aplicar función
A = MDE[:,1:3]
covarianza(A)
"""
Obtener Componentes principales
"""
eval,evec = np.linalg.eig(MVC)
# Ordenar los eigenvalores descendiente para encontrar las componentes principales
idx = eval.argsort()[::-1]
# print(idx)
# Reordenar los valores descendientemente con sus respectivos eigenvectores
eval = eval[idx]
evec = evec[:,idx]
print(f"Datos PCR TiempoxArea{fibra}")
print("Eigenvalores: ",eval,"\nEigenvectores: \n",evec)
"""
valores rotados graficar
"""
tie = np.tile(tiempo,11) # Eje de los tiempos originales
xdata = tie
a = MD[:,2]
ar = np.transpose(a)
ydata = ar # eje de las areas originales
# Scores, valores rotados
dr = A@evec
xrdata = dr[:,0]
yrdata = dr[:,1]
# Scores de los valores originales para Regresión
B = MD[:,1:3]
OG = B@evec
# Graficar
fig, axis = plt.subplots(1,2)
# Original
axis[0].scatter(xdata,ydata)
axis[0].set_title("OG")
axis[0].set_xlabel("tiempo[min]")
axis[0].set_ylabel("area")
# Rotados
axis[1].scatter(xrdata,yrdata)
axis[1].set_title("Rotados")
axis[1].set_xlabel("PC1")
axis[1].set_ylabel("PC2")
# Mostrar
plt.grid(True)
plt.show()
"""
Realizar regresión
"""
# Tomar los loadings que nos interesan
m10 = [9,19,29,39,49,59,69,79,89,99,109]
loadings1 = OG[:,0]
# Lista de valores t=10min
val1 = []
for l in m10:
    val1 = np.append(val1,loadings1[l])

# Visualizar
fig = plt.figure()
volu = np.array(volumen)/10
colors = np.array([0,1,2,3,4,5,6,7,8,9,10])
plt.scatter(val1,volu,c=colors,cmap='viridis')
plt.colorbar()
plt.xlabel("PC1")
plt.ylabel("Volumen")
plt.title("")
plt.grid(True)
# Hacemos regresión
gradient, intercept, r_value, p_value, std_err = stats.linregress(val1,volu)
mn = np.min(val1)
mx = np.max(val1)
x1 = np.linspace(mn,mx,1000)
y1 = (gradient*x1)+intercept
print("Gradient:\n",gradient,"\nIntercept:\n",intercept)
plt.plot(x1,y1,'-r')
plt.title(f"Regresión {fibra} tomando variables tiempo y área")

# Sacar error y LoD
resp = ((gradient*val1)+intercept)
errorc = np.sqrt((np.sum((volu-resp)**2))/val1.size)
print("LoD: ",errorc*332,"ppm")

plt.show() 
