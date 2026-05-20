import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import os
from datetime import datetime, timedelta

# ================= CONFIG =================
bot.run(os.getenv("TOKEN"))
TICKET_CHANNEL_ID = 1412218164607057937
TICKET_CATEGORY_ID = 1434521318744657950
ARCHIVE_CATEGORY_ID = 1412218165017972752
AVALIACAO_CHANNEL_ID = 1412218164607057934
LOG_CHANNEL_ID = 1412218164774699127  # 🔥 LOGS AQUI
STATUS_CHANNEL_ID = 1492005222967677070
status_entregas = False  # começa OFF

PIX_KEY = "f5e19e12-d8d9-4ead-8985-54da17dd140b"

MAX_TICKETS = 2
SALES_FILE = "vendas.txt"

if not os.path.exists(SALES_FILE):
    open(SALES_FILE, "w").close()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

cancel_control = {}

# ================= LOJA =================
shop = {
   
    "accension_5": {
        "nome": "🔮 Ascensão 1 até 5",
        "preco": "R$6,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491942338480701540/content.png"
    },
    "accension_10": {
        "nome": "🔮 Ascensão 5 até 10",
        "preco": "R$15,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491942338480701540/content.png"
    },
    "aby_sigil": {
        "nome": "🎀 (150x) Abyssal Sigil",
        "preco": "R$3,50",
        "img": "https://cdn.virtualities.com.br/catalog/product-f9ee454138ef7df52f2912fa09aa3a02.webp"
    },
    "Power_shard": {
        "nome": "🎀 (150x) Power Shard",
        "preco": "R$3,50",
        "img": "https://cdn.virtualities.com.br/catalog/product-740ef37f9e1269518d0d79434991389d.webp"
    },
    "Frost_Relic": {
        "nome": "🎀 (150x) Frost Relic",
        "preco": "R$4,00",
        "img": "https://cdn.discordapp.com/attachments/1339672109793935360/1491478635323068459/image.png"
    },
    "upper_seal": {
        "nome": "🎀 (150x) Upper Seal",
        "preco": "R$5,50",
        "img": "https://cdn.virtualities.com.br/catalog/product-e016fee17e9a38ea3e3829b2eb436a04.webp"
    },
    "Broken_sword": {
        "nome": "🎀 (150x) Broken Swords",
        "preco": "R$3,50",
        "img": "https://cdn.virtualities.com.br/catalog/product-d2e038a4c1bb8bd3c24185d0c75d8a3b.webp"
    },
    "reroll_clan": {
        "nome": "🔄 (100x) Clan Reroll",
        "preco": "R$1,50",
        "img": "https://cdn.virtualities.shop/catalog/product-16297cc6201266ea7476b4c041a9cfe5.webp"
    },
    "reroll_race": {
        "nome": "🧬 (1000x) Race Reroll",
        "preco": "R$1,15",
        "img": "https://cdn.virtualities.shop/catalog/product-b109b4ac544fb6d96cbd1327207d114f.webp"
    },
    "divine_grail": {
        "nome": "🎀 (155x) Divine Grail",
        "preco": "R$10,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951362089418853/image.png"
    },
    "tempest_relic": {
        "nome": "🎀 (155x) Tempest Relic",
        "preco": "R$4,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951361804341320/image.png"
    },
    "slime_key": {
        "nome": "🎀 (155x) Slime Key",
        "preco": "R$5,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951361544425572/image.png"
    },

    "madara_Iceqqueen": {
        "nome": "💥(Especial da Update) Set da Ice Queen",
        "preco": "R$13,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491908057137938473/image.png"
    },
    "Set_madara": {
        "nome": "🔥 Set Madara",
        "preco": "R$10,20",
        "img": "https://cdn.discordapp.com/attachments/1412218164607057939/1491480544695947388/image.png"
    },
    "set_guilga": {
        "nome": "🔥 Set Completo Guilga",
        "preco": "R$6,50",
        "img": "https://cdn.virtualities.com.br/catalog/product-7a05145c80de5d4607aee7a215e634ea.png"
    },
    "f_guilga": {
        "nome": "🔥 F do Guilga",
        "preco": "R$6,50",
        "img": "https://cdn.discordapp.com/attachments/1339672109793935360/1491213973385773187/image.png"
    },
    "set_atomic": {
        "nome": "🔮 Set Atomic",
        "preco": "R$8,90",
        "img": "https://cdn.discordapp.com/attachments/1412218164607057939/1491463841240977640/image.png"
    },
    "set_saber": {
        "nome": "⚔️ Set Completo Saber",
        "preco": "R$6,50",
        "img": "https://cdn.virtualities.shop/catalog/product-85946a787ed0f93222826dbf55619d70.png"
    },
    "set_rimuru": {
        "nome": "❄️ Set Rimuru",
        "preco": "R$6,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951361309278308/image.png"
    },
    "set_anos": {
        "nome": "🔥 Set Demon King",
        "preco": "R$6,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951361015681266/image.png"
    },
    "set_blessed": {
        "nome": "✨ Set Blessed Maiden",
        "preco": "R$6,50",
        "img": "https://cdn.discordapp.com/attachments/1449247545728696576/1491951843125887068/image.png"
    },
    
    

    "aura": {
        "nome": "✨ (1x) Aura Crate",
        "preco": "R$2,20",
        "img": "https://cdn.virtualities.shop/catalog/product-5f24a3325a89f08f17110ef25944d3db.webp"
    },
    "cosmetic": {
        "nome": "🎁 (1x) Cosmetic Crate",
        "preco": "R$2,20",
        "img": "https://cdn.virtualities.shop/catalog/product-de811a89462c287485003289c18d1db2.webp"
    },
    "100_baumitico": {
        "nome": "🎁 (100x) Baú Mítico",
        "preco": "R$3,20",
        "img": "https://cdn.virtualities.shop/catalog/product-c0ceab3d0461cd9d428bece5208937ab.webp"
    }
}


