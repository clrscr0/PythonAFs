import pytest

from Pages.login_page import LoginPage
from Utilities.read_config import AppConfiguration
from playwright.sync_api import sync_playwright
from Pages.products_list_page import ProductsListPage


@pytest.fixture()
def setup(request):
    configuration = AppConfiguration.get_app_configuration()
    common_info = AppConfiguration.get_common_info()
    base_url = common_info["Url"]

    # Browser options
    headless = eval(configuration["Headless"])  # convert to bool
    slow_mo = float(configuration["SlowMo"])
    launch_options = {"headless": headless, "slow_mo": slow_mo}

    # Start Playwright
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(**launch_options, args=['--start-maximized'])

    context_options = {'base_url': base_url}

    # Browser context settings
    browser_context = browser.new_context(**context_options, no_viewport=True)
    browser_context.set_default_navigation_timeout(float(configuration["DefaultNavigationTimeout"]))
    browser_context.set_default_timeout(float(configuration["DefaultTimeout"]))

    # Create Page
    page = browser_context.new_page()

    request.cls.page = page
    page.goto(base_url)

    yield page
    page.close()
    browser.close()
    playwright.stop()