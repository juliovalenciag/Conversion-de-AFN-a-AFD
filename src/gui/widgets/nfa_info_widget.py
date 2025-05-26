from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout,
    QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PySide6.QtCore    import Qt

class NFAInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        # ── Grupo Quíntupla ────────────────────────────────────────────
        quint_group = QGroupBox("Quíntupla del AFN")
        quint_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        form = QFormLayout(quint_group)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.Q_lbl     = QLabel()
        self.Sigma_lbl = QLabel()
        self.delta_lbl = QLabel()
        self.q0_lbl    = QLabel()
        self.F_lbl     = QLabel()

        for lbl in (self.Q_lbl, self.Sigma_lbl, self.delta_lbl, self.q0_lbl, self.F_lbl):
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            lbl.setWordWrap(True)

        form.addRow("<b>Q:</b>",     self.Q_lbl)
        form.addRow("<b>Σ:</b>",     self.Sigma_lbl)
        form.addRow("<b>δ:</b>",     self.delta_lbl)
        form.addRow("<b>q₀:</b>",    self.q0_lbl)
        form.addRow("<b>F:</b>",     self.F_lbl)

        main_layout.addWidget(quint_group, stretch=0)

        # ── Tabla de transiciones δ ────────────────────────────────────
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

        main_layout.addWidget(self.table, stretch=1)

    def set_nfa(self, nfa):
        Q = sorted(nfa.states)
        Σ = sorted(nfa.sigma)
        q0 = nfa.q0
        F = sorted(nfa.finals)

        self.Q_lbl.setText("{" + ", ".join(Q) + "}")
        self.Sigma_lbl.setText("{" + ", ".join(Σ) + "} ∪ {ε}")
        lines = []
        for (s, sym), dests in sorted(nfa.delta.items()):
            symbol = sym if sym else "ε"
            targets = ", ".join(sorted(dests)) or "∅"
            lines.append(f"δ({s}, {symbol}) = &#123;{targets}&#125;")
        self.delta_lbl.setText("<br>".join(lines))

        self.q0_lbl.setText(q0)
        self.F_lbl.setText("{" + ", ".join(F) + "}")

        headers = ["Estado"] + Σ + ["ε"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(Q))

        for i, state in enumerate(Q):
            self.table.setItem(i, 0, QTableWidgetItem(state))
            for j, sym in enumerate(Σ, start=1):
                dests = nfa.delta.get((state, sym), set())
                text = ", ".join(sorted(dests)) if dests else "∅"
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

            edests = nfa.delta.get((state, ""), set())
            text = ", ".join(sorted(edests)) if edests else "∅"
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, len(headers)-1, item)

        self.table.resizeColumnsToContents()

    def clear(self):
        for lbl in (self.Q_lbl, self.Sigma_lbl, self.delta_lbl, self.q0_lbl, self.F_lbl):
            lbl.clear()
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
