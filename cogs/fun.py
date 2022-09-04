import discord
from discord import Option
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.utils import get
import numpy as np
import pandas as pd
import random
import typing
from typing import List


servers=[957056381154918461,747312626605883423]

#Google Sheet Info
sheet = "https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid={}"
infosheet_id="1zhrJue-WXa6p1kRFqtdcDnqFQosXofHvEmCrY3JXYqQ"

# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used.
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

# This is our actual board View.
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons.
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner and is used by the TicTacToeButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # If we're here, we need to check if a tie has been reached.
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

class fun(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        
    # Tic Tac Toe ------------------

    @discord.slash_command(guild_ids=servers, description="Play Tic-Tac-Toe!")
    async def tic(self, ctx: commands.Context):
        """Starts a tic-tac-toe game with yourself."""
        # Setting the reference message to ctx.message makes the bot reply to the member's message.
    
        await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())
    
    pd.set_option('display.max_colwidth', None)

    #Quotes!!
    @discord.slash_command(guild_ids=servers, description="Pull a random quote from our quotes bank!")
    async def quote(self, ctx, name=Option(str,"The name of who you want a quote from.",choices=["Talon"])):
        url = sheet.format(infosheet_id, "1852740932")
        data = pd.read_csv(url)
        df = pd.DataFrame(data)
        column_index = df.columns.get_loc(name.title())
        quote_size = df[df.columns[column_index]].count()
        var=random.randint(0,quote_size-1)
        quote=df.iloc[var][name.title()]
        await ctx.respond(quote)
        
    #fortunetelling
    @discord.slash_command(guild_ids=servers, description="Tell your fortune!")
    async def fortune(self, ctx):
        url = sheet.format(infosheet_id, '1232354598')
        data= pd.read_csv(url)
        df = pd.DataFrame(data)
        #fortune ranomizer
        index = df.columns.get_loc('fortune')
        size = df[df.columns[index]].count()
        var=random.randint(0,size-1)
        fortune=df.iloc[var]['fortune']
        await ctx.respond(fortune)

def setup(bot):
    bot.add_cog(fun(bot))
