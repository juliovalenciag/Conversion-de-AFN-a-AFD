from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore    import Qt
from typing import List, Tuple, Set

class SubsetConstructionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<h2>3. Construcción del AFD (subset construction)</h2>"))

        intro = QLabel(
            "<p>Estado inicial del AFD: <b>S<sub>0</sub> = ε-closure({q<sub>0</sub>})</b></p>"
            "<p>Para cada subconjunto S y símbolo a &in; Σ:</p>"
            "<ol>"
            "<li>formamos &cup;<sub>p&in;S</sub> δ(p,a)</li>"
            "<li>aplicamos ε-closure</li>"
            "</ol>"
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self.table = QTableWidget()
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #444444;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #555555;
            }
        """)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        # ────────────────────────────────────────────────────────────────

        layout.addWidget(self.table)

    def set_steps(
        self,
        steps: List[Tuple[str, str, str]],
        sigma: List[str],
        finals: Set[str]
    ):
        """
        Llena la tabla con los pasos de la construcción.
        - steps: lista de (estado_origen, símbolo, estado_destino)
        - sigma: lista de símbolos del alfabeto (sin ε)
        - finals: conjunto de estados finales en el AFD
        """
        origins: List[str] = []
        for origin, symbol, dest in steps:
            if origin not in origins:
                origins.append(origin)

        headers = ["Estado"] + sigma + ["¿Final?"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(origins))

        for row_idx, origin in enumerate(origins):

            self.table.setItem(row_idx, 0, QTableWidgetItem(origin))

            for col_idx, sym in enumerate(sigma, start=1):
                dest = ""
                for o, a, d in steps:
                    if o == origin and a == sym:
                        dest = d
                        break
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(dest))

            is_final = "Sí" if origin in finals else "No"
            self.table.setItem(row_idx, len(headers) - 1, QTableWidgetItem(is_final))

        self.table.resizeColumnsToContents()

    def clear(self):

        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
