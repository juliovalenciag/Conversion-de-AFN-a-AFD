from typing import Set, Dict, List, Tuple

class DFA:
    """
    Autómata finito determinista.
    states: set de nombres de estado (strings)
    sigma:  set de símbolos del alfabeto (strings)
    delta:  dict[(estado, símbolo)] -> estado de destino
    q0:     estado inicial (string)
    finals: set de estados finales (strings)
    """
    def __init__(
        self,
        states: Set[str],
        sigma: Set[str],
        delta: Dict[Tuple[str, str], str],
        q0: str,
        finals: Set[str]
    ):
        self.states = states
        self.sigma  = sigma
        self.delta  = delta
        self.q0     = q0
        self.finals = finals

    def quintuple(self) -> str:
        """Devuelve M = (Q, Σ, δ, q₀, F) más la lista de δ en texto."""
        Q     = "{" + ", ".join(sorted(self.states)) + "}"
        Σ     = "{" + ", ".join(sorted(self.sigma)) + "}"
        F     = "{" + ", ".join(sorted(self.finals)) + "}"

        # Construir lista de transiciones con ∅ cuando no hay destino
        parts = []
        for q in sorted(self.states):
            for a in sorted(self.sigma):
                dest = self.delta.get((q, a), "")
                dest = dest if dest else "∅"
                parts.append(f"δ({q}, {a}) = {dest}")

        delta_str = "{ " + ", ".join(parts) + " }"
        return f"M = ({Q}, {Σ}, δ, {self.q0}, {F})\n{delta_str}"

    def transition_table(self) -> List[Dict[str, str]]:
        """
        Devuelve una lista de filas, donde cada fila es:
          {'state': q, 'a': destino_o_∅, 'b': ..., ...}
        """
        table: List[Dict[str, str]] = []
        for q in sorted(self.states):
            row = {'state': q}
            for a in sorted(self.sigma):
                dest = self.delta.get((q, a), "")
                row[a] = dest if dest else "∅"
            table.append(row)
        return table
