import graphviz

# Binary DFA (0/1)
binary_dfa = {
    's1': {'1': 's2', '0': 's2'},
    's2': {'1': 's3', '0': 's4'},
    's3': {'1': 's5', '0': 's6'},
    's4': {'1': 's5', '0': 's6'},
    's5': {'1': 's8', '0': 's7'},
    's6': {'1': 's8', '0': 's11'},
    's7': {'1': None, '0': 's11'},
    's8': {'1': 's10', '0': 's9'},
    's9': {'1': 's12', '0': 's13'},
    's10': {'1': 's13', '0': 's12'},
    's11': {'1': 's15', '0': 's17'},
    's12': {'1': 's14', '0': 's14'},
    's13': {'1': 's16', '0': 's17'},
    's14': {'1': 's19', '0': 's16'},
    's15': {'1': 's22', '0': 's23'},
    's16': {'1': 's20', '0': 's21'},
    's17': {'1': 's21', '0': 's16'},
    's18': {'1': 's22', '0': 's17'},
    's19': {'1': 's25', '0': 's25'},
    's20': {'1': 's26', '0': 's27'},
    's21': {'1': 's26', '0': 's27'},
    's22': {'1': 's21', '0': 's24'},
    's23': {'1': 's28', '0': 's11'},
    's24': {'1': 's27', '0': 's22'},
    's25': {'1': 's26', '0': 's26'},
    's26': {'1': 's27', '0': 's21'},
    's27': {'1': 's26', '0': 's25'},
    's28': {'1': 's22', '0': 's27'},   
}

# Alphabet DFA (a/b)
alphabet_dfa = {
    's1': {'a': 's2', 'b': 's3'},
    's2': {'a': 's5', 'b': 's4'},
    's3': {'a': None, 'b': 's5'},
    's4': {'a': 's5', 'b': None},
    's5': {'a': 's6', 'b': 's7'},
    's6': {'a': 's5', 'b': 's8'},
    's7': {'a': 's8', 'b': 's5'},
    's8': {'a': 's9', 'b': 's10'},
    's9': {'a': 's12', 'b': 's13'},
    's10': {'a': 's11', 'b': 's13'},
    's11': {'a': 's5', 'b': 's14'},
    's12': {'a': 's12', 'b': 's12'},
    's13': {'a': 's12', 'b': 's12'},
    's14': {'a': 's13', 'b': 's13'}
}

# DFA configurations
dfa_configs = {
    'binary': {
        'transitions': binary_dfa,
        'start_state': 's1',
        'accept_states': {'s26', 's27'},
        'valid_symbols': {'0', '1'}
    },
    'alphabet': {
        'transitions': alphabet_dfa,
        'start_state': 's1',
        'accept_states': {'s12', 's13', 's14'},
        'valid_symbols': {'a', 'b'}
    }
}

def simulate_dfa(input_string, dfa_type='binary'):
    config = dfa_configs[dfa_type]
    current_state = config['start_state']
    visited = {current_state}
    path = []

    for symbol in input_string:
        if symbol not in config['valid_symbols']:
            break
        next_state = config['transitions'].get(current_state, {}).get(symbol)
        if not next_state:
            break
        path.append((current_state, next_state, symbol))
        visited.add(next_state)
        current_state = next_state

    accepted = current_state in config['accept_states']
    return path, visited, accepted

def generate_graph(path, visited, dfa_type='binary'):
    config = dfa_configs[dfa_type]
    dot = graphviz.Digraph(format='svg')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle', style='filled', fontname='Arial')
    dot.attr('edge', fontname='Arial')

    # Add nodes
    for state in config['transitions']:
        attrs = {
            'style': 'filled',
            'fillcolor': '#f8f9fa',
            'fontsize': '12',
            'width': '0.6',
            'height': '0.6',
            'id': f'node_{state}'
        }
        
        if state in config['accept_states']:
            attrs['shape'] = 'doublecircle'
            attrs['fillcolor'] = '#d4edda'
        if state in visited:
            attrs['color'] = '#007bff'
            attrs['penwidth'] = '2'
        dot.node(state, **attrs)

    # Add start arrow
    dot.node('start', shape='point', width='0.1', height='0.1')
    dot.edge('start', config['start_state'], arrowhead='normal', arrowsize='0.5')

    # Add transitions with IDs for animation
    for from_state, transitions in config['transitions'].items():
        for symbol, to_state in transitions.items():
            if to_state:
                is_in_path = any(p[0] == from_state and p[1] == to_state and p[2] == symbol for p in path)
                attrs = {
                    'label': symbol,
                    'fontsize': '10',
                    'arrowsize': '0.5',
                    'id': f'edge_{from_state}_{to_state}_{symbol}'
                }
                if is_in_path:
                    attrs['color'] = '#007bff'
                    attrs['penwidth'] = '2'
                dot.edge(from_state, to_state, **attrs)

    # Add animation information
    animation_data = {
        'path': path,
        'start_state': config['start_state'],
        'accept_states': list(config['accept_states'])
    }

    return dot.pipe().decode('utf-8'), animation_data