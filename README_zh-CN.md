# my-github-2024

生成你的 GitHub 年度数据统计图。

[English](README.md) | 简体中文

**👉 立即体验: [`https://2024.ch3nyang.top`](https://2024.ch3nyang.top)**

> [!WARNING]
>
> This tool involves a large number of network requests, and the server may be restricted by GitHub, resulting in failure to use it normally. If the server is down, please refer to the [Run locally](README.md#run-locally) section to run locally.
>
> 本工具涉及到海量网络请求，服务器很可能会被 GitHub 限制，导致无法正常使用。如遇服务器宕机，请参考[本地运行](#本地运行)部分在本地运行。

## 示例

![example](example.png)

## 自行部署

1. 确保您已安装 Python3.12 和其它必要的依赖：

    ```bash
    apt install python3.12 python3-pip python3-gunicorn python3-virtualenv nginx certbot python3-certbot-nginx -y
    ```

2. 克隆仓库：

    ```bash
    mkdir /var/www
    cd /var/www
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

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
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

5. 运行：

    ```bash
    nohup python3 my-github-2024.py &
    ```

6. 安装并配置 Gunicorn：

    ```bash
    pip3 install gunicorn
    cp my-github-2024.service /etc/systemd/system
    ```

    启动服务：

    ```bash
    systemctl daemon-reload
    systemctl start my-github-2024
    systemctl enable my-github-2024
    ```

7. 配置 SSL 证书：

    ```bash
    certbot --nginx -d YOUR_URL
    certbot renew --dry-run
    ```

    > 你需要修改 `YOUR_URL` 为你的域名。

8. 配置 Nginx：

    ```bash
    cp my-github-2024 /etc/nginx/sites-available
    rm /etc/nginx/sites-enabled/default
    ```

    > 在此之前，你需要修改 `my-github-2024` 文件中的 `YOUR_URL` 为你的域名。

    启用站点：

    ```bash
    ln -s /etc/nginx/sites-available/my-github-2024 /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx
    nginx -s reload
    ```

9. 访问 `https://YOUR_URL` 即可查看效果。

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
