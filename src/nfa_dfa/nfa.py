from typing import Set, Dict, List, Tuple

class NFA:
    """
        Clase para representar un autómata finito no determinista (AFN).
        Atributos:
            states: Conjunto de nombres de estados.
            sigma: Alfabeto del autómata (sin incluir \u03B5).
            delta: Función de transición: dict[(estado, simbolo)] -> set(estados).
            q0: Estado inicial.
            finals: Conjunto de estados finales.
    """

    def __init__(self, states: Set[str], sigma: Set[str], delta: Dict[Tuple[str, str], Set[str]], q0: str, finals:Set[str]):
        self.states = states
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.finals = finals

    def epsilon_closure(self, state: str) -> Set[str]:
        """
            Calcula la clausura epsilon de un estado.
        """
        stack = [state]
        closure = {state}
        while stack:
            s = stack.pop()
            for t in self.delta.get(( s, '' ), set()):
                if t not in closure:
                    closure.add(t)
                    stack.append(t)
        return closure

    def epsilon_closures(self) -> Dict[str, Set[str]]:
        """
            Calcula la clausura epsilon de cada estado.
        """
        return {s: self.epsilon_closure(s) for s in self.states}

    def quintuple(self) -> str:
        """
            Devuelve la representación en texto de la quíntupla M = (Q, Sigma, delta, q0, F).
        """
        Q = '{' + ', '.join(sorted(self.states)) + '}'
        Sigma = '{' + ', '.join(sorted(self.sigma)) + '}'
        delta_str = '{ ' + ', '.join(
            f"delta({q}, '{a}') = {{{', '.join(sorted(self.delta.get((q, a), [])))}}}"
            for q in sorted(self.states) for a in list(self.sigma) + ['']
        ) + ' }'
        F = '{' + ', '.join(sorted(self.finals)) + '}'
        return f"M = ({Q}, {Sigma} ∪ {{ε}}, delta, {self.q0}, {F})\n{delta_str}"

    def transition_table(self) -> List[Dict[str, str]]:
        """
            Construye una tabla de transiciones en formato lista de diccionarios,
            donde cada diccionario representa un estado y sus movimientos.
            Las claves son 'state', luego cada simbolo en sigma y '' para epsilon.
        """
        table = []
        headers = ['state'] + sorted(self.sigma) + ['']
        for q in sorted(self.states):
            row = {'state': q}
            for a in sorted(self.sigma):
                row[a] = ','.join(sorted(self.delta.get((q, a), set())))
            # epsilon
            row[''] = ','.join(sorted(self.delta.get((q, ''), set())))
            table.append(row)
        return table

