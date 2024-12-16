# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

## Example

![example](example.png)

## Self-deployment

1. Make sure you have Python and Pip installed:

    ```bash
    apt install python3 python3-pip -y
    ```

2. Clone the repository:

    ```bash
    cd /var/www
    git clone -b online https://github.com/WCY-dt/my-github-2024.git
    cd my-github-2024
    ```

3. Start the virtual environment and install dependencies:

    ```bash
    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Run:

    ```bash
    python3 my-github-2024.py
    ```

5. Install and configure Gunicorn:

    ```bash
    pip install gunicorn
    mv my-github-2024.service /etc/systemd/system
    ```

    Start the service:

    ```bash
    systemctl start my-github-2024
    systemctl enable my-github-2024
    ```

6. Configure Nginx:

    ```bash
    apt install nginx -y
    mv my-github-2024 /etc/nginx/sites-available
    ```

    Enable the site:

    ```bash
    ln -s /etc/nginx/sites-available/my-github-2024 /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx
    ```

7. Visit `http://your-domain.com` to see the effect.
