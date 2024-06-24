import discord
import random
import nacl
import datetime
import json
import os
import re
import time
from discord.ext import commands, tasks
from itertools import count, cycle
from discord_slash import SlashCommand
from keep_alive import keep_alive

copyright = os.environ['Copy']
infoc = os.environ['infoc']

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix='$', intents=intents)
slash = SlashCommand(client, sync_commands=True)

#status = cycle(
#    ["MRP - Mallu Roleplay", "KAMMATTIPADAM", "MATTANCHERRY", "KAMMATTIPADAM | PVP"])

#=====================🅲🅾🅿🆈🆁🅸🅶🅷🆃===========================

#𝘾𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙤𝙬𝙣𝙚𝙙 𝙗𝙮 𝘼𝙨𝙝_25
#𝘿𝙞𝙨𝙘𝙤𝙧𝙙 𝙣𝙖𝙢𝙚 : Ash_25#0846 𝙞𝙙 765885050125942804
#for any queries contact through discord https://www.ash2500.repl.co/copyright/

#===========================================================================

#=========== DC ROLES ===================================
management = 1051366401392267275
leader = 989013571474165831
coleader = 989013709554855977
access = 989013932561797180
finance = 992649435697926144
turf = 1005416931219734528
club_head = 1074617304786149397
armourymag = 1102315952282030100
#===========================================================

#==================================🅾🅽 ​ 🆁🅴🅰🅳🆈=====================================
#@client.event
#async def on_ready():
#    change_status.start()
#    print(f'Connected as {client.user}  to DISCORD')
#    VC = client.get_channel(988890347012759575)
#    await VC.connect()
#    log = client.get_channel(992655133081092176)
#    mylog = client.get_channel(987972624137191518)
#    await log.send("RESTARTED")
#    await mylog.send("RESTARTED")

#@tasks.loop(seconds=120)
#async def change_status():
#    await client.change_presence(status=discord.Status.dnd,
#                                activity=discord.Game(next(status)))

activities = [
    (discord.Activity(type=discord.ActivityType.playing,
                      name="KAMMATTIPADAM | PVP"), "gang_logo", "gang_logo"),
    (discord.Activity(type=discord.ActivityType.playing,
                      name="MRP - MalluRoleplay"), "mrp", "mrp"),
    (discord.Activity(type=discord.ActivityType.listening,
                      name="Admins"), "admin", "admin"),
    #(discord.Activity(type=discord.ActivityType.listening,
    #                  name="Ash"), "admin", "admin"),
    #(discord.Activity(type=discord.ActivityType.listening,
    #                  name="Ash"), "admin", "admin"),
    (discord.Activity(type=discord.ActivityType.watching,
                      name="KAMMATTIPADAM"), "gang_logo", "gang_logo"),
    (discord.Activity(type=discord.ActivityType.watching,
                      name="MATTACHERRY"), "mtb", "mtb"),
    (discord.Activity(type=discord.ActivityType.competing,
                      name="KPM-Deathmatch"), "gang_logo", "gang_logo"),
]


@tasks.loop(seconds=30)
async def change_presence():
    activity = random.choice(activities)
    if activity[0].type == discord.ActivityType.streaming:
        presence = discord.Streaming(name=activity[0].name,
                                     url="https://www.twitch.tv/mychannel")
    else:
        presence = discord.Activity(type=activity[0].type,
                                    name=activity[0].name)
    await client.change_presence(activity=presence, status=discord.Status.dnd)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    change_presence.start()
    VC = client.get_channel(988890347012759575)
    await VC.connect()
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(987972624137191518)
    await log.send("RESTARTED")
    await mylog.send("RESTARTED")



################################################################################################################
################################################################################################################
#####################################  ▀██ █▀█  ################################################################
#####################################  ██▄ █▄█  UPDATE_BOT #####################################################
################################################################################################################
################################################################################################################


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            "You do not have the necessary roles to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply(
            "Sorry, I didn't recognize that command. Please try again.")
    else:
        raise error


funny_messages = [
    "Hey {member.mention}, buckle up for a wild ride! 🚀 Welcome to the chaos! 🎉",
    "Greetings, {member.mention}! Prepare to embark on a journey of memes and mayhem! 😄",
    "Hold on tight, {member.mention}! The Discord adventure begins now! 🌟",
    "Welcome to the server, {member.mention}! We promise, it's not always this crazy... just kidding! 😜",
    "Howdy, {member.mention}! Saddle up and get ready for some epic Discord shenanigans! 🤠",
    "Good to see you, {member.mention}! Time to unleash your inner Discord ninja! 🥷",
    "Ready or not, {member.mention}, here comes a tidal wave of fun and friendship! 🌊",
]

# List of channel IDs where links are allowed
allowed_channels = [
    989015771667656744, 1018893517793267732, 990948143023681556,
    1051377870934655057, 994328496224600074, 1084197579404877865
]

# List of role IDs for roles that are allowed to post links
allowed_roles = [
    989013399914565662, 989013709554855977, 989013571474165831,
    1051366401392267275, 1074617621636468849, 1029108735181860925,
    1084412171695423558
]


@client.event
async def on_member_join(member):
    channel = client.get_channel(988890347012759574)
    welcome_message = random.choice(funny_messages).format(member=member)
    await channel.send(welcome_message)


@slash.slash(description="Show server information")
async def serverstats(ctx):
    guild = ctx.guild
    await guild.fetch_members(limit=None)  # Fetch all members to ensure accurate online status

    total_members = len(guild.members)

    online_members = sum(
        member.status in [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]
        for member in guild.members
    )

    offline_members = total_members - online_members

    unique_roles = len(guild.roles)
    text_channels = len([
        c for c in guild.text_channels
        if c.permissions_for(guild.me).send_messages
    ])

    voice_channels = len([
        c for c in guild.voice_channels
        if c.permissions_for(guild.me).connect
    ])

    embed = discord.Embed(title="Server Statistics 📊", color=0x00ff00)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(
        name="Members",
        value=f"Total: {total_members}  |  Online: {online_members}  |  Offline: {offline_members} 🌐"
    )

    embed.add_field(name="Roles", value=f"Total: {unique_roles} roles 👥")
    embed.add_field(name="Text Channels", value=f"Total: {text_channels} channels 📝")
    embed.add_field(name="Voice Channels", value=f"Total: {voice_channels} channels 🔊")

    embed.set_footer(text="Powered by CW")

    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.reply(f"**My ping : {round(client.latency * 1000)} ms**")
    print(f"My ping : {round(client.latency * 1000)} ms")


@slash.slash(description="Shows bot ping")
async def ping(ctx):
    await ctx.reply(f"**My ping : {round(client.latency * 1000)} ms**")
    print(f"My ping : {round(client.latency * 1000)} ms")


@slash.slash(description="FOR GANG ANNONCEMENT!")
@commands.has_any_role(management, leader, coleader, access)
async def an(ctx, *, content):
    kpmchat = client.get_channel(989015176542040116)
    await kpmchat.send(
        f"<@&989013399914565662> {content} <:KPM:998261860153434234>"
    )
    await ctx.reply("Done <a:Verify:1051515642383192106>")
