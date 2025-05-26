from lxml import etree
from typing import Set, Dict, Tuple
from src.nfa_dfa.nfa import NFA


def parse_nfa_from_jff(path: str) -> NFA:
    """
    Parsea un archivo JFLAP (.jff) y devuelve un objeto NFA.
    Valida estructura y reporta errores precisos.
    """
    try:
        tree = etree.parse(path)
    except (etree.XMLSyntaxError, OSError) as e:
        raise ValueError(f"Error al abrir o parsear JFLAP file: {e}")

    root = tree.getroot()
    automaton = root.find('.//automaton')
    if automaton is None:
        raise ValueError("No se encontró el elemento <automaton> en el JFLAP file")

    states: Set[str] = set()
    finals: Set[str] = set()
    initial_state: str = None
    state_id_map: Dict[str, str] = {}

    # Leer estados
    for state in automaton.findall('state'):
        sid = state.get('id')
        name = state.get('name')
        if sid is None or name is None:
            raise ValueError(f"Estado mal formado: {etree.tostring(state)}")
        state_id_map[sid] = name
        states.add(name)
        if state.find('initial') is not None:
            if initial_state is not None:
                raise ValueError("Múltiples estados iniciales detectados")
            initial_state = name
        if state.find('final') is not None:
            finals.add(name)

    if initial_state is None:
        raise ValueError('No se encontró estado inicial en el JFLAP file')

    # Leer transiciones
    delta: Dict[Tuple[str, str], Set[str]] = {}
    sigma: Set[str] = set()

    for trans in automaton.findall('transition'):
        src_id = trans.findtext('from')
        dst_id = trans.findtext('to')
        sym = trans.findtext('read') or ''
        if src_id not in state_id_map or dst_id not in state_id_map:
            raise ValueError(f"Transición con referencia de estado desconocido: {src_id}->{dst_id}")
        src = state_id_map[src_id]
        dst = state_id_map[dst_id]

        if sym:
            sigma.add(sym)
        key = (src, sym)
        delta.setdefault(key, set()).add(dst)

    return NFA(states=states, sigma=sigma, delta=delta, q0=initial_state, finals=finals)
