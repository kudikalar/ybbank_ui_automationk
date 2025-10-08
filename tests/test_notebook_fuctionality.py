import allure
import pytest
from pages.notebook_fuctionality_page import NotebookPage
from pages.home_page import HomePage

class TestNotebooksSelection:
    @allure.story("Select Your Notebook")
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
        assert "Demo Web Shop. Shopping Cart" in driver.title #confirmation end