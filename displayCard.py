import discord
from discord.ext import commands


async def displayCard(ctx, list_of_cards, card_to_draw):
    file = discord.File(
        f'C:/PATH_TO_CARD_IMAGES/{list_of_cards[card_to_draw]}', filename="image.png")
    embed_msg = discord.Embed(title='Card Drawer:', color=0x179142)
    embed_msg.add_field(name='Here is the card I drew from the deck',
                        value='...', inline=False)
    embed_msg.set_image(url="attachment://image.png")
    await ctx.send(file=file, embed=embed_msg)
