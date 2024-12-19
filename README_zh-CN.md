<div align="center">
  <img src="logo.png" alt="logo" />

  统计 2024 年你在 GitHub 上的活动.

  [English](README.md) | 简体中文

  [![Pylint and Mypy](https://github.com/WCY-dt/my-github-2024/actions/workflows/pylint_and_mypy.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/pylint_and_mypy.yml) [![Deploy state](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml) [![Server Status](https://img.shields.io/badge/dynamic/json?logo=linux&color=brightgreen&label=Server%20status&query=%24.status&cacheSeconds=600&url=https%3A%2F%2F2024.ch3nyang.top%2Fstatus)](https://2024.ch3nyang.top)

  [![GitHub issues](https://img.shields.io/github/issues/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/issues) [![GitHub pull requests](https://img.shields.io/github/issues-pr/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/pulls) [![GitHub license](https://img.shields.io/github/license/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/blob/main/LICENSE)

  <strong style="font-size: 24px;">👉 立即体验: <a href="https://2024.ch3nyang.top">https://2024.ch3nyang.top</a></strong>
</div>

> [!WARNING]
>
> This project is running on a VPS with poor performance. If the server is down, please refer to the [Run locally](README.md#run-locally) section.
>
> 本项目运行在一台性能较弱的 VPS 上。如遇服务器宕机，请参考[本地运行](#本地运行)部分。

## 示例

![example](example.png)

## 本地运行

> [!IMPORTANT]
>
> 受到 `datetime` 库特性影响，本项目需要 Python-3.12 及以上版本。

1. 克隆仓库：

    ```bash
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

2. 创建 Github OAuth App：

    访问 [GitHub Developer Settings](https://github.com/settings/developers) 创建一个新的 OAuth App。其中，`Homepage URL` 和 `Authorization callback URL` 分别填写 `http://127.0.0.1:5000` 和 `http://127.0.0.1:5000/callback`。

    获取 `Client ID` 和 `Client Secret`。

3. 在项目根目录下配置环境变量 `.env` 文件内容形如：

    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4. 安装依赖：

    ```bash
    pip3 install -r requirements.txt
    ```

5. 运行：

    ```bash
    python3 my-github-2024.py
    ```

6. 访问 `http://127.0.0.1:5000` 即可查看效果。

## 统计

> 感谢[阮一峰老师](https://github.com/ruanyf)的推荐！

[![Stargazers over time](https://starchart.cc/WCY-dt/my-github-2024.svg?background=%23FFFFFF&axis=%23333333&line=%232da44e)](https://starchart.cc/WCY-dt/my-github-2024)
