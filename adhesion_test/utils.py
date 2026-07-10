def load_dataset(file_path):
    with open(file_path, "r") as file:
        data = file.read()

    return [float(i.strip(',')) for i in data.split()]

if __name__ == "__main__":
    amostra = load_dataset("entrada-lista-1.txt")
    print(amostra)