#!/bin/bash

# Este programa filtra los resultados de nmap y contruye un documento html
# Declarar Variables
TITULO="Resultados nmap"
FECHA_ACTUAL="$(date)"
TIMESTAMP="Informe generado el $FECHA_ACTUAL por el usuario $USER"
# Inicio del programa

# Funciones
# Función de ejecución de nmap
nmap_exec () {
	echo "[NOTIF] Ejecutando nmap en red $1, espere un momento"
	sudo nmap -sV $1 > $2
	echo "[NOTIF] Ya quedó. Fichero $2 tiene la información"
}

# Generar reporte raw con nmap
# Pedir que si existe el fichero, en caso de que ya, revisar si el tiempo es menor a 30 minutos
if [ -f $SALIDANMAP ]; then
	echo "[WARN] Ya existe $2"
	harchivo="$(date -r $2)"
	hlimite="$(date -d "$harchivo 30 minutes" +"%s")"
	# Poner condicional para revisar si el archivo tiene más de 30 minutos de antiguedad
	if [ "$(date +"%s")" -ge  "$hlimite" ]; then
		echo "[WARN] $2 tiene más de 30 minutos, actualizando:"
		nmap_exec $1 "$2"
	else
		echo "[WARN] $2 es reciente."
		while true; do
			read -p "[?] Desea sobreescribir [y/n]: "
			case "$REPLY" in
				y) echo "[NOTIF] Sobreescribiendo"
				   rm xx*
				   nmap_exec $1 $2
				   break
				   ;;
				n) echo "vale"
				   break
				   ;;
				[[:digit:]]*) echo "[ORA] ¿Qué?"
			esac
		done
	fi
else
	nmap_exec $1 $2
fi
# Dividiento el archivo de salida
echo "[NOTIF] Dividiendo el fichero $SALIDANMAP"
csplit $2 '/^$/' {*} > /dev/null
echo "[NOTIF] $S2 dividido en: \n
$(ls xx*)"
# Generar HTML
echo "[NOTIF] Reporte HTML en proceso"
# importamos el fichero que genera el reporte HTML
source nmap-html.sh
gen_html > resultados_nmap.html
echo "[NOTIF] Ya quedó"
