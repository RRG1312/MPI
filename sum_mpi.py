# Creado por Ruben el 06/01/2025

from mpi4py import MPI
import numpy as np

def main():
    # aqui se inicializan las variables de MPI 
    comm = MPI.COMM_WORLD 
    rank = comm.Get_rank()  
    size = comm.Get_size()  

    # checkeo que hay 4 procesos exactos
    if size != 4:
        if rank == 0: 
            print("Este programa requiere exactamente 4 procesos")
        MPI.Finalize() 
        return

    # el proceso 0 crea la matriz
    if rank == 0:
        matriz = np.array([[i] * 10 for i in range(10)]) 
        print("Matriz original:\n")
        print(f"{matriz}\n")
        print("Distribuyendo trabajo entre procesos...\n")

        # el proceso 0 suma la priemra fila
        suma_parcial = np.sum(matriz[0]) 
        print(f"Proceso {rank} suma fila 0\n")
        print(f"Suma parcial del proceso {rank}: {suma_parcial}\n")

        # se distribuyen las fials entre los procesos restantes
        for i in range(1, size):
            start_row = 1 + (i-1) * 3 
            end_row = start_row + 3 if i < size-1 else 10 
            rows_to_send = matriz[start_row:end_row]
            comm.send(rows_to_send, dest=i) 
            print(f"Enviando filas {start_row} a {end_row-1} al proceso {i}\n")

    # aqui se reciben las filas y se suman
    else:
        filas = comm.recv(source=0)
        suma_parcial = np.sum(filas)
        print(f"Proceso {rank} suma filas {1+(rank-1)*3} a {min(1+(rank-1)*3+2, 9)}")
        print(f"Suma parcial del proceso {rank}: {suma_parcial}\n")


    # se recogen todas las sumas parciales en el proceso maestro
    sumas_parciales = comm.gather(suma_parcial, root=0) 
    
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