<div align="center">
  <img src="logo.png" alt="logo" />

  Generate your GitHub yearly statistics chart.

  [简体中文](README_zh-CN.md) | English

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

1. Make sure you have installed Python3.12 and other necessary dependencies:

    ```bash
    apt install python3.12 python3-pip python3-gunicorn python3-virtualenv nginx certbot python3-certbot-nginx -y
    ```

2. Clone the repository:

    ```bash
    mkdir /var/www
    cd /var/www
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

3. Configure environment variables:

    ```bash
    nano .env
    ```

    `.env` The file content is as follows:

    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4. Install dependencies:

    ```bash
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

5. Run:

    ```bash
    nohup python3 my-github-2024.py &
    ```

6. Install and configure Gunicorn:

    ```bash
    pip3 install gunicorn
    cp my-github-2024.service /etc/systemd/system
    ```

    Start the service:

    ```bash
    systemctl daemon-reload
    systemctl start my-github-2024
    systemctl enable my-github-2024
    ```

7. Configure SSL certificate:

    ```bash
    certbot --nginx -d YOUR_URL
    certbot renew --dry-run
    ```

    > You need to change `YOUR_URL` to your domain name.

8. Configure Nginx:

    ```bash
    cp my-github-2024 /etc/nginx/sites-available
    rm /etc/nginx/sites-enabled/default
    ```

    > Before that, you need to modify `YOUR_URL` in the `my-github-2024` file to your domain name.

    Enable the site:

    ```bash
    ln -s /etc/nginx/sites-available/my-github-2024 /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx
    nginx -s reload
    ```

9. Visit `https://YOUR_URL` to see the effect.

## Run locally

1. Clone the repository:

    ```bash
    mkdir /var/www
    cd /var/www
    git clone https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

2. Create a Github OAuth App:

    Visit [GitHub Developer Settings](https://developer.github.com/settings/applications/new) to create a new OAuth App. In the Homepage URL and Authorization callback URL, fill in `http://127.0.0.1:5000` and `http://127.0.0.1:5000/callback` respectively.

    Get `Client ID` and `Client Secret`.

3. Configure environment variables:

    ```bash
    nano .env
    ```

    `.env` file content is as follows:

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
