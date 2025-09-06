## Razonador QBF basado en la herramienta BICA.

Repositorio que incluye mi Trabajo de Fin de Grado. El proyecto incluye las siguientes tres utilidades:

* Un procesado de ficheros QDIMACS.
* Un razonador QBF con un enfoque más similar al de la fuerza bruta, llamado Naíf.
* Un razonador QBF basado en BICA.

El desarrollo se ha llevado a cabo en Python. 
***
### Estructura 

* El directorio `src` contiene toda la implementación necesaria del proyecto. 
  * El direcotrio `bica` contiene todo el código fuente modificado parcialmente del autor original.
* El directorio `pruebas` contiene instancias para verificar el funcionamiento de la herramienta. Cada instancia se encuentra dividida en su propio directorio:
  * El directorio `sat` contiene las instancias QBF que son TRUE.
  * El directorio `unsat` contiene las instancias QBF que son FALSE.
  * El direcotrio `time` contiene las instancias QBF que ninguno de los dos razonadores QBF puede resolver en un tiempo razonable.

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.
***
### Prerequisitos

Se necesita instalar la herramienta PySAT en el caso de no disponer de ella. En el sigueinte [enlace]([click here](https://github.com/pysathq/pysat)) se encuentra el repositorio que contiene la última versión lanzada.  

### Instalación

Se debe clonar el repositorio. A continuación, hay que situarse en el directorio de `bica` y ejecutar el siguiente comando:

```bash
python3 link-bin.py
```
Para enlazar los programas necesarios en función de la arquitectura del sistema del usuario.

### Uso

Después de clonar el repositorio, los dos razonadores QBF están disponibles para su uso. Se debe especificar cuál se debe usar de los dos mediante un parámetro en el fichero `qbf_solver.py`. 

Si se desea emplear el razonador naíf:

```bash
python3 qbf_solver.py --bica [instancia_qbf]
```

Si se desea emplear el razonador con BICA:

```bash
python3 qbf_solver.py --naive [instancia_qbf]
```

Para que se muestre la información sobre el tiempo de ejecución, se añade el parámetro `-v`. Para más información:

```bash
python3 qbf_solver.py -h
```
