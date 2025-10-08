import allure
import pytest
from pages.notebook_fuctionality_page import NotebookPage
from pages.home_page import HomePage

class TestNotebooksSelection:
    @allure.story("Select and Checkout Your Notebook")
    @pytest.mark.smoke
    def test_notebook_functionality(self, driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        np = NotebookPage(driver, env)
        np.open_computers_menu()
        np.open_notebooks()
        np.select_notebook()
        np.add_to_cart()
        np.view_shopping_cart()

        assert np.check_cart_items_present(), "Cart items are not visible"
        assert "Demo Web Shop. Shopping Cart" in driver.title

        np.select_country("India")
        np.enter_zip_postal_code("500081")
        np.agree_terms()
        np.proceed_checkout()