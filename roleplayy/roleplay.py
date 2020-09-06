import discord
from redbot.core import commands, Config
from random import randint
import aiohttp
import logging

log = logging.getLogger("Roleplay")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Roleplay(BaseCog):
    """Interact with people!"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {

            "kill": [
                "https://img2.gelbooru.com/images/ff/63/ff63a3c4329fda2bf1e9704d4e150fea.gif",
                "https://img2.gelbooru.com/images/2c/e8/2ce81403e0279f1a570711f7472b3abb.gif",
                "https://img2.gelbooru.com/images/e2/05/e205e349535e22c07865913770dcad5f.gif",
                "https://img2.gelbooru.com/images/09/f6/09f63a79f70700abb2593862525ade10.gif",
                "https://safebooru.org//images/1174/5ebeacd87b22a0c5949ecb875667ae75702c2fed.gif",
                "https://safebooru.org//images/848/4828fc43e39f52abd5bac6b299e822ae02786974.gif",
                "https://safebooru.org//images/160/ba09bc95bc05b4f47af22671950e66f085c7ea9e.gif",
                "https://img2.gelbooru.com/images/3f/73/3f73b1c3703d91a9300aebdaab6e26c0.gif",
                "https://img2.gelbooru.com/images/7d/7c/7d7c8ce0c4e561804f16adc7907a78e8.gif",
                "https://img2.gelbooru.com/images/5e/8c/5e8c1a33470c62f6907d0ea5a03ae644.gif",
                "https://img2.gelbooru.com/images/2b/b9/2bb9dc89cf991181bce06279d8d5f0f4.gif",
                "https://cdn.weeb.sh/images/rJaog0FtZ.gif",
                "https://cdn.weeb.sh/images/Hyv6uOQPZ.gif",
                "https://cdn.weeb.sh/images/BJx2l0ttW.gif",
                "https://cdn.weeb.sh/images/Hk4qu_XvZ.gif",
                "https://cdn.weeb.sh/images/ByuHsvu8z.gif",
                "https://cdn.weeb.sh/images/Hy4hxRKtW.gif",
                "https://cdn.weeb.sh/images/Sk2gmRZZG.gif",
                "https://cdn.weeb.sh/images/HkfgF_QvW.gif",
                "https://cdn.weeb.sh/images/HJTWcTNCZ.gif",
                "https://cdn.weeb.sh/images/rko9O_mwW.gif",
                "https://cdn.weeb.sh/images/rkx1dJ25z.gif",
                "https://media.giphy.com/media/KMQoRt68bFei4/giphy.gif",
                "https://cdn.weeb.sh/images/BkZngAYtb.gif",
            ],
            "cuddle": [
                "https://cdn.weeb.sh/images/BkTe8U7v-.gif",
                "https://cdn.weeb.sh/images/SykzL87D-.gif",
                "https://cdn.weeb.sh/images/BywGX8caZ.gif",
                "https://cdn.weeb.sh/images/SJceIU7wZ.gif",
                "https://cdn.weeb.sh/images/SJn18IXP-.gif",
                "https://cdn.weeb.sh/images/B1Qb88XvW.gif",
                "https://cdn.weeb.sh/images/r1XEOymib.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/SyUYOJ7iZ.gif",
                "https://cdn.weeb.sh/images/rkBl8LmDZ.gif",
                "https://cdn.weeb.sh/images/Byd1IUmP-.gif",
                "https://cdn.weeb.sh/images/B1S1I87vZ.gif",
                "https://cdn.weeb.sh/images/r1s9RqB7G.gif",
                "https://cdn.weeb.sh/images/Hy5y88mPb.gif",
                "https://cdn.weeb.sh/images/rkA6SU7w-.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
                "https://cdn.weeb.sh/images/SJYxIUmD-.gif",
                "https://cdn.weeb.sh/images/H1SfI8XwW.gif",
                "https://cdn.weeb.sh/images/rJCAH8XPb.gif",
                "https://cdn.weeb.sh/images/By03IkXsZ.gif",
                "https://cdn.weeb.sh/images/ryfyLL7D-.gif",
                "https://cdn.weeb.sh/images/BJwpw_XLM.gif",
                "https://cdn.weeb.sh/images/r1VzDkmjW.gif",
                "https://cdn.weeb.sh/images/BJkABImvb.gif",
                "https://cdn.weeb.sh/images/HkzArUmvZ.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
            ],

        }
        self.config.register_global(**default_global)



    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kill(self, ctx, *, user: discord.Member):
        """Cuddles a user!"""

        author = ctx.message.author
        images = await self.config.cuddle()

        nekos = await self.fetch_nekos_life(ctx, "cuddle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} killed {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)


    async def fetch_nekos_life(self, ctx, rp_action):

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.nekos.dev/api/v3/images/sfw/gif/{rp_action}/?count=20") as resp:
                try:
                    content = await resp.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError) as ex:
                    log.debug("Pruned by exception, error below:")
                    log.debug(ex)
                    return []

        if content["data"]["status"]["code"] == 200:
            return content["data"]["response"]["urls"]

