import asyncio
import nest_asyncio
nest_asyncio.apply()

from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig

with open("links.txt","r",encoding="utf-8") as f:
    links = f.read().strip().split('\n')
async def simple_crawl(links):

    crawler_run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    
    async with AsyncWebCrawler() as crawler:
        for i, link in enumerate(links):
            result = await crawler.arun(
                url=link,
                config=crawler_run_config
            )
            
            # Create a safe filename by replacing invalid characters
            safe_filename = link.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace("?", "_").replace("&", "_")
            output_filename = f"page_{i+1:03d}_{safe_filename}.md"
            
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(result.markdown.raw_markdown)
            
            print(f"Content saved to {output_filename}")
            print(f"URL: {link}")
            print(f"Total characters: {len(result.markdown.raw_markdown)}")
            print("-" * 50)

asyncio.run(simple_crawl(links))
