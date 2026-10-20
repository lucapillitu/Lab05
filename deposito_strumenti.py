from strumento import Strumento
from prestito import Prestito
from operator import attrgetter


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []
        self._prossimo_numero_prestito = 1

    def get_responsabile(self):
        return self.responsabile

    def set_responsabile(self, valore):
        if not valore.strip():
            raise ValueError("Nome responsabile non valido")
        self.responsabile = valore.strip()






    def carica_file_strumenti(self, file_path):

        with open(file_path, "r") as f:
            for l in f.readlines():
                line = l.strip()
                if not line:
                    continue
                campi = line.split(",")
                if any(s.codice == campi[0] for s in self.strumenti):
                    continue

                self.strumenti.append(Strumento(campi[0], campi[1], campi[2], int(campi[3]), float(campi[4])))

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        nuovo_num = max((int(s.codice[1:]) for s in self.strumenti), default=0) + 1

        s = Strumento(f"S{nuovo_num}", tipo, marca, anno_acquisto, valore)

        self.strumenti.append(s)

        return s

    def strumenti_ordinati_per_marca(self):

        return sorted(self.strumenti, key=attrgetter("marca"))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):

        if not any(s.codice == id_strumento for s in self.strumenti):
            raise Exception(f"Strumento {id_strumento} non presente nel deposito")

        if any(p.id_strumento == id_strumento for p in self.prestiti):
            raise Exception(f"Strumento {id_strumento} già in prestito")

        prestito = Prestito(f"P{self._prossimo_numero_prestito}", data, id_strumento, cognome_allievo)
        self.prestiti.append(prestito)
        self._prossimo_numero_prestito += 1
        return prestito


    def termina_prestito(self, id_prestito):

        for p in self.prestiti:
            if p.codice == id_prestito:
                self.prestiti.remove(p)
                return
        raise Exception(f"Non è stato trovato nessun prestito : {id_prestito}")

