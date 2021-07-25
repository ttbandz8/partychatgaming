import discord
from discord.ext import commands
import DiscordUtils
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
import textwrap



class Senpai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Senpai Cog is ready!")

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    # @commands.command()
    # async def legend(self, ctx):
    #     embed1 = discord.Embed(title= f":crown: " + "Senpai™️ Legend:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn about Exhibitions, Kings Gambit and Gods of COD!\n*Write your name is history...*\n\n*The #legend tutorial will walk you through the Tournament System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
    #     embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed2 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#legend = Tournaments!", value="Welcome to Senpai:tm: Legend!\n(Commands are described in this format:arrow_down:\n\n#command 'argument' 'argument' ...etc )\n\n:warning:Do not go on before completing Senpai:tm: Franchise!\n*Use #franchise*")
    #     embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed3 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "*Exhibitions* :medal:", value="Exhibitions are 1v1 duels between 2 players!\n*Winner Gets 1 Tournament Win*\n\nHow can you join an exhibition you may ask?\nWell you can't, you'll be invited when your time comes.\n\n*Make sure you accept the Invitation*")
    #     embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed4 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#jkg to Join a *Kings Gambit* :crown:", value="Kings Gambits are King of the Hill Lobbies\nRules are....the KING picks the rules\nAdmins can start Kings Gambits matches open for all players\nPlayers can join using the #jkg 'AdminName' command\n\nBe the King at the end of the lobby to win extra :coin: and a Tournament Win!")
    #     embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed5 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gods of COD", value="Gods of Cod are the largest CODM tournaments Party Chat Gaming has to offer\nEach Tournament length, prize and rules are different and are announced before Registrations\nAs long as Registrations are open\nteams can use #rgoc to register their team for GOC\n\n*NOTE as long as 1 player in your team registers, your entire team will be registed!*")
    #     embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed6 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gauntlet Week", value="When the tournament starts, registration is closed and the games begin with The Gauntlet!\nWeeks of fierce competition betweem Teams!\n\nTournament Brackets will be determined based on the number of wins each team earns during Gauntlet Week!")
    #     embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed7 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Brackets", value="Brackets take place at the end of Gauntlet!\nTeams are placed according to their total number of wins!\nThe Brackets consist of single elimination matches\nThe Winner of the brackets earns Tournament exclusive loot !\n*And Bragging rights for life*")
    #     embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed8 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "CONGRATULATIONS !", value="You completed Legend!!\nNow you can start competing in Exhibitions, Kings Gambits, and Gods of Cod Tournaments!!!\nEarn Tournament Wins to gain access to exclusive Cards and Titles and bounties of :coin:!!!\nDon't forget to check out Flex Shop:tm: with that big bag you got now:eyes:\n*Make sure to say thank you*:heart_exclamation:")
    #     embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
    #     embed9 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️:\n" + "GOOD-BYE!", value="*Thank You*:heart_exclamation:")
    #     embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")   
        
    #     paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    #     paginator.add_reaction('⏮️', "first")
    #     paginator.add_reaction('⏪', "back")
    #     paginator.add_reaction('🔐', "lock")
    #     paginator.add_reaction('⏩', "next")
    #     paginator.add_reaction('⏭️', "last")
    #     embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8,embed9]
    #     await paginator.run(embeds)

    # @commands.command()
    # async def franchise(self, ctx):
    #     embed1 = discord.Embed(title= f":checkered_flag: " + "Senpai™️ Franchise:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn how to create and manage your own Team!\nTeams gain access to 3v3-5v5 Scrims\n\n*The #franchise tutorial will walk you through the Team System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
    #     embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed2 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#franchise = Team Play!", value="Welcome to Senpai:tm: Franchise!\n(Commands are described in this format:arrow_down:\n\n#command 'argument' 'argument' ... etc)\n\n:warning:Do not go on before passing Senpai:tm: Bootcamp!\n*Use #bootcamp*")
    #     embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed3 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#cteam = Create Team! :military_helmet:", value="Let's start by creating our very own CODM team!\n*Use #cteam 'game' 'teamname'*\n\nOnce the team is created run a #flex or #lk\n\n*HINT: use #cteam codm CODMteamname")
    #     embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed4 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#lkt = Lookup Team then #dt = Delete Team", value="Use #lkt to bring up the Team Page\n#lkt 'teamname'\n\nHere you can view Team Members, Stats and the Team Logo\n\n*Try #lkt SenpaiFranchise*")
    #     embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed5 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#att = Add To Team ", value="Time to start recruiting Teammates!\n*Make sure you have a teammate ready to reaction respond!*\n\nTo send an invite use\n#att @user 'teamname'\n\nIf your friend accepts your invite they will be added to the members list!\n\n*Players can only be apart of 1 team per game choose your alliances wisely!*")
    #     embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed6 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#dtm = Delete Teammate and #lteam = Leave Team", value="Owners can use\n#dtm @user\nTo remove teammates\n*#dtm @SenpaiSays*\n\nTo leave a Team use the #lteam command\n#lteam 'teamname'")
    #     embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")  
        
    #     embed7 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : 3v3 - 5v5", value="Teams can compete in Scrims!\nScrims or Scrimmages are team based lobbies up to 10 players!\n\nThats Right, you can run #c3v3 #c4v4 and #c5v5!\n\nJust use #c3v3 'type' @user @user to create a SCRIM lobby!\n*#c3v3 n @teammate @teammate*\n\n*HINT #c4v4 and #c5v5 work the same way just add more players !*")
    #     embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed8 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : #jl = Join Lobby/Join Scrim", value="Remember the #jl command from #bootcamp?\nTeammates can join Scrims together using #jl\n*#jl @opponentUser @'teammate 1' @'teammate 2'\n\nThis will pull all members into the Scrim Lobby!\n*Like always this works for 4v4's and 5v5s just add more teammates*")
    #     embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed9 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : Scorin and Recordin'", value="Now its time to play IRL!\nPlayers get +1 score per round like usual\nThe Lobby Owner can #score any teammate to add a point for the team!\nOnce you are done playing IRL\nThe Lobby Owner uses #el to close the lobby\nThis will record the scores and update the Player AND Team Profiles!\n\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*")
    #     embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
    #     embed10 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "CONGRATULATIONS !", value="You completed franchise!\nNow you can start creating and joining teams!\nWin SCRIMS and earn :coin: to buy new items from the Flex Shop:tm:\nWhen your're ready to compete in Tournaments\n*Use #legend!*")
    #     embed10.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")   
        
    #     paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    #     paginator.add_reaction('⏮️', "first")
    #     paginator.add_reaction('⏪', "back")
    #     paginator.add_reaction('🔐', "lock")
    #     paginator.add_reaction('⏩', "next")
    #     paginator.add_reaction('⏭️', "last")
    #     embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10]
    #     await paginator.run(embeds)
    
    @commands.command()
    async def bootcamp(self, ctx):

            # embed11 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "Games !:video_game:\n#lkg , `.ag` and `.uign`", value="Use the `.lk`g command to bring up the available games!\nAdd games using the `.ag` 'gamename' 'InGameName' command.\nCrown Unlimitd has already been added for you\nTry .ag game 'gameIGN'!\n\n*Hint use .uign 'game' 'newIGN' to update your In Game Name.*")
            # embed11.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
    #     embed1 = discord.Embed(title= f":military_helmet: " + "Senpai™️ Bootcamp:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn how to Create, Lookup and Score Lobbies.\n\n*The #bootcamp tutorial will walk you through the Lobby System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
    #     embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed2 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + ".bootcamp = training!", value="Welcome to Senpai:tm: Bootcamp!\nCommands are described in this format!:arrow_down:\n\n#command 'argument' 'argument' ... etc)\n\n:warning:Do not go on before playing Senpai:tm: Says!\n*Use #senpai*")
    #     embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")
        
    #     embed3 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "Lobbies!", value="Now that you've registered!\nCreate Lobbies and #challenge players!\n\n*Hint Make sure you've registered!")
    #     embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed4 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#ml = My Lobby , #lo = Lobby Owner,\nand #cl = Check Lobby", value="Now try the #ml command...\nThis brings up the Lobby you currently Own!\n\nUse the #lo @user to see if another Player Owns a lobby.\n*Hint #lo @yourself*\n\nUse #cl @user to check the current Lobby of any player.\n*Use #cl @yourself!*")
    #     embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed5 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#c1v1 = Create 1v1 ", value="Lets create a 1v1 Lobby...\n\nLobbies are scored by 'type'.\nEither NORMAL(n) or RANKED(r).\n\nTo create a 1v1 Lobby...\nUse #c1v1 'type'\n\n*Hint use #c1v1 n*")
    #     embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed6 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#dl = Delete Lobby", value="To delete a Lobby use #dl .")
    #     embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed7 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#Jl = Join Lobby!", value="Players can join Lobbies using #jl .\nUse #jl @user to join any open 1v1 Lobby.\n\n*HINT #jl @opponent ")
    #     embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed8 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#challenge a friend!", value="Call out players using #challenge!\nTry #challenge 'type' @user\n*Hint #challenge n @SenpaiSays*\n\nIf your oppenent accepts via *reaction*.\nYou will both be pulled into your Own 1v1 Lobby.\n\nNext we'll learn how to #score points and record Wins and Losses.")
    #     embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed9 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#score the Lobby", value="Now its time to play IRL!\nPlayers get +1 #score per IRL round.\n*Lobbies may be open for multiple rounds*\n\nThe Owner tallies the round using the #score command\n*#score @user*\n\nOnce you are done playing IRL...\nThe Lobby OWNER uses #el to End the Lobby.\n#el will record scores and update the the W and L of the players\n\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*\n\n*Hint #el will record session data, to delete a incorrect lobby use #dl*")
    #     embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed10 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "Team up with #c2v2 = Create 2v2", value="Creating 2v2 lobbies is similar to using #challenge !\n\nUse *#c2v2 'type' @teammate'*\n*Hint try #c2v2 n @senpaisays\n\nIf your teammate accepts you will pull them into a 2v2 Lobby - as Teammates!\nNow other duos can join your 2v2 using #jl\n*Hint #jl @opponentUser @teammateUser*")
    #     embed10.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

    #     embed11 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "CONGRATULATIONS !", value="You completed bootcamp!\nNow you can start creating and joining lobbies!\nWin Lobbies and earn :coin: to buy new items from the Flex Shop:tm:\nWhen your're ready to start/join Teams!\nUse #Franchise!\n\n*HINT use #iby @'playername' to see how many times you beat another player:eyes:")
    #     embed11.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")

    #     paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    #     paginator.add_reaction('⏮️', "first")
    #     paginator.add_reaction('⏪', "back")
    #     paginator.add_reaction('🔐', "lock")
    #     paginator.add_reaction('⏩', "next")
    #     paginator.add_reaction('⏭️', "last")
    #     embeds = [embed1, embed2, embed3, embed5, embed4, embed6, embed7, embed8, embed9, embed6, embed10, embed11]
    #     await paginator.run(embeds)
    
        avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png"


        embedVar1 = discord.Embed(title= f":military_helmet: " + "Senpai™️",colour=0x7289da)
        embedVar1.set_thumbnail(url=avatar)
        embedVar1.add_field(name="Use the Reactions to learn with Senpai™️", value=textwrap.dedent(f"""\
        Bootcamp tuturial coming soon !
        use .help to learn 
        """))


        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embedVar1]
        await paginator.run(embeds)

    @commands.command()
    async def senpai(self, ctx):
        avatar="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png"


        embedVar1 = discord.Embed(title= f":woman_teacher: " + "Senpai™️",colour=0x7289da)
        embedVar1.set_thumbnail(url=avatar)
        embedVar1.add_field(name="Use the Reactions to learn with Senpai™️", value=textwrap.dedent(f"""\
        :brain: Learn how to register!

        *The **.senpai** tutorial will walk you through **Registration**!*

        *To read the **Crown Unlimted Manual** use **.crown***
        *For help with specific commands use **.help***
        *Make sure to say thank you*:heart_exclamation:
        """))

        embedVar2 = discord.Embed(title= f":woman_teacher: " + "Senpai™️",colour=0x7289da)
        embedVar2.set_thumbnail(url=avatar)
        embedVar2.add_field(name="**.senpai** = Teacher!", value=textwrap.dedent(f"""\
        Great you did your first **Command**!
        
        **Commands** are written in this format:arrow_down:
        **.command** `argument1` `argument2`

        This bot uses over 50 **Commands** to deliever an in depth gaming experience.
        *Let's play Senpai:tm: Says to get familar with the **Core Commands***
        """))

        embedVar3 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar3.set_thumbnail(url=avatar)
        embedVar3.add_field(name="**.r** = REGISTER !", value=textwrap.dedent(f"""\
        Use **.r** to register your account!:thumbsup:
        
        *We only sweep your internet history once... jk :eyes:*

        When you register, the **Party Chat Gaming Bot** will send you a introductory DM!

        *Hint use .r!*
        """))

        embedVar4 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar4.set_thumbnail(url=avatar)
        embedVar4.add_field(name="**.build** :muscle:", value=textwrap.dedent(f"""\
        Now try the **.build** command!
        
        **.build** shows your current Crown Unlimited Character Build!
        
        Your Build consist of Your Equipped **Card**, **Title**, **Arm** and **Pet**.
        
        *Hint use **.build** to see your build!*
        """))

        embedVar5 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar5.set_thumbnail(url=avatar)
        embedVar5.add_field(name="The **VAULT**", value=textwrap.dedent(f"""\
        **Items** are stored in the **Vault**! 
        You can access the vault with 1 of 4 different **Commands**.
        
        Access Your **Cards** with **.cvault**.
        Access Your **Titles** with **.tvault**.
        Access Your **Arms** with **.avault**.
        Access Your **Pets** with **.pvault**.
        
        Earn :coin: playing **Crown Unlimted**, winning Party Chat Gaming **Lobbies** and competing in Sponsored **Tournaments**.
        
        *Spend :coin: to buy **Items** from the **.shop**!*
        """))

        embedVar6 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar6.set_thumbnail(url=avatar)
        embedVar6.add_field(name="**.shop** till you drop!", value=textwrap.dedent(f"""\
        Use **.shop** to open the **Crown Unlimited Pop Up Shop**!
        
        View and Buy new **Cards**, **Titles** and **Arms** here!

        To View a full list of items by **Universe**, use the **Universe Commands**

        **Universe Commands**
        **Cards**: **.cards** `universe`
        **Titles**: **.titles** `universe`
        **Arms**: **.arms** `universe`
        **Pets**: **.pets** `universe`
        
        As you gain :coin: and complete **Universes**, new items will appear in the **.shop**!
        
        *New Items are added regularly so check the **Shop** often if something is out of **Stock**!*

        *Pets are earned through drops and P2P trading*
        """))

        embedVar7 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar7.set_thumbnail(url=avatar)
        embedVar7.add_field(name="View the options!", value=textwrap.dedent(f"""\
        Use the **.view___ Commands** To preview Items before purchase.

        **View Commands**: *Item names are Case-Sensitive*
        View Card Info : **.viewcard** `Card Name`
        View Title Info :**.viewtitle** `Title Name`
        View Arm Info : **.viewarm** `Arm Name`
        View Pet Info:  **.viewpet** `Pet Name`

        *Hint Try **.viewcard** `Ochaco Uraraka`*
        """))

        embedVar8 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar8.set_thumbnail(url=avatar)
        embedVar8.add_field(name="Buy with .buy____", value=textwrap.dedent(f"""\
        Use the **.buy___ Commands** to buy items.

        **Buy Commands**: *Item names are Case-Sensitive*
        Buy Card : **.buycard** `Card Name`
        Buy Title :**.buytitle** `Title Name`
        Buy Arm : **.buyarm** `Arm Name`

        *Hint Try **.buyarm** `Shield`*

        """))

        embedVar9 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar9.set_thumbnail(url=avatar)
        embedVar9.add_field(name="Equip with .equip____", value=textwrap.dedent(f"""\
        Use the **.equip___ Commands** to equip items.

        **Equip Commands**: *Item names are Case-Sensitive*
        Equip Card : **.equipcard** `Card Name`
        Equip Title :**.equiptitle** `Title Name`
        Equip Arm : **.equiparm** `Arm Name`
        Equip Pet : **.equippet** `Pet Name`

        *Hint Try **.equiparm `Shield`*

        """))

        embedVar10 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar10.set_thumbnail(url=avatar)
        embedVar10.add_field(name="Time to **.senpaibattle**", value=textwrap.dedent(f"""\
        Now its time for your first **Crown Unlimited** Battle !

        Use **.senpaibattle** to open the **Crown Unlimited** Tutorial Battle **Lobby**
        
        This will be your first **Crown Unlimited** Battle against Me! **Senpai:tm:**!
        
        Make sure your **.build** is set before entering the **Lobby**.
        
        Now use **.start** to begin the tutorial match. **Good Luck**!
        
        Once you are done use the **.end** **Command** to close the **Lobby**

        *Unable to begin the tutorial? First make sure you are **Registered**
        **IF SO**, try the **.end** command to end any lingering Lobbies*
        
        *Too Easy??? Hint use **.legendbattle** to face my Final Form!*
        """))

        embedVar11 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar11.set_thumbnail(url=avatar)
        embedVar11.add_field(name="Many Game Modes!", value=textwrap.dedent(f"""\
        **Crown Unlimited** includes both **Single Player** and **Multiplayer** Game Modes
        
        **Single Player** consit of **Solo** and **Duo**
        
        **Solo** Modes include **.tales**, **.dungeon** and **.boss**
        
        **Duo** Modes include **.dtales**, **.ddungeon** and **.dboss**
        
        **Multiplayer** consist of **Ranked** and **Co-Op**
        
        **Co-Op** Modes include **.ctales**, **.cdungeon**, and **.cboss**
        
        **Ranked**
        
        Use **.battle** `@User` to start a **Ranked Lobby**
        
        Use **.start** to start a **Ranked** Match.
        Use **.wager** to start a **Wager** Match.

        All **Matches** are stored in **Sessions** via the **Party Chat Gaming Database**
        Match **Data** and **Player** W/L records are recorded!

        To see your W/L record vs another user: 
        Use **.vs** `@user` `Game`
        *Example: .vs @senpai crown*
               
        *Hint use .analysis `Card Name` to view optimal PvE and PvP builds for your favorite Cards*"

        """))

        embedVar12 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar12.set_thumbnail(url=avatar)
        embedVar12.add_field(name="**.lookup** = Lookup:eyes:", value=textwrap.dedent(f"""\
        Use the **.lookup** `@User`to Lookup other Registered Players!:mag:.
        
        Try **.lookup** `@Senpai`.
        *Great you should see my equipped **Card**, **Title**, **Arm**, and **Pet** as well as **Analytics** and **Alignments**
        
        **Analytics**
        Every Crown Unlimited Match is recorded for analytics!
        My most used **Card**, **Single Player and **PVP** data
        Use the .analysis **Card Name** command to view optimal builds and **Card Masters**
        
        **Alighment**
        Align yourself with a **Team** and **Family** to enhance the multiplayer experience
        Alighments also grant boost in game!
        We will go over alignments in more detail during **.bootcamp**
        
        
        On the next page are the **Games** I play frequently followed by my **Stats**
        
        The final page shows my Completed **Crown Tales**, **Crown Dungeons** and **Boss Souls**
        
        *Try **.lookup** `@User` on another **User** for practice!*

        """))

        embedVar13 = discord.Embed(title= f":woman_teacher: " + "Senpai™️ Says:",colour=0x7289da)
        embedVar13.set_thumbnail(url=avatar)
        embedVar13.add_field(name="CONGRATULATIONS !", value=textwrap.dedent(f"""\
        You've completed the Senpai:tm: tutorial!
        
        **Crown Unlimited** is a large Discord game with over 50 Commands!
        
        Please read the **Game Manual** using **.crown** to get familar with all the **Game Modes** and **Mechanics**.
        
        Access the full **Command List** and **Help Page** with **.help**

        This Tutorial reviews the **Core Commands** of the **PCG Bot**.
        However this bot has many other **Features** including but not limited to :

        **-In Game Music
        -Black Market
        -Team System
        -Family System
        -Housing System
        -Lobby and Tournament System
        -Support for 10 Player Lobbies
        -AND MORE!**

        
        *When your're ready to start using the PCG bot to its fullest potential.*
        
        *Use .bootcamp!*

        """))



        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embedVar1, embedVar2, embedVar3, embedVar4, embedVar5, embedVar6, embedVar7, embedVar8, embedVar9, embedVar10, embedVar11, embedVar12, embedVar13]
        await paginator.run(embeds)


def setup(bot):
    bot.add_cog(Senpai(bot))