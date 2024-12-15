# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

## Example

![example](example.png)

## Usage

0. Prepare a GitHub access token. You can generate a new token in [Personal Access Tokens (Classic)](https://github.com/settings/tokens). It should look like `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

1. Run the following command to install dependencies.

    ```shell
    pip install -r requirements.txt
    ```

2. Run the following command to start the program.

    ```shell
    flask --app my-github-2024 run
    ```

3. Open a browser and visit [`http://127.0.0.1:5000`](http://127.0.0.1:5000), fill in your GitHub access token, GitHub username and time zone. Click the `Generate` button to generate your GitHub anual data statistics chart.

    > This process may take a long time, depending on the size of your GitHub data. Please be patient.

## TODO

The online version is under development, please stay tuned.
