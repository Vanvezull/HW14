import json
import sqlite3


class Data:
    def __init__(self, path):
        self.path = path

    def connection(self):
        """
        Подключение к базе и создание курсора
        :return:
        """
        with sqlite3.connect("netflix.db") as connection:
            cursor = connection.cursor()
        return cursor

    def search_by_title(self, title):
        """
        Производим поиск по названию фильма и выводим словарем данные о нём
        :param title:
        :return:
        """
        cursor = self.connection()

        query = """
                SELECT `title`, `country`, `release_year`, `listed_in`, `description` 
                FROM netflix
                WHERE title = ?
                ORDER BY release_year DESC
                LIMIT 1
                """
        cursor.execute(query, (title,))
        result = cursor.fetchall()

        movie_title = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "listed_in": result[0][3],
            "description": result[0][4]
        }
        return movie_title

    def search_by_rating(self, rating):
        """
        Поиск фильма по сортировке по рейтингу
        :param rating:
        :return:
        """
        cursor = self.connection()

        list_ratings = []

        qwerty = """
                SELECT `title`, `rating`, `description`
                FROM netflix
                WHERE rating = ?
                OR rating = ?
                OR rating = ?
                """

        if rating.lower() == "children":
            rating_movie = ('G', ' ', ' ')
        elif rating.lower() == "family":
            rating_movie = ('G', 'PG', 'PG-13')
        elif rating.lower() == "adult":
            rating_movie = ('R', 'NC-17', ' ')
        else:
            return "Данной категории не существует"

        cursor.execute(qwerty, rating_movie)
        results = cursor.fetchall()

        for result in results:
            list_ratings.append({'title': result[0],
                                 'rating': result[1],
                                 'description': result[2]})

        return list_ratings

    def search_by_years(self, year1, year2):
        """
        Поиск фильма в БД в промежутке заданных лет
        :param year1:
        :param year2:
        :return:
        """

        cursor = self.connection()

        list_movies_by_year = []

        query = """
                SELECT `title`, `release_year`
                FROM netflix
                WHERE release_year BETWEEN ? AND ?
                ORDER BY release_year ASC
                LIMIT 100
                """
        cursor.execute(query, (year1, year2))
        results = cursor.fetchall()

        for movie in results:
            list_movies_by_year.append({
                "title": movie[0],
                "release_year": movie[1]
            })
        return list_movies_by_year

    def search_by_genre(self, genre):
        """
        Поиск фильмов в БД по жанру
        :param genre:
        :return:
        """

        cursor = self.connection()

        list_movies_by_genre = []

        query = """
                SELECT `title`, `description`, `listed_in` as жанр, `release_year`, `type`
                FROM netflix
                WHERE description != ''
                AND жанр = ?
                AND type = 'Movie'
                ORDER BY release_year DESC
                LIMIT 10
                """
        cursor.execute(query, (genre,))
        results = cursor.fetchall()

        for movie in results:
            list_movies_by_genre.append({
                "title": movie[0],
                "description": movie[1]
            })
        return list_movies_by_genre


    def search_by_actor(self, actor1, actor2):
        """
        Поиск каста актеров в БД и вывод каста (задание 5)
        :param actor1:
        :param actor2:
        :return:
        """
        cursor = self.connection()
        list_of_actors = []

        query = f"""
                SELECT `cast`, COUNT(*)
                FROM netflix
                WHERE `cast` != ''
                AND `cast` LIKE '%{actor1}%, %{actor2}%'
                OR `cast` LIKE '%{actor2}%, %{actor1}%'
                GROUP BY `cast`
                HAVING `cast` > 2
                """

        cursor.execute(query,)
        actors_cast = cursor.fetchall()
        for actor in actors_cast:
            list_of_actors.append({"cast": actor})
        return list_of_actors


    def search_by_type_year_genre(self, type_picture, genre, year):

        """
        Поиск фильма из БД по заданным параметрам (задание 6)
        :param type_picture:
        :param genre:
        :param year:
        :return:
        """

        cursor = self.connection()

        list_movies_by_type_year_genre = []

        query = f"""
                SELECT `title`, `description`, `listed_in`
                FROM netflix
                WHERE description != ''
                AND `type` LIKE '%{type_picture}%'
                AND `release_year` = {year}
                AND `listed_in` LIKE '%{genre}%'
                """
        cursor.execute(query,)
        results = cursor.fetchall()

        for movie in results:
            list_movies_by_type_year_genre.append({
                "title": movie[0],
                "description": movie[1]
                })
        return json.dumps(list_movies_by_type_year_genre, ensure_ascii=False, indent=4)

# st = Data("../netflix.db")
# step6 = st.search_by_type_year_genre('Movie', 'Dramas', 2021)
# step5 = st.search_by_actor("Rose McIve", "Ben Lamb")
#
# print(step6)
# print(step5)
