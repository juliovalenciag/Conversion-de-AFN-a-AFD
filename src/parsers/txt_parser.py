import re
from typing import List, Set, Dict, Tuple
from src.nfa_dfa.nfa import NFA

def parse_nfa_from_txt(path: str) -> NFA:
    """
    Parsea un AFN desde un .txt (etiquetado o crudo) y retorna un objeto NFA.
    Ahora separa siempre por comas los destinos, con o sin llaves.
    """
    def _parse_dests(tok: str) -> List[str]:
        # tok puede ser "A,B", "{A,B}" o "C"
        tok = tok.strip()
        if tok.startswith('{') and tok.endswith('}'):
            core = tok[1:-1]
        else:
            core = tok
        return [d.strip() for d in core.split(',') if d.strip()]

    with open(path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    has_labels = any(line.lower().startswith('estados') for line in lines)

    delta: Dict[Tuple[str, str], Set[str]] = {}
    states: List[str] = []
    sigma: List[str] = []
    q0: str = None
    finals: Set[str] = set()

    if has_labels:
        # — Formato etiquetado —
        for line in lines:
            low = line.lower()
            if low.startswith('estados'):
                parts = re.split(r'[:\s]+', line, maxsplit=1)[1]
                states = [s.strip() for s in parts.split(',') if s.strip()]
            elif low.startswith('alfabeto'):
                parts = line.split(':', 1)[1]
                sigma = [s.strip() for s in parts.split(',') if s.strip()]
            elif low.startswith('inicial'):
                q0 = line.split(':', 1)[1].strip()
            elif low.startswith('finales'):
                parts = line.split(':', 1)[1]
                finals = set(s.strip() for s in parts.split(',') if s.strip())
            elif low.startswith('transiciones'):
                start = lines.index(line) + 1
                raw = lines[start:]
                break
        else:
            raise ValueError('Sección "Transiciones:" no encontrada')

        syms = sigma + ['']
        for row in raw:
            if ':' not in row:
                continue
            src, rest = row.split(':', 1)
            src = src.strip()
            toks = re.split(r'\s+', rest.strip())
            toks = ['' if t in ('-', '–', '—') else t for t in toks]
            for sym, tok in zip(syms, toks):
                if not tok:
                    continue
                for d in _parse_dests(tok):
                    delta.setdefault((src, sym), set()).add(d)

    else:
        # — Formato crudo —
        if len(lines) < 5:
            raise ValueError('Formato crudo inválido: se requieren al menos 5 líneas')
        states = lines[0].split()
        q0     = lines[1].strip()
        finals = set(lines[2].split())
        sigma  = lines[3].split()
        raw    = lines[4:]
        if len(raw) != len(states):
            raise ValueError(f'Se esperaban {len(states)} filas de transiciones, hay {len(raw)}')

        syms = sigma + ['']
        for src, row in zip(states, raw):
            toks = re.split(r'\s+', row.strip())
            toks = ['' if t in ('-', '–', '—') else t for t in toks]
            for sym, tok in zip(syms, toks):
                if not tok:
                    continue
                for d in _parse_dests(tok):
                    delta.setdefault((src, sym), set()).add(d)

    # — Validaciones finales —
    if not states:
        raise ValueError('No se encontraron estados válidos')
    if q0 is None:
        raise ValueError('No se encontró estado inicial')
    unknown_finals = set(finals) - set(states)
    if unknown_finals:
        raise ValueError(f'Estados finales desconocidos: {unknown_finals}')

    sigma_set = set(sigma)
    for (s, sym), dests in list(delta.items()):
        if s not in states:
            raise ValueError(f'Transición desde estado desconocido: {s}')
        if sym and sym not in sigma_set:
            raise ValueError(f'Símbolo desconocido en transiciones: {sym}')
        for d in dests:
            if d not in states:
                raise ValueError(f'Transición hacia estado desconocido: {d}')

    nfa = NFA(states=set(states), sigma=sigma_set, delta=delta, q0=q0, finals=finals)
    nfa.source_path = path
    return nfa
