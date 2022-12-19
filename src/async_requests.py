import asyncio
from pprint import pprint

from bs4 import BeautifulSoup
import aiohttp


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
    async with aiohttp.ClientSession() as session:
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
