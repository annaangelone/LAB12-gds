import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listCountry = self._model.getDDCountry()

        self._listYear = [2015, 2016, 2017, 2018]

        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        country = self._view.ddcountry.value
        anno = int(self._view.ddyear.value)
        self._model.getRetailers(country)

        if anno is None:
            self._view.create_alert("Inserire un anno")
            return

        if country is None:
            self._view.create_alert("Inserire una nazione")
            return

        self._model.buildGraph(anno)
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))

        self._view.update_page()




    def handle_volume(self, e):
        retailersOrdinati = self._model.getRetailersOrdinati()
        self._view.txtOut2.controls.clear()

        for r in retailersOrdinati:
            if r.Volume != 0:
                self._view.txtOut2.controls.append(ft.Text(f"{r.Retailer_name} --> {r.Volume}"))

        self._view.update_page()


    def handle_path(self, e):
        lunghezza = self._view.txtN.value
        self._view.txtOut3.controls.clear()

        try:
            lun = int(lunghezza)

        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Il valore inserito non è un numero"))
            self._view.update_page()
            return

        if lun < 2:
            self._view.create_alert("Inserire una lunghezza maggiore di 2")


        path, peso = self._model.getPercorso(lun)

        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))

        for i in range(len(path) - 1):
            w = self._model._grafo[path[i]][path[i+1]]["weight"]
            self._view.txtOut3.controls.append(ft.Text(f"{path[i].Retailer_name} --> {path[i+1].Retailer_name}: {w}"))


        self._view.update_page()

