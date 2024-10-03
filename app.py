from flask import Flask, request, render_template
import main

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        players = [request.form.get(f'player{i}') for i in range(1, 11)]
        players = [p for p in players if p]
        if players is None:
            return "Error: No Input Provided", 400
        else:
            print(f'Received input: {players}')
        img_base64 = main.main(season=102, matchDay=25, pals=players)

        img_data = f"data:image/png;base64,{img_base64}"
        print(f'Length of Input IMG_data: {len(img_data)}')

        return render_template('index.html', img_data=img_data)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
