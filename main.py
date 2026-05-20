import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import os
from datetime import datetime, timedelta

# ================= CONFIG =================
TICKET_CHANNEL_ID = 1412218164607057937
TICKET_CATEGORY_ID = 1434521318744657950
ARCHIVE_CATEGORY_ID = 1412218165017972752
AVALIACAO_CHANNEL_ID = 1412218164607057934
LOG_CHANNEL_ID = 1412218164774699127
STATUS_CHANNEL_ID = 1492005222967677070

status_entregas = False
PIX_KEY = "SUA_CHAVE_PIX_AQUI"

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

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"🟢 Ticket Aberto\n👤 {interaction.user.mention}\n📦 {item['nome']}"
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

        view = View(timeout=None)

        async def finalizar(i):
            if not i.user.guild_permissions.administrator:
                await i.response.send_message("Só ADM pode finalizar.", ephemeral=True)
                return

            archive_category = discord.utils.get(guild.categories, id=ARCHIVE_CATEGORY_ID)

            await channel.set_permissions(interaction.user, send_messages=False)
            await channel.edit(category=archive_category)

            await i.response.send_message("Pedido finalizado!")

        async def cancelar(i):
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

        await channel.send(embed=embed, view=ShopView())

# ================= START =================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("ERRO: TOKEN não encontrado!")
else:
    bot.run(TOKEN)
