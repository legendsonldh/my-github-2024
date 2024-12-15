# my-github-2024

生成你的 GitHub 年度数据统计图。

[English](README.md) | 简体中文

## 示例

![example](example.png)

## 使用方法

0. 准备 GitHub 访问令牌。你可以在 [Personal Access Tokens (Classic)](https://github.com/settings/tokens) 生成新令牌。其应该形如 `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`。

1. 运行以下命令安装依赖项。

    ```shell
    pip install -r requirements.txt
    ```

2. 运行以下命令启动程序。

    ```shell
    flask --app my-github-2024 run
    ```

3. 打开浏览器，访问 [`http://127.0.0.1:5000`](http://127.0.0.1:5000)，填写你的 GitHub 访问令牌、GitHub 用户名和时区。点击 `Generate` 按钮生成你的 GitHub 年度数据统计图。

    > 这个过程耗时可能较长，取决于你的 GitHub 数据量大小。请耐心等待。

## TODO

在线版本正在开发中，敬请期待。
