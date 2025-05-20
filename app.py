from flask import Flask, request, render_template, jsonify
from dfa import simulate_dfa, generate_graph
from cfg import cfg, cfg2
from pda import generate_pda_graph

app = Flask(__name__)

# Define the regex strings
binary_regex = "(1+0)(1+0)*(11+00+01+10)*(11+00+01+10)(1010+001+111+000)(1+0)*(101+011+111+010)"
alphabet_regex = "(a+b+aa+bb+aba)(a+b+bb+aa)*(a+b+aa+bb)(a+b)*(ab+ba+bab+aba)(a+b)*)"

def create_cfg_visualization_text(cfg_dict):
    # This function will format the CFG dictionary into a list of strings for display
    cfg_lines = []
    for non_terminal, productions in cfg_dict.items():
        line = f"<strong>{non_terminal} &rarr;</strong> "
        prod_list = []
        for production in productions:
            if production:
                prod_list.append(' '.join(production))
            else:
                prod_list.append('&varepsilon;')
        line += ' | '.join(prod_list)
        cfg_lines.append(line)
    return cfg_lines

@app.route('/', methods=['GET', 'POST'])
def index():
    input_string = request.form.get('input_string', '')
    dfa_type = request.form.get('dfa_type', 'binary')
    graph_svg = result = animation_data = pda_graph = None
    selected_regex = ""
    selected_cfg = None
    cfg_display_lines = []

    # Select CFG and Regex based on dfa_type
    if dfa_type == 'binary':
        selected_regex = binary_regex
        selected_cfg = cfg2
    else: # alphabet
        selected_regex = alphabet_regex
        selected_cfg = cfg
        pda_graph = generate_pda_graph()

    # Format the selected CFG for display
    if selected_cfg:
        cfg_display_lines = create_cfg_visualization_text(selected_cfg)

    if input_string:
        path, visited, accepted = simulate_dfa(input_string, dfa_type)
        graph_svg, animation_data = generate_graph(path, visited, dfa_type)
        result = "Accepted" if accepted else "Rejected"

    return render_template('index.html', 
                         input_string=input_string, 
                         dfa_type=dfa_type,
                         graph_svg=graph_svg, 
                         result=result,
                         animation_data=animation_data,
                         selected_regex=selected_regex,
                         cfg_display_lines=cfg_display_lines,
                         pda_graph=pda_graph)

if __name__ == '__main__':
    app.run(debug=True)