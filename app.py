from flask import Flask, request, render_template
from os import environ
import time
import main

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    t_start = time.time()
    if request.method == 'POST':
        players = [request.form.get(f'player{i}') for i in range(1, 11)]
        players = [p for p in players if p]
        if players is None:
            players = ['BeattieW', 'GrekL', 'GrekF', 'QuinlanK', 'GeorgasP', 'ReynenG', 'JainA1933', 'FoxA6', 'MillsH',
                       'ThompsonA5', 'BaechlerC', 'deGrootD', 'JenningsK']

    else:
        # Default behaviour for page load
        players = ['BeattieW', 'GrekL', 'GrekF', 'QuinlanK', 'GeorgasP', 'ReynenG', 'JainA1933', 'FoxA6', 'MillsH',
                   'ThompsonA5', 'BaechlerC', 'deGrootD', 'JenningsK']

    img_base64 = main.main(season=102, matchDay=25, pals=players)

    img_data = f"data:image/png;base64,{img_base64}"
    print(time.time()-t_start)
    return render_template('index.html', img_data=img_data)


if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))  # Use the port from environment variable, default to 5000
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
