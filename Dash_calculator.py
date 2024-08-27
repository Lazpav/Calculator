from flask import Flask, render_template_string
from dash import dcc, html, Input, Output, State
import time
import webview
import dash
import threading
import socket


# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app and integrate with Flask
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# Define the layout of the Dash app with custom styling
app.layout = html.Div([
    html.H1("Programmer's Calculator", style={
        'textAlign': 'center', 
        'color': '#ffffff',
        'fontFamily': 'Arial',
        'backgroundColor': '#2c3e50',
        'padding': '20px',
        'borderRadius': '8px'
    }),
    
    html.Div([
        dcc.Input(
            id='display', 
            type='text', 
            value='', 
            style={
                'width': '93%', 
                'height': '70px', 
                'fontSize': '36px', 
                'textAlign': 'right', 
                'padding': '10px',
                'borderRadius': '8px',
                'border': '2px solid #3498db',
                'backgroundColor': '#ecf0f1',
                'color': '#2c3e50'
            }
        )
    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'margin-bottom': '20px'
    }),

    html.Div([
        html.Button('7', id='btn-7', className='button'),
        html.Button('8', id='btn-8', className='button'),
        html.Button('9', id='btn-9', className='button'),
        html.Button('/', id='btn-divide', className='button operator'),
        html.Button('Bin', id='btn-bin', className='button base'),
    ], className='button-row'),
    
    html.Div([
        html.Button('4', id='btn-4', className='button'),
        html.Button('5', id='btn-5', className='button'),
        html.Button('6', id='btn-6', className='button'),
        html.Button('*', id='btn-multiply', className='button operator'),
        html.Button('Oct', id='btn-oct', className='button base'),
    ], className='button-row'),
    
    html.Div([
        html.Button('1', id='btn-1', className='button'),
        html.Button('2', id='btn-2', className='button'),
        html.Button('3', id='btn-3', className='button'),
        html.Button('-', id='btn-subtract', className='button operator'),
        html.Button('Hex', id='btn-hex', className='button base'),
    ], className='button-row'),
    
    html.Div([
        html.Button('0', id='btn-0', className='button'),
        html.Button('C', id='btn-clear', className='button clear'),
        html.Button('=', id='btn-equals', className='button equals'),
        html.Button('+', id='btn-add', className='button operator'),
        html.Button('Dec', id='btn-dec', className='button base'),
    ], className='button-row'),
], style={
    'width': '400px',
    'margin': 'auto',
    'backgroundColor': '#34495e',
    'padding': '20px',
    'borderRadius': '8px',
    'boxShadow': '0px 0px 10px #2c3e50',
    'position': 'absolute',
    'top': '50%',
    'left': '50%',
    'transform': 'translate(-50%, -50%)'
})

# Define the callback to handle button clicks
@app.callback(
    Output('display', 'value'),
    [Input(f'btn-{i}', 'n_clicks') for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']] +
    [Input('btn-add', 'n_clicks'), Input('btn-subtract', 'n_clicks'), Input('btn-multiply', 'n_clicks'), Input('btn-divide', 'n_clicks'),
     Input('btn-equals', 'n_clicks'), Input('btn-clear', 'n_clicks'),
     Input('btn-bin', 'n_clicks'), Input('btn-oct', 'n_clicks'), Input('btn-hex', 'n_clicks'), Input('btn-dec', 'n_clicks')],
    [State('display', 'value')]
)
def update_display(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-clear':
        return ''
    
    if button_id == 'btn-equals':
        try:
            return str(eval(args[-1]))
        except:
            return 'Error'
    
    if button_id == 'btn-bin':
        try:
            return bin(int(args[-1]))[2:]  # Convert to binary and strip the '0b' prefix
        except:
            return 'Error'

    if button_id == 'btn-oct':
        try:
            return oct(int(args[-1]))[2:]  # Convert to octal and strip the '0o' prefix
        except:
            return 'Error'

    if button_id == 'btn-hex':
        try:
            return hex(int(args[-1]))[2:].upper()  # Convert to hexadecimal and strip the '0x' prefix
        except:
            return 'Error'

    if button_id == 'btn-dec':
        try:
            return str(int(args[-1], 0))  # Convert to decimal
        except:
            return 'Error'
    
    button_map = {
        'btn-0': '0', 'btn-1': '1', 'btn-2': '2', 'btn-3': '3', 'btn-4': '4',
        'btn-5': '5', 'btn-6': '6', 'btn-7': '7', 'btn-8': '8', 'btn-9': '9',
        'btn-add': '+', 'btn-subtract': '-', 'btn-multiply': '*', 'btn-divide': '/'
    }
    
    return args[-1] + button_map.get(button_id, '')

# Add custom CSS styling directly in the app
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
})

# Custom CSS styling for buttons
app.index_string += '''
<style>
body {
    background-color: #000000;
    margin: 0;
    padding: 0;
    height: 100%;
    font-family: Arial, sans-serif;
}

.button {
    width: 19%;
    height: 60px;
    font-size: 18px;
    border-radius: 8px;
    margin: 5px;
    background-color: #ecf0f1;
    color: #2c3e50;
    border: 2px solid #3498db;
    transition: background-color 0.3s, color 0.3s;
}
.button:hover {
    background-color: #3498db;
    color: #ffffff;
}
.button.operator {
    background-color: #f39c12;
    color: #ffffff;
}
.button.operator:hover {
    background-color: #e67e22;
    color: #ffffff;
}
.button.clear {
    background-color: #e74c3c;
    color: #ffffff;
}
.button.clear:hover {
    background-color: #c0392b;
    color: #ffffff;
}
.button.equals {
    background-color: #2ecc71;
    color: #ffffff;
}
.button.equals:hover {
    background-color: #27ae60;
    color: #ffffff;
}
.button.base {
    background-color: #9b59b6;
    color: #ffffff;
}
.button.base:hover {
    background-color: #8e44ad;
    color: #ffffff;
}
.button-row {
    display: flex;
    justify-content: space-between;
}
</style>
'''

# Define a simple route for the Flask app
@server.route('/')
def index():
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <title>Calculator App</title>
    <meta charset="UTF-8">
</head>
<body>
    <iframe src="/dash" width="100%" height="100%" style="border:none;"></iframe>
</body>
</html>''')

def run_flask():
    server.run(port=8050)

def check_server():
    """Check if the Flask server is up and running."""
    while True:
        try:
            # Try to create a connection to the server
            with socket.create_connection(("127.0.0.1", 8050), timeout=1):
                return True
        except OSError:
            time.sleep(1)  # Wait a bit before trying again

def run_webview():
    check_server()  # Wait until the server is running
    window = webview.create_window('Calculator App', 'http://127.0.0.1:8050')
    webview.start()

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Start webview in the main thread
    run_webview()
    
    flask_thread.join()





