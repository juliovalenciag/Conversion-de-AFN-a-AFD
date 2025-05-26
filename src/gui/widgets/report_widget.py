from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel,
    QTableWidget, QTableWidgetItem, QFormLayout, QTextEdit
)
from PySide6.QtCore    import Qt
from typing             import List, Tuple
from nfa_dfa.nfa        import NFA

class ReportWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main = QVBoxLayout(self)
        main.setSpacing(12)

        grp_steps = QGroupBox("Pasos del algoritmo de subconjuntos")
        lay_steps = QVBoxLayout(grp_steps)
        self.steps_table = QTableWidget()
        self.steps_table.setColumnCount(4)
        self.steps_table.setHorizontalHeaderLabels(
            ["Origen", "Símbolo", "Mover", "ε-cierre"]
        )
        self._style_table(self.steps_table)
        lay_steps.addWidget(self.steps_table)
        main.addWidget(grp_steps)

        grp_det = QGroupBox("Detalles del AFD")
        form    = QFormLayout(grp_det)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.initial_lbl = QLabel()
        self.initial_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.finals_lbl  = QLabel()
        self.finals_lbl .setTextInteractionFlags(Qt.TextSelectableByMouse)
        form.addRow("Estado inicial:", self.initial_lbl)
        form.addRow("Estados finales:", self.finals_lbl)

        self.delta_list = QTextEdit()
        self.delta_list.setReadOnly(True)
        self.delta_list.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444444;
                padding: 4px;
            }
        """)
        form.addRow("Transiciones δ′:", self.delta_list)

        main.addWidget(grp_det)

    def _style_table(self, tbl: QTableWidget):
        tbl.setShowGrid(True)
        tbl.setGridStyle(Qt.SolidLine)
        tbl.setAlternatingRowColors(True)
        tbl.verticalHeader().setVisible(False)
        tbl.horizontalHeader().setStretchLastSection(True)
        tbl.setStyleSheet("""
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

    def set_steps(self, steps: List[Tuple[str,str,str]], nfa: NFA):
        """
        Rellena la tabla de pasos:
          steps: lista de tuplas (origen_str, símbolo, cierre_str),
                 donde cierre_str es la representación sin llaves de ε-cierre.
          nfa: para calcular mover(p, símbolo).
        """
        rows = []
        for origen_str, sym, cierre_str in steps:
            origen_set = set(origen_str.split(','))
            mover = set()
            for p in origen_set:
                mover |= nfa.delta.get((p, sym), set())
            mover_txt  = "{" + ",".join(sorted(mover)) + "}" if mover else "∅"
            cierre_txt = "{" + cierre_str + "}"         if cierre_str else "∅"
            rows.append((
                "{" + origen_str + "}",
                sym or "ε",
                mover_txt,
                cierre_txt
            ))

        self.steps_table.clearContents()
        self.steps_table.setRowCount(len(rows))
        for i, cols in enumerate(rows):
            for j, txt in enumerate(cols):
                it = QTableWidgetItem(txt)
                it.setTextAlignment(Qt.AlignCenter)
                self.steps_table.setItem(i, j, it)
        self.steps_table.resizeColumnsToContents()

    def set_details(self, dfa):
        """
        Muestra:
         - Estado inicial (q0)
         - Estados finales (F)
         - Listado completo de δ′ en formato δ′(s,a) = {destinos}
        """
        # Inicial y finales
        self.initial_lbl.setText(dfa.q0)
        finals = sorted(dfa.finals)
        self.finals_lbl.setText("{" + ", ".join(finals) + "}")

        lines = []
        for (s, sym), dests in sorted(dfa.delta.items()):
            symbol = sym if sym else "ε"
            tgt    = ", ".join(sorted(dests)) if dests else "∅"
            lines.append(f"δ′({s}, {symbol}) = &#123;{tgt}&#125;")
        self.delta_list.setHtml("<br>".join(lines))

    def clear(self):
        self.steps_table.clearContents()
        self.steps_table.setRowCount(0)
        self.initial_lbl.clear()
        self.finals_lbl.clear()
        self.delta_list.clear()
