import asyncio

async def no_permission(no_permission_message):
    permission_error = await no_permission_message.channel.send('你沒有權限')
    await asyncio.sleep(1)
    await permission_error.delete()
    await no_permission_message.delete()