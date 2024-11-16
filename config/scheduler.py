from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.messages import daily_horo


async def setup_scheduler() -> AsyncIOScheduler:
    '''Настройка планировщика'''
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(daily_horo, trigger='cron', hour='10')
    return scheduler
