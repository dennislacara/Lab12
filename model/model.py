import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.rifugio_map = {}
        self.lista_connessioni = []
        self.difficolta_map = {'facile': 1, 'media': 1.5, 'difficile': 2}
        # TODO

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        #implementazione nodi del grafo
        self.load_rifugi()
        #creazione degli archi
        self.load_connessioni(year)
        # TODO

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        pesi = [arco[2]['peso'] for arco in self.G.edges.data()]
        return min(pesi), max(pesi)
        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori, maggiori = 0,0
        for arco in self.G.edges.data():
            if arco[2]['peso'] < soglia:
                minori += 1
            elif arco[2]['peso'] > soglia:
                maggiori += 1
        return minori, maggiori
        # TODO

    def load_connessioni(self, year: int):
        #importo le connessioni dal Dao che interroga il database
        self.lista_connessioni = DAO.get_all_connessioni(year)

        #incremento il grafo
        for connessione in self.lista_connessioni:
            fattore_difficolta = self.difficolta_map[connessione.difficolta]
            distanza = connessione.distanza
            peso = float(distanza) * fattore_difficolta
            oggetto_rifugio1 = self.rifugio_map[connessione.id_rifugio1]
            oggetto_rifugio2 = self.rifugio_map[connessione.id_rifugio2]
            self.G.add_edge(oggetto_rifugio1, oggetto_rifugio2, peso= peso)
            #print('fattore_difficolta:', fattore_difficolta)
            #print(self.G.edges[connessione.id_rifugio1, connessione.id_rifugio2]['peso'])
        print('Grafo implementato!')

    """Implementare la parte di ricerca del cammino minimo"""
    def get_edges_min_weight(self, soglia: int):
        #nodi degli archi ammessi, con peso >= alla soglia
        archi_ammessi = self.load_archi_ammessi(soglia)

        #creo un grafo relativo con gli archi ammessi
        g = nx.Graph()
        g.add_edges_from(archi_ammessi)
        #ricavo i percorsi minimi
        percorso_salvato = []
        percorsi_minimi = dict(nx.all_pairs_all_shortest_paths(g, weight='peso'))
        for key_partenza in percorsi_minimi:
            for key_arrivo in percorsi_minimi[key_partenza]:
                for percorso in percorsi_minimi[key_partenza][key_arrivo]:
                    #condizione necessaria
                    if len(percorso) <=2 :
                        continue
                    else:
                        # assegno primo percorso valido
                        if percorso_salvato == []:
                            percorso_salvato = percorso
                        # comparazione del peso da secondo percorso valido in poi
                        else:
                            peso1 = nx.path_weight(g, percorso, weight='peso')
                            peso2 = nx.path_weight(g, percorso_salvato, weight='peso')
                            if peso1 > peso2:
                                continue
                            percorso_salvato = percorso
                    #se non ci sono percorsi validi, la lista rimane vuota
        #print(percorso_salvato)
        return percorso_salvato

    def load_archi_ammessi(self, soglia):
        archi = []
        for arco in self.G.edges.data():
            if arco[2]['peso'] > soglia:
                #print(arco)
                archi.append(arco)
        return archi

    def load_rifugi(self):
        self.rifugio_map = DAO.get_all_rifugi()
        for id in self.rifugio_map:
            self.G.add_node(self.rifugio_map[id])
            #print(self.rifugio_map[id])