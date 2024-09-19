"""
Programa para cortar las filas deseadas de un documento *.csv
Específicamente hecho para los archivos del trabajo de investigación.
Movido 05/09/24 : Adler
"""
# Importaciones pertinentes
import pandas as pd
import numpy as np
# Elementos requeridos
fibra = 'F5' # Fibra a selección
rutad = '$HOME/Documents/datos_csv/' # Ruta de donde se tomarán los datos
vol = [0,1,2,3,4,5,6,7,8,9,10]
min = [1,2,3,4,5,6,7,8,9,10]
# lista de filas con ceros
lceros = np.arange(751,1001,1,dtype=int) # Alterar valores de  ser necesario
# Función para cortar a los de una sola fibra
def cortar(c,t):
    # Valor de concentracion
    if c == 0:
        con = '0'
    elif c == 10:
        con = '1'
    else:
        con = '0_'+str(c)
    # Valor de tiempo
    tiempo = str(t)
    # Archivo a cortar
    medicion = con+'-'+tiempo+'minutos.csv'
    archivo = rutad+fibra+'-'+medicion
    # Leer archivo
    elemento = pd.read_csv(archivo)
    # Cortar las filas
    elemento.drop(lceros,axis=0,inplace=True)
    # Guardar
    elemento.to_csv(archivo,index=False)
# Ciclo for para aplicar la función
for v in vol:
    for m in min:
        cortar(v,m)

