import discord
async def permission(ctx, Lang):
    embed = discord.Embed(title='⛔｜'+Lang['permission-error'], color=0xEC2E2E)
    await ctx.channel.send(embed=embed)