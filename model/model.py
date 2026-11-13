from database.distributore_DAO import DistributoreDAO
import copy
'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        risultato = []
        for d in self._distributori:
            i=0
            s=0.0
            for p in d.get_prezzi():
                if p.data.month == mese:
                    i=i+1
                    s=s+p.prezzo_litro
            if i!=0:
                a = s/i
                risultato.append((d.nome, a))
        return risultato







    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)


    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """

        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                # Usiamo deepcopy per non perdere la sequenza quando facciamo i pop()
                self.__sequenza_ottima = copy.deepcopy(sequenza_parziale)
            return

        for id_dist, lista_prezzi_7giorni in prezzi_settimana.items():

            costo_carburante = lista_prezzi_7giorni[giorno - 1] * 100

            costo_spostamento = 0
            if ultimo_distributore is not None and ultimo_distributore != id_dist:
                costo_spostamento = 5

            nuovo_costo = costo_corrente + costo_carburante + costo_spostamento

            if self.__costo_ottimo == -1 or nuovo_costo < self.__costo_ottimo:
                sequenza_parziale.append(id_dist)

                self.__ricorsione(sequenza_parziale, giorno + 1, id_dist, nuovo_costo, prezzi_settimana)

                sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        prezzi_settimana = {}
        for d in self._distributori:
            # Filtro i prezzi per il mese corrente
            prezzi_mese = [p for p in d.get_prezzi() if p.data.month == mese]
            # Li ordino per data in modo da essere sicuro di prendere i giorni dall'1 al 7 in ordine
            prezzi_mese.sort(key=lambda x: x.data)

            # Prendo solo i primi 7 elementi e ne estraggo il prezzo (convertito in float per sicurezza)
            prezzi_settimana[d.id] = [float(p.prezzo_litro) for p in prezzi_mese[:7]]

        return prezzi_settimana