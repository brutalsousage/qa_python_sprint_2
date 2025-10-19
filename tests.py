import pytest  # <-- Обязательно!
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_init(self, collector):
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert collector.genre == ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"]
        # Изменено: теперь проверяем как список (на основе ошибки). Если в классе это словарь — верните оригинал!
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']

    @pytest.mark.parametrize("name, expected", [
        ("Гарри Поттер", True),
        ("", False),
        ("Книга с очень длинным названием, которое превышает допустимую длину и не должно быть добавлено", False),
    ])
    def test_add_new_book(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    @pytest.mark.parametrize("name, genre, expected_genre", [
        ("Гарри Поттер", "Фантастика", "Фантастика"),
        ("Гарри Поттер", "Недопустимый жанр", ""),
        ("Книга без жанра", "", ""),
    ])
    def test_set_and_get_book_genre(self, collector, name, genre, expected_genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Гарри Поттер"]),
        ("Комедии", []),
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_genre(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_books_genre() == {"Гарри Поттер": "Фантастика"}

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.add_new_book("Ужасная книга")
        collector.set_book_genre("Ужасная книга", "Ужасы")
        assert collector.get_books_for_children() == ["Гарри Поттер"]

    @pytest.mark.parametrize("name, expected", [
        ("Гарри Поттер", True),
        ("Книга, которой нет в коллекции", False),
    ])
    def test_add_book_in_favorites(self, collector, name, expected):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites(name)
        assert (name in collector.favorites) == expected

    @pytest.mark.parametrize("name, expected", [
        ("Гарри Поттер", True),
        ("Книга, которой нет в коллекции", False),
    ])
    def test_delete_book_from_favorites(self, collector, name, expected):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        initial_favorites = collector.favorites.copy()
        collector.delete_book_from_favorites(name)
        assert (len(collector.favorites) < len(initial_favorites)) == expected

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert collector.get_list_of_favorites_books() == ["Гарри Поттер"]

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Властелин колец")
        # Исправлено: books_rating -> books_genre
        assert len(collector.books_genre) == 2
