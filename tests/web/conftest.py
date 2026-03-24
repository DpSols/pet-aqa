import pytest
from pathlib import Path

from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
from config.settings import Settings
from src.web.browser_factory import create_browser, create_context
from src.web.pages.login_page import LoginPage
from src.web.pages.inventory_page import InventoryPage
from src.web.pages.cart_page import CartPage
from src.steps.web_steps import WebSteps


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser = create_browser(playwright_instance, settings.web)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def browser_context(browser: Browser, settings: Settings, request: pytest.FixtureRequest) -> BrowserContext:
    ctx = create_context(browser, settings.web)
    yield ctx

    if request.node.rep_call.failed:
        trace_path = Path(f"allure-results/traces/{request.node.name}.zip")
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        ctx.tracing.stop(path=str(trace_path))

    ctx.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext, settings: Settings) -> Page:
    page = browser_context.new_page()
    page.goto(settings.web.base_url)
    yield page
    page.close()


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture(scope="function")
def web_steps(
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
) -> WebSteps:
    return WebSteps(login_page, inventory_page, cart_page)
