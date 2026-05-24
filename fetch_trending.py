#!/usr/bin/env python3
"""
Fetch GitHub Trending and save as markdown digest.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def fetch_trending():
    """Fetch GitHub Trending page and parse repositories."""
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=30, verify=False)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='Box-row')
    
    repos = []
    for article in articles[:15]:  # Top 15
        # Extract repo name
        h2 = article.find('h2', class_='h3')
        if h2:
            repo_link = h2.find('a')
            repo_name = repo_link['href'].strip('/') if repo_link else None
        else:
            repo_name = None
            
        # Extract description
        desc_p = article.find('p', class_='col-9')
        description = desc_p.get_text(strip=True) if desc_p else "No description"
        
        # Extract language
        lang_span = article.find('span', itemprop='programmingLanguage')
        language = lang_span.get_text(strip=True) if lang_span else "N/A"
        
        # Extract stars
        stars_a = article.find('a', href=lambda x: x and '/stargazers' in x)
        stars = stars_a.get_text(strip=True) if stars_a else "0"
        
        # Extract today's stars
        stars_today_span = article.find('span', class_='float-sm-right')
        stars_today = "N/A"
        if stars_today_span:
            text = stars_today_span.get_text(strip=True)
            if 'stars today' in text:
                stars_today = text.split('stars')[0].strip()
        
        if repo_name:
            repos.append({
                'name': repo_name,
                'description': description,
                'language': language,
                'stars': stars,
                'stars_today': stars_today
            })
    
    return repos

def generate_markdown(repos):
    """Generate markdown digest from repos list."""
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M GMT+8')
    
    md = f"# GitHub 日报 - {today}\n\n"
    md += f"**生成时间**: {now}  \n"
    md += f"**数据来源**: GitHub Trending (自动抓取)\n\n"
    md += "---\n\n"
    md += "## 🔥 Top 15 趋势项目\n\n"
    
    for i, repo in enumerate(repos, 1):
        md += f"### {i}. {repo['name']} ⭐ {repo['stars']} (+{repo['stars_today']} today)\n"
        md += f"- **语言**: {repo['language']}\n"
        md += f"- **简介**: {repo['description']}\n"
        md += f"- **GitHub**: https://github.com/{repo['name']}\n\n"
    
    md += "---\n\n"
    md += "**自动生成**: 由 GitHub Actions 每日自动抓取\n"
    
    return md

def save_digest(md_content):
    """Save digest to file."""
    today = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('digest', exist_ok=True)
    
    filename = f"digest/{today}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Saved digest to {filename}")
    return filename

if __name__ == '__main__':
    # Fix Windows console encoding issue
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("[START] Fetching GitHub Trending...")
    repos = fetch_trending()
    print(f"[OK] Fetched {len(repos)} repositories")
    
    md_content = generate_markdown(repos)
    filename = save_digest(md_content)
    
    print(f"[OK] Digest saved to {filename}")
