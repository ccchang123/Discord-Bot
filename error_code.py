import asyncio

async def permission(error, Lang):
    await error.channel.send(Lang['permission-error'], delete_after=1)
    await asyncio.sleep(1)
    await error.message.delete()