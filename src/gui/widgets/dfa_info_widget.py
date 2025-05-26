from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout,
    QLabel, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PySide6.QtCore    import Qt

class DFAInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        # ── Grupo: Quíntupla del AFD ───────────────────────────────────
        quint_group = QGroupBox("Quíntupla del AFD")
        quint_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        form = QFormLayout(quint_group)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.Q_lbl     = QLabel(); self.Q_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.Sigma_lbl = QLabel(); self.Sigma_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.delta_lbl = QLabel(); self.delta_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.q0_lbl    = QLabel(); self.q0_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.F_lbl     = QLabel(); self.F_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        for lbl in (self.Q_lbl, self.Sigma_lbl, self.delta_lbl, self.q0_lbl, self.F_lbl):
            lbl.setWordWrap(True)

        form.addRow("<b>Q′:</b>",  self.Q_lbl)
        form.addRow("<b>Σ:</b>",   self.Sigma_lbl)
        form.addRow("<b>δ′:</b>",  self.delta_lbl)
        form.addRow("<b>q₀′:</b>", self.q0_lbl)
        form.addRow("<b>F′:</b>",  self.F_lbl)

        main_layout.addWidget(quint_group, stretch=0)

        # ── Tabla de δ′ ───────────────────────────────────────────────
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

    def set_dfa(self, dfa):
        states = sorted(dfa.states)
        name_map = {s: f"S{i}" for i, s in enumerate(states)}

        Qp     = ", ".join(name_map[s] for s in states)
        Sigma  = ", ".join(sorted(dfa.sigma))
        q0p    = name_map[dfa.q0]
        Fp     = ", ".join(name_map[s] for s in states if s in dfa.finals)

        lines = []
        for (src, sym), dest in sorted(dfa.delta.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            src_lbl = name_map[src]
            sym_lbl = sym if sym else "ε"
            if not dest:
                tgt_lbl = "∅"
            else:
                tgt_lbl = name_map.get(dest, dest)
            lines.append(f"δ′({src_lbl}, {sym_lbl}) = &#123;{tgt_lbl}&#125;")

        self.Q_lbl.setText(f"{{{Qp}}}")
        self.Sigma_lbl.setText(f"{{{Sigma}}}")
        self.delta_lbl.setText("<br>".join(lines))
        self.q0_lbl.setText(q0p)
        self.F_lbl.setText(f"{{{Fp}}}")

        headers = ["Estado"] + sorted(dfa.sigma)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(states))

        for i, state in enumerate(states):
            it0 = QTableWidgetItem(name_map[state])
            it0.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, it0)

            for j, sym in enumerate(sorted(dfa.sigma), start=1):
                dest = dfa.delta.get((state, sym), "")
                if not dest:
                    text = "∅"
                else:
                    text = name_map.get(dest, dest)
                cell = QTableWidgetItem(text)
                cell.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, cell)

        self.table.resizeColumnsToContents()

    def clear(self):
        for lbl in (self.Q_lbl, self.Sigma_lbl, self.delta_lbl, self.q0_lbl, self.F_lbl):
            lbl.clear()
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
