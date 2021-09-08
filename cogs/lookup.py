import discord
from discord.embeds import Embed
from discord.ext import commands
import bot as main
import db
import classes as data
import messages as m
import numpy as np
import help_commands as h
# Converters
from discord import User
from discord import Member
from PIL import Image, ImageFont, ImageDraw
import requests
from collections import ChainMap
import DiscordUtils
import textwrap
from collections import Counter
from discord_slash import cog_ext, SlashContext

emojis = ['👍', '👎']

class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Lookup Cog is ready!')

    async def cog_check(self, ctx):
        return await main.validate_user(ctx)

    @cog_ext.cog_slash(description="Check if player is in Lobby", guild_ids=main.guild_ids)
    async def check(self, ctx, player: User):
        user = player
        current_session = {'TEAMS.TEAM': str(user), "AVAILABLE": True}
        session = db.querySessionMembers(current_session)
        if session:
            game_query = {'ALIASES': session['GAME'].lower()}
            game = db.queryGame(game_query)

            name = session['OWNER'].split("#",1)[0]
            games = game['GAME']
            avatar = game['IMAGE_URL']
            tournament = session['TOURNAMENT']
            owner = session['OWNER']
            scrim = session['SCRIM']
            kingsgambit = session['KINGSGAMBIT']
            gods = session['GODS']
            godsname = session['GODS_TITLE']
            game_type = " "
            if session['TYPE'] == 1:
                game_type = "1v1"
            elif session['TYPE'] == 2:
                game_type = "2v2"
            elif session['TYPE'] == 3:
                game_type = "3v3"
            elif session['TYPE'] == 4:
                game_type = "4v4"
            elif session['TYPE'] == 5:
                game_type = "5v5"

            owner_query = db.queryUser({'DISNAME': owner})
            lobby_owner = await self.bot.fetch_user(owner_query['DID'])

            teams = [x for x in session['TEAMS']]
            
            team_list = []
            team_1 = [x for x in teams if x['POSITION'] == 0] # position 0
            team_2 = [x for x in teams if x['POSITION'] == 1] # position 1
            other_teams = [x for x in teams if x['POSITION'] > 1] # position 1




            team_1_comp_with_ign = []
            team_2_comp_with_ign = []

            team_1_score = ""
            team_2_score = ""

            king_score = 0

            other_teams_comp = []

            for x in team_1:
                # n = x['TEAM'].split("#",1)[1]
                team_1_score = f" Score: {x['SCORE']}"
                king_score = x['SCORE']
                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_1_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_1_comp_with_ign:
                    team_1_comp_with_ign.append(f"{data['DISNAME']}")



            
            for x in team_2:
                team_2_score = f" Score: {x['SCORE']}"

                for y in x['TEAM']:
                    data = db.queryUser({'DISNAME': y})
                    ign = ""
                    for z in data['IGN']:
                        if games in z:
                            ign = z[games]
                            team_2_comp_with_ign.append(f"{data['DISNAME']} : 🎮 {ign}".format(self))
                if not team_2_comp_with_ign:
                    team_2_comp_with_ign.append(f"{data['DISNAME']}")   


            if kingsgambit:
                for x in other_teams:
                    p = x['POSITION']
                    for a in x['TEAM']:
                     other_teams_comp.append({a:p})

            other_teams_comp_to_str = dict(ChainMap(*other_teams_comp))
            n = dict(sorted(other_teams_comp_to_str.items(), key=lambda item: item[1]))
            other_teams_sorted_list = "\n".join(f'{k}' for k,v in n.items())

            team1="Team 1"
            team2="Team 2"

            if games == "Crown Unlimited":
                if team_1:
                    team1=team_1[0]['CARD']
                if team_2:
                    team2=team_2[0]['CARD']

            if gods:
                embedVar = discord.Embed(title=f":trophy: {godsname} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby.\n" + "Compete in PCGs Grand Tournament to determine the one true God of the game!", colour=000000)
            elif kingsgambit:
                embedVar = discord.Embed(title=f":crown: [Kings Gambit]\n{games} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby.\n" + "Compete in 1v1 matches where the winner stays on to determine the king of the game!", colour=000000)
            else:
                embedVar = discord.Embed(title=f"{games} Lobby: {game_type} ".format(self), description=f"{lobby_owner.mention} owns this lobby", colour=000000)            
            embedVar.set_image(url=avatar)

            if scrim:
                embedVar.add_field(name="Scrim", value="Yes")
            
            if kingsgambit and king_score > 0:
                embedVar.add_field(name=f":crown:King - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            elif not team_1_score:
                embedVar.add_field(name=f":military_helmet:{team1}", value="Vacant", inline=False)
            else:
                embedVar.add_field(name=f":military_helmet:{team1} - {team_1_score}", value="\n".join(team_1_comp_with_ign))
            
            if team_2_comp_with_ign:
                embedVar.add_field(name=f":military_helmet:{team2} - {team_2_score}", value="\n".join(team_2_comp_with_ign))
            else:
                embedVar.add_field(name=f":military_helmet:{team2}", value="Vacant")

            if kingsgambit and other_teams:
                embedVar.add_field(name=f"Up Next...", value=other_teams_sorted_list)

            await ctx.send(embed=embedVar)
        else:
            await ctx.send(m.SESSION_DOES_NOT_EXIST, delete_after=5)

    @cog_ext.cog_slash(description="Lookup player stats", guild_ids=main.guild_ids)
    async def lookup(self, ctx, player: User):
        try:
            query = {'DISNAME': str(player)}
            d = db.queryUser(query)
            m = db.queryManyMatchesPerPlayer({'PLAYER': str(player)})
            v = db.queryVault({'OWNER': str(player)})
            if d:
                balance = v['BALANCE']
                if balance >= 150000:
                    bal_icon = ":money_with_wings:"
                elif balance >= 100000:
                    bal_icon = ":moneybag:"
                elif balance >= 50000 or balance <= 49999:
                    bal_icon = ":dollar:"

                bal_message = f"{bal_icon}{'{:,}'.format(balance)}"

                all_cards = len(v['CARDS'])
                all_titles = len(v['TITLES'])
                all_arms = len(v['ARMS'])
                all_pets = len(v['PETS'])

                name = d['DISNAME'].split("#",1)[0]
                games = d['GAMES']
                abyss_level = d['LEVEL']
                card = d['CARD']
                ign = d['IGN']
                team = d['TEAM']
                guild = d['GUILD']
                if team != "PCG":
                    team_info = db.queryTeam({'TNAME' : str(team)})
                    guild = team_info['GUILD']
                family = d['FAMILY']
                titles = d['TITLE']
                arm = d['ARM']
                avatar = d['AVATAR']
                matches = d['MATCHES']
                tournament_wins = d['TOURNAMENT_WINS']
                crown_tales = d['CROWN_TALES']
                dungeons = d['DUNGEONS']
                bosses = d['BOSS_WINS']
                pet = d['PET']
                rebirth = d['REBIRTH']
                icon = ':triangular_flag_on_post:'
                if rebirth == 0:
                    icon = ':triangular_flag_on_post:'
                elif rebirth == 1:
                    icon = ':heart_on_fire:'
                elif rebirth == 2:
                    icon = ':heart_on_fire::heart_on_fire:'
                elif rebirth == 3:
                    icon = ':heart_on_fire::heart_on_fire::heart_on_fire:'
                elif rebirth == 4:
                    icon = ':heart_on_fire::heart_on_fire::heart_on_fire::heart_on_fire:'
                elif rebirth == 5:
                    icon = ':heart_on_fire::heart_on_fire::heart_on_fire::heart_on_fire::heart_on_fire:'

                pvp_matches = []
                boss_matches = []
                dungeon_matches = []
                tales_matches = []
                most_played_card = []
                most_played_card_message = "_No Data For Analysis_"
                match_history_message = ""

                wlmatches = list(d['MATCHES'][0].values())[0]
                wins = wlmatches[0]
                losses = wlmatches[1]
                if m:
                    for match in m:
                        most_played_card.append(match['CARD'])
                        if match['UNIVERSE_TYPE'] == "Tales":
                            tales_matches.append(match)
                        elif match['UNIVERSE_TYPE'] == "Dungeon":
                            dungeon_matches.append(match)
                        elif match['UNIVERSE_TYPE'] == "Boss":
                            boss_matches.append(match)
                        elif match['UNIVERSE_TYPE'] == "PVP":
                            pvp_matches.append(match)

                    card_main = most_frequent(most_played_card)

                    if not most_played_card:
                        most_played_card_message = "_No Data For Analysis_"
                    else:
                        most_played_card_message = f"**Most Played Card: **{card_main}"
                        match_history_message = f"""
                        **Tales Played: **{len(tales_matches)}
                        **Dungeons Played: **{len(dungeon_matches)}
                        **Bosses Played: **{len(boss_matches)}
                        **Pvp Played: **{len(pvp_matches)}
                        """

                crown_list = []
                for crown in crown_tales:
                    if crown != "":
                        crown_list.append(crown)
                
                dungeon_list = []
                for dungeon in dungeons:
                    if dungeon != "":
                        dungeon_list.append(dungeon)

                boss_list =[]
                for boss in bosses:
                    if boss != "":
                        boss_list.append(boss)

                matches_to_string = dict(ChainMap(*matches))
                ign_to_string = dict(ChainMap(*ign))



                embed1 = discord.Embed(title= f"{icon} | " + f"{name}".format(self), description=textwrap.dedent(f"""\
                :new_moon: | **Abyss Rank**: {abyss_level}
                :flower_playing_cards: | **Card:** {card}
                :reminder_ribbon:** | Title: **{titles}
                :mechanical_arm: | **Arm: **{arm}
                :bird: | **Pet: **{pet}

                :military_medal: | {most_played_card_message}
                **Tales Played: **{len(tales_matches)}
                **Dungeons Played: **{len(dungeon_matches)}
                **Bosses Played: **{len(boss_matches)}
                **Pvp Played: **{len(pvp_matches)}
                **W/L:** {wins}**/**{losses}
                
                **Balance** {bal_message}
                :flower_playing_cards: **Cards** {all_cards}
                :reminder_ribbon: **Titles** {all_titles}
                :mechanical_arm: **Arms** {all_arms}
                :bird: **Pets** {all_pets}
                
                :flags: | **Guild: **{guild}
                :military_helmet: | **Team: **{team} 
                :family_mwgb: | **Family: **{family}

                
                """), colour=000000)
                embed1.set_thumbnail(url=avatar)
                # embed1.add_field(name="Team" + " :military_helmet:", value=team)
                # embed1.add_field(name="Family" + " :family_mwgb:", value=family)
                # embed1.add_field(name="Card" + " ::flower_playing_cards: :", value=' '.join(str(x) for x in titles))
                # embed1.add_field(name="Title" + " :crown:", value=' '.join(str(x) for x in titles))
                # embed1.add_field(name="Arm" + " :mechanical_arm: ", value=f"{arm}")
                # embed1.add_field(name="Pet" + " :dog:  ", value=f"{pet}")
                # embed1.add_field(name="Tournament Wins" + " :fireworks:", value=tournament_wins)

                if crown_list:
                    embed4 = discord.Embed(title= f"{icon} | " + f"{name}".format(self), description=":bank: | Party Chat Gaming Database™️", colour=000000)
                    embed4.set_thumbnail(url=avatar)
                    embed4.add_field(name="Completed Tales" + " :medal:", value="\n".join(crown_list))
                    if dungeon_list:
                        embed4.add_field(name="Completed Dungeons" + " :fire: ", value="\n".join(dungeon_list))
                        if boss_list:
                            embed4.add_field(name="Boss Souls" + ":japanese_ogre:",value="\n".join(boss_list))
                        else:
                            embed4.add_field(name="Boss Souls" + " :japanese_ogre: ", value="No Boss Souls Collected, yet!")
                    else:
                        embed4.add_field(name="Completed Dungeons" + " :fire: ", value="No Dungeons Completed, yet!")
                else:
                    embed4 = discord.Embed(title= f"{icon} " + f"{name}".format(self), description=":bank: Party Chat Gaming Database™️", colour=000000)
                    embed4.set_thumbnail(url=avatar)
                    embed4.add_field(name="Completed Tales" + " :medal:", value="No completed Tales, yet!")
                    embed4.add_field(name="Completed Dungeons" + " :fire: ", value="No Dungeons Completed, yet!")
                    embed4.add_field(name="Boss Souls" + " :japanese_ogre: ", value="No Boss Souls Collected, yet!")

                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏮️', "first")
                paginator.add_reaction('⏪', "back")
                paginator.add_reaction('🔐', "lock")
                paginator.add_reaction('⏩', "next")
                paginator.add_reaction('⏭️', "last")
                embeds = [embed1, embed4 ]
                await paginator.run(embeds)
            else:
                await ctx.send(m.USER_NOT_REGISTERED)
        except Exception as ex:
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append({
                    "filename": tb.tb_frame.f_code.co_filename,
                    "name": tb.tb_frame.f_code.co_name,
                    "lineno": tb.tb_lineno
                })
                tb = tb.tb_next
            print(str({
                'type': type(ex).__name__,
                'message': str(ex),
                'trace': trace
            }))
            await ctx.send("There's an issue with your lookup command. Check with support.")
            return

    @cog_ext.cog_slash(description="Lookup team stats", guild_ids=main.guild_ids)
    async def team(self, ctx, team: str):
        team_name = team
        team_query = {'TNAME': team_name}
        team = db.queryTeam(team_query)
        owner_name = ""
        if team:
            team_name = team['TNAME']
            owner_name = team['OWNER']
            games = team['GAMES']
            # avatar = game['IMAGE_URL']
            badges = team['BADGES']
            scrim_wins = team['SCRIM_WINS']
            scrim_losses = team['SCRIM_LOSSES']
            tournament_wins = team['TOURNAMENT_WINS']
            logo = team['LOGO_URL']
            balance = team['BANK']
            icon = ":coin:"
            guild = team['GUILD']
            if balance >= 500000:
                icon = ":money_with_wings:"
            elif balance >=300000:
                icon = ":moneybag:"
            elif balance >= 150000:
                icon = ":dollar:"
            

            team_list = []
            for members in team['MEMBERS']:
                mem_query = db.queryUser({'DISNAME': members})
                ign_list = [x for x in mem_query['IGN']]
                ign_list_keys = [k for k in ign_list[0].keys()]
                if ign_list_keys == games:
                    team_list.append(f"{ign_list[0][games[0]]}") 
                else:
                    team_list.append(f"{members}")


            embed1 = discord.Embed(title=f":checkered_flag: | {team_name} Team Card - {icon} {'{:,}'.format(balance)}".format(self), description=":bank: | Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed1.set_image(url=logo)
            embed1.add_field(name=":man_detective: | **~ Owner ~**", value= owner_name.split("#",1)[0], inline=True)
            embed1.add_field(name=":flags: | **~ Guild ~** ", value= guild, inline=False)
            embed1.add_field(name=":medal: | **~ Scrim Wins ~**", value=scrim_wins)
            embed1.add_field(name=":crossed_swords: | **~ Scrim Losses ~**", value=scrim_losses)
            embed1.add_field(name=":fireworks: | **~ Tournament Wins ~**", value=tournament_wins, inline=False)
            
            embed2 = discord.Embed(title=f":checkered_flag: | {team_name} Team Members - {icon} {'{:,}'.format(balance)}".format(self), description=":bank: | Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed2.set_image(url=logo)
            embed2.add_field(name=":military_helmet: | **~ Members ~**", value="\n".join(f'{t}'.format(self) for t in team_list), inline=False)

            embed3 = discord.Embed(title=f":checkered_flag: | {team_name} Team Members - {icon} {'{:,}'.format(balance)}".format(self), description=":bank: | Party Chat Gaming Database", colour=000000)
            if team['LOGO_FLAG']:
                embed3.set_image(url=logo)
            embed3.add_field(name=":video_game: | Games ", value="\n".join(games), inline=False)
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embed1, embed2, embed3]
            await paginator.run(embeds)
        else:
            await ctx.send(m.TEAM_DOESNT_EXIST)

    @cog_ext.cog_slash(description="Lookup Guild", guild_ids=main.guild_ids)
    async def guild(self, ctx, guild: str):
        guild_name = guild
        guild_query = {'GNAME': guild_name}
        guild = db.queryGuildAlt(guild_query)
        founder_name = ""
        if guild:
            hall = db.queryHall({'HALL' : guild['HALL']})
            hall_name = hall['HALL']
            hall_multipler = hall['MULT']
            hall_split = hall['SPLIT']
            hall_fee = hall['FEE']
            hall_def = hall['DEFENSE']
            hall_img = hall['PATH']
            guild_name = guild['GNAME']
            founder_name = guild['FOUNDER']
            sworn_name = guild['SWORN']
            shield_name = guild['SHIELD']
            shield_info = db.queryUser({'DISNAME' : str(shield_name)})
            shield_card = shield_info['CARD']
            shield_arm = shield_info['ARM']
            shield_title = shield_info['TITLE']
            shield_rebirth = shield_info['REBIRTH']
            streak = guild['STREAK']
            # games = guild['GAMES']
            # avatar = game['IMAGE_URL']
            crest = guild['CREST']
            balance = guild['BANK']
            bounty = guild['BOUNTY']
            bonus = int((streak/100) * bounty)
            picon = ":shield:"
            sicon = ":beginner:"
            icon = ":coin:"
            if balance >= 1000000:
                icon = ":money_with_wings:"
            elif balance >=500000:
                icon = ":moneybag:"
            elif balance >= 300000:
                icon = ":dollar:"
                
            if streak >= 100:
                sicon = ":skull_crossbones:"     
            elif streak >= 50:
                sicon = ":skull:"
            elif streak >=25:
                sicon = ":ghost:"
            elif streak >= 10:
                sicon = ":diamond_shape_with_a_dot_inside:"
                
            # if shield_rebirth > 0:
            #     picon = "::heart_on_fire::"
            

            sword_list = []
            sword_count = 0
            blade_count = 0
            for swords in guild['SWORDS']:
                blade_count = 0
                sword_count = sword_count + 1
                sword_team = db.queryTeam({'TNAME': swords})
                dubs = sword_team['SCRIM_WINS']
                els = sword_team['SCRIM_LOSSES']
                for blades in sword_team['MEMBERS']:
                    blade_count = blade_count + 1
                sword_bank = sword_team['BANK']
                sword_list.append(f"~ {swords} ~ W**{dubs}** / L**{els}**\n:man_detective: | **Owner: **{sword_team['OWNER']}\n:coin: | **Bank: **{'{:,}'.format(sword_bank)}\n:knife: | **Blades: **{blade_count}\n_______________________")
            crest_list = []
            for c in crest:
                crest_list.append(f"{Crest_dict[c]} | {c}")




            # embed1 = discord.Embed(title=f":flags: {guild_name} Guild Card - {icon}{'{:,}'.format(balance)}".format(self), description=":bank: Party Chat Gaming Database", colour=000000)
            # if guild['LOGO_FLAG']:
            #     embed1.set_image(url=logo)
            # embed1.add_field(name="Founder :dolls:", value= founder_name.split("#",1)[0], inline=True)
            # embed1.add_field(name="Sworn :dolls:", value= sworn_name.split("#",1)[0], inline=True)
            embed1 = discord.Embed(title= f":flags: |{guild_name} Alliance Card - {icon} {'{:,}'.format(balance)}".format(self), description=textwrap.dedent(f"""\
            
            :nesting_dolls: | **Founder ~** {founder_name.split("#",1)[0]}
            :dolls: | **Sworn ~** {sworn_name.split("#",1)[0]}
            
            *Guilds Owners can /knight a **Shield** to defend the Hall from **Raids**! Use /raid*
            :japanese_goblin: | **Shield: ~**{shield_name.split("#",1)[0].format(self)} ~ {sicon} | **Victories: **{streak}
            :flower_playing_cards: | **Card: **{shield_card}
            :reminder_ribbon: | **Title: **{shield_title}
            :mechanical_arm: | **Arm: **{shield_arm}
              
            ***Swords** are employed by the guild to win PVP battles! They can claim the **Shield** by defeating them in a /raid*
            :ninja: | **Swords: **{sword_count}
            :dollar: | **Split: **{hall_split} *Team Income Multiplier*
            :secret: | **Crest: **{len(crest_list)} *Current Crest Holdings. Run /dungeons to Claim **Universe Crest***
              
            
            :coin: | **Raid Fee: **{'{:,}'.format(hall_fee)} *Cost to /raid*
            :yen: | **Bounty: **{'{:,}'.format(bounty)} *use /bounty to set Guild Bounty*
            :moneybag: | **Bonus: **{'{:,}'.format(bonus)} *Victory Bonus Multiplier*
                   
            
            :shinto_shrine: | **Hall: **{hall_name} *Current Guild Hall*
            :shield: | **Defenses: **{hall_def} *Current Raid Defense Multiplier*
            """), colour=000000)
            embed1.set_image(url=hall_img)
            embed1.set_footer(text=f"/raid {guild_name} - Raid Guild")
            
            embed2 = discord.Embed(title=f":flags: |  {guild_name} **Sword** List".format(self), description=":bank: |  Party Chat Gaming Database", colour=000000)
            embed2.add_field(name=f"**Swords: | ** :ninja: ~ {sword_count}", value="\n".join(f'**{t}**'.format(self) for t in sword_list), inline=False)
            embed2.set_footer(text=f"/lookupteam - Lookup Guild Teams")
            
            embed3 = discord.Embed(title=f":flags: |  {guild_name} **OWNED CREST**".format(self), description=":bank: |  Party Chat Gaming Database", colour=000000)
            embed3.add_field(name=f":secret: | **CREST**", value="\n".join(f'**{c}**'.format(self) for c in crest_list), inline=False)
            embed3.set_footer(text=f"/dungeons - Earn Universe Crest!")
            # if guild['LOGO_FLAG']:
            #     embed3.set_image(url=logo)
            
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            embeds = [embed1,embed2, embed3]
            await paginator.run(embeds)
        else:
            await ctx.send(m.GUILD_DOESNT_EXIST)


    @cog_ext.cog_slash(description="Lookup player family", guild_ids=main.guild_ids)
    async def family(self, ctx, member: User):
        user_profile = db.queryUser({'DISNAME': str(member)})
        family = db.queryFamily({'HEAD': user_profile['FAMILY']})
        if family:
            family_name = family['HEAD'] + "'s Family"
            head_name = family['HEAD']
            partner_name = family['PARTNER']
            savings = int(family['BANK'])
            house = family['HOUSE']
            house_info = db.queryHouse({'HOUSE' : house})
            house_img = house_info['PATH']
            kid_list = []
            for kids in family['KIDS']:
                kid_list.append(kids.split("#",1)[0])
            icon = ":coin:"
            if savings >= 300000:
                icon = ":money_with_wings:"
            elif savings >=150000:
                icon = ":moneybag:"
            elif savings >= 100000:
                icon = ":dollar:"


            embed1 = discord.Embed(title=f":family_mwgb: | {family_name} - {icon}{'{:,}'.format(savings)}".format(self), description=":bank: | Party Chat Gaming Database", colour=000000)
            # if team['LOGO_FLAG']:
            #     embed1.set_image(url=logo)
            embed1.add_field(name=":brain: | Head Of Household", value= head_name.split("#",1)[0], inline=False)
            if partner_name:
                embed1.add_field(name=":anatomical_heart: | Partner", value= partner_name.split("#",1)[0], inline=False)
            if kid_list:
                embed1.add_field(name=":baby: | Kids", value="\n".join(f'{k}'.format(self) for k in kid_list), inline=False)
            embed1.add_field(name=":house: | House", value=house, inline=False)
            embed1.set_image(url=house_img)
    
            await ctx.send(embed = embed1)
        else:
            await ctx.send(m.FAMILY_DOESNT_EXIST)


def setup(bot):
    bot.add_cog(Lookup(bot))

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

Crest_dict = {'Unbound': ':ideograph_advantage:',
              'My Hero Academia': ':sparkle:',
              'League Of Legends': ':u6307:',
              'Kanto Region': ':chart:',
              'Naruto': ':u7121:',
              'Bleach': ':u6709:',
              'God Of War': ':u7533:',
              'Chainsawman' : ':accept:',
              'One Punch Man': ':u55b6:',
              'Johto Region': ':u6708:',
              'Black Clover': ':ophiuchus:',
              'Demon Slayer': ':aries:',
              'Attack On Titan': ':taurus:',
              '7ds': ':capricorn:',
              'Hoenn Region': ':leo:',
              'Digimon': ':cancer:',
              'Fate': ':u6e80:',
              'Solo Leveling': ':u5408:',
              'Souls': ':sos:',
              'Dragon Ball Z': ':u5272:',
              'Sinnoh Region': ':u7981:',
              'Death Note': ':white_flower:',
              'Crown Rift Awakening': ':u7a7a:',
              'Crown Rift Slayers': ':sa:',
              'Crown Rift Madness': ':loop:'}