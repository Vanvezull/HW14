import main
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    return app


app = create_app()

data = main.Data("../netflix.db")


@app.route('/movie/<title>')
def search_by_title(title):
    result = data.search_by_title(title)
    return result


@app.route('/movie/rating/<rating>')
def search_by_rating(rating):
    return jsonify(data.search_by_rating(rating))


@app.route('/movie/<year1>/to/<year2>')
def search_by_years(year1, year2):
    result = data.search_by_years(year1, year2)
    return jsonify(result)


@app.route('/movie/genre/<genre>')
def search_by_genre(genre):
    result = data.search_by_genre(genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