@an.error
async def an_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="For Usual message")
@commands.has_any_role(management, leader, coleader, access)
async def msg(ctx, channel: discord.TextChannel, *, content):
    await channel.send(f"{content}")
    await ctx.reply("Done <a:Verify:1051515642383192106>")
@msg.error
async def msg_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="send an anon dm message")
@commands.has_any_role(management, leader, coleader, access)
async def dm(ctx, member: discord.Member, *, content):
    await member.create_dm()
    await member.dm_channel.send(f"{content}")
    await ctx.reply("Done <a:Verify:1051515642383192106>")
@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="dm all")
@commands.has_any_role(management, leader, coleader, access)
async def dmall(ctx, *, content):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        rank = members[f'{id}']['rank']
        if rank != 5:
            gang_member = client.get_user(id)
            await gang_member.create_dm()
            await gang_member.dm_channel.send(
                f"{content}")
        i = i + 1
    await ctx.channel.send("Done <a:Verify:1051515642383192106>")
@dmall.error
async def dmall_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Warn a member from gang")
@commands.has_any_role(management, leader, coleader, access)
async def warn(ctx, member: discord.Member, *, reason):
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(996134136613982279)
    await member.create_dm()
    warndm = discord.Embed(
        title="WARNED",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"Hey {member.mention} you have been **warned** from gang **KAMMATTIPADAM** \n \n Reason : {reason}",
        color=0x992d22)
    warndm.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    warndm.set_footer(text="KAMMATTIPADAM BOT")
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        if member_id == id:
            members[f'{member.id}']['warning'] += 1
            await ctx.send("Warn point added")
            break
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await member.dm_channel.send(embed=warndm, content=f"{member.mention}")
    warnlog = discord.Embed(
        title="Used Warn command",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{ctx.author.mention} used **WARN** command to warn {member.mention} \n **Member id:** {member.id}",
        color=0x992d22)
    warnlog.set_author(name=f"{ctx.author}", icon_url=(ctx.author.avatar_url))
    warnlog.set_footer(text="KAMMATTIPADAM BOT")
    await log.send(embed=warnlog)
    await mylog.send(embed=warnlog)
    await ctx.reply("Done <a:Verify:1051515642383192106>")
    print(f"{member} warned by {ctx.author}")
@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )





################################################################################################################
################################################################################################################
###########################################    █▀▀ ▄▀▄ █▄ █ █▀▀    #############################################
###########################################    █▄█ █▀█ █ ▀█ █▄█    #############################################
################################################################################################################
################################################################################################################


