import discord
from discord import Option
from discord.commands import SlashCommandGroup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cogs.variables import variables

servers=variables.servers
infosheet_id= variables.infosheet_id

gc = gspread.service_account(filename='client_key.json')
url = gc.open_by_key(infosheet_id)
worksheet = url.worksheet("sheets")
#CLASS FOR THE MODAL/INPUT BOX ------------
class CharacterInput(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Name", placeholder="Character Name",required=True)) #0
        self.add_item(discord.ui.InputText(label="Link to Character Sheet", placeholder="https://legendofransera.com/...",required=True)) #1
        self.add_item(discord.ui.InputText(label="Is this PC available for new threads?", placeholder="Yes? No? Maybe!",required=True)) #2
        self.add_item(discord.ui.InputText(label="Location", placeholder="Somewhere in Ransera...", required=True)) #3

    async def callback(self, interaction: discord.Interaction):
        csname = self.children[0].value
        cslink = self.children[1].value
        csavail = self.children[2].value
        csloc = self.children[3].value
        def next_available_row(worksheet): #finding next open row
            str_list = list(filter(None, worksheet.col_values(1)))
            return str(len(str_list)+1)
        next_row = next_available_row(worksheet)
        worksheet.update_acell("A{}".format(next_row), csname)
        name = worksheet.find(csname)
        row = name.row
        worksheet.update_cell(row, 2, cslink)
        worksheet.update_cell(row, 3, csavail)
        worksheet.update_cell(row, 4, csloc)
        #Embed with submitted information
        embed = discord.Embed(title="You have submitted your character to the directory!",
                            description= """Here is the information you have submitted. 
List the characters in the directory with /directory, or lookup a specific character with /lookup [PC name].
Update your character with /update [character name] [location] [availability].
                            """,
                            color=discord.Colour.green(),)
        embed.add_field(name="Name", value=f"[{csname}]({cslink})")
        embed.add_field(name="Location", value=csloc)
        embed.add_field(name="Thread Availability?", value=csavail)
        await interaction.response.send_message(embed=embed)


class playercharacter(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    #slash command group time
    pchar = SlashCommandGroup("pc", "PC directory related commands.")


    @pchar.command(guild_ids=servers, description="Add a new character to the directory.")
    async def add(self, ctx: discord.ApplicationContext):
        modal = CharacterInput(title="Add your PC to the directory!")
        await ctx.send_modal(modal)

    @pchar.command(guild_ids=servers, description="Shows the list of characters in the directory.")
    async def directory(self, ctx: discord.ApplicationContext):
        names_list = worksheet.col_values(1)
        names_dir = ""
        for i in names_list:
            names_dir += i+"\n"
        await ctx.respond(names_dir)

    #lookup a character!
    @pchar.command(guild_ids=servers, description="Look up a character in the directory.")
    async def lookup(self, ctx: discord.ApplicationContext, name=Option(str, "Name of the character. Must be a name in the directory. Use /character directory if you are unsure.", required=True)):
        pc = worksheet.find(name.lower())
        row = pc.row
        #lookups
        csname = worksheet.cell(row, 1).value
        cslink = worksheet.cell(row, 2).value
        csavail = worksheet.cell(row, 3).value
        csloc = worksheet.cell(row, 4).value
        #real embed hours
        embed = discord.Embed(title=csname,
                                color=discord.Colour.random(),)
        embed.add_field(name= "Character Sheet", value=f"[Link!]({cslink})")
        embed.add_field(name="Location", value=csloc)
        embed.add_field(name="Thread Availability?", value=csavail)
        await ctx.respond(embed=embed)

    #update a character!
    @pchar.command(guild_ids=servers, description="Update a character in the directory.")
    async def update(self, ctx: discord.ApplicationContext, name=Option(str, "Name of the character. Must be a name in the directory. Use /directory if you are unsure.", required=True), 
                                                    location=Option(str, "The location your PC is in now.", required=True),
                                                    avail=Option(str, "Your current thread availability.", required=True)):
        pc = worksheet.find(name.lower())
        row = pc.row
        # Updating the Sheet ---
        worksheet.update_cell(row, 3, avail)
        worksheet.update_cell(row, 4, location)

        #lookups
        csname = worksheet.cell(row, 1).value
        cslink = worksheet.cell(row, 2).value
        csavail = worksheet.cell(row, 3).value
        csloc = worksheet.cell(row, 4).value
        #real embed hours
        embed = discord.Embed(title=csname,
                                color=discord.Colour.random())
        embed.add_field(name= "Character Sheet", value=f"[Link!]({cslink})")
        embed.add_field(name="Location", value=csloc)
        embed.add_field(name="Thread Availability?", value=csavail)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(playercharacter(bot))