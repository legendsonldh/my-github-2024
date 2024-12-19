<div align="center">
  <img src="logo.png" alt="logo" />

  Statistics of your activities on GitHub in 2024.

  [简体中文](README_zh-CN.md) | English

  [![Pylint](https://github.com/WCY-dt/my-github-2024/actions/workflows/pylint.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/pylint.yml) [![Deploy state](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml) [![Server Status](https://img.shields.io/badge/dynamic/json?logo=linux&color=brightgreen&label=Server%20status&query=%24.status&cacheSeconds=600&url=https%3A%2F%2F2024.ch3nyang.top%2Fstatus)](https://2024.ch3nyang.top)

  [![GitHub issues](https://img.shields.io/github/issues/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/issues) [![GitHub pull requests](https://img.shields.io/github/issues-pr/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/pulls) [![GitHub license](https://img.shields.io/github/license/WCY-dt/my-github-2024)](https://github.com/WCY-dt/my-github-2024/blob/main/LICENSE)

  <strong style="font-size: 24px;">👉 Try it now: <a href="https://2024.ch3nyang.top">https://2024.ch3nyang.top</a></strong>
</div>

> [!WARNING]
>
> This project is running on a VPS with poor performance. If the server is down, please refer to the [Run locally](#run-locally) section.
>
> 本项目运行在一台性能较弱的 VPS 上。如遇服务器宕机，请参考[本地运行](README_zh-CN.md#本地运行)部分。


> [!TIP]
>
> If it keeps in waiting page, reasons can be that you have too many commits. You can close the webpage and come back later. The server will continue to process your data.
>
> 如果一直在转圈等待，可能是因为您的 commit 数量过多。您可以放心关闭网页，过会儿再来看，服务器会继续处理您的数据。

## Example

![example](example.png)

## Run locally

> [!IMPORTANT]
>
> Due to the features of the `datetime` library, this project requires Python-3.12 or above.

1. Clone the repository:

    ```bash
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

2. Create a Github OAuth App:

    Visit [GitHub Developer Settings](https://github.com/settings/developers) to create a new OAuth App. In it, fill in `Homepage URL` and `Authorization callback URL` with `http://127.0.0.1:5000` and `http://127.0.0.1:5000/callback` respectively.

    Get `Client ID` and `Client Secret`.

3. Configure the environment variable `.env` file in the root directory of the project. The content is as follows:

    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

5. Run the project:

    ```bash
    python3 my-github-2024.py
    ```

6. Visit `http://127.0.0.1:5000` and complete!

## Statistics

> Thanks to [Ruanyifeng](https://github.com/ruanyf) for the recommendation!

[![Stargazers over time](https://starchart.cc/WCY-dt/my-github-2024.svg?background=%23FFFFFF&axis=%23333333&line=%232da44e)](https://starchart.cc/WCY-dt/my-github-2024)
