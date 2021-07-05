import collections
from typing import Dict, List, Union

from utils import string_to_letters, EPSILON, concat_regex, add_regex

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

    def get_edges_by_label(self, edge_key: str, include_epsilon_edges=False) -> List['Edge']:
        epsilon_edges = []

        if edge_key is not EPSILON and include_epsilon_edges:
            epsilon_nodes = [e.n2 for e in self.get_edges_by_label(EPSILON)]

            for node in epsilon_nodes:
                epsilon_edges += node.get_edges_by_label(edge_key)

        return [e for e in self.edges if e.label == edge_key] + epsilon_edges

    def get_edges_by_node(self, node_key: str) -> List['Edge']:
        return [e for e in self.edges if e.n2.id == node_key]

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
            state.label: [[e.n2.label for e in state.get_edges_by_label(w)] for w in self.words + [EPSILON]]
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
        epsilon_nodes = state.get_edges_by_label(EPSILON)
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
            epsilon_edges = state.get_edges_by_label(EPSILON)

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
        return f'digraph {{' \
               f'{sep}graph [rankdir=LR];' \
               f'{sep}node [shape=point,label=""]ENTRY;' \
               f'{sep}node [shape=circle];' \
               f'{sep}{sep.join(states)}' \
               f'{sep}{sep.join(edges)}' \
               f'{sep[0]}}}'

    def get_input_edges(self, state_key: str):
        edges = []

        for state in self.states:
            for state_edges in state.edges:
                if state_edges.n2.id == state_key:
                    edges.append(state_edges)

        return edges

    def eliminate_state(self):
        # separate the finish node if we have multiple finish nodes
        if len(self.finish_states) > 1:
            out_state = Node('z')

            for state in self.finish_states:
                state.edges.append(Edge(state, out_state, EPSILON))

            self.states.append(out_state)
            self.finish_states = [out_state]
            return 'Separated finish states'

        # group edges if start and end node are same
        join_count = 0
        for state in self.states:
            end_node_keys = [e.n2.id for e in state.edges]
            duplicate_edges = [item for item, count in collections.Counter(end_node_keys).items() if count > 1]

            for key in duplicate_edges:
                labels = set()
                edges = state.get_edges_by_node(key)
                n2 = edges[0].n2

                for e in edges:
                    labels.add(e.label)
                    state.edges.remove(e)

                state.edges.append(Edge(state, n2, add_regex(*labels)))
                join_count += 1

        if join_count:
            return f'Joined common edges'

        # eliminate nodes
        for state in list(self.states):
            if self.is_finish_state(state) or state == self.start_state:
                continue

            # handle edges to self
            self_loop = ''
            self_edges = state.get_edges_by_node(state.id)
            if len(self_edges) > 0:
                self_loop = f'({self_edges[0].label})*'
                state.edges.remove(self_edges[0])
                print(f'removed self edge {self_edges[0]}')

            # rewire all the input and output edges
            input_edges = self.get_input_edges(state.label)
            for input_edge in input_edges:
                n1 = input_edge.n1
                l1 = input_edge.label

                for output_edge in state.edges:
                    l2 = output_edge.label
                    n2 = output_edge.n2
                    print(input_edge, output_edge, concat_regex(l1, self_loop, l2))
                    n1.edges.append(Edge(n1, n2, concat_regex(l1, self_loop, l2)))

                n1.edges.remove(input_edge)

            self.states.remove(state)
            return f'removed state {state}'

    def to_dfa(self):
        transition_table = {}
        stack = [[self.start_state]]

        while stack:
            states = stack.pop()
            tt_row = []

            for word in self.words:
                next_states_edges = sum([s.get_edges_by_label(word) for s in states], [])
                next_states = [nse.n2 for nse in next_states_edges]
                next_state_ids = [s.id for s in next_states]
                next_state_id = ''.join(next_state_ids)

                if next_state_id not in transition_table and len(next_state_id) > 0:
                    stack.append(next_states)

                tt_row.append(next_state_ids)

            transition_table[''.join([str(s) for s in states])] = tt_row

        return self.words, transition_table, self.start_state.id, [fs.id for fs in self.finish_states]

    def remove_hanging_node(self):
        stack = [self.start_state]
        visited = []

        while stack:
            state = stack.pop()
            visited.append(state)

            stack.extend([e.n2 for e in state.edges if e.n2 not in visited])

        to_delete = [s for s in self.states if s not in visited]
        print(', '.join([str(s) for s in to_delete]))
        for state in to_delete:
            self.states.remove(state)


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
