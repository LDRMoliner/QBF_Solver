import file_parser
import naive_solver
import bica_solver
import sys
import os
import getopt
import time

def uso():
    """
    Muestra el uso correcto del script.
    """
    print('Uso: ' + os.path.basename(sys.argv[0]) + ' [opciones] fichero_qbf')
    print("Opciones:")
    print("  -h, --help: Muestra este mensaje de ayuda.")
    print("  --bica: Utiliza el Razonador con BICA para resolver la QBF.")
    print("  --naif: Utiliza el Razonador Naíf para resolver la QBF.")
    sys.exit(1)

if __name__ == "__main__":

    """
    Punto de entrada del script.
    Permite seleccionar entre el razonador BICA o el Naíf para resolver una QBF.
    """
    if len(sys.argv) < 2:
        uso()
        sys.exit(1)

    bica = True
    naif = False
    verbose = False
    try:
        opciones, nombre_fichero = getopt.getopt(sys.argv[1:], "hbnv", ['help', 'bica', 'naive', 'verbose'])
    except getopt.GetoptError as e:
        uso()
        sys.exit()
    for opcion, arg in opciones:
        if opcion in ("-h", "--help"):
            uso()
            sys.exit(0)
        elif opcion in ("-b", "--bica"):
            bica = True
        elif opcion in ("-n", "--naive"):
            naif = True
            bica = False
        elif opcion in ("-v", "--verbose"):
            verbose = True


    # En función de la flag, "--bica" o "--naive", se elige el solver

    qbf = file_parser.QBF(nombre_fichero[0])
    if bica:
        instancia = bica_solver.BicaSolver(qbf)
        start_time = time.time()
        resultado = instancia.solve()
        end_time = time.time()
        if not verbose:
            print(resultado)
        if verbose:
            print("{},{},{}".format(os.path.basename(sys.argv[3]),end_time - start_time, resultado))
    if naif:
        instancia = naive_solver.NaiveSolver(qbf)
        start_time = time.time()
        resultado = instancia.solve()
        end_time = time.time()
        if not verbose:
            print(resultado)
        if verbose:
            print("{},{},{}".format(os.path.basename(sys.argv[3]),end_time - start_time, resultado))
