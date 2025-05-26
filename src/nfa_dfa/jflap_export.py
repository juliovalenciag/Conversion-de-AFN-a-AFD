from lxml import etree
import math
from .nfa import NFA
from .dfa import DFA


def _layout_positions(states, width=800, height=600, margin=50):
    """
    Distribuye los estados en un grid dentro de un área width×height,
    dejando un margen alrededor. Retorna dict: estado -> (x,y).
    """
    n = len(states)
    # determinamos columnas y filas
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    # espacio utilizable
    usable_w = width - 2 * margin
    usable_h = height - 2 * margin
    dx = usable_w / (cols - 1) if cols > 1 else 0
    dy = usable_h / (rows - 1) if rows > 1 else 0

    positions = {}
    for idx, q in enumerate(sorted(states)):
        r = idx // cols
        c = idx % cols
        x = margin + c * dx
        y = margin + r * dy
        positions[q] = (x, y)
    return positions


def export_nfa_to_jff(nfa: NFA, path: str) -> None:
    """
    Exporta un NFA a JFLAP (.jff) con layout en rejilla de estados.
    """
    root = etree.Element("structure")
    etree.SubElement(root, "type").text = "fa"
    automaton = etree.SubElement(root, "automaton")

    # calculamos posiciones en grid
    positions = _layout_positions(nfa.states)
    state_ids = {q: idx for idx, q in enumerate(sorted(nfa.states))}

    # Crear estados
    for q, idx in state_ids.items():
        x, y = positions[q]
        s = etree.SubElement(automaton, "state", id=str(idx), name=q)
        etree.SubElement(s, "x").text = f"{x:.1f}"
        etree.SubElement(s, "y").text = f"{y:.1f}"
        if q == nfa.q0:
            etree.SubElement(s, "initial")
        if q in nfa.finals:
            etree.SubElement(s, "final")

    # Transiciones
    for (q, a), dests in nfa.delta.items():
        for dest in dests:
            t = etree.SubElement(automaton, "transition")
            etree.SubElement(t, "from").text = str(state_ids[q])
            etree.SubElement(t, "to").text   = str(state_ids[dest])
            etree.SubElement(t, "read").text = a or ""  # vacío para ε

    tree = etree.ElementTree(root)
    tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def export_dfa_to_jff(dfa: DFA, path: str) -> None:
    """
    Exporta un DFA a JFLAP (.jff) con layout en rejilla de estados.
    """
    root = etree.Element("structure")
    etree.SubElement(root, "type").text = "fa"
    automaton = etree.SubElement(root, "automaton")

    positions = _layout_positions(dfa.states)
    state_ids = {q: idx for idx, q in enumerate(sorted(dfa.states))}

    # Crear estados
    for q, idx in state_ids.items():
        x, y = positions[q]
        s = etree.SubElement(automaton, "state", id=str(idx), name=q)
        etree.SubElement(s, "x").text = f"{x:.1f}"
        etree.SubElement(s, "y").text = f"{y:.1f}"
        if q == dfa.q0:
            etree.SubElement(s, "initial")
        if q in dfa.finals:
            etree.SubElement(s, "final")

    # Transiciones
    for (q, a), dest in dfa.delta.items():
        t = etree.SubElement(automaton, "transition")
        etree.SubElement(t, "from").text = str(state_ids[q])
        etree.SubElement(t, "to").text   = str(state_ids[dest])
        etree.SubElement(t, "read").text = a or ""

    tree = etree.ElementTree(root)
    tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
