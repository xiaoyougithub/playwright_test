# Playwright Python 自动化测试项目

## 简介

本项目使用 Playwright (Python) 实现自动化测试。Playwright 是一个由 Microsoft 开发的现代化、快速且可靠的浏览器自动化工具，支持 Chromium、Firefox 和 WebKit 等主流浏览器。

## 官方文档

[Playwright 官方文档 (Python)](https://playwright.dev/python/docs/intro)

## 环境准备

1.  **安装 Python:** 确保你的机器上安装了 Python 3.7 或更高版本。 你可以从 [Python 官网](https://www.python.org/downloads/) 下载最新版本。

2.  **安装 Playwright:** 使用 pip 安装 Playwright 及其浏览器驱动：

    ```bash
    pip install playwright
    playwright install
    ```

3.  **安装 Pytest:**  本项目使用 pytest 作为测试框架，安装 pytest 和 pytest-playwright 插件：

    ```bash
    pip install pytest pytest-playwright
    ```

## 快速上手

### 1. 生成测试脚本

Playwright 提供了代码生成器，可以自动生成测试脚本。 例如，要生成访问 GitHub 的测试脚本，运行：

```bash
playwright codegen github.com


```

指定测试文件运行：

```bash
playwright test_example.py
```