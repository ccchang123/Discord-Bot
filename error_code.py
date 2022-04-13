import asyncio

async def permission(error, Lang):
    permission_error = await error.channel.send(Lang['permission-error'])
    await asyncio.sleep(1)
    await permission_error.delete()
    await error.delete()