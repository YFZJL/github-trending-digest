# GitHub Trending Digest

自动化抓取 GitHub 每日趋势项目，生成 Markdown 格式日报。

## 📋 功能

- 🔄 **每日自动抓取**：通过 GitHub Actions 每天北京时间 21:00 自动运行
- 📊 **Top 15 项目**：提取 GitHub Trending 页面前 15 个热门项目
- 📝 **Markdown 格式**：生成易读的 Markdown 文档，保存在 `digest/` 目录
- 🔄 **自动提交**：抓取后自动提交到仓库

## 🚀 使用方法

### 1. Fork 或克隆此仓库

```bash
git clone https://github.com/你的用户名/github-trending-digest.git
cd github-trending-digest
```

### 2. 本地测试

```bash
pip install -r requirements.txt
python fetch_trending.py
```

生成的文件会保存在 `digest/YYYY-MM-DD.md`

### 3. 启用 GitHub Actions

1. 在 GitHub 仓库设置中启用 Actions
2. Actions 将每天自动运行并推送更新

## 📁 文件结构

```
github-trending-digest/
├── .github/
│   └── workflows/
│       └── daily-trending.yml  # GitHub Actions 配置
├── digest/                      # 日报存储目录
│   └── YYYY-MM-DD.md
├── fetch_trending.py           # 抓取脚本
├── requirements.txt             # Python 依赖
└── README.md
```

## 🔧 依赖

- Python 3.11+
- requests
- beautifulsoup4

## 📊 数据来源

- [GitHub Trending](https://github.com/trending)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License
