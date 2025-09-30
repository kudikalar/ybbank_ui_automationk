import pytest
from time import sleep

from pages.books_functionality_page import BooksPage
from pages.home_page import HomePage


class TestBookSelection:

    @pytest.mark.smoke
    def test_book_functionality(self, driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        bp = BooksPage(driver, env)
        bp.open_books_page()

        bp.click_book_link()
        bp.set_quantity("8")
        bp.click_add_to_cart()

        bp.click_shopping_cart()

        bp.select_country("India")
        bp.enter_zip("500081")
        bp.select_checkbox()
        bp.select_checkout()

        sleep(6)
