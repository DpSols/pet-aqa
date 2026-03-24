from playwright.sync_api import Browser, BrowserContext, Playwright
from loguru import logger

from config.settings import WebSettings


def create_browser(playwright_instance: Playwright, settings: WebSettings) -> Browser:

    logger_inst = logger.bind(layer="web", component="browser_factory")
    logger_inst.debug(f"Launching browser (headless={settings.headless})")

    browser = playwright_instance.chromium.launch(headless=settings.headless)
    logger_inst.info("Browser launched successfully")
    return browser


def create_context(browser: Browser, settings: WebSettings) -> BrowserContext:

    logger_inst = logger.bind(layer="web", component="browser_context")
    logger_inst.debug("Creating browser context with tracing")

    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="playwright-videos/" if settings.record_video else None,
    )

    ctx.tracing.start(screenshots=True, snapshots=True)
    logger_inst.info("Browser context created with tracing enabled")

    return ctx
