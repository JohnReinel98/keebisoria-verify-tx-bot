from typing import Optional
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

#local
import utilities as util

class Confirm(nextcord.ui.View):
   def __init__(self):
      super().__init__()
      self.value = None

   @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
   async def confirm(self, button: nextcord.ui.Button, interaction: Interaction):
      fields = interaction.message.embeds[0].fields

      clicker = str(interaction.user.id)
      tag_id = str(fields[5].value.translate(str.maketrans('', '', '<@!>')))

      if (clicker != tag_id):
         return None
      else:
         embed = nextcord.Embed(color=0x00BCE3, title="Verify Transaction")
         embed.add_field(name="Type", value=fields[0].value, inline=False)
         embed.add_field(name="Item", value=fields[1].value, inline=True)
         embed.add_field(name="Price", value=fields[2].value, inline=True)
         embed.add_field(name="Details", value=fields[3].value, inline=False)
         embed.add_field(name="Author", value=fields[4].value, inline=True)
         embed.add_field(name="Tag", value=fields[5].value, inline=True)
         embed.add_field(name="Photo", value=fields[6].value, inline=False)
         embed.add_field(name="Status", value="Confirmed", inline=False)
         return await interaction.response.edit_message(embed=embed, view=None)

class DropDown(nextcord.ui.Select):
   def __init__(self):
      options = [
         nextcord.SelectOption(label="Sold", description="Choose if item sold."),
         nextcord.SelectOption(label="Bought", description="Choose if item bought."),
         nextcord.SelectOption(label="Traded", description="Choose if item traded."),
      ]
      super().__init__(placeholder="Choose Transaction Type...", min_values=1, max_values=1, options=options)

   async def callback(self, interaction: Interaction):
      fields = interaction.message.embeds[0].fields

      embed = nextcord.Embed(color=0x00BCE3, title="Verify Transaction")
      embed.add_field(name="Type", value=self.values[0], inline=False)
      embed.add_field(name="Item", value=fields[0].value, inline=True)
      embed.add_field(name="Price", value=fields[1].value, inline=True)
      embed.add_field(name="Details", value=fields[2].value, inline=False)
      embed.add_field(name="Author", value=fields[3].value, inline=True)
      embed.add_field(name="Tag", value=fields[4].value, inline=True)
      embed.add_field(name="Photo", value=fields[5].value, inline=False)
      embed.add_field(name="Status", value="Unconfirmed", inline=False)
      view = Confirm()
      return await interaction.response.send_message(embed=embed, view=view)

class DropDownView(nextcord.ui.View):
   def __init__(self):
      super().__init__()
      self.add_item(DropDown())

class Misc(commands.Cog):

   def __init__(self, client):
      self.client = client

   #config load
   config = util.loadConfig()

   self_server_id = config["self_server_id"]

   @nextcord.slash_command(name = "verify", description = "Verify a transaction.", guild_ids=[self_server_id])
   async def verify(self, interaction: Interaction, tag: nextcord.Member, item, price: float, details, imgur: Optional[str]):
      author = interaction.user.mention
      view = DropDownView()
      embed = nextcord.Embed(color=0x00BCE3, title="Verify Transaction")
      embed.add_field(name="Item", value=item, inline=True)
      embed.add_field(name="Price", value=f'₱{"{:.2f}".format(price)}', inline=True)
      embed.add_field(name="Details", value=details, inline=False)
      embed.add_field(name="Author", value=author, inline=True)
      embed.add_field(name="Tag", value=tag.mention, inline=True)
      embed.add_field(name="Photo", value=imgur, inline=False)
      await interaction.response.send_message(embed=embed, view=view, ephemeral=True, delete_after=10)

def setup(client):
   client.add_cog(Misc(client))