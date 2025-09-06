import file_parser
import naive_solver
import bica_solver
import sys
import os
import getopt

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

    bica = True
    naif = False
    try:
        opciones, nombre_fichero = getopt.getopt(sys.argv[1:], "hbn", ['help', 'bica', 'naive'])
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


    # En función de la flag, "-bica" o "-naive", se elige el solver

    qbf = file_parser.QBF(nombre_fichero[0])
    if bica:
        print("Usando el Razonador BICA para resolver la QBF.")
        print(bica_solver.BicaSolver(qbf).solve())
    if naif:
        print("Usando el Razonador Naíf para resolver la QBF.")
        print(naive_solver.NaiveSolver(qbf).solve())