# ================= MENU =================
class ShopSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=data["nome"],
                description=f"💰 {data['preco']}",
                value=key
            )
            for key, data in shop.items()
        ]
        super().__init__(placeholder="Escolha o item...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.channel.id != TICKET_CHANNEL_ID:
            await interaction.response.send_message("Use no canal correto.", ephemeral=True)
            return

        uid = interaction.user.id
        guild = interaction.guild

        tickets = sum(
            1 for ch in guild.text_channels
            if str(uid) in ch.name and ch.category and ch.category.id == TICKET_CATEGORY_ID
        )

        if tickets >= MAX_TICKETS:
            await interaction.response.send_message("Você já tem 2 pedidos abertos.", ephemeral=True)
            return

        item = shop[self.values[0]]

        print(f"[ABERTO] {interaction.user} abriu ticket | Item: {item['nome']}")

        # 🔥 LOG ABERTURA
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"🟢 **Ticket Aberto**\n👤 {interaction.user.mention}\n📦 {item['nome']}"
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"pedido-{uid}",
            category=discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID),
            overwrites=overwrites
        )

        embed = discord.Embed(title="📦 Pedido Aberto", color=0x00ff88)
        embed.set_thumbnail(url=item["img"])
        embed.add_field(name="🛒 Item", value=item["nome"], inline=False)
        embed.add_field(name="💰 Preço", value=item["preco"], inline=True)
        embed.add_field(name="💳 Pix", value=PIX_KEY, inline=False)
        embed.add_field(
            name="⚠️ Importante",
            value="Envie o comprovante.\n\nEntrega apenas em servidor privado.\n\n⭐ Avalie em <#1412218164607057934>",
            inline=False
        )

        view = View(timeout=None)

        async def finalizar(i):
            if not i.user.guild_permissions.administrator:
                await i.response.send_message("Só ADM pode finalizar.", ephemeral=True)
                return

            print(f"[FINALIZADO] {i.user} finalizou ticket de {interaction.user}")

            # 🔥 LOG FINALIZADO
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    f"🟡 **Pedido Finalizado**\n👤 Cliente: {interaction.user.mention}\n🛠 Staff: {i.user.mention}\n📦 {item['nome']}"
                )

            archive_category = discord.utils.get(guild.categories, id=ARCHIVE_CATEGORY_ID)

            await channel.set_permissions(interaction.user, send_messages=False)
            await channel.edit(category=archive_category)

            await i.response.send_message("Pedido finalizado!")

        async def cancelar(i):
            now = datetime.now()
            user_id = i.user.id

            cancel_control.setdefault(user_id, [])
            cancel_control[user_id] = [t for t in cancel_control[user_id] if now - t < timedelta(minutes=20)]

            if len(cancel_control[user_id]) >= 2:
                await i.response.send_message("Limite de cancelamento.", ephemeral=True)
                return

            cancel_control[user_id].append(now)

            print(f"[CANCELADO] {i.user} cancelou ticket")

            # 🔥 LOG CANCELADO
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    f"🔴 **Pedido Cancelado**\n👤 {i.user.mention}\n📦 {item['nome']}"
                )

            await i.response.send_message("Cancelado.", ephemeral=True)
            await channel.delete()

        b1 = Button(label="Finalizar", style=discord.ButtonStyle.success)
        b2 = Button(label="Cancelar", style=discord.ButtonStyle.danger)

        b1.callback = finalizar
        b2.callback = cancelar

        view.add_item(b1)
        view.add_item(b2)

        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Criado: {channel.mention}", ephemeral=True)

class ShopView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ShopSelect())

# ================= EVENTOS =================

@bot.check
async def only_admins(ctx):
    # bloqueia DM também
    if ctx.guild is None:
        return False

    # permite só ADM
    return ctx.author.guild_permissions.administrator

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Só administradores podem usar comandos.")
        
        print(f"[BLOQUEADO] {ctx.author} ({ctx.author.id}) tentou usar comando em {ctx.channel}")
@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

    channel = bot.get_channel(TICKET_CHANNEL_ID)

    if channel:
        await channel.purge()

        embed = discord.Embed(
            title="🛒 Muts Store",
            description="Escolha um item abaixo 👇",
            color=0x6f00ff
        )

        file = discord.File("vabber.png", filename="vabber.png")
        embed.set_image(url="attachment://vabber.png")
        embed.set_footer(text="Atendimento rápido ⚡")

        await channel.send(embed=embed, view=ShopView(), file=file)

# ❤️ AUTO REAÇÃO NO CANAL DE AVALIAÇÃO
@bot.event
async def on_message(message):
    if message.channel.id == AVALIACAO_CHANNEL_ID and not message.author.bot:
        try:
            await message.add_reaction("❤️")
        except:
            pass

    await bot.process_commands(message)

@bot.command()
async def turnon(ctx):
    global status_entregas

    status_entregas = True
    channel = bot.get_channel(STATUS_CHANNEL_ID)

    if channel:
        await channel.edit(name="🚨 • Entregas: ON")

    await ctx.send("🚨 Status On")


@bot.command()
async def turnoff(ctx):
    global status_entregas

    status_entregas = False
    channel = bot.get_channel(STATUS_CHANNEL_ID)

    if channel:
        await channel.edit(name="🚨 • Entregas: OFF")

    await ctx.send("🚨 Status Off")

# ================= COMANDOS =================
@bot.command()
async def status(ctx):
    await ctx.send("🤖 Online!")

# ================= START =================


