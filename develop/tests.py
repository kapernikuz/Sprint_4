import pytest


class TestAddNewBook:

    @pytest.mark.parametrize("name", [
        "Гарри Поттер",
        "Книга",
        "A" * 40,
    ])
    def test_add_new_book_valid_name(self, collector, name):
        collector.add_new_book(name)
        assert collector.get_book_genre(name) == ''

    @pytest.mark.parametrize("name", [
        "",
        "B" * 41,
    ])
    def test_add_new_book_invalid_name(self, collector, name):
        collector.add_new_book(name)
        assert collector.get_book_genre(name) is None

    def test_add_new_book_does_not_duplicate(self, collector):
        collector.add_new_book("Дюна")
        collector.add_new_book("Дюна")
        assert collector.get_books_genre() == {"Дюна": ""}


class TestSetBookGenre:

    def test_set_book_genre_sets_genre(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_book_genre("Дюна") == "Фантастика"

    @pytest.mark.parametrize("name, genre", [
        ("Несуществующая книга", "Фантастика"),
        ("Дюна", "Поэзия"),
    ])
    def test_set_book_genre_invalid_data(self, collector, name, genre):
        collector.add_new_book("Дюна")
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre("Дюна") == ''


class TestGetBookGenre:

    def test_get_book_genre_returns_genre(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_book_genre("Дюна") == "Фантастика"

    def test_get_book_genre_unknown_book_returns_none(self, collector):
        assert collector.get_book_genre("Нет такой книги") is None


class TestGetBooksWithSpecificGenre:

    def test_get_books_with_specific_genre_returns_matching_books(self, collector):
        collector.add_new_book("Дюна")
        collector.add_new_book("Солярис")
        collector.add_new_book("Оно")
        collector.set_book_genre("Дюна", "Фантастика")
        collector.set_book_genre("Солярис", "Фантастика")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_books_with_specific_genre("Фантастика") == ["Дюна", "Солярис"]

    @pytest.mark.parametrize("genre", ["Поэзия", ""])
    def test_get_books_with_specific_genre_unknown_genre_returns_empty(self, collector, genre):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_books_with_specific_genre(genre) == []


class TestGetBooksGenre:

    def test_get_books_genre_returns_books_dict(self, collector):
        collector.add_new_book("Дюна")
        collector.add_new_book("Оно")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_books_genre() == {"Дюна": "Фантастика", "Оно": ""}


class TestGetBooksForChildren:

    def test_get_books_for_children_excludes_age_rated_genres(self, collector):
        collector.add_new_book("Оно")
        collector.add_new_book("История игрушек")
        collector.add_new_book("Дюна")
        collector.set_book_genre("Оно", "Ужасы")
        collector.set_book_genre("История игрушек", "Мультфильмы")
        children_books = collector.get_books_for_children()
        assert "История игрушек" in children_books
        assert "Оно" not in children_books
        assert "Дюна" not in children_books


class TestAddBookInFavorites:

    def test_add_book_in_favorites_adds_existing_book(self, collector):
        collector.add_new_book("Дюна")
        collector.add_book_in_favorites("Дюна")
        assert "Дюна" in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("name", ["Дюна", "Оно"])
    def test_add_book_in_favorites_no_duplicates(self, collector, name):
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.add_book_in_favorites(name)
        assert collector.get_list_of_favorites_books().count(name) == 1

    def test_add_book_in_favorites_ignores_unknown_book(self, collector):
        collector.add_book_in_favorites("Нет такой книги")
        assert collector.get_list_of_favorites_books() == []


class TestDeleteBookFromFavorites:

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book("Дюна")
        collector.add_book_in_favorites("Дюна")
        collector.delete_book_from_favorites("Дюна")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_unknown_book_does_not_raise(self, collector):
        collector.delete_book_from_favorites("Нет такой книги")
        assert collector.get_list_of_favorites_books() == []


class TestGetListOfFavoritesBooks:

    def test_get_list_of_favorites_books_returns_favorites(self, collector):
        collector.add_new_book("Дюна")
        collector.add_new_book("Оно")
        collector.add_book_in_favorites("Дюна")
        collector.add_book_in_favorites("Оно")
        assert collector.get_list_of_favorites_books() == ["Дюна", "Оно"]

    def test_get_list_of_favorites_books_empty_initially(self, collector):
        assert collector.get_list_of_favorites_books() == []