# Creado por Ruben el 06/01/2025

from mpi4py import MPI
import numpy as np

def main():
    # aqui se inicializan las variables de MPI 
    comm = MPI.COMM_WORLD # se crea el comunicador de procesos
    rank = comm.Get_rank()  # esta varible sirve para identificar al proceso actual
    size = comm.Get_size()  # para saber la cantidad de procesos totales

    # checkeo que hay 4 procesos exactos
    if size != 4:
        if rank == 0: # si no pones esto todos los procesos sacan el mensaje y solo debe hacerlo el proceso maestro
            print("Este programa requiere exactamente 4 procesos")
        MPI.Finalize() # se ciera MPI
        return

    # el proceso 0 crea la matriz
    if rank == 0:
        # crea matriz 10x10 donde cada fila contiene su número de indice
        matriz = np.array([[i] * 10 for i in range(10)]) # esta linea esta sacada de internet, se usa una funcion de numpy para agilizar el proceso de creacion de la matriz y sus contenidos
        print("Matriz original:\n")
        print(f"{matriz}\n")
        print("Distribuyendo trabajo entre procesos...\n")

        # el proceso 0 suma la priemra fila
        suma_parcial = np.sum(matriz[0]) # sum tambien es una funcion de numpy que suma todos los elementos de la fila
        print(f"Proceso {rank} suma fila 0\n")
        print(f"Suma parcial del proceso {rank}: {suma_parcial}\n")

        # se distribuyen las fials entre los procesos restantes
        for i in range(1, size):
            start_row = 1 + (i-1) * 3 # se decide la fila inicial en funcion del proceso 
            end_row = start_row + 3 if i < size-1 else 10 # se decide la fila final
            rows_to_send = matriz[start_row:end_row]
            comm.send(rows_to_send, dest=i) # se usa la funcion send para mandar las filas al proceso correspondiente
            print(f"Enviando filas {start_row} a {end_row-1} al proceso {i}\n")

    # aqui se reciben las filas y se suman
    else:
        # los procesos trabajadores reciben desde el proceso maestro
        filas = comm.recv(source=0) # recv recoge la informacion mandada por el proceso maestro, source es el proceso desde el cual se recibe por eso es 0
        # calcula la suma de las fials recibidas
        suma_parcial = np.sum(filas)
        print(f"Proceso {rank} suma filas {1+(rank-1)*3} a {min(1+(rank-1)*3+2, 9)}")
        print(f"Suma parcial del proceso {rank}: {suma_parcial}\n")


    # se recogen todas las sumas parciales en el proceso maestro
    sumas_parciales = comm.gather(suma_parcial, root=0) # gather recoge la variable definida entre los parentesis de cada proceso, y los alamcena en un array

    # el proceso maestro calcula y muestra la suma total
    if rank == 0:
        suma_total = sum(sumas_parciales)
        print("Resultados finales:")
        print(f"Sumas parciales de cada proceso: {sumas_parciales}")
        print(f"Suma total de la matriz: {suma_total}\n")
        
        # verificación de que los calculos son correctos
        expected_sum = np.sum(matriz)
        print(f"Verificación:")
        print(f"Suma calculada de forma distribuida: {suma_total}")
        print(f"Suma calculada directamente: {expected_sum}")
        print(f"¿Resultados coinciden? {suma_total == expected_sum}\n")
if __name__ == "__main__":
    main()