# Proyecto: Suma de una Matriz de 10x10 con Py-MPI
#Link al repositorio: https://github.com/RRG1312/MPI.git
## Descripción
Este proyecto implementa un sistema distribuido utilizando **Py-MPI** para calcular la suma de los elementos de una matriz de 10x10. Se divide el cálculo entre cuatro procesos, lo que permite explorar conceptos de programación paralela y comunicación entre procesos.

## Objetivos
- Dividir y distribuir el cálculo de la suma de una matriz entre múltiples procesos.
- Implementar un sistema que utilice la interfaz de paso de mensajes MPI con Python.
- Verificar la correcta ejecución mediante cálculos centralizados y distribuidos.


### Dependencias
1. **MPI y librerías de sistema**:
   ```bash
   sudo apt-get install openmpi-bin libopenmpi-dev
   ```
2. **Librerías de Python**:
   ```bash
   pip install mpi4py numpy
   ```
3. **Actualizar listas de paquetes del sistema** (en caso de errores):
   ```bash
   sudo apt-get update
   ```

## Instalación
1. Clonar este repositorio:
   ```bash
   git clone https://github.com/RRG1312/MPI.git
   cd MPI
   ```
2. Verificar que `mpirun` está correctamente instalado:
   ```bash
   which mpirun
   mpirun --version
   ```

## Cómo Ejecutar el Código

### Comando para ejecución:
Para ejecutar el programa con 4 procesos, usa el siguiente comando:
```bash
mpirun -n 4 python sum_mpi.py
```
Donde:
- `-n 4`: Especifica el número de procesos a utilizar.
- `sum_mpi.py`: Archivo que contiene la lógica del programa.

### Salida esperada:
- **Proceso 0**:
  - Creará la matriz original.
  - Distribuirá filas a los procesos trabajadores.
  - Recolectará los resultados parciales y calculará la suma total.

- **Procesos 1-3**:
  - Recibirán filas de la matriz y calcularán las sumas parciales.

## Explicación del Código
El programa sigue los siguientes pasos:
1. **Inicialización de MPI**:
   - `comm = MPI.COMM_WORLD`: Crea un comunicador global.
   - `rank`: Identifica el proceso.
   - `size`: Obtiene el número total de procesos.

2. **Creación y distribución de la matriz**:
   - El proceso 0 crea una matriz de 10x10 donde cada fila contiene el mismo número.
   - Divide las filas entre los procesos trabajadores utilizando `comm.send` y `comm.recv`.

3. **Cálculo de sumas parciales**:
   - Cada proceso suma los elementos de las filas asignadas utilizando `numpy.sum`.

4. **Recolección de resultados**:
   - El proceso 0 recolecta las sumas parciales de todos los procesos con `comm.gather`.
   - Calcula la suma total y la verifica contra un cálculo directo.

## Ejemplo de Salida
```plaintext
Matriz original:
[[0 0 0 ... 0]
 [1 1 1 ... 1]
 ...
 [9 9 9 ... 9]]

Distribuyendo trabajo entre procesos...
Enviando filas 1 a 3 al proceso 1
Enviando filas 4 a 6 al proceso 2
Enviando filas 7 a 9 al proceso 3

Proceso 0 suma fila 0
Suma parcial del proceso 0: 0
Proceso 1 suma filas 1 a 3
Suma parcial del proceso 1: 30
...
Resultados finales:
Sumas parciales de cada proceso: [0, 30, 75, 120]
Suma total de la matriz: 225
Verificación:
¿Resultados coinciden? True
```

## Créditos
Este proyecto fue desarrollado por el siguiente equipo:
- **Pablo Alonso Serrano**
- **Jacob Altenburger Villar**
- **Jorge Alejandro Cadrecha Del Rey**
- **Rubén Rodríguez García**
- **Diego Villena Macarron**

