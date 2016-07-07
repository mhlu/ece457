import sys

if __name__ == "__main__":
    capacity = 0
    cities = 0
    trucks = 0
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        line = f.readline()
        trucks = int(line[line.rfind('k') + 1:])
        while not line.startswith('DIMENSION'):
            line = f.readline()
        cities = int(line[line.rfind(":") + 1:])

        while not line.startswith('CAPACITY'):
            line = f.readline()
        capacity = int(line[line.rfind(":") + 1:])

        while not line.startswith('NODE_COORD_SECTION'):
            line = f.readline()

