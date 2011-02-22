Fiscal3G is a complete system to live integraton of electoral information.

Installation and Setup
======================

Download
--------

 * Tar/Zip from http://github.com/pointtonull/Fiscal3G/archives/master
 * Using git: git clone git://github.com/pointtonull/Fiscal3G.git

Use
---

Fiscal3G is a cmd tool to do fecth the creadit info of Fiscal3G accounts.

Experiencia del 30/01/2010
==========================

Por problemas de multithreading de smsd de gnokii se recurrió a la solución de
urgencia de serializar las consultas a través de fiscal.sh . Este método poco
elegante resultó suficientemente bueno para satisfacer las demandas del día y
el cuello de botella lo constituyó el hardware (3 modems GSM).

Aunque nunca se estuvo cerca de llenar los inboxs de los modems recomendamos
contar con al menos un modem por cada mil mensajes por hora.

TODO:
-----

- Reimplementar sistema en función de:
    - las librerías de gnokii (previo verificar que el bug no esté implementado
      a este nivel)
    - gnokii como aplicación stand-alone (mejorando versión actual)
- Incluir una interfaz más amigable
- Prepararlo para generar estadisticas en vivo.
    - Se puede tomar como referencia los reportes*.txt en este directorio.
    - Se debe discriminar la información de modo que se pueda apreciar la
      evolución en vivo de los datos.
- Implementar envios secuencias no bloqueantes a partir de agenda.py

