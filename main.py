import discord
from discord.ext import commands, tasks

from conf import config
from parse import get_new_news, parse_rss_feed
from db_utils import (add_news_to_cache, add_subscriber, create_tables, get_news_cache, get_subscribers, remove_subscriber)

RSS_URL = config.get('RSS_URL')
BOT_TOKEN = config.get('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    create_tables()
    fetch_news.start()


@bot.command()
async def subscribe(ctx):
    add_subscriber(ctx.author.id)
    await ctx.send(f'{ctx.author.mention}, вы успешно подписались на новостную рассылку!')


@bot.command()
async def unsubscribe(ctx):
    remove_subscriber(ctx.author.id)
    await ctx.send(f'{ctx.author.mention}, вы успешно отписались от новостной рассылки.')


@tasks.loop(minutes=3)
async def fetch_news():
    news_items = parse_rss_feed(RSS_URL)
    news_cache = get_news_cache()
    new_news = get_new_news(news_items, news_cache)

    if new_news:
        subscribers = get_subscribers()
        for subscriber_id in subscribers:
            user = await bot.fetch_user(subscriber_id)
            for item in new_news:
                await user.send(f"Новость: {item['title']}\nСсылка: {item['link']}\nДата: {item['published']}")
                add_news_to_cache(item)


bot.run(BOT_TOKEN)
