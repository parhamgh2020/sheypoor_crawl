import asyncio
from pprint import pprint

from bs4 import BeautifulSoup
import aiohttp

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


async def fetch_one_url(s, url):
    try:
        async with s.get(url) as r:
            if r.status != 200:
                r.raise_for_status()
            return await r.text()
    except:
        return None


async def fetch_all(s, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_one_url(s, url))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def run_fetch(urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        results = await fetch_all(session, urls)
        return results

# if __name__ == "__main__":
#     urls = [
#         "https://toplearn.com/",
#         "https://www.varzesh3.com/",
#         "https://www.sheypoor.com/",
#         "https://www.google.com/",
#     ]
#     results = asyncio.run(run_fetch(urls))
#     soups = [BeautifulSoup(http, features="html.parser") for http in results if http]
#     titles = [soup.title for soup in soups]
#     pprint(titles)
