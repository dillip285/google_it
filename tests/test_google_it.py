import google_it
import pytest


@pytest.mark.asyncio
async def test_search_query():
    search_results = google_it.search('Stephen Hawking')
    print(search_results)
    assert len(search_results) > 0


@pytest.mark.asyncio
async def test_search_images():
    image_results = google_it.image('Supermassive Blackhole')
    assert len(image_results) > 0


@pytest.mark.asyncio
async def test_get_top_news():
    news = google_it.get_top_news('en', 'AU')
    assert len(news.headline_stories) > 0
