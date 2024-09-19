"""
Programa para convertir archivos de *.txt a *.csv de los datos tomados
Modificado 18/09/2024 : Adler
Forma guardada de los archivos F1-0_1-2minutos.txt
NúmeroSensor-concentraciónquímico-tiempo.txt
"""
# realizar importaciones necesarias
import pandas as pd
# Programa para volver .csv todos los archivos
# Poner las rutas de origen y destino
ruta = '$HOME/Documents/datos-txt/'
destino = '$HOME/Documents/datos_csv/'
# Función para elegir el archivo que se va a convertir
def archivo(fibra, concentracion, minutos):
    # El código de identificación del sensor
    f = fibra.upper()
    # If para las concentraciones volverlas str
    # para  que coincidan con sus respectivos archivos
    if concentracion == 0:
        cons = "0"
    elif concentracion%10 == 0:
        cons = str(concentracion)[0]
    elif concentracion > 0 and concentracion < 10:
        cons = "0_"+str(concentracion)
    else:
        cons = str(concentracion)
        cons = cons[0]+"_"+cons[1:]
    # Volver el tiempo strings
    mins = str(minutos)
    tiempoe = mins+"minutos"
    # Formar las rutas de archivo y de salida
    global artexto
    artexto = ruta+f+"-"+cons+"-"+tiempoe+".txt"
    global out
    out = destino+f+"-"+cons+"-"+tiempoe+".csv"

# Función para convertir los archivos seleccionados
def convertir(fichero,salida):
    leer = pd.read_csv(fichero, header=None, sep=r"\s+")
    guardar = leer.to_csv(salida,header= ["Lambda", "Respuesta"] ,index=False)
# Sensor al cual convertir los datos
fibra = "F1"
# ciclos for para convertir los archivos
for i in range(11): # Representando las concentraciones medidas, cambiar de ser necesario
    for j in range(1,11): # Representando los minutos, cambiar de ser necesario
        archivo(fibra,i,j)
        convertir(artexto,out)

