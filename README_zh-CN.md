<div align="center">
  <img src="logo.png" alt="logo" />

  生成你的 GitHub 年度数据统计图。

  [English](README.md) | 简体中文

  [![Deploy state](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml/badge.svg)](https://github.com/WCY-dt/my-github-2024/actions/workflows/deploy.yml)

  <strong style="font-size: 20px;">👉 立即体验: <a href="https://2024.ch3nyang.top">https://2024.ch3nyang.top</a></strong>
</div>

> [!NOTE]
>
> Since this project counts every commits, it may take 1-10 minutes to generate. Please be patient.
>
> 由于本项目统计了每一次提交的信息，因此可能需要 1-10 分钟的时间来生成。请耐心等待。


> [!WARNING]
>
> This tool involves a large number of network requests, and the server may be restricted by GitHub, resulting in failure to use it normally. If the server is down, please refer to the [Run locally](README.md#run-locally) section to run locally.
>
> 本工具涉及到海量网络请求，服务器很可能会被 GitHub 限制，导致无法正常使用。如遇服务器宕机，请参考[本地运行](#本地运行)部分在本地运行。

## 示例

![example](example.png)

## 自行部署

0. 假设你的 URL 为 `YOUR_URL`、服务器 IP 为 `YOUR_IP`、用户名为 `YOUR_USERNAME`。

1. [Fork](https://github.com/WCY-dt/my-github-2024/fork) 本仓库。

2. 创建 Github OAuth App：

    访问 [GitHub Developer Settings](https://developer.github.com/settings/applications/new) 创建一个新的 OAuth App。其中，`Homepage URL` 和 `Authorization callback URL` 分别填写 `http://YOUR_URL` 和 `http://YOUR_URL/callback`。

    获取 `Client ID` 和 `Client Secret`。

3. 将 [`script/setup.sh`](script/setup.sh) 脚本中的 `YOUR_URL` 替换为你的 URL、`YOUR_CLIENT_ID` 替换为你的 `Client ID`、`YOUR_CLIENT_SECRET` 替换为你的 `Client Secret`。然后在服务器中运行该脚本。

    > [!WARNING]
    >
    > 该脚本可能会覆盖现有的配置文件，请谨慎使用。

4. 在本地生成 SSH 密钥并添加到服务器：

    ```bash
    ssh-keygen -t rsa -b 4096 -C "action@github.com" -f ~/.ssh/id_rsa -N ""
    cat ~/.ssh/id_rsa.pub | ssh YOUR_USERNAME@YOUR_IP 'cat >> ~/.ssh/authorized_keys'
    cat ~/.ssh/id_rsa | clip
    ```

5. 添加 GitHub Actions 的 Secrets：

    - `SERVER_IP`: 服务器 IP
    - `SERVER_USERNAME`: 服务器用户名
    - `SERVER_SSH_KEY`: 生成的 SSH 密钥

6. 运行 GitHub Actions 的 `Deploy to Server` 工作流，即可自动部署并运行。

## 本地运行

1. 克隆仓库：

    ```bash
    mkdir /var/www
    cd /var/www
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

2. 创建 Github OAuth App：

    访问 [GitHub Developer Settings](https://developer.github.com/settings/applications/new) 创建一个新的 OAuth App。其中，`Homepage URL` 和 `Authorization callback URL` 分别填写 `http://127.0.0.1:5000` 和 `http://127.0.0.1:5000/callback`。

    获取 `Client ID` 和 `Client Secret`。

3. 配置环境变量：

    ```bash
    nano .env
    ```

    `.env` 文件内容形如：

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
