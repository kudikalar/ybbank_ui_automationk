import allure
import pytest
from pages.computers_functionality_page import ComputersPage
from pages.home_page import HomePage

class TestComputerSelection:
    @allure.story("Build Your Cheap PC")
    @pytest.mark.smoke
    def test_computer_functionality(self, driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        cp = ComputersPage(driver, env)

        cp.open_computers_menu()
        cp.open_desktops()
        cp.select_build_computer()
        cp.add_to_cart()
        cp.view_shopping_cart()
        assert "Demo Web Shop. Build your own cheap computer" in driver.title #confirmation