@slash.slash(description="recruit a member to gang")
@commands.has_any_role(management, leader, coleader, access)
async def recruit(ctx, member: discord.Member):
    with open('applications.json', 'r') as f:
        applications = json.load(f)
    if f'{member.id}' in applications:
        await ctx.reply("loading....")
        real_name = applications[f'{member.id}']['Realname'] 
        print(f"{real_name}")
        phone_number = applications[f'{member.id}']['phone'] 
        steam_url = applications[f'{member.id}']['steam']
        instagram_id = applications[f'{member.id}']['Instagram'] 
        dob = applications[f'{member.id}']['DOB']
        ingame_name = applications[f'{member.id}']['Ingame name']
        user_email = applications[f'{member.id}']['email'] 
        announcement = client.get_channel(1103600831258968074)
        await announcement.send(
            f"@everyone We officially welcome {member.mention} to GANG **KAMMATTIPADAM** <:GANG_LOGO:998261860153434234>"
        )
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        members_count += 1
        with open('members_count.json', 'w') as f:
            json.dump(members_count, f)
        await add_member_id(members_id, members_count, member)
        with open('members_id.json', 'w') as f:
            json.dump(members_id, f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await add_member(members, member, ingame_name, members_count, steam_url, phone_number, instagram_id, real_name, dob, user_email)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        role = discord.utils.get(ctx.guild.roles, name="social-media")
        users_with_role = [user for user in ctx.guild.members if role in user.roles]
        for user in users_with_role:
                    try:
                        await user.send(f"Add {phone_number} to Whatsapp group!  {ingame_name}")
                        await user.send(f"follow {instagram_id} on official account")
                        print(f"Sent a DM to {user.name}")
                    except discord.Forbidden:
                        print(f"Could not send a DM to {user.name}")
        await member.create_dm()
        await member.dm_channel.send(
            "Welcome to GANG **KAMMATTIPADAM** <:GANG_LOGO:998261860153434234>")
        await member.edit(nick=f"KPM | {ingame_name}")
        await member.dm_channel.send(
            "https://cdn.discordapp.com/attachments/989015771667656744/1007293080640180345/WELCOME.png"
        )
        await member.dm_channel.send(
            "UPDATE YOUR DETAILS IN <#1051377870934655057>")
        await member.dm_channel.send(f"```diff\n+Change your discord name in MRP-MALLUROLEPLAY Discord server to `KPM | {ingame_name}`\n```")
        guild_id = ctx.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        gangrole = discord.utils.get(guild.roles, name='KAMMATTIPADAM')
        kpmfamrole = discord.utils.get(guild.roles, name='KAMMATTIPADAM-FAM')
        whitelist = discord.utils.get(guild.roles, name='Whitelisted🎫')
        await member.add_roles(gangrole)
        await member.add_roles(whitelist)
        await member.add_roles(kpmfamrole)
        await member.dm_channel.send(
            "```diff\n+Whitelist added in KAMMATTIPADAM | PVP\n``` \n **CONNECT : https://cfx.re/join/v4lqzq**"
        )
        del applications[f'{member.id}']
        with open('applications.json', 'w') as f:
            json.dump(applications, f)
        await ctx.channel.send("Done <a:Verify:1051515642383192106>")
        await refresh_members(members_id, members_count, members)
    else:
        await ctx.reply("The user hasn't applied <a:fail:1051515623705944145>")


@recruit.error
async def recruit_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Add money")
@commands.has_any_role(management, leader, coleader, access, finance)
async def add(ctx, member: discord.Member, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        await add_donation(members, member, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await donation_update(members_id, members_count, members)
        await member.create_dm()
        member_fund = members[f'{member.id}']['gang_fund']
        await member.dm_channel.send(
            f"Hey {member.mention} you just gave {amount}$ to GANG **KAMMATTIPADAM** \n Your Total : **{member_fund}$** "
        )
        kpmfinlog = client.get_channel(992649859448451142)
        mykpmfinlog = client.get_channel(987973054527311873)
        await kpmfinlog.send(f"{member.mention} just donated {amount}$")
        await mykpmfinlog.send(f"{member.mention} just donated {amount}$")
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Add FINE")
@commands.has_any_role(management, leader, coleader, access, finance)
async def fine(ctx, member: discord.Member, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await add_fine(members, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        await donation_update(members_id, members_count, members)
        kpmfinlog = client.get_channel(992649859448451142)
        mykpmfinlog = client.get_channel(987973054527311873)
        await member.create_dm()
        await member.dm_channel.send(
            f"Hey {member.mention} your fine of {amount}$ has bee added.")
        await kpmfinlog.send(f"Added a `FINE` of {amount}$ to {member.mention}"
                             )
        await mykpmfinlog.send(
            f"Added a `FINE` of {amount}$ to {member.mention}")
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@fine.error
async def fine_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Add TURF money")
@commands.has_any_role(management, leader, coleader, access, turf)
async def addturf(ctx, member: discord.Member, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        await add_turf_donation(members, member, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await turf_fund_update(members_id, members_count, members)
        await member.create_dm()
        member_fund = members[f'{member.id}']['turf_fund']
        await member.dm_channel.send(
            f"Hey {member.mention} you just gave {amount}$ to GANG **KAMMATTIPADAM** \n Your Total : **{member_fund}$   `TURF`** "
        )
        kpmturflog = client.get_channel(1027114017157816360)
        mykpmturflog = client.get_channel(1027274037157707776)
        await kpmturflog.send(
            f"{member.mention} just donated {amount}$   ``TURF``")
        await mykpmturflog.send(
            f"{member.mention} just donated {amount}$  ``TURF``")
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@addturf.error
async def addturf_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Add EXPENSE")
@commands.has_any_role(management, leader, coleader, access, finance)
async def expense(ctx, amount: int, *, reason):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await add_expense(members, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        await donation_update(members_id, members_count, members)
        kpmfinlog = client.get_channel(992649859448451142)
        mykpmfinlog = client.get_channel(987973054527311873)
        await kpmfinlog.send(
            f"{ctx.author.mention} Added an EXPENSE {amount}$ Reason : {reason}"
        )
        await mykpmfinlog.send(
            f"{ctx.author.mention} Added an EXPENSE {amount}$ Reason : {reason}"
        )
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@expense.error
async def expense_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Add TURF EXPENSE")
@commands.has_any_role(management, leader, coleader, access, turf)
async def turfexpense(ctx, amount: int, *, reason):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await add_turf_expense(members, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        await turf_fund_update(members_id, members_count, members)
        kpmturflog = client.get_channel(1027114017157816360)
        mykpmturflog = client.get_channel(1027274037157707776)
        await kpmturflog.send(
            f"{ctx.author.mention} Added a `TURF` EXPENSE {amount}$ Reason : {reason}"
        )
        await mykpmturflog.send(
            f"{ctx.author.mention} Added a `TURF` EXPENSE {amount}$ Reason : {reason}"
        )
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@turfexpense.error
async def turfexpense_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Rank up a member")
@commands.has_any_role(management, leader, coleader, access)
async def promote(ctx, member: discord.Member, level: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        rankold = members[f'{member.id}']['rank']
        members[f'{member.id}']['rank'] = level
        rank = members[f'{member.id}']['rank']
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)

        await member.create_dm()
        if rank == 0:
            rank = "Worker"
        if rank == 1:
            rank = "Member"
        if rank == 2:
            rank = "Co-Leader"
        if rank == 3:
            rank = "Leader"
        if rank == 5:
            rank == "KICKED"
        else:
            rank == "undefined"
        if rankold == 0:
            rankold = "Worker"
        if rankold == 1:
            rankold = "Member"
        if rankold == 2:
            rankold = "Co-Leader"
        if rankold == 3:
            rankold = "Leader"
        if rankold == 5:
            rankold == "KICKED"
        else:
            rankold == "undefined"
        await member.dm_channel.send(
            f"Hey {member.mention} you ranked up from **{rankold}** to **{rank}**"
        )
        announcement = client.get_channel(989015176542040116)
        await announcement.send(
            f"@everyone {member.mention} just became GANG **{rank}**")
        await ctx.reply("Done <a:Verify:1051515642383192106>")
        await refresh_members(members_id, members_count, members)


@promote.error
async def promote_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="remove a member from gang")
@commands.has_any_role(management, leader, coleader, access)
async def remove(ctx, member: discord.Member, how: int = 0, *, reason=None):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        members[f'{member.id}']['rank'] = 5
        with open('members.json', 'w') as f:
            json.dump(members, f)
        await member.create_dm()
        announcement = client.get_channel(989015176542040116)
        guild_id = ctx.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        gangrole = discord.utils.get(guild.roles, name='KAMMATTIPADAM')
        exmember = discord.utils.get(guild.roles, name='ex-member❄️')
        await member.add_roles(exmember)
        await member.remove_roles(gangrole)
        await member.edit(nick=f"{member.name}")
        if how == 0:
            await member.dm_channel.send(
                f"You Just left from GANG **KAMMATTIPADAM** <:GANG_LOGO:998261860153434234>"
            )
            await announcement.send(
                f"@everyone {member.mention} just left from GANG **KAMMATTIPADAM** <:GANG_LOGO:998261860153434234>"
            )
        elif how == 1:
            await member.dm_channel.send(
                f"You have been **KICKED** from GANG **KAMMATTIPADAM** <:GANG_LOGO:998261860153434234> \n Reason : {reason}"
            )
            await announcement.send(
                f"@everyone {member.mention} removed from GANG **KAMMATTIPADAM**, Reason : {reason} <:GANG_LOGO:998261860153434234>"
            )
        else:
            await ctx.reply("HOW 0 = LEFT , How 1 = KICKED")
        await ctx.reply("Done <a:Verify:1051515642383192106>")
        await refresh_members(members_id, members_count, members)


@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Warning call for a member from gang")
@commands.has_any_role(management, leader, coleader, access)
async def call(ctx, member: discord.Member):
    log = client.get_channel(992655133081092176)
    annu = client.get_channel(989015176542040116)
    mylog = client.get_channel(996134136613982279)
    member_id = member.id
    await member.create_dm()
    warndm = discord.Embed(
        title="WARNED",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"Hey {member.mention} you have been **warned** from gang **KAMMATTIPADAM** \n \n come to [GANG WARNING VC](https://discord.gg/uT8DwURpqe) and talk to any `GANG OFFICIALS`",
        color=0x992d22)
    warndm.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    warndm.set_footer(text="KAMMATTIPADAM BOT")
    await member.dm_channel.send(embed=warndm, content=f"{member.mention}")
    warnlog = discord.Embed(
        title="Used Warn command",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{ctx.author.mention} used **Call** command to warn {member.mention} \n **Member id:** {member.id}",
        color=0x992d22)
    warnlog.set_author(name=f"{ctx.author}", icon_url=(ctx.author.avatar_url))
    warnlog.set_footer(text="KAMMATTIPADAM BOT")
    await log.send(embed=warnlog)
    await mylog.send(embed=warnlog)
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        if member_id == id:
            members[f'{member.id}']['warning'] += 1
            await ctx.send("Warn point added")
            break
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await annu.send(
        f"{member.mention} Come to vc and talk to any <@&989013709554855977> or <@&989013571474165831>"
    )
    await ctx.reply("Done <a:Verify:1051515642383192106>")
    print(f"{member} warned by {ctx.author}")


@call.error
async def call_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Show gang member details!")
@commands.has_any_role(management, leader, coleader, access)
async def user(ctx, member: discord.Member):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    member_id = member.id
    channelid = ctx.channel.id
    await get_member(members_id, members_count, members, member_id, channelid)
    await ctx.reply("Done <a:Verify:1051515642383192106>")

@user.error
async def user_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )



@slash.slash(description="Clear warning point!")
@commands.has_any_role(management, leader, coleader, access)
async def clear_warn_point(ctx, member: discord.Member):
    member_id = member.id
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        if member_id == id:
            members[f'{member.id}']['warning'] = 0
            await ctx.send("Warn point set to 0")
            break
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await ctx.reply("Done <a:Verify:1051515642383192106>")


@clear_warn_point.error
async def clear_warn_point_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Set warning point!")
@commands.has_any_role(management, leader, coleader, access)
async def set_warn_point(ctx, member: discord.Member, point: int):
    member_id = member.id
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        if member_id == id:
            members[f'{member.id}']['warning'] = point
            await ctx.send(f"Warn point set to {point}")
            break
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await ctx.reply("Done <a:Verify:1051515642383192106>")


@set_warn_point.error
async def set_warn_point_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="set TURF balance money")
@commands.has_any_role(management, leader, coleader, access, turf)
async def setturfbalance(ctx, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        balance = members[f'GANGTOAL']['TURF_BALANCE']
        members[f'GANGTOAL']['TURF_BALANCE'] = 0
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await turf_fund_update(members_id, members_count, members)
        kpmturflog = client.get_channel(1027114017157816360)
        mykpmturflog = client.get_channel(1027274037157707776)
        await kpmturflog.send(
            f"{ctx.author.mention} set turf balance to {amount}$ from {balance}  ``TURF``"
        )
        await mykpmturflog.send(
            f"{ctx.author.mention} set turf balance to {amount}$ from {balance}  ``TURF``"
        )
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@setturfbalance.error
async def setturfbalance_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )

@slash.slash(description="Add cafe fund")
@commands.has_any_role(management, leader, coleader, access, turf)
async def cafe_fund(ctx, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        members[f'GANGTOAL']['CAFE'] += amount
        members[f'GANGTOAL']['TOTAL']  += amount
        members[f'GANGTOAL']['BALANCE']  += amount
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await donation_update(members_id, members_count, members)
        kpmfinlog = client.get_channel(992649859448451142)
        mykpmfinlog = client.get_channel(987973054527311873)
        await kpmfinlog.send(
            f"{ctx.author.mention} Added {amount}$ to cafe"
        )
        await mykpmfinlog.send(
            f"{ctx.author.mention} Added {amount}$ to cafe"
        )
        await ctx.reply("Done <a:Verify:1051515642383192106>")
@cafe_fund.error
async def cafe_fund(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )

@slash.slash(description="Add TURF fund to GANG fund (White)")
@commands.has_any_role(management, leader, coleader, access, finance)
async def turf_to_gang_fund(ctx, amount: int):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        await add_turf_to_gang_fund(members, amount)
        with open('members.json', 'w') as f:
            json.dump(members, f)
        await donation_update(members_id, members_count, members)
        await turf_fund_update(members_id, members_count, members)
        kpmfinlog = client.get_channel(992649859448451142)
        mykpmfinlog = client.get_channel(987973054527311873)
        kpmturflog = client.get_channel(1027114017157816360)
        mykpmturflog = client.get_channel(1027274037157707776)
        await kpmfinlog.send(
            f"Added {amount} from turf fund to gang fund by {ctx.author.mention}"
        )
        await mykpmfinlog.send(
            f"Added {amount} from turf fund to gang fund by {ctx.author.mention}"
        )
        await kpmturflog.send(
            f"Added {amount} from turf fund to gang fund by {ctx.author.mention}"
        )
        await mykpmturflog.send(
            f"Added {amount} from turf fund to gang fund by {ctx.author.mention}"
        )
        await ctx.reply("Done <a:Verify:1051515642383192106>")


@turf_to_gang_fund.error
async def turf_to_gang_fund_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Show gang member details!")
@commands.has_any_role(management, leader, coleader, access)
async def print_members_list(ctx):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    channelid = ctx.channel.id
    await print_members(members_id, members_count, members, channelid)
    await ctx.reply("Done <a:Verify:1051515642383192106>")


@print_members_list.error
async def print_members_list_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


#@slash.slash(description="Show gang member details!")
#@commands.has_any_role(management, leader, coleader, access)
#async def db_add(ctx):
#    with open('members.json', 'r') as f:
#        members = json.load(f)
#    with open('members_id.json', 'r') as f:
#        members_id = json.load(f)
#    with open('members_count.json', 'r') as f:
#        members_count = json.load(f)
#    await db_add(members_count, members, members_id)
#    with open('members.json', 'w') as f:
#        json.dump(members, f)
#    await ctx.channel.send("Done <a:Verify:1051515642383192106>")


@slash.slash(description="Set member details")
@commands.has_any_role(management, leader, coleader, access)
async def set_details(ctx,
                      member: discord.Member,
                      ingame_name=None,
                      steam=None,
                      phone=None,
                      instagram=None,
                      realname=None,
                      dob=None):
    member_id = member.id
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    role = discord.utils.get(ctx.guild.roles, name="social-media")
    members_with_role = [member for member in ctx.guild.members if role in member.roles]
    channel = client.get_channel(989015801245863936)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        if member_id == id:
            if ingame_name != None:
                members[f'{member.id}']['Ingame name'] = ingame_name
                await channel.send(f"Ingame name set to {ingame_name}")
            if steam != None:
                members[f'{member.id}']['steam'] = steam
                await channel.send(f"Steam set to {steam}")
            if phone != None:
                members[f'{member.id}']['phone'] = phone
                await channel.send(f"phone set to {phone}")
                for member in members_with_role:
                  try:
                    await member.send(f"Add {phone} to Whatsapp group!")
                    print(f"Sent a DM to {member.name}")
                  except discord.Forbidden:
                    print(f"Could not send a DM to {member.name}")
            if instagram != None:
                members[f'{member.id}']['Instagram'] = instagram
                await channel.send(f"Instagram set to {instagram}")
                for member in members_with_role:
                  try:
                    await member.send(f"follow {instagram} on official account")
                    print(f"Sent a DM to {member.name}")
                  except discord.Forbidden:
                    print(f"Could not send a DM to {member.name}")
            if realname != None:
                members[f'{member.id}']['Realname'] = realname
                await channel.send(f"Realname set to {realname}")
            if dob != None:
                members[f'{member.id}']['DOB'] = dob
                await channel.sendd(f"DOB set to {dob}")
            #else:
            #await ctx.reply("Nothing updated <:lol:1051462961492918273>")
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await ctx.reply("Done <a:Verify:1051515642383192106>")


@set_details.error
async def set_details_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Refresh member list")
@commands.has_any_role(management, leader, coleader, access)
async def refresh_members(ctx):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    await refresh_members(members_id, members_count, members)
    await ctx.reply("Done <a:Verify:1051515642383192106>")



@slash.slash(description="Refresh discord name with ")
@commands.has_any_role(management, leader, coleader, access)
async def refresh_discord(ctx):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        rank = members[f'{id}']['rank']
        if rank != 5:
            member = await client.fetch_user(id)
            members[f'{id}']['Discord'] = member.name
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await ctx.channel.send("Done <a:Verify:1051515642383192106>")


@refresh_discord.error
async def refresh_discord_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="Refresh discord name with ingame name")
@commands.has_any_role(management, leader, coleader, access)
async def refresh_discord_name(ctx):
    with open('members.json', 'r') as f:
        members = json.load(f)
    with open('members_id.json', 'r') as f:
        members_id = json.load(f)
    with open('members_count.json', 'r') as f:
        members_count = json.load(f)
    guild = client.get_guild(988890344785604710)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        rank = members[f'{id}']['rank']
        if rank != 5:
            member = await guild.fetch_member(id)
            ingame_name = members[f'{id}']['Ingame name']
            await member.edit(nick=f"KPM | {ingame_name}")
        i = i + 1
    with open('members.json', 'w') as f:
        json.dump(members, f)
    await ctx.channel.send("Done <a:Verify:1051515642383192106>")


@refresh_discord_name.error
async def refresh_discord_name_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


@slash.slash(description="SET GANG MEMBER AS INACTIVE")
@commands.has_any_role(management, leader, coleader, access)
async def set_inactive(ctx, member: discord.Member):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        members[f'{member.id}']['rank'] = 4
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        announcement = client.get_channel(989015176542040116)
        await announcement.send(f"@everyone {member.mention} set as inactive")
        await ctx.reply("Done <a:Verify:1051515642383192106>")
        await refresh_members(members_id, members_count, members)

@slash.slash(description="Rank up a member")
@commands.has_any_role(management, leader, coleader, access)
async def bench_add(ctx, member: discord.Member):
    if ctx.author.bot == False:
        with open('members.json', 'r') as f:
            members = json.load(f)
        members[f'{member.id}']['rank'] = 0
        with open('members.json', 'w') as f:
            json.dump(members, f)
        with open('members_id.json', 'r') as f:
            members_id = json.load(f)
        with open('members_count.json', 'r') as f:
            members_count = json.load(f)
        announcement = client.get_channel(989015176542040116)
        await announcement.send(f"{member.mention} Added to bench")
        guild_id = ctx.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        bench = discord.utils.get(guild.roles, name='bench')
        await member.add_roles(bench)
        await ctx.reply("Done <a:Verify:1051515642383192106>")
        await refresh_members(members_id, members_count, members)
@bench_add.error
async def bench_add_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(
            f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>"
        )


#@slash.slash(description="Clear gang fund")
#@commands.has_any_role(management)
#async def clear_gang_fund(ctx):
#    if ctx.author.bot == False:
#        with open('members.json', 'r') as f:
#            members = json.load(f)
#        with open('members_id.json', 'r') as f:
#            members_id = json.load(f)
#        with open('members_count.json', 'r') as f:
#            members_count = json.load(f)
#        i = 1
#        while i <= members_count:
#            id = members_id[f'{i}'][f'member id']
#            members[f'{id}']['gang_fund'] = 0
#            i = i + 1
#        members[f'GANGTOAL']['TOTAL'] = 0
#        members[f'GANGTOAL']['EXPENSE'] = 0
#        members[f'GANGTOAL']['BALANCE'] = 0
#        members[f'GANGTOAL']['FINE'] = 0
#        with open('members.json', 'w') as f:
#            json.dump(members, f)
#        await donation_update(members_id, members_count, members)
#        kpmfinlog = client.get_channel(992649859448451142)
#        mykpmfinlog = client.get_channel(987973054527311873)
#        await kpmfinlog.send("@everyone GANG FUND CLEARED")
#        await mykpmfinlog.send("@everyone GANG FUND CLEARED")
#        await ctx.reply("Done <a:Verify:1051515642383192106>")
#
#@slash.slash(description="Clear turf fund")
#@commands.has_any_role(management)
#async def clear_turf_fund(ctx):
#    if ctx.author.bot == False:
#        with open('members.json', 'r') as f:
#            members = json.load(f)
#        with open('members_id.json', 'r') as f:
#            members_id = json.load(f)
#        with open('members_count.json', 'r') as f:
#            members_count = json.load(f)
#        i = 1
#        while i <= members_count:
#            id = members_id[f'{i}'][f'member id']
#            members[f'{id}']['turf_fund'] = 0
#            i = i + 1
#        members[f'GANGTOAL']['TURF_TOTAL'] = 0
#        members[f'GANGTOAL']['TURF_BALANCE'] = 0
#        members[f'GANGTOAL']['TURF_EXPENSE'] = 0
#        with open('members.json', 'w') as f:
#            json.dump(members, f)
#        await donation_update(members_id, members_count, members)
#        kpmfinlog = client.get_channel(992649859448451142)
#        mykpmfinlog = client.get_channel(987973054527311873)
#        await kpmfinlog.send("@everyone GANG FUND CLEARED")
#        await mykpmfinlog.send("@everyone GANG FUND CLEARED")
#        await ctx.reply("Done <a:Verify:1051515642383192106>")


@slash.slash(description="Add armoury item")
@commands.has_any_role(management, leader, coleader, access, armourymag)
async def armoury_add_item(ctx, item=None):
    if ctx.author.bot == False:
        if item == None:
            await ctx.reply("Item not specified.<a:fail:1051515623705944145>")
        else:
            with open('armoury.json', 'r') as f:
                armoury = json.load(f)
            if not item in armoury:
                armoury[f'{item}'] = {}
                armoury[f'{item}']['stock'] = 0
                with open('armoury.json', 'w') as f:
                    json.dump(armoury, f)
                    armourylog = client.get_channel(1102320110246576218)
                    myarmourylog = client.get_channel(1102659779173810196)
                    await armourylog.send(
                        f"{item} added to armoury by {ctx.author.mention}")
                    await myarmourylog.send(
                        f"{item} added to armoury by {ctx.author.mention}")
                    await armoury_update(armoury)
                    await ctx.reply("Done <a:Verify:1051515642383192106>")
            else:
                await ctx.reply(
                    "Item already exists.<a:fail:1051515623705944145>")
@armoury_add_item.error
async def armoury_add_item(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>")

@slash.slash(description="Add armoury item count")
@commands.has_any_role(management, leader, coleader, access, armourymag)
async def add_armoury(ctx, count: int, item=None):
    if ctx.author.bot == False:
        if item == None:
            await ctx.reply("Item not specified.<a:fail:1051515623705944145>")
        else:
            with open('armoury.json', 'r') as f:
                armoury = json.load(f)
            if not item in armoury:
                await ctx.reply(
                    "Item dosen't exists.<a:fail:1051515623705944145>")
            else:
                armoury[f'{item}']['stock'] += count
                with open('armoury.json', 'w') as f:
                    json.dump(armoury, f)
                armourylog = client.get_channel(1102320110246576218)
                myarmourylog = client.get_channel(1102659779173810196)
                await armoury_update(armoury)
                await armourylog.send(f"{count}  x {item} added to armoury by {ctx.author.mention}")
                await myarmourylog.send(f"{count}  x {item} added to armoury by {ctx.author.mention}")
                await ctx.reply("Done <a:Verify:1051515642383192106>")
@add_armoury.error
async def add_armoury(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(f"{ctx.author.mention} You don't have permission to use this command. <a:fail:1051515623705944145>")


################################################################################################################
################################################################################################################
###########################################      █▀▀▄  █     █  █  █▀▀▄    #####################################
###########################################      █     █     █  █  █▀▀▄    #####################################
###########################################      █▄▄▀  █▄▄█  ▀▄▄▀  █▄▄█    Mattancherry Bois ###################
################################################################################################################
################################################################################################################



################################################################################################################
################################################################################################################
###########################|| ASH || █▀▀ █ █ █▄ █ █▀▀ ▀█▀ ▀█▀ █▀█ █▄ █ █▀▀  ####################################
#################################### █▀  █▄█ █ ▀█ █▄▄  █  ▄█▄ █▄█ █ ▀█ ▄██  ####################################
################################################################################################################
################################################################################################################


async def add_member(members, member, ingame_name, members_count, steam, phone, insta, realname, dob, email):
    if not f'{member.id}' in members:
        members[f'{member.id}'] = {}
        members[f'{member.id}']['rank'] = 1
        members[f'{member.id}']['Ingame name'] = ingame_name
        members[f'{member.id}']['Discord'] = member.name
        members[f'{member.id}']['gang_fund'] = 0
        members[f'{member.id}']['turf_fund'] = 0
        members[f'{member.id}']['warning'] = 0
        members[f'{member.id}']['steam'] = steam
        members[f'{member.id}']['phone'] = phone
        members[f'{member.id}']['Instagram'] = insta
        members[f'{member.id}']['Realname'] = realname
        members[f'{member.id}']['DOB'] = dob
        members[f'{member.id}']['email'] = email
    else:
        members[f'{member.id}']['rank'] = 1
        members[f'{member.id}']['Ingame name'] = ingame_name
        members[f'{member.id}']['Discord'] = member.name
        members[f'{member.id}']['gang_fund'] = 0
        members[f'{member.id}']['turf_fund'] = 0
        members[f'{member.id}']['warning'] = 0
        members[f'{member.id}']['steam'] = steam
        members[f'{member.id}']['phone'] = phone
        members[f'{member.id}']['Instagram'] = insta
        members[f'{member.id}']['Realname'] = realname
        members[f'{member.id}']['DOB'] = dob
        members[f'{member.id}']['email'] = email


async def add_member_id(members_id, members_count, member):
    members_id[f'{members_count}'] = {}
    members_id[f'{members_count}']['member id'] = member.id


async def add_donation(members, member, amount):
    members[f'{member.id}']['gang_fund'] += amount
    members[f'GANGTOAL']['TOTAL'] += amount
    members[f'GANGTOAL']['BALANCE'] += amount


async def add_fine(members, amount):
    members[f'GANGTOAL']['TOTAL'] += amount
    members[f'GANGTOAL']['BALANCE'] += amount
    members[f'GANGTOAL']['FINE'] += amount


async def add_turf_donation(members, member, amount):
    members[f'{member.id}']['turf_fund'] += amount
    members[f'GANGTOAL']['TURF_TOTAL'] += amount
    members[f'GANGTOAL']['TURF_BALANCE'] += amount


async def add_turf_to_gang_fund(members, amount):
    members[f'GANGTOAL']['TOTAL'] += amount
    members[f'GANGTOAL']['BALANCE'] += amount
    members[f'GANGTOAL']['TURF_BALANCE'] -= amount


async def donation_update(members_id, members_count, members):
    fincahnnel = client.get_channel(992649793476235284)
    donationembed = discord.Embed(title="GANG FUND ~ KAMMATTIPADAM",
                                  timestamp=datetime.datetime.utcnow(),
                                  description=f"GANG FUND DETAILS",
                                  color=0x992d22)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        ingame_name = members[f'{id}']['Ingame name']
        fund = members[f'{id}']['gang_fund']
        rank = members[f'{id}']['rank']
        if rank != 5:
            if rank != 4:
                donationembed.add_field(name=f"{ingame_name}",
                                        value=f"${fund} ")
        i = i + 1
    gang_total = members[f'GANGTOAL']['TOTAL']
    expense = members[f'GANGTOAL']['EXPENSE']
    balance = members[f'GANGTOAL']['BALANCE']
    fine = members[f'GANGTOAL']['FINE']
    cafe = members[f'GANGTOAL']['CAFE']
    donationembed.add_field(name=f"GANG FINE", value=f"${fine}", inline=False)
    donationembed.add_field(name=f"CAFE", value=f"${cafe}", inline=False)
    donationembed.add_field(name=f"GANG TOTAL",
                            value=f"${gang_total}",
                            inline=False)
    donationembed.add_field(name=f"GANG EXPENSE",
                            value=f"${expense}",
                            inline=False)
    donationembed.add_field(name=f"GANG BALANCE",
                            value=f"${balance}",
                            inline=False)
    donationembed.set_author(
        name=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    donationembed.set_footer(
        text=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    await fincahnnel.send(embed=donationembed)


async def turf_fund_update(members_id, members_count, members):
    turfchannel = client.get_channel(1027113707727233044)
    donationembed = discord.Embed(title="TURF FUND ~ KAMMATTIPADAM",
                                  timestamp=datetime.datetime.utcnow(),
                                  description=f"TURF FUND DETAILS",
                                  color=0x992d22)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        ingame_name = members[f'{id}']['Ingame name']
        fund = members[f'{id}']['turf_fund']
        rank = members[f'{id}']['rank']
        if rank != 5:
            donationembed.add_field(name=f"{ingame_name}", value=f"${fund} ")
        i = i + 1
    gang_total = members[f'GANGTOAL']['TURF_TOTAL']
    expense = members[f'GANGTOAL']['TURF_EXPENSE']
    balance = members[f'GANGTOAL']['TURF_BALANCE']
    donationembed.add_field(name=f"GANG TURF TOTAL",
                            value=f"${gang_total}",
                            inline=False)
    donationembed.add_field(name=f"GANG TURF EXPENSE",
                            value=f"${expense}",
                            inline=False)
    donationembed.add_field(name=f"GANG TURF BALANCE",
                            value=f"${balance}",
                            inline=False)
    donationembed.set_author(
        name=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    donationembed.set_footer(
        text=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    await turfchannel.send(embed=donationembed)


async def add_expense(members, amount):
    members[f'GANGTOAL']['BALANCE'] -= amount
    members[f'GANGTOAL']['EXPENSE'] += amount


async def add_turf_expense(members, amount):
    members[f'GANGTOAL']['TURF_BALANCE'] -= amount
    members[f'GANGTOAL']['TURF_EXPENSE'] += amount


async def get_member(members_id, members_count, members, member_id, channelid):
  channel = client.get_channel(channelid)
  i = 1
  while i <= members_count:
      id = members_id[f'{i}'][f'member id']
      if id == member_id:
          ingame_name = members[f'{id}']['Ingame name']
          Rank = members[f'{id}']['rank']
          gang_fund = members[f'{id}']['gang_fund']
          turf_fund = members[f'{id}']['turf_fund']
          warning = members[f'{id}']['warning']
          steam = members[f'{id}']['steam']
          phone = members[f'{id}']['phone']
          Instagram = members[f'{id}']['Instagram']
          Realname = members[f'{id}']['Realname']
          DOB = members[f'{id}']['DOB']
          email = members[f'{id}']["email"]

          embed = discord.Embed(title=f"KAMMATTIPADAM - ABOUT {ingame_name} <:KAMMATTIPADAM:998261860153434234>", color=0x7289DA)
          embed.add_field(name="Discord ID", value=member_id, inline=False)
          embed.add_field(name="Gang ID", value=i, inline=False)
          embed.add_field(name="Rank", value=Rank, inline=False)
          embed.add_field(name="Gang Fund", value=gang_fund, inline=False)
          embed.add_field(name="Turf Fund", value=turf_fund, inline=False)
          embed.add_field(name="Warnings", value=warning, inline=False)
          embed.add_field(name="Steam", value=steam, inline=False)
          embed.add_field(name="Phone", value=phone, inline=False)
          embed.add_field(name="Instagram", value=Instagram, inline=False)
          embed.add_field(name="Realname", value=Realname, inline=False)
          embed.add_field(name="Date of Birth", value=DOB, inline=False)
          embed.add_field(name="Email", value=email, inline=False)

          await channel.send(embed=embed)

          break
      i += 1


async def print_members(members_id, members_count, members, channelid):
    channel = client.get_channel(channelid)
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        await channel.send(f"id : {i}, Discord : <@{id}>")
        i = i + 1


#async def db_add(members_count, members, members_id):
#    i = 1
#    while i <= members_count:
##        id = members_id[f'{i}'][f'member id']
#        members[f'{id}']['email'] = "NONE"
#        i = i + 1


async def refresh_members(members_id, members_count, members):
    members_channel = client.get_channel(990922958841212968)
    await members_channel.purge()
    time.sleep(10)
    await members_channel.send("**GANG  KAMMATTIPADAM**")
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        discord_name = members[f'{id}']['Discord']
        ingame_name = members[f'{id}']['Ingame name']
        rank = members[f'{id}']['rank']
        if rank == 3:
            await members_channel.send(
                f"```fix\nLEADER: \t {discord_name}  \t  -   \t {ingame_name}\n```"
            )
        i = i + 1
    i = 1
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        discord_name = members[f'{id}']['Discord']
        ingame_name = members[f'{id}']['Ingame name']
        rank = members[f'{id}']['rank']
        if rank == 2:
            await members_channel.send(
                f"```fix\nCO-LEADER: \t {discord_name}  \t  -   \t {ingame_name}\n```"
            )
        i = i + 1
    i = 1
    j = 4
    await members_channel.send("\n\n **MEMBERS:** \n\n")
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        discord_name = members[f'{id}']['Discord']
        ingame_name = members[f'{id}']['Ingame name']
        rank = members[f'{id}']['rank']
        if rank == 1:
            await members_channel.send(
                f"```yaml\n{j} {discord_name}  \t  -   \t {ingame_name}\n```")
            j += 1
        i = i + 1
    i = 1
    await members_channel.send("\n\n **BENCH:** \n\n")
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        discord_name = members[f'{id}']['Discord']
        ingame_name = members[f'{id}']['Ingame name']
        rank = members[f'{id}']['rank']
        if rank == 0:
            await members_channel.send(
                f"```yaml\n{j} {discord_name}  \t  -   \t {ingame_name}  \n```"
            )
            j += 1
        i = i + 1
    i = 1
    await members_channel.send("\n\n **INACTIVE:** \n\n")
    while i <= members_count:
        id = members_id[f'{i}'][f'member id']
        discord_name = members[f'{id}']['Discord']
        ingame_name = members[f'{id}']['Ingame name']
        rank = members[f'{id}']['rank']
        if rank == 4:
            await members_channel.send(
                f"```yaml\n{j} {discord_name}  \t  -   \t {ingame_name}\n```")
            j += 1
        i = i + 1


async def armoury_update(armoury):
    armourychannel = client.get_channel(1102319919057600512)
    donationembed = discord.Embed(title="KAMMATTIPADAM ARMOURY",
                                  timestamp=datetime.datetime.utcnow(),
                                  color=0x992d22)
    keys = list(armoury.keys())
    num_keys = len(armoury)
    i = 1
    print(num_keys)
    for i in range(len(keys)):
        key = keys[i]
        stock = armoury[key]['stock']
        donationembed.add_field(name=f"{key}", value=f"{stock}", inline=True)
    donationembed.set_author(
        name=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    donationembed.set_footer(
        text=f"KAMMATTIPADAM",
        icon_url=
        "https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
    )
    await armourychannel.send(embed=donationembed)


################        CLUB           #################################################


################################################################################################################
################################################################################################################
####################################### █   █▀█ █▀▀ █▀▀ █▀▀ ▀█▀ █▄ █ █▀▀ #######################################
####################################### █▄▄ █▄█ █▄█ █▄█ █▄█ ▄█▄ █ ▀█ █▄█ #######################################
################################################################################################################
################################################################################################################


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    MESSAGElog = client.get_channel(987975390515580938)
    if message.author == client.get_user(765885050125942804):
        authormention = "Ash"
    else:
        authormention = message.author.mention
    await MESSAGElog.send(
        f"{authormention}\t {message.content} \n Attachements : {message.attachments} \n Embeds : {message.embeds} \n CHANNEL ID : {message.channel.id}"
    )

    if isinstance(message.channel, discord.DMChannel):
        channel_id = 1090206968876109934  # replace with the ID of the channel you want to forward messages to
        forward_channel = await client.fetch_channel(channel_id)
        await forward_channel.send(f"{message.author} : {message.content}")

    if message.channel.id == 994328496224600074:
        if not message.attachments and not any(
            (isinstance(a, str) and
             (a.startswith('https://cdn.discordapp.com/attachments/')
              or a.startswith('https://media.discordapp.net/attachments/')))
                for a in message.content.split()):
            await message.delete()
            await message.author.create_dm()
            await message.author.dm_channel.send(
                "Your message was deleted because it didn't have any images. Use <#994328496224600074> only for sharing pictures"
            )
    await client.process_commands(message)

    livealert = client.get_channel(1054065812023021688)
    if message.channel == livealert:
        await message.add_reaction('✅')
        await message.add_reaction('🚫')
    leave = client.get_channel(1113450018418995302)
    if message.channel == leave:
        await message.add_reaction('✅')
        await message.add_reaction('🚫')

    ##  ALL OTHER THINGS ABOVE THIS

    if message.channel.id in allowed_channels or any(
            role.id in allowed_roles for role in message.author.roles
    ) or not re.search(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            message.content):
        return
    await message.delete()
    warn = discord.Embed(
        title="WARNING",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"Hey {message.author.mention} no links allowed in this chat",
        color=0x992d22)
    warn.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    warn.set_footer(text="KAMMATTIPADAM BOT")
    await message.author.create_dm()
    await message.author.dm_channel.send(embed=warn,
                                         content=f"{message.author.mention}")
    await message.channel.send(
        f"{message.author.mention} no links alllowed use other chats")


@client.event
async def on_member_ban(guild, user):
    print(f"{user} got banned from {guild}")
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655223988424786)
    banlog = discord.Embed(
        title="Banned",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{user.mention} (id: {user.id}) has been 🔨 banned from the server!",
        color=0x992d22)
    banlog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    banlog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=banlog)
    await mylog.send(embed=banlog)


@client.event
async def on_member_unban(guild, user):
    print(f"{user} has unbanned from {guild}")
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655223988424786)
    unbanlog = discord.Embed(
        title="Unbanned",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{user.mention} (id: {user.id}) has been 🔓 unbanned from the server!",
        color=0x992d22)
    unbanlog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    unbanlog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=unbanlog)
    await mylog.send(embed=unbanlog)


@client.event
async def on_member_remove(member):
    print(f"{member} left the server")
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655530734653450)
    leftlog = discord.Embed(
        title="Member left",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{member.mention} (id: {member.id}) has ✈️ left the server! \n MEMBER NAME: \t ({member.name})",
        color=0x992d22)
    leftlog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    leftlog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=leftlog)
    await mylog.send(embed=leftlog)


@client.event
async def on_message_edit(before, after):
    print(
        f"message edited;  old message |: {before.content}  new message |: {after.content}"
    )
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655593909264395)
    editlog = discord.Embed(
        title=
        f"Message edited \n old message :` {before.content}` \n new message :  `{after.content}`",
        color=0x992d22)
    editlog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    editlog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=editlog)
    await mylog.send(embed=editlog)


@client.event
async def on_voice_state_update(member, before, after):
    voicelog = discord.Embed(
        title="Voice state updated",
        timestamp=datetime.datetime.utcnow(),
        description=f"{member.mention} voice state updated",
        color=0x992d22)
    if before.afk != after.afk:
        voicelog.add_field(
            name="AFK UPDATE",
            value=f"OLD: **{before.afk}** \n New: **{after.afk}**")
    if before.channel != after.channel:
        if before.channel == None:
            voicelog.add_field(name="Channel UPDATE",
                               value=f"joined **`{after.channel}`**")
        elif after.channel == None:
            voicelog.add_field(name="Channel UPDATE",
                               value=f"left **`{before.channel}`**")
        else:
            voicelog.add_field(
                name="Channel UPDATE",
                value=
                f"moved from **`{before.channel}`** \n  To **`{after.channel}`**"
            )
    if before.deaf != after.deaf:
        voicelog.add_field(
            name="Server DEAF UPDATE",
            value=f"OLD: **{before.deaf}** \n New: **{after.deaf}**")
    if before.mute != after.mute:
        voicelog.add_field(
            name="Server MUTE UPDATE",
            value=f"OLD: {before.mute}** \n New: **{after.mute}**")
    if before.self_mute != after.self_mute:
        voicelog.add_field(
            name="Self MUTE UPDATE",
            value=f"OLD: **{before.self_mute}** \n New: **{after.self_mute}**")
    if before.self_deaf != after.self_deaf:
        voicelog.add_field(
            name="Self DEAF UPDATE",
            value=f"OLD: **{before.self_deaf}** \n New: **{after.self_deaf}**")
    if before.self_stream != after.self_stream:
        voicelog.add_field(
            name="STREAM UPDATE",
            value=
            f"OLD: **{before.self_stream}** \n New: **{after.self_stream}**")
    if before.self_video != after.self_video:
        voicelog.add_field(
            name="VIDEO UPDATE",
            value=f"OLD: **{before.self_video}** \n New: **{after.self_video}**"
        )
    if before.suppress != after.suppress:
        voicelog.add_field(
            name="SUPRESS UPDATE",
            value=f"OLD: **{before.suppress}** \n New: **{after.suppress}**")
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655706475986949)
    voicelog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    voicelog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=voicelog)
    await mylog.send(embed=voicelog)


@client.event
async def on_invite_create(invite):
    print(f"{invite.inviter} created an invite")
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655790114619533)
    invitelog = discord.Embed(
        title="Member left",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"{invite.inviter.mention} created an invite to {invite.channel.mention} \n Code: {invite.code}",
        color=0x992d22)
    invitelog.set_author(
        name="KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    invitelog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=invitelog)
    await mylog.send(embed=invitelog)


@client.event
async def on_message_delete(message):
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655914815467620)
    embeddltlog = discord.Embed(
        title="Message deleted",
        timestamp=datetime.datetime.utcnow(),
        description=
        f"🗑️ Message sent by {message.author.mention} deleted in {message.channel.mention} \n **User id** : {message.author.id} \n  **Content : **{message.content} \n **Attachment** Details if any {message.attachments}",
        color=0xe74c3c)
    embeddltlog.set_author(name=f"{message.author}",
                           icon_url=(message.author.avatar_url))
    embeddltlog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=embeddltlog)
    await mylog.send(embed=embeddltlog)


@client.event
async def on_guild_channel_create(channel):
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655986114428968)
    channellog = discord.Embed(
        title="Channel created",
        timestamp=datetime.datetime.utcnow(),
        description=f"A channel with name {channel.mention} has been created",
        color=0xe74c3c)
    channellog.set_author(
        name=f"KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    channellog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=channellog)
    await mylog.send(embed=channellog)


@client.event
async def on_guild_channel_delete(channel):
    log = client.get_channel(992655133081092176)
    mylog = client.get_channel(992655986114428968)
    channellog = discord.Embed(
        title="Channel Deleted",
        timestamp=datetime.datetime.utcnow(),
        description=f"A channel with name {channel.name} has been Deleted",
        color=0xe74c3c)
    channellog.set_author(
        name=f"KAMMATTIPADAM",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    channellog.set_footer(
        text="KAMMATTIPADAM BOT",
        icon_url=
        ("https://cdn.discordapp.com/attachments/989015771667656744/1006995816164114463/GANG_LOGO.png"
         ))
    await log.send(embed=channellog)
    await mylog.send(embed=channellog)


keep_alive()

if infoc == copyright:
    BotToken = os.environ['TOKEN']
client.run(BotToken)

#  © 2021 | Ash_25
# https://www.ash2500.repl.co/copyright/
