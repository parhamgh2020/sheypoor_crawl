import asyncio

import aiohttp


async def fetch_one_url(s, url):
    async with s.get(url) as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.text()


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
