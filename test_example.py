import pytest
from playwright.sync_api import expect

import os

USERNAME = os.environ.get("GITHUB_USERNAME")
PASSWORD = os.environ.get("GITHUB_PASSWORD")
if not USERNAME or not PASSWORD:
    raise Exception("请设置 GITHUB_USERNAME 和 GITHUB_PASSWORD 环境变量")

@pytest.fixture(scope="session")
def auth_state(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://github.com/")
    page.get_by_role("link", name="Sign in").click()
    page.get_by_label("Username or email address").fill(USERNAME)
    page.get_by_label("Password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()

    # 验证登录成功
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible(timeout=5000)

    # 保存存储状态
    storage_state = context.storage_state(path="state.json")
    context.close()
    browser.close()
    return storage_state


def test_github_login(playwright, auth_state):
    # 使用存储状态创建新上下文
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(storage_state=auth_state)
    page = context.new_page()
    page.goto("https://github.com/dashboard")

    # 验证 Dashboard 存在
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()
    expect(page.get_by_label("Page context").locator("span")).to_contain_text("Dashboard")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible(timeout=5000)

    context.close()
    browser.close()