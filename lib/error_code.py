import discord
async def permission(ctx, Lang):
    embed = discord.Embed(title='⛔｜'+Lang['permission-error'], color=0xEC2E2E)
    await ctx.channel.send(embed=embed)

async def bypass(ctx, Lang):
    embed = discord.Embed(title='❌｜'+Lang['user-bypassed'], color=0xEC2E2E)
    await ctx.channel.send(embed=embed)