<div align="center">
  <img src="logo.png" alt="logo" />

  Generate your GitHub yearly statistics chart.

  [简体中文](README_zh-CN.md) | English

  [![Deploy state](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml)

  <strong style="font-size: 20px;">👉 Try it now: <a href="https://2024.ch3nyang.top">https://2024.ch3nyang.top</a></strong>
</div>

> [!NOTE]
>
> Since this project counts every commits, it may take 1-10 minutes to generate. Please be patient.
>
> 由于本项目统计了每一次提交的信息，因此可能需要 1-10 分钟的时间来生成。请耐心等待。


> [!WARNING]
>
> This tool involves a large number of network requests, and the server may be restricted by GitHub, resulting in failure to use it normally. If the server is down, please refer to the [Run locally](#run-locally) section to run locally.
>
> 本工具涉及到海量网络请求，服务器很可能会被 GitHub 限制，导致无法正常使用。如遇服务器宕机，请参考[本地运行](README_zh-CN.md#本地运行)部分在本地运行。

## Example

![example](example.png)

## Self-deployment

0. Assume your URL is `YOUR_URL`, server IP is `YOUR_IP`, and username is `YOUR_USERNAME`.

1. [Fork](https://github.com/WCY-dt/my-github-2024/fork) this repository.

2. Create a Github OAuth App:

    Visit [GitHub Developer Settings](https://developer.github.com/settings/applications/new) to create a new OAuth App. In it, `Homepage URL` and `Authorization callback URL` are filled in `http://YOUR_URL` and `http://YOUR_URL/callback` respectively.

    Get `Client ID` and `Client Secret`.

3. Replace `YOUR_URL` with your URL, `YOUR_CLIENT_ID` with your `Client ID`, and `YOUR_CLIENT_SECRET` with your `Client Secret` in the [`script/setup.sh`](script/setup.sh) script. Then run the script on the server.

> [!WARNING]
>
> This script may overwrite existing configuration files, please use with caution.

4. Generate SSH keys locally and add them to the server:

    ```bash
    ssh-keygen -t rsa -b 4096 -C "action@github.com" -f ~/.ssh/id_rsa -N ""
    cat ~/.ssh/id_rsa.pub | ssh YOUR_USERNAME@YOUR_IP 'cat >> ~/.ssh/authorized_keys'
    cat ~/.ssh/id_rsa | clip
    ```

5. Add Secrets of GitHub Actions:

    - `SERVER_IP`: Server IP
    - `SERVER_USERNAME`: Server username
    - `SERVER_KEY`: Generated SSH key

6. Run the `Deploy to Server` workflow of GitHub Actions to automatically deploy and run.

## Run locally

1. Clone the repository:

    ```bash
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

2. Create a Github OAuth App:

    Visit [GitHub Developer Settings](https://developer.github.com/settings/applications/new) to create a new OAuth App. In it, fill in `Homepage URL` and `Authorization callback URL` with `http://127.0.0.1:5000` and `http://127.0.0.1:5000/callback` respectively.

    Get `Client ID` and `Client Secret`.

3. Configure the environment variable `.env` file in the project root directory. The content is as follows:

    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

5. Run:

    ```bash
    python3 my-github-2024.py
    ```

6. Visit `http://127.0.0.1:5000` to see the effect.
