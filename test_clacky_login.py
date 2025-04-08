import re
from playwright.sync_api import Playwright, sync_playwright, expect
import pytest
import os

USERNAME = os.environ.get("GITHUB_USERNAME")
PASSWORD = os.environ.get("GITHUB_PASSWORD")
if not USERNAME or not PASSWORD:
    raise Exception("请设置 GITHUB_USERNAME 和 GITHUB_PASSWORD 环境变量")

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://github.com/")
#     page.get_by_role("link", name="Sign in").click()
#     page.get_by_role("textbox", name="Username or email address").click()
#     page.get_by_role("textbox", name="Username or email address").fill(USERNAME)
#     page.get_by_role("textbox", name="Password").click()
#     page.get_by_role("textbox", name="Password").fill(PASSWORD)
#     page.get_by_role("button", name="Sign in", exact=True).click()
#     expect(page.get_by_role("link", name="Dashboard")).to_be_visible()
#     expect(page.get_by_label("Page context").locator("span")).to_contain_text("Dashboard")
#     page1 = context.new_page()
#     page1.goto("https://staging.app.clackyai.com/sign-in?redirect_url=https%3A%2F%2Fstaging.app.clackyai.com%2F")
#     page1.get_by_role("button", name="Github").click()
#     expect(page1.get_by_text("Welcome to Clacky!")).to_be_visible()
#     expect(page1.get_by_role("main")).to_contain_text("Welcome to Clacky!")
#     page1.get_by_role("button", name="Create Project").click()
#     page1.get_by_role("button", name="Connect").click()
#     page1.get_by_text("Select branch").click()
#     page1.get_by_role("option", name="main").click()
#     page1.get_by_role("button", name="Continue").click()
#     expect(page1.get_by_role("main").get_by_text("simple_html", exact=True)).to_be_visible()
#     expect(page1.get_by_role("main")).to_contain_text("simple_html")
#     expect(page1.get_by_text("Environment template *")).to_be_visible(timeout=120000)
#     expect(page1.get_by_role("main")).to_contain_text("Environment template *")
#     page1.get_by_role("button", name="Confirm & Continue").click()
#     page1.get_by_role("button", name="I knew, let's create").click()
#     expect(page1.get_by_text("Editor")).to_be_visible()
#     expect(page1.locator("body")).to_contain_text("Editor")
#
#     context.close()
#     browser.close()
#
# with sync_playwright() as playwright:
#     run(playwright)

@pytest.fixture(scope="session")
def auth_state(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://github.com/")
    page.get_by_role("link", name="Sign in").click()
    page.get_by_role("textbox", name="Username or email address").click()
    page.get_by_role("textbox", name="Username or email address").fill(USERNAME)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()
    expect(page.get_by_label("Page context").locator("span")).to_contain_text("Dashboard")
    page1 = context.new_page()
    page1.goto("https://staging.app.clackyai.com/sign-in?redirect_url=https%3A%2F%2Fstaging.app.clackyai.com%2F")
    page1.get_by_role("button", name="Github").click()

    # 验证登录成功
    expect(page1.get_by_text("Welcome to Clacky!")).to_be_visible()

    # 保存存储状态
    storage_state = context.storage_state(path="state_clacky.json")
    context.close()
    browser.close()
    return storage_state


def test_clacky_main_process(playwright, auth_state):
    # 使用存储状态创建新上下文
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state=auth_state)
    page1 = context.new_page()
    page1.goto("https://staging.app.clackyai.com/sign-in?redirect_url=https%3A%2F%2Fstaging.app.clackyai.com%2F")
    page1.get_by_role("button", name="Create Project").click()
    page1.get_by_role("button", name="Connect").click()
    page1.get_by_text("Select branch").click()
    page1.get_by_role("option", name="main").click()
    page1.get_by_role("button", name="Continue").click()
    expect(page1.get_by_role("main").get_by_text("simple_html", exact=True)).to_be_visible()
    expect(page1.get_by_role("main")).to_contain_text("simple_html")
    expect(page1.get_by_text("Environment template *")).to_be_visible(timeout=120000)
    expect(page1.get_by_role("main")).to_contain_text("Environment template *")
    page1.get_by_role("button", name="Confirm & Continue").click()
    page1.get_by_role("button", name="I knew, let's create").click()
    expect(page1.get_by_text("Editor")).to_be_visible()
    expect(page1.locator("body")).to_contain_text("Editor")

    context.close()
    browser.close()
