from modules.coda import Coda

def main():
    coda = Coda()
    coda.push(1)
    coda.push(2)
    coda.push(3)
    coda.push(4)
    coda.push(5)
    print(coda)
    print(f"lunghezza coda: {coda.lenght()}")
    print(f"Rimosso il valore {coda.pop()}")

if __name__ == "__main__":
    main()