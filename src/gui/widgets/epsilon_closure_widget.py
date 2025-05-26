from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore    import Qt
from typing import Dict, Set

class EpsilonClosureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<h2>2. Cálculo de clausuras ε</h2>"))

        # Tabla de ε-closures
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Estado", "ε-closure({Estado})"])

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
        # ───────────────────────────────────────────────────────────────

        lay.addWidget(self.table)

    def set_closures(self, closures: Dict[str, Set[str]]):
        """
        closures: mapeo estado -> conjunto de estados en su ε-closure
        """
        items = sorted(closures.items(), key=lambda x: x[0])
        self.table.setRowCount(len(items))
        for i, (state, clset) in enumerate(items):
            # Columna Estado
            item_state = QTableWidgetItem(state)
            item_state.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, item_state)

            # Columna ε-closure
            text = "{ " + ", ".join(sorted(clset)) + " }"
            item_cl = QTableWidgetItem(text)
            item_cl.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, item_cl)

        self.table.resizeColumnsToContents()

    def clear(self):
        """Borra todas las filas de la tabla, dejando intactas las columnas."""
        self.table.clearContents()
        self.table.setRowCount(0)
