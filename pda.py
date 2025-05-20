from graphviz import Digraph

def generate_pda_graph():
    # Initialize directed graph
    dot = Digraph(format='svg')
    dot.attr(rankdir='TB')  # Top to bottom layout

    # Define nodes
    states = {
        'start', 'read1', 'read2', 'read3', 'read4', 'read5', 'read6', 'read7',
        'read8', 'read9', 'read10', 'read11', 'read12', 'end'
    }

    # Accepting/final states
    final_states = {'end'}

    # Add all nodes, marking final ones with doublecircle
    for state in states:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        elif state == 'start':
            dot.node(state, shape='ellipse')
        else:
            dot.node(state, shape='diamond')

    # Transition edges: (source, destination, label)
    transitions = [
        ('start', 'read1', ''),
        ('read1', 'read2', 'b'),
        ('read1', 'read3', 'a'),
        ('read2', 'read4', 'a'),
        ('read2', 'read4', 'b'),
        ('read3', 'read2', 'b'),
        ('read3', 'read4', 'a'),
        ('read4', 'read5', 'b'),
        ('read4', 'read6', 'a'),
        ('read5', 'read7', 'a'),
        ('read6', 'read7', 'b'),
        ('read7', 'read8', 'a'),
        ('read7', 'read9', 'b'),
        ('read8', 'end', 'a'),
        ('read9', 'read10', 'a'),
        ('read9', 'read12', 'b'),
        ('read10', 'read11', 'b'),
        ('read11', 'end', 'null'),
        ('read12', 'end', 'null'),
    ]

    # Add edges
    for src, dst, label in transitions:
        dot.edge(src, dst, label=label)

    return dot.pipe().decode('utf-8')
