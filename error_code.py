import discord
async def permission(error, Lang):
    embed = discord.Embed(title=Lang['permission-error'], color=0xEC2E2E)
    await error.channel.send(embed=embed)