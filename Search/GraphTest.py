import graph
import search

def main():
    # Hier kann beliebiger Testcode stehen, der bei der Korrektur ignoriert wird
    network = graph.graph()
    for x in network:
        print(x)
        print(network[x].id)
        for y in network[x].schedule:
            print('___________')
            print(y)
            print('_____')
            print(y.id)
            print(y.stop)
            print(y.arrival)
            print(y.departure)
            print(y.distance)
            print(y.nextStation)
        print('-----')
    pass


if __name__ == "__main__": main()