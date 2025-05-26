from typing import Set, Dict, List, Tuple
from .nfa import NFA
from .dfa import DFA

class ConversionResult:

    def __init__(
        self,
        nfa_quint: str,
        afn_table: List[Dict[str, str]],
        dfa: DFA,
        dfa_quint: str,
        dfa_table: List[Dict[str, str]],
        steps: List[Tuple[str, str, str]]
    ):
        self.nfa_quint = nfa_quint
        self.afn_table = afn_table
        self.dfa = dfa
        self.dfa_quint = dfa_quint
        self.dfa_table = dfa_table
        self.steps = steps

def convert_nfa_to_dfa(nfa: NFA, step_by_step: bool = False) -> ConversionResult:

    def closure(states: Set[str]) -> Set[str]:
        result = set()
        for s in states:
            result |= nfa.epsilon_closure(s)
        return result

    start_closure = closure({nfa.q0})
    unmarked: List[Set[str]] = [start_closure]
    marked: List[Set[str]] = []
    dfa_states: List[Set[str]] = []
    transitions: Dict[Tuple[str, str], str] = {}
    steps: List[Tuple[str, str, str]] = []

    sigma = nfa.sigma

    while unmarked:
        T = unmarked.pop(0)
        marked.append(T)
        dfa_states.append(T)
        T_name = ','.join(sorted(T)) or '∅'

        for a in sorted(sigma):
            # movimiento y clausura
            move_set: Set[str] = set()
            for p in T:
                move_set |= nfa.delta.get((p, a), set())
            U = closure(move_set)
            U_name = ','.join(sorted(U)) or '∅'

            transitions[(T_name, a)] = U_name
            if step_by_step:
                steps.append((T_name, a, U_name))

            if U not in marked and U not in unmarked:
                unmarked.append(U)

    # Construir DFA
    state_names = {','.join(sorted(s)) or '∅' for s in dfa_states}
    finals = set(filter(
        lambda name: any(fs in nfa.finals for fs in name.split(',')),
        state_names
    ))
    dfa = DFA(
        states=state_names,
        sigma=sigma,
        delta=transitions,
        q0=','.join(sorted(start_closure)),
        finals=finals
    )

    result = ConversionResult(
        nfa_quint=nfa.quintuple(),
        afn_table=nfa.transition_table(),
        dfa=dfa,
        dfa_quint=dfa.quintuple(),
        dfa_table=dfa.transition_table(),
        steps=steps
    )
    return result