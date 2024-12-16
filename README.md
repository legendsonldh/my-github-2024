# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

**👉 Try it now: [`https://2024.ch3nyang.top`](https://2024.ch3nyang.top)**

## Example

![example](example.png)

## Self-deployment

1. Make sure you have installed Python and Pip:

    ```bash
    apt install python3 python3-pip -y
    ```

2. Clone the repository:

    ```bash
    cd /var/www
    git clone -b online https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

3. Configure environment variables:

    ```bash
    nano .env
    ```

    `.env` file content is as follows:

    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4. Start the virtual environment and install dependencies:

    ```bash
    pip3 install virtualenv
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
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d YOUR_URL
    certbot renew --dry-run
    ```

8. Configure Nginx:

    ```bash
    apt install nginx -y
    cp my-github-2024 /etc/nginx/sites-available
    ```

    > Before that, you need to modify `YOUR_URL` in the `my-github-2024` file to your domain name.

    Enable the site:

    ```bash
    ln -s /etc/nginx/sites-available/my-github-2024 /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx
    ```

9. Visit `https://YOUR_URL` to see the effect.
