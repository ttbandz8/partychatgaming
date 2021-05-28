import discord
from discord.ext import commands
import DiscordUtils
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h



class Senpai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Senpai Cog is ready!")

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @commands.command()
    async def legend(self, ctx):
        embed1 = discord.Embed(title= f":crown: " + "Senpai™️ Legend:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn about Exhibitions, Kings Gambit and Gods of COD!\n*Write your name is history...*\n\n*The #legend tutorial will walk you through the Tournament System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
        embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed2 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#legend = Tournaments!", value="Welcome to Senpai:tm: Legend!\n(Commands are described in this format:arrow_down:\n\n#command 'argument' 'argument' ...etc )\n\n:warning:Do not go on before completing Senpai:tm: Franchise!\n*Use #franchise*")
        embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed3 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "*Exhibitions* :medal:", value="Exhibitions are 1v1 duels between 2 players!\n*Winner Gets 1 Tournament Win*\n\nHow can you join an exhibition you may ask?\nWell you can't, you'll be invited when your time comes.\n\n*Make sure you accept the Invitation*")
        embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed4 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "#jkg to Join a *Kings Gambit* :crown:", value="Kings Gambits are King of the Hill Lobbies\nRules are....the KING picks the rules\nAdmins can start Kings Gambits matches open for all players\nPlayers can join using the #jkg 'AdminName' command\n\nBe the King at the end of the lobby to win extra :coin: and a Tournament Win!")
        embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed5 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gods of COD", value="Gods of Cod are the largest CODM tournaments Party Chat Gaming has to offer\nEach Tournament length, prize and rules are different and are announced before Registrations\nAs long as Registrations are open\nteams can use #rgoc to register their team for GOC\n\n*NOTE as long as 1 player in your team registers, your entire team will be registed!*")
        embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed6 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Gauntlet Week", value="When the tournament starts, registration is closed and the games begin with The Gauntlet!\nWeeks of fierce competition betweem Teams!\n\nTournament Brackets will be determined based on the number of wins each team earns during Gauntlet Week!")
        embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed7 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "Brackets", value="Brackets take place at the end of Gauntlet!\nTeams are placed according to their total number of wins!\nThe Brackets consist of single elimination matches\nThe Winner of the brackets earns Tournament exclusive loot !\n*And Bragging rights for life*")
        embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed8 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️ Legend:\n" + "CONGRATULATIONS !", value="You completed Legend!!\nNow you can start competing in Exhibitions, Kings Gambits, and Gods of Cod Tournaments!!!\nEarn Tournament Wins to gain access to exclusive Cards and Titles and bounties of :coin:!!!\nDon't forget to check out Flex Shop:tm: with that big bag you got now:eyes:\n*Make sure to say thank you*:heart_exclamation:")
        embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")
        
        embed9 = discord.Embed(color=ctx.author.color).add_field(name=":crown: " + "Senpai™️:\n" + "GOOD-BYE!", value="*Thank You*:heart_exclamation:")
        embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")   
        
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8,embed9]
        await paginator.run(embeds)

    @commands.command()
    async def franchise(self, ctx):
        embed1 = discord.Embed(title= f":checkered_flag: " + "Senpai™️ Franchise:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn how to create and manage your own Team!\nTeams gain access to 3v3-5v5 Scrims\n\n*The #franchise tutorial will walk you through the Team System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
        embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed2 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#franchise = Team Play!", value="Welcome to Senpai:tm: Franchise!\n(Commands are described in this format:arrow_down:\n\n#command 'argument' 'argument' ... etc)\n\n:warning:Do not go on before passing Senpai:tm: Bootcamp!\n*Use #bootcamp*")
        embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed3 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#cteam = Create Team! :military_helmet:", value="Let's start by creating our very own CODM team!\n*Use #cteam 'game' 'teamname'*\n\nOnce the team is created run a #flex or #lk\n\n*HINT: use #cteam codm CODMteamname")
        embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed4 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#lkt = Lookup Team then #dt = Delete Team", value="Use #lkt to bring up the Team Page\n#lkt 'teamname'\n\nHere you can view Team Members, Stats and the Team Logo\n\n*Try #lkt SenpaiFranchise*")
        embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed5 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#att = Add To Team ", value="Time to start recruiting Teammates!\n*Make sure you have a teammate ready to reaction respond!*\n\nTo send an invite use\n#att @user 'teamname'\n\nIf your friend accepts your invite they will be added to the members list!\n\n*Players can only be apart of 1 team per game choose your alliances wisely!*")
        embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed6 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "#dtm = Delete Teammate and #lteam = Leave Team", value="Owners can use\n#dtm @user\nTo remove teammates\n*#dtm @SenpaiSays*\n\nTo leave a Team use the #lteam command\n#lteam 'teamname'")
        embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")  
        
        embed7 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : 3v3 - 5v5", value="Teams can compete in Scrims!\nScrims or Scrimmages are team based lobbies up to 10 players!\n\nThats Right, you can run #c3v3 #c4v4 and #c5v5!\n\nJust use #c3v3 'type' @user @user to create a SCRIM lobby!\n*#c3v3 n @teammate @teammate*\n\n*HINT #c4v4 and #c5v5 work the same way just add more players !*")
        embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed8 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : #jl = Join Lobby/Join Scrim", value="Remember the #jl command from #bootcamp?\nTeammates can join Scrims together using #jl\n*#jl @opponentUser @'teammate 1' @'teammate 2'\n\nThis will pull all members into the Scrim Lobby!\n*Like always this works for 4v4's and 5v5s just add more teammates*")
        embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed9 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "SCRIMS! : Scorin and Recordin'", value="Now its time to play IRL!\nPlayers get +1 score per round like usual\nThe Lobby Owner can #score any teammate to add a point for the team!\nOnce you are done playing IRL\nThe Lobby Owner uses #el to close the lobby\nThis will record the scores and update the Player AND Team Profiles!\n\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*")
        embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")   
        
        embed10 = discord.Embed(color=ctx.author.color).add_field(name=":checkered_flag: " + "Senpai™️ Franchise:\n" + "CONGRATULATIONS !", value="You completed franchise!\nNow you can start creating and joining teams!\nWin SCRIMS and earn :coin: to buy new items from the Flex Shop:tm:\nWhen your're ready to compete in Tournaments\n*Use #legend!*")
        embed10.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Senpai.png")   
        
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9, embed10]
        await paginator.run(embeds)
    
    @commands.command()
    async def bootcamp(self, ctx):
        embed1 = discord.Embed(title= f":military_helmet: " + "Senpai™️ Bootcamp:", description="Use the Reactions to learn with Senpai™️\n\n:brain: Learn how to Create, Lookup and Score Lobbies.\n\n*The #bootcamp tutorial will walk you through the Lobby System!*\n*For help with specific commands use #help*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
        embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed2 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + ".bootcamp = training!", value="Welcome to Senpai:tm: Bootcamp!\nCommands are described in this format!:arrow_down:\n\n#command 'argument' 'argument' ... etc)\n\n:warning:Do not go on before playing Senpai:tm: Says!\n*Use #senpai*")
        embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")
        
        embed3 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "Lobbies!", value="Now that you've registered!\nCreate Lobbies and #challenge players!\n\n*Hint Make sure you've registered!")
        embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed4 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#ml = My Lobby , #lo = Lobby Owner,\nand #cl = Check Lobby", value="Now try the #ml command...\nThis brings up the Lobby you currently Own!\n\nUse the #lo @user to see if another Player Owns a lobby.\n*Hint #lo @yourself*\n\nUse #cl @user to check the current Lobby of any player.\n*Use #cl @yourself!*")
        embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed5 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#c1v1 = Create 1v1 ", value="Lets create a 1v1 Lobby...\n\nLobbies are scored by 'type'.\nEither NORMAL(n) or RANKED(r).\n\nTo create a 1v1 Lobby...\nUse #c1v1 'type'\n\n*Hint use #c1v1 n*")
        embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed6 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#dl = Delete Lobby", value="To delete a Lobby use #dl .")
        embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed7 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#Jl = Join Lobby!", value="Players can join Lobbies using #jl .\nUse #jl @user to join any open 1v1 Lobby.\n\n*HINT #jl @opponent ")
        embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed8 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#challenge a friend!", value="Call out players using #challenge!\nTry #challenge 'type' @user\n*Hint #challenge n @SenpaiSays*\n\nIf your oppenent accepts via *reaction*.\nYou will both be pulled into your Own 1v1 Lobby.\n\nNext we'll learn how to #score points and record Wins and Losses.")
        embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed9 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "#score the Lobby", value="Now its time to play IRL!\nPlayers get +1 #score per IRL round.\n*Lobbies may be open for multiple rounds*\n\nThe Owner tallies the round using the #score command\n*#score @user*\n\nOnce you are done playing IRL...\nThe Lobby OWNER uses #el to End the Lobby.\n#el will record scores and update the the W and L of the players\n\nRemember we are operating off the HONOR system so use *Screenshots* to dispute any *cheating*\n\n*Hint #el will record session data, to delete a incorrect lobby use #dl*")
        embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed10 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "Team up with #c2v2 = Create 2v2", value="Creating 2v2 lobbies is similar to using #challenge !\n\nUse *#c2v2 'type' @teammate'*\n*Hint try #c2v2 n @senpaisays\n\nIf your teammate accepts you will pull them into a 2v2 Lobby - as Teammates!\nNow other duos can join your 2v2 using #jl\n*Hint #jl @opponentUser @teammateUser*")
        embed10.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")

        embed11 = discord.Embed(color=ctx.author.color).add_field(name=":military_helmet: " + "Senpai™️ Bootcamp:\n" + "CONGRATULATIONS !", value="You completed bootcamp!\nNow you can start creating and joining lobbies!\nWin Lobbies and earn :coin: to buy new items from the Flex Shop:tm:\nWhen your're ready to start/join Teams!\nUse #Franchise!\n\n*HINT use #iby @'playername' to see how many times you beat another player:eyes:")
        embed11.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Franchise.png")

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3, embed5, embed4, embed6, embed7, embed8, embed9, embed6, embed10, embed11]
        await paginator.run(embeds)

    @commands.command()
    async def senpai(self, ctx):
        embed1 = discord.Embed(title= f":woman_teacher: " + "Senpai™️", description=" Use the Reactions to learn with Senpai™️\n\n:brain: Learn how to register!\n\n*The `.senpai` tutorial will walk you through registration!*\n*For help with specific commands use `.help`*\n\n*Make sure to say thank you*:heart_exclamation:", colour=000000, value="Page 1")
        embed1.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")

        embed2 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️\n" + "`.senpai` = Teacher!", value="Great you did your first `Command`!\n`Commands` are written in this format:arrow_down:\n\n`.command` `'TypeHere'` `'Type Here'`\n\n*Let's play Senpai:tm: Says!*")
        embed2.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed3 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says:\n" + "`.r` = REGISTER !", value="Use .r to register your account!:thumbsup:\n*We only sweep your internet history once... jk :eyes:*\n\n*Hint use .r!*")
        embed3.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed4 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says:\n" + "`.build` :muscle:", value="Now try the `.build` command!:muscle:\n`.build` shows your current Crown Unlimited Characted Build!\n\nWell Talk about Crown Unlimited more in `.bootcamp`\n*Hint use `.build`!*")
        embed4.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed5 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says:\n" + "`.lookup` = Lookup:eyes:", value="type `.lookup` @`user` to Lookup other Registered Players!:mag:\n\nTry `.lookup` @Senpai\nGreat you should see my `Stats`, `Games`, `Teams`, `Title` and `Arm`!\n\n*Try `.lookup` @`user` on another user for practice!*")
        embed5.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png") 
        
        embed6 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says:\n" + "The `.vault`", value="Use `.vault` to bring up the `Vault`\nYour current :coin: and all items are stored in the `vault`!\n\nEarn :coin: by playing Crown Unlimted, winning Party Chat Gaming Lobbies and Competing in Sponsored Tournaments.\nSpend :coin: to buy `items` from the `.shop`!\n\n*Hint earn special `cards`, `titles` and `arms` by competing in `tournaments`!*")
        embed6.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed7 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "`.shop` till you drop!", value="Type `.shop` to open the `Crown Unlimited Shop`!\nView and Buy new `Cards`, `Titles` and `Arms` here!\n\n*As you gain :coin: and complete `.tales`, you will see new items appear in the .shop!\nNew Items are added regularly so check the #shop often if something is out of stock!!*")
        embed7.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed8 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "`.viewcard `= View Card", value="View the options!\n\nUse `.viewcard` `'cardname'` to View Card.\nType card name exactly as seen\n\n *Hint Try .viewcard Naruto*")
        embed8.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed9 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "Buy with .buycard, .buyarm and .buytitle", value="Use `.buycard` 'card', .buyarm `'armn'` or .buytitle 'title' to add items to your `.vault`!\n\n*Remember you can use `.viewcard` to view `items` in the `.shop`*")
        embed9.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed10 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "Equip! `.equipcard`, `.equiparm` and `.equiptitle`", value="Use .equipcard 'card' to Equip a Card.\nNow use .equiptitle 'title' to equip a Title.\nNow use .equiparm 'arm' to equip an Arm.\nOnce you've decided on your new build use .build!\n\n*Hint Use .vault to see your available items!*")
        embed10.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed11 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "Games !:video_game:\n#lkg , `.ag` and `.uign`", value="Use the `.lk`g command to bring up the available games!\nAdd games using the `.ag` 'gamename' 'InGameName' command.\nCrown Unlimitd has already been added for you\nTry .ag game 'gameIGN'!\n\n*Hint use .uign 'game' 'newIGN' to update your In Game Name.*")
        embed11.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Legend.png")
        
        embed12 = discord.Embed(color=ctx.author.color).add_field(name=":woman_teacher: " + "Senpai™️ Says :\n" + "CONGRATULATIONS !", value="Welcome to Party Chat Gaming:tm:\nWhen your're ready to start creating lobbies\n*Use #bootcamp!*")
        embed12.set_thumbnail(url="https://res.cloudinary.com/dkcmq8o15/image/upload/v1620496215/PCG%20LOGOS%20AND%20RESOURCES/Bootcamp.png")
        
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8,embed9,embed10,embed11,embed12]
        await paginator.run(embeds)

def setup(bot):
    bot.add_cog(Senpai(bot))