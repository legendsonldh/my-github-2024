# my-github-2024

Generate your GitHub yearly statistics chart.

[简体中文](README_zh-CN.md) | English

👉 Try it now: [`my-github-2024.vercel.app`](https://my-github-2024.vercel.app/)

## Example

![example](example.png)

## Self-deployment

1. Deploy the contents of this repository to Vercel, assuming the address is `https://my-github-2024.vercel.app/`

2. Create a GitHub oauth application, with the Homepage URL and Authorization callback URL as `https://my-github-2024.vercel.app/` and `https://my-github-2024.vercel.app/callback` respectively.

3. Set the `CLIENT_ID` and `CLIENT_SECRET` environment variables on Vercel to the Client ID and Client Secret of your GitHub oauth application.
