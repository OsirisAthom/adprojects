#!/bin/bash

# Función para poner los resultados en el formato HTML
result_html () {
        for i in xx*; do
                host_ip=$(grep -E "Nmap scan report" $i | grep -E -o '([0-9]{1,3}\.){3}([0-9]+)')
                if [ $host_ip ]; then
                        echo "<tr>"
                        # Ponemos las ip obtenidas
                        echo "<td>$host_ip</td>"
                        # Obtenemos los puertos abiertos en la ip obtenida
                        op_port=$(grep -E -h "^[0-9]{1,5}/(tcp|udp) +open" $i | grep -o -E "^[0-9]{1,5}/(tcp|udp)")
                        if [ "$op_port" ]; then
                                echo "<td>$op_port</td>"
                        else
                                echo "<td>NONE</td>"
                        fi
                        # Poner los servicios
                        service=$(grep -E -h "^[0-9]{1,5}/(tcp|udp) +open" $i | sed -E 's/[0-9]{1,5}\/(tcp|udp) +open +//g' | grep -E -o "^[[:alnum:]]+")
                        if [ "$service" ]; then
                                echo "<td>$service</td>"
                        else
                                echo "<td>NONE</td>"
                        fi
                        echo "</tr>"
                fi
        done
}
# Función para genera el .html
gen_html () {
cat <<EOF
<html>
        <head>
                <title>$TITULO</title>
        </head>
        <style>
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        tr:nth-child(even) {
          background-color: #dddddd;
        }
        </style>
        <body>
               <h1>$TITULO</h1>
                <p1>$TIMESTAMP</p1>

                <table>
                  <tr>
                    <th>Host IP</th>
                    <th>Puertos abiertos</th>
                    <th>Servicio</th>
                  </tr>
                  $(result_html)
                </table>
        </body>
</html>
EOF
}
