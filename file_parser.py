class QBF(object):
    def __init__(self, file_name = None):
        self.clauses = []
        self.quantifiers = []
        self.is_cnf = None
        self.file_name = file_name
        self.num_vars = 0
        if file_name:
            self.read_qdimacs()

    def read_qdimacs(self):
        self.clauses = []
        self.quantifiers = []
        self.is_cnf = None
        self.num_vars = 0
        if not self.file_name:
            raise ValueError("El nombre del archivo no puede ser None.")
        with open(self.file_name, mode = 'r') as file:
            for line in file:
                self.read_line(line)
            if len(self.quantifiers) == 0:
                print("No hay cuantificadores en el archivo QDIMACS. Tratando como si todas las variables fueran cuantificadas existencialmente.")
                self.quantifiers.append(list(('e', set(range(1, self.num_vars + 1)))))

    def read_dimacs(self, file_name, negate = False):
        self.clauses = []
        self.is_cnf = None
        self.num_vars = 0
        if not file_name:
            raise ValueError("El nombre del archivo debe proporcionarse para leer el formato DIMACS.")
        with open(file_name, mode = 'r') as file:
            for line in file:
                self.read_line(line, negate = negate)

    def write_file(self, file_name, negate = False):
        with open(file_name, mode = 'w') as file:
            file.write("c n orig vars {}\n".format(self.num_vars))
            file.write("p {} {} {}".format( "cnf" if self.is_cnf else "dnf", self.num_vars, len(self.clauses)))
            for clause in self.clauses:
                if negate:
                    clause = set(-lit for lit in clause)
                file.write("\n" + " ".join(map(str, clause)) + " 0")

    def read_line(self, line, negate = False):
        line = line.strip()
        if line:
            if line[0] == 'c':
                return
            if line[0] == 'p':
                self.num_vars = int(line.split()[2])
                self.is_cnf = True if line.split()[1] == 'cnf' else False
                return
            if line[0] == 'a' or line[0] == 'e':
                self.quantifiers.append(list((line[0], set(map(int, line.split()[1:-1])))))
                return
            if negate:
                self.clauses.append((set(-int(lit) for lit in line.split()[:-1])))
                return
            self.clauses.append((set(map(int, line.split()[:-1]))))