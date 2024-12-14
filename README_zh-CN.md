# my-github-2024

生成你的 GitHub 年度数据统计图。

[English](README.md) | 简体中文

## 示例

![example](example.png)

## 使用方法

0. 准备 GitHub 访问令牌。你可以在 [Personal Access Tokens (Classic)](https://github.com/settings/tokens) 生成新令牌。

1. 修改根目录中的 `.env` 文件。并填写你的 GitHub 访问令牌、用户名和时区。

    ```shell
    GITHUB_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    GITHUB_USERNAME=your-github-username
    GITHUB_TIMEZONE=Asia/Shanghai
    ```

2. 运行以下命令安装依赖项。

    ```shell
    pip install -r requirements.txt
    ```

3. 运行以下命令启动程序。

    ```shell
    python main.py
    ```

4. 点击 VSCode 窗口右下角的 `Go Live` 按钮进行预览。

    或者，您也可以在浏览器中打开 [`dist/index.html`](dist/index.html) 文件。

## TODO

在线版本正在开发中，敬请期待。
