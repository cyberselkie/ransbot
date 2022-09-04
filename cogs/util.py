import discord
import numpy as np
import pandas as pd
from discord import InputText, Option, OptionChoice
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.utils import get
import datetime
from datetime import date, datetime

#required variables
servers=[957056381154918461,747312626605883423]

#Google Sheet Info
sheet = "https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid={}"
infosheet_id="1zhrJue-WXa6p1kRFqtdcDnqFQosXofHvEmCrY3JXYqQ"


class util(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    #slash command group time
    info = SlashCommandGroup("info", "PC directory related commands.")
    wiki = SlashCommandGroup("wiki", "Find exact wiki page or search the wiki.")
    #------INFO COMMAND GROUP------
    #City Lookup
    @info.command(guild_ids=servers, description="Look up the links for a city.")
    async def city(self, ctx,*,lookup= Option(str,"Name of the city or region you want to look up.",choices=["Zaichaer","Kalzasi","Imperium","Ecith","Solunarium"])):
        url = sheet.format(infosheet_id, "315884010")
        data=pd.read_csv(url)
        df=pd.DataFrame(data)
        city=df[lookup.title()]
        embed = discord.Embed(
        title=lookup.title(),
        description=city[0],
        colour = discord.Colour.blue()
        )

        # embed.set_footer(text="This is a footer")
        # embed.set_image(url='https://i.imgur.com/VOiAxE8.jpg')
        embed.set_author(name=city[4],icon_url='https://i.imgur.com/VOiAxE8.jpg')
        embed.add_field(name='Forum Links',value='[Forum]('+city[1]+')'+'\n '+'[Codex]('+city[2]+')'+'\n '+'[Character Registry]('+city[3]+')',inline=False)
        await ctx.respond(embed=embed)

    #Open City Lookup
    @info.command(name="open", guild_ids=servers, description="Pull up a list of open cities and regions.")
    async def open_(self, ctx):
        url = sheet.format(infosheet_id, "267986942")
        data = pd.read_csv(url)
        df=pd.DataFrame(data)
        city=df['Cities'].tolist()
        open_cities = "The following cities are open for play: "
        for i in city:
            open_cities+= i+", "
        await ctx.respond(open_cities)

    #Command Lookup
    @info.command(guild_ids=servers, description="A list of commands currently available with RanseraBot.")
    async def commands(self, ctx):
        url = sheet.format(infosheet_id, "1385919884")
        data = pd.read_csv(url)
        df=pd.DataFrame(data)
        comm=df['Commands'].tolist() 
        commands1 = ""
        commands2 = ""
        cmax=10
        c1 = 0
        c2 = 0
        for i in comm: #Iterate through the google sheet with the commands
            if c1 < cmax:
                commands1+= i+"\n"
                c1+=1
            elif c2 < cmax:
                commands2+= i+"\n"
                c2+=1
            else:
                pass
        embed=discord.Embed(
            title="RanseraBot v2",
            description="RanseraBot was built to help the staff and players of [Ransera](https://legendofransera.com/). It comes with several useful commands that will give players more information about the world, and a handful of fun features that we hope will add to the enjoyment of the game.",
            colour=discord.Colour.purple())
        embed.add_field(name="Commands",value= commands1)
        embed.add_field(name="Commands Cont.",value= commands2)
        await ctx.respond(embed=embed)

    #Basic Lookup
    @info.command(guild_ids=servers, description="General, useful links for Ransera.")
    async def ransera(self, ctx):
        url = sheet.format(infosheet_id, "1250196624")
        data=pd.read_csv(url)
        df=pd.DataFrame(data)
        nwiki=df["Wiki"].tolist() 
        wmax = len(nwiki)
        wlinks=df["Wiki Links"]
        nforum=df["Forum"].tolist()
        fmax = len(nforum)
        flinks=df["Forum Links"]
        forum = "" #forum links embed
        fnum = 0
        for i in nforum:
            if fnum < fmax-1:
                forum+=f"[{i}]({str(flinks[fnum])})"
                forum+='\n'
                fnum+=1
            else:
                pass
        wiki = "" #wiki links embed
        wnum = 0
        for i in nwiki:
            if wnum < wmax:
                wiki+=f"[{i}]({str(wlinks[wnum])})"
                wiki+='\n'
                wnum+=1
            else:
                pass
        embed = discord.Embed(
            title="Ransera",
            description= "Ransera is a play by post forum that blends elements of high fantisy with semi-modern undertones. It is a world where knights and mages ride on air ships and trains powered by magical crystals, where guns are not uncommon to see next to a wand or staff. The world of Ransera is filled with adventure to be had, and you the player have an impact on the world as a whole.",
            colour = discord.Colour.red()
        )

        embed.set_image(url='https://legendofransera.com/ext/planetstyles/flightdeck/store/logo.png')
        embed.add_field(name="Forum Links",
        value=forum)
        embed.add_field(name="Wiki Links",
        value=wiki)

        await ctx.respond(embed=embed)
    
    #-------OTHER UTIL COMMANDS------
    #---- WIKI ---
    #Wiki Search
    @wiki.command(guild_ids=servers, description="Look up an article in the wiki. You do not have to use the exact page name.")
    async def search(self,ctx,*,article):
        link = f"https://legendofransera.com/wiki/index.php?search={article}"
        await ctx.respond(link)
    
    #Exact Page Lookup
    @wiki.command(guild_ids=servers, description="Look up an article in the wiki. Use the exact page name.")
    async def lookup(self,ctx,*,article):
            article=article.title()
            final=article.replace(" ", "_")
            link="https://legendofransera.com/wiki/index.php?title=%s" %(final)
            await ctx.respond(link)

    #Season!
    @discord.slash_command(guild_ids=servers, description="The current season of Ransera, and the countdown to the next.")
    async def season(self, ctx):
    # get the current day of the year
        doy = datetime.today().timetuple().tm_yday
    #get the rest of the information
        url = sheet.format(infosheet_id, "1041011236")
        data = pd.read_csv(url)
        df = pd.DataFrame(data)
        links=df['Links']
        city=df['City']
        linklist = ""
        num = 0
        for i in city: #iterate through the cities
            linklist+=f"[{str(city[num].title())}]({str(links[num])})"
            linklist+='\n'
            num+=1
        
     # season ranges
        glade = range(60, 152)
        searing = range(152, 244)
        ash = range(244, 334)
        if doy in glade:
            season = 'Glade 123 AoS'
            countdown = abs(152 - doy)
            seasoncolor = discord.Colour.green()
            nextseason = 'Searing'
        elif doy in searing:
            season = 'Searing 123 AoS'
            countdown = abs(244 - doy)
            seasoncolor = discord.Colour.gold()
            nextseason = 'Ash'
        elif doy in ash:
            season = 'Ash 122 AoS'
            countdown = abs(334 - doy)
            seasoncolor = discord.Colour.dark_orange()
            nextseason = 'Frost'
        else:
            season = 'Frost 122 AoS'
            countdown = abs(60 - doy)
            seasoncolor = discord.Colour.blue()
            nextseason = 'Glade'

        if countdown <= 5:
            embed = discord.Embed(
                title="Current Season",
                description=f"It is currently {season} and there are {str(countdown)} days until {nextseason}."+ '\n' + '\n' + "**Don't forget to make placeholders if you need them!**"+ '\n ' +
                '[Wage & CNPC EXP Requests](https://ransera.com/viewtopic.php?f=15&t=406)',
                colour=seasoncolor
            )
        else:
            embed = discord.Embed(
                title="Current Season",
                description=f"It is currently {season} and there are {str(countdown)} days until {nextseason}.",
                colour=seasoncolor
            )

            embed.add_field(name="Calendar Links & Events",
                     value=linklist)

        await ctx.respond(embed=embed)

    #Pronouns Assignment
    @discord.slash_command(guild_ids=servers, description="Assign pronoun roles to yourself. Please contact a mod for custom pronouns or role unassignment!")
    async def pronouns(self,ctx,pronouns: Option(str, choices=['He', 'She', 'They'])):
        member = ctx.author
        he = get(member.guild.roles, name="He/Him")
        she = get(member.guild.roles, name="She/Her")
        they = get(member.guild.roles, name="They/Them")
        if pronouns == "She":
            await member.add_roles(she)
            await ctx.respond("You have been given the role She/Her.")
        elif pronouns == "They":
            await member.add_roles(they)
            await ctx.respond("You have been given the role They/Them.")
        elif pronouns == "He":
            await member.add_roles(he)
            await ctx.respond("You have been given the role He/Him.")
        else:
            await ctx.respond("Available commands are **she**, **they**, and **he**. If you would like a custom pronouns role, please ask a mod!")

def setup(bot):
    bot.add_cog(util(bot))