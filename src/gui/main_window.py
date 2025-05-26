# src/gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTabWidget, QMessageBox, QFileDialog,
    QStatusBar, QWidget, QSizePolicy, QStyle
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize, Qt

from parsers.txt_parser import parse_nfa_from_txt
from parsers.jflap_parser import parse_nfa_from_jff
from nfa_dfa.step_engine import convert_nfa_to_dfa
from nfa_dfa.jflap_export import export_nfa_to_jff, export_dfa_to_jff

from gui.widgets.nfa_info_widget import NFAInfoWidget
from gui.widgets.epsilon_closure_widget import EpsilonClosureWidget
from gui.widgets.subset_construction_widget import SubsetConstructionWidget
from gui.widgets.dfa_info_widget import DFAInfoWidget
from gui.widgets.report_widget import ReportWidget
from gui.widgets.theory_widget import TheoryWidget
from gui.widgets.log_widget import LogWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ── Toolbar ─────────────────────────────────────────────────────────
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        style = self.style()

        # Cargar AFN
        icon_open = style.standardIcon(QStyle.SP_DialogOpenButton)
        self.open_action = QAction(icon_open, "Cargar AFN", self)
        self.open_action.setToolTip("Elige un archivo .txt o .jff de tu AFN")
        self.open_action.triggered.connect(self.on_load)
        toolbar.addAction(self.open_action)

        # Convertir
        icon_run = style.standardIcon(QStyle.SP_CommandLink)
        self.convert_action = QAction(icon_run, "Convertir", self)
        self.convert_action.setEnabled(False)
        self.convert_action.setToolTip("Convierte el AFN cargado a AFD")
        self.convert_action.triggered.connect(self.on_convert)
        toolbar.addAction(self.convert_action)

        toolbar.addSeparator()

        clear_icon = style.standardIcon(QStyle.SP_TrashIcon)
        self.clear_action = QAction(clear_icon, "Limpiar", self)
        self.clear_action.setToolTip("Limpiar toda la información cargada")
        self.clear_action.triggered.connect(self.on_clear)
        toolbar.addAction(self.clear_action)

        toolbar.addSeparator()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Exportar AFN
        icon_save = style.standardIcon(QStyle.SP_DialogSaveButton)
        self.exp_nfa_action = QAction(icon_save, "Exportar AFN", self)
        self.exp_nfa_action.setEnabled(False)
        self.exp_nfa_action.setToolTip("Guardar el AFN en formato .jff para JFLAP")
        self.exp_nfa_action.triggered.connect(self.on_export_nfa)
        toolbar.addAction(self.exp_nfa_action)

        # Exportar AFD
        icon_apply = style.standardIcon(QStyle.SP_DialogApplyButton)
        self.exp_dfa_action = QAction(icon_apply, "Exportar AFD", self)
        self.exp_dfa_action.setEnabled(False)
        self.exp_dfa_action.setToolTip("Guardar el AFD resultado en formato .jff para JFLAP")
        self.exp_dfa_action.triggered.connect(self.on_export_dfa)
        toolbar.addAction(self.exp_dfa_action)

        # ── Pestañas ────────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.nfa_tab = NFAInfoWidget(parent=self)
        self.closure_tab = EpsilonClosureWidget(parent=self)
        self.subset_tab = SubsetConstructionWidget(parent=self)
        self.dfa_tab = DFAInfoWidget(parent=self)
        self.rep_tab = ReportWidget(parent=self)
        self.theory_tab = TheoryWidget(parent=self)
        self.log_tab = LogWidget(parent=self)

        for widget, title in [
            (self.nfa_tab, "AFN"),
            (self.closure_tab, "Clausuras ε"),
            (self.subset_tab, "Construcción"),
            (self.dfa_tab, "AFD"),
            (self.rep_tab, "Report"),
            (self.theory_tab, "Teoría"),
            (self.log_tab, "Log"),
        ]:
            self.tabs.addTab(widget, title)

        # ── Barra de estado ────────────────────────────────────────────────
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("Carga tu AFN para empezar")

        # ── Estado interno ─────────────────────────────────────────────────
        self.current_nfa = None
        self.current_dfa = None
        self.result = None

    def on_load(self):
        self.on_clear()
        path, _ = QFileDialog.getOpenFileName(
            self, "Abrir AFN", filter="Text Files (*.txt);;JFLAP Files (*.jff)"
        )
        self.log_tab.log(f"Dialogo abrió: {path or '<ningún archivo>'}")
        if not path:
            return

        try:
            if path.lower().endswith(".txt"):
                self.current_nfa = parse_nfa_from_txt(path)
            else:
                self.current_nfa = parse_nfa_from_jff(path)
        except Exception as ex:
            QMessageBox.critical(self, "Error al cargar AFN", str(ex))
            self.log_tab.log(f"❌ Error parseando {path}: {ex}")
            return

        self.log_tab.log(f"✅ AFN cargado: {path}")
        self.nfa_tab.set_nfa(self.current_nfa)

        # También preparo la tabla de clausuras
        closures = self.current_nfa.epsilon_closures()
        self.closure_tab.set_closures(closures)

        self.convert_action.setEnabled(True)
        self.exp_nfa_action.setEnabled(True)
        self.statusBar().showMessage("Ahora convierte el AFN a AFD")
        self.tabs.setCurrentWidget(self.nfa_tab)

    def on_convert(self):
        try:
            # 1. Ejecutar la conversión
            self.result = convert_nfa_to_dfa(self.current_nfa, step_by_step=True)
        except Exception as ex:
            QMessageBox.critical(self, "Error al convertir a AFD", str(ex))
            self.log_tab.log(f"❌ Error convirtiendo AFN→AFD: {ex}")
            return

        self.current_dfa = self.result.dfa
        self.log_tab.log("✅ Conversión AFN→AFD completada")

        sigma = sorted(self.current_nfa.sigma)
        self.subset_tab.set_steps(
            steps=self.result.steps,
            sigma=sigma,
            finals=self.current_dfa.finals
        )

        self.dfa_tab.set_dfa(self.current_dfa)

        self.rep_tab.set_steps(self.result.steps, self.current_nfa)

        self.rep_tab.set_details(self.current_dfa)

        self.dfa_tab.set_dfa(self.current_dfa)

        self.exp_dfa_action.setEnabled(True)
        self.statusBar().showMessage("AFD listo para revisión y exportación")
        self.tabs.setCurrentWidget(self.dfa_tab)

    def on_export_nfa(self):
        """Exporta el AFN cargado a .jff y confirma al usuario."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar AFN (.jff)", filter="JFLAP Files (*.jff)"
        )
        if not path:
            return
        try:
            export_nfa_to_jff(self.current_nfa, path)

            QMessageBox.information(
                self,
                "Exportación completada",
                f"✅ AFN exportado exitosamente a:\n{path}"
            )
            self.log_tab.log(f"✅ AFN exportado: {path}")
            self.statusBar().showMessage("AFN exportado correctamente", 5000)
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Error en exportación del AFN",
                f"No se pudo exportar el AFN:\n{ex}"
            )
            self.log_tab.log(f"❌ Error exportando AFN: {ex}")
            self.statusBar().showMessage("Error al exportar AFN", 5000)

    def on_export_dfa(self):
        """Exporta el AFD generado a .jff y confirma al usuario."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar AFD (.jff)", filter="JFLAP Files (*.jff)"
        )
        if not path:
            return
        try:
            export_dfa_to_jff(self.current_dfa, path)
            QMessageBox.information(
                self,
                "Exportación completada",
                f"✅ AFD exportado exitosamente a:\n{path}"
            )
            self.log_tab.log(f"✅ AFD exportado: {path}")
            self.statusBar().showMessage("AFD exportado correctamente", 5000)
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Error en exportación del AFD",
                f"No se pudo exportar el AFD:\n{ex}"
            )
            self.log_tab.log(f"❌ Error exportando AFD: {ex}")
            self.statusBar().showMessage("Error al exportar AFD", 5000)

    def on_clear(self):

        # Reset datos internos
        self.current_nfa = None
        self.current_dfa = None
        self.result = None

        # Deshabilitar botones
        self.convert_action.setEnabled(False)
        self.exp_nfa_action.setEnabled(False)
        self.exp_dfa_action.setEnabled(False)

        # Limpiar cada pestaña
        self.nfa_tab.clear()
        self.closure_tab.clear()
        self.subset_tab.clear()
        self.dfa_tab.clear()
        self.rep_tab.clear()
        self.log_tab.clear()
        self.statusBar().showMessage("Estado limpio. Carga un nuevo AFN para comenzar.")

        self.tabs.setCurrentWidget(self.nfa_tab)
