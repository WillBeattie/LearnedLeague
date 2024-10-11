import base64

from flask import Flask, request, render_template, redirect, url_for
from markupsafe import escape
from os import environ
import time
import main

app = Flask(__name__)
N_PLAYERS = 12

@app.route('/', methods=['GET', 'POST'])
@app.route('/<user_input>', methods=['GET','POST'])
def index(user_input=None):
    user_agent = request.headers.get('User-Agent')

    # Ignore health check requests from Render
    if user_agent == 'Go-http-client/1.1':
        return '', 204  # Respond with 204 No Content to indicate success without logging

    print(request.method)
    t_start = time.time()
    if user_input and request.method=='GET':
        safe_input = escape(user_input)
        players = safe_input.split(';')
        img_base64 = main.main(season=102, matchDay=25, pals=players)

    elif request.method == 'POST':
        players = [request.form.get(f'player{i}') for i in range(1, N_PLAYERS + 1)]
        players = [p for p in players if p]
        print(players)
        if players is None:
            players = [''] * N_PLAYERS
            with open('res/Default.png', 'rb') as img:
                img_base64 = base64.b64encode(img.read()).decode('utf-8')

        else:
            players_url = ';'.join(players)
            return redirect(url_for('index', user_input = escape(players_url)))
            # img_base64 = main.main(season=102, matchDay=25, pals=players)

    else:
        players = ['']*N_PLAYERS
        with open('res/Default.png', 'rb') as img:
            img_base64 = base64.b64encode(img.read()).decode('utf-8')

    img_data = f"data:image/png;base64,{img_base64}"
    print(time.time() - t_start)
    players = players + [''] * (N_PLAYERS - len(players))  # Make sure we have 12 items for pre-populating input fields
    return render_template('index.html', img_data=img_data, input_values=players)


if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))  # Use the port from environment variable, default to 5000
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
