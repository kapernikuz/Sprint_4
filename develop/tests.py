import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# ---------- add_new_book ----------

@pytest.mark.parametrize("name", [
    "Гарри Поттер",
    "Книга",
    "A" * 40,  # ровно 40 символов — граничное значение
])
def test_add_new_book_valid_name(collector, name):
    collector.add_new_book(name)
    assert name in collector.get_books_genre()
    assert collector.get_book_genre(name) == ''


@pytest.mark.parametrize("name", [
    "",
    "B" * 41,  # на 1 символ больше допустимого
])
def test_add_new_book_invalid_name(collector, name):
    collector.add_new_book(name)
    assert name not in collector.get_books_genre()


def test_add_new_book_does_not_duplicate(collector):
    collector.add_new_book("Дюна")
    collector.add_new_book("Дюна")
    assert list(collector.get_books_genre().keys()).count("Дюна") == 1


# ---------- set_book_genre / get_book_genre ----------

def test_set_book_genre_sets_genre(collector):
    collector.add_new_book("Дюна")
    collector.set_book_genre("Дюна", "Фантастика")
    assert collector.get_book_genre("Дюна") == "Фантастика"


@pytest.mark.parametrize("name, genre", [
    ("Несуществующая книга", "Фантастика"),   # книги нет в словаре
    ("Дюна", "Поэзия"),                        # жанра нет в списке genre
])
def test_set_book_genre_invalid_data(collector, name, genre):
    collector.add_new_book("Дюна")
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre("Дюна") == ''


def test_get_book_genre_unknown_book_returns_none(collector):
    assert collector.get_book_genre("Нет такой книги") is None


# ---------- get_books_with_specific_genre ----------

def test_get_books_with_specific_genre_returns_matching_books(collector):
    collector.add_new_book("Дюна")
    collector.add_new_book("Солярис")
    collector.add_new_book("Оно")
    collector.set_book_genre("Дюна", "Фантастика")
    collector.set_book_genre("Солярис", "Фантастика")
    collector.set_book_genre("Оно", "Ужасы")

    assert collector.get_books_with_specific_genre("Фантастика") == ["Дюна", "Солярис"]


# ---------- get_books_for_children ----------

def test_get_books_for_children_excludes_age_rated_genres(collector):
    collector.add_new_book("Оно")
    collector.add_new_book("История игрушек")
    collector.add_new_book("Дюна")  # без жанра — не попадёт в детские
    collector.set_book_genre("Оно", "Ужасы")
    collector.set_book_genre("История игрушек", "Мультфильмы")

    children_books = collector.get_books_for_children()

    assert "История игрушек" in children_books
    assert "Оно" not in children_books
    assert "Дюна" not in children_books


# ---------- add_book_in_favorites / delete_book_from_favorites / get_list_of_favorites_books ----------

def test_add_book_in_favorites_adds_existing_book(collector):
    collector.add_new_book("Дюна")
    collector.add_book_in_favorites("Дюна")
    assert collector.get_list_of_favorites_books() == ["Дюна"]


@pytest.mark.parametrize("name", ["Дюна"])
def test_add_book_in_favorites_no_duplicates(collector, name):
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    collector.add_book_in_favorites(name)
    assert collector.get_list_of_favorites_books().count(name) == 1


def test_add_book_in_favorites_ignores_unknown_book(collector):
    collector.add_book_in_favorites("Нет такой книги")
    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book("Дюна")
    collector.add_book_in_favorites("Дюна")
    collector.delete_book_from_favorites("Дюна")
    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_unknown_book_does_not_raise(collector):
    collector.delete_book_from_favorites("Нет такой книги")
    assert collector.get_list_of_favorites_books() == []