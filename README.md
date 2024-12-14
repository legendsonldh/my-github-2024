# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

## Example

![example](example.png)

## Usage

0. Prepare your GitHub access token. You can generate a new token at [Personal Access Tokens (Classic)](https://github.com/settings/tokens).

1. Create a `.env` file in the root directory of the project. And fill in your GitHub access token and username.

    ```shell
    GITHUB_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    GITHUB_USERNAME=your-username
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
