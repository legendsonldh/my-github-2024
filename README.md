# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

## Example

![example](example.png)

## Usage

0. Prepare your GitHub access token. You can generate a new token at [Personal Access Tokens (Classic)](https://github.com/settings/tokens).

1. Modify the `.env` file in the root directory. Fill in your GitHub access token, username, and time zone.

    ```shell
    GITHUB_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    GITHUB_USERNAME=your-github-username
    GITHUB_TIMEZONE=Asia/Shanghai
    ```

2. Run the following command to install dependencies.

    ```shell
    pip install -r requirements.txt
    ```

3. Run the following command to start the program.

    ```shell
    python main.py
    ```

4. Click the `Go Live` button in the bottom right corner of the VSCode window to preview.

    In alternative, you can open the [`dist/index.html`](dist/index.html) file in the browser.

## TODO

The online version is under development, please stay tuned.
