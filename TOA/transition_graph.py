from typing import Dict, List, Union

from utils import string_to_letters


EPSILON = 'λ'

"""
1. REGEX to TG
2. NFA to DFA
3. Moore, mealy machine
4. Moore to mealy
"""


class Node:
    def __init__(self, label: str, edges: List['Edge'] = (), output=None):
        self.label = label
        self.output = output
        self.edges = edges

    def get_edges(self, edge_key: str) -> List['Edge']:
        return [e for e in self.edges if e.label == edge_key]

    @property
    def id(self):
        return self.label

    def __str__(self):
        return self.id


class Edge:
    def __init__(self, n1: Node, n2: Node, label: str, output=None):
        self.n1 = n1
        self.n2 = n2
        self.label = label
        self.output = output

    def __str__(self):
        return f'{self.n1}-({self.label})->{self.n2}'


class TransitionGraph:
    def __init__(self, states: List[Node], start_state: Node, finish_states: List[Node], words: List[str]):
        self.states = states
        self.start_state = start_state
        self.finish_states = finish_states
        self.words = words

    def clone(self):
        return TransitionGraph.from_transition_table(*self.to_transition_table())

    def to_transition_table(self):
        words = list(self.words)
        start_node = self.start_state.label
        finish_nodes = [s.label for s in self.finish_states]
        table = {
            state.label: [[e.n2.label for e in state.get_edges(w)] for w in self.words + [EPSILON]]
            for state in self.states
        }

        return [words, table, start_node, finish_nodes]

    @classmethod
    def from_transition_table(
        cls,
        words: List[str],
        table: Dict[str, List[Union[str, List[str]]]],
        start_node: str,
        finish_nodes: Union[str, List[str]]
    ) -> 'TransitionGraph':
        finish_nodes = [finish_nodes] if type(finish_nodes) is str else finish_nodes

        nodes: Dict[str, Node] = {}
        start_state = None

        def get_or_add_node(s: str):
            n = nodes[s] if s in nodes else Node(s)
            if s not in nodes:
                nodes[s] = n
            return n

        for state, next_states in table.items():
            node = get_or_add_node(state)

            if start_node == state:
                start_state = node

            edges = []
            for i, next_state in enumerate(next_states):
                if next_state is None:
                    continue

                label = EPSILON if i >= len(words) else words[i]
                if type(next_state) is str:
                    next_node = get_or_add_node(next_state)
                    edges.append(Edge(node, next_node, label))
                    continue

                for ns in next_state:
                    next_node = get_or_add_node(ns)
                    edges.append(Edge(node, next_node, label))

            node.edges = edges

        finish_states = [n for n in nodes.values() if n.label in finish_nodes]
        return cls(list(nodes.values()), start_state, finish_states, words)

    def is_finish_state(self, state: Node):
        epsilon_nodes = state.get_edges(EPSILON)
        is_finished = state in self.finish_states

        if len(epsilon_nodes) > 0 and not is_finished:
            is_finished = len([es for es in epsilon_nodes if es in self.finish_states]) > 0

        return is_finished

    def evaluate(self, string):
        letters = string_to_letters(string, self.words)
        if len(letters) == 0 and len(string) != 0:
            raise ValueError(
                f'Invalid String "{string}" for language of words ({", ".join(self.words)})')

        stack = [(self.start_state, 0)]

        while stack:
            state, pos = stack.pop()
            epsilon_edges = state.get_edges(EPSILON)

            for ee in epsilon_edges:
                stack.append((ee.n2, pos))

            if pos >= len(letters):
                if len(stack) == 0 or self.is_finish_state(state):
                    return [self.is_finish_state(state), state.label, pos]
                continue

            for edge in state.edges:
                if edge.label == letters[pos]:
                    stack.append((edge.n2, pos + 1))

        return [False, None, None]

    def to_dot_diagram(self):
        states = []
        edges = []

        for state in self.states:
            states.append(f'{state.id}[label="{state.label}"];')

            if state == self.start_state:
                edges.append(f'ENTRY->{state.id};')

            if state in self.finish_states:
                states.append(f'{state.id}[label="{state.label}",peripheries=2];')
            else:
                states.append(f'{state.id}[label="{state.label}"];')

            for edge in state.edges:
                edges.append(f'{edge.n1.id}->{edge.n2.id} [label="{edge.label}"];')

        sep = "\n    "
        return f'digraph {{'\
            f'{sep}graph [rankdir=LR];'\
            f'{sep}node [shape=point,label=""]ENTRY;'\
            f'{sep}node [shape=circle];'\
            f'{sep}{sep.join(states)}'\
            f'{sep}{sep.join(edges)}'\
            f'{sep[0]}}}'

    def get_input_edges(self, state_key: str):
        edges = []

        for state in self.states:
            for state_edges in state.edges:
                if state_edges.n2.id == state_key:
                    edges.append(state_edges)

        return edges

    def eliminate_state(self):
        tg = self.clone()

        if len(tg.finish_states) > 1:
            out_state = Node('z')

            for state in tg.finish_states:
                state.edges.append(Edge(state, out_state, EPSILON))

            tg.states.append(out_state)
            tg.finish_states = [out_state]
            return tg

        for state in [*tg.states]:
            input_edges = tg.get_input_edges(state.label)
            print(state.label, len(state.edges), len(input_edges))

            if len(state.edges) == 1 and len(input_edges) == 1:
                l1 = input_edges[0].label
                l2 = state.edges[0].label

                n1 = input_edges[0].n1
                n2 = state.edges[0].n2

                n1.edges.remove(input_edges[0])
                n1.edges.append(Edge(n1, n2, l1 + l2))

                print(n1, n1.edges)
                tg.states.remove(state)
                return tg


if __name__ == '__main__':
    tg = TransitionGraph.from_transition_table(['a', 'b'], {
        'q0': [None, None, ['q1', 'q2']],
        'q1': ['q3', None],
        'q2': ['q4', None],
        'q3': [None, 'q1'],
        'q4': [None, 'q5'],
        'q5': ['q2', None]
    }, start_node='q0', finish_nodes=['q1', 'q2'])

    # print(tg.to_dot_diagram())
    # print(tg.evaluate('ab'))
    tg.eliminate_state()\
        .eliminate_state()\
        .eliminate_state()
