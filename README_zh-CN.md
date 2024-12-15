# my-github-2024

生成你的 GitHub 年度数据统计图。

[English](README.md) | 简体中文

👉立即体验：[`my-github-2024.vercel.app`](https://my-github-2024.vercel.app/)

## 示例

![example](example.png)

## 自行部署

1. 将本仓库内容部署到 Vercel 上，假设地址为 `https://my-github-2024.vercel.app/`

2. 创建一个 GitHub oauth 应用，Homepage URL 和 Authorization callback URL 分贝为 `https://my-github-2024.vercel.app/` 和 `https://my-github-2024.vercel.app/callback`。

3. 在 Vercel 上将 `CLIENT_ID` 和 `CLIENT_SECRET` 环境变量设置为你的 GitHub oauth 应用的 Client ID 和 Client Secret。
