import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._retailers = []

        self._bestPath = []
        self._pesoMax = 0


    def getRetailers(self, country):
        self._retailers = DAO.getRetailersByCountry(country)
        for r in self._retailers:
            self._idMap[r.Retailer_code] = r
        return self._retailers

    def getDDCountry(self):
        countries = DAO.getDDCountry()
        return countries

    def buildGraph(self, anno):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._retailers)

        for u in self._retailers:
            for v in self._retailers:
                if u != v:
                    peso = DAO.getEdges(anno, u, v)[0]

                    if peso > 0:
                        self._grafo.add_edge(u, v, weight=peso)



    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def calcolaVolumeVendita(self, r0):
        volume = 0

        nodi_vicini = self._grafo.neighbors(r0)
        for n in nodi_vicini:
            volume += self._grafo[r0][n]["weight"]

        r0.Volume = volume
        return volume

    def getRetailersOrdinati(self):
        for r in self._grafo.nodes:
            self.calcolaVolumeVendita(r)

        retailersOrdinati = sorted(self._retailers, key=lambda x: x.Volume, reverse=True)

        return retailersOrdinati


    def getPercorso(self, lunghezza):
        self._bestPath = []
        self._pesoMax = 0

        for n in self._retailers:
            parziale = [n]
            self.ricorsione(parziale, n, lunghezza)


        return self._bestPath, self._pesoMax


    def ricorsione(self, parziale, v0, lunghezza):

        if len(parziale) == lunghezza:
            if parziale[-1] == v0 and self.calcolaPeso(parziale) > self._pesoMax:
                self._pesoMax = self.calcolaPeso(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return


        for n in self._grafo.neighbors(parziale[-1]):
            if len(parziale) == lunghezza - 1:
                parziale.append(n)
                self.ricorsione(parziale, v0, lunghezza)
                parziale.pop()
            else:
                if n not in parziale:
                    parziale.append(n)
                    self.ricorsione(parziale, v0, lunghezza)
                    parziale.pop()


    def calcolaPeso(self, parziale):
        pesoTotale = 0

        for i in range(len(parziale)-1):
            pesoTotale += self._grafo[parziale[i]][parziale[i+1]]["weight"]

        return pesoTotale
