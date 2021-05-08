# Need to run "pip install discord" for packages to work

import discord
import datetime
from discord.ext import commands
from datetime import date
import time
import asyncio


def main():
    client = commands.Bot(command_prefix='$')

    @client.event
    async def on_ready():
        channel = client.get_channel('CHANNEL_ID')

        await channel.send('Bot online!') # Lets us know our bot is online

    # Temporarily bans users for X amount of days
    @client.command(name='tempban', pass_context=True) 
    @commands.has_role('Moderators')
    async def tempban(ctx, member: discord.Member, duration: int, *, reason=None):
        channel = client.get_channel('CHANNEL_ID')
        # num_of_days = duration * 86400  # converts number you enter from seconds to days
        num_of_minutes = duration * 60
        time_banned = duration
        today = date.today()

        # Displays card in punishment log channel with info on temp ban
        embed_msg = discord.Embed(title='User Receiving Temporary Ban:', description=str(
            member.display_name), color=0xF1E94B)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Number of days banned:',
                            value=int(time_banned), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been temporarily banned from the Discord server for {time_banned} day(s). The reason for this ban is because {reason}.')
        await member.ban()
        await ctx.message.delete()
        # await client.delete_message(ctx.message)
        await asyncio.sleep(num_of_minutes)
        await member.unban()
        await channel.send(f'User {member.display_name} has been unbanned.')

    #Bans users from the discord server
    @client.command(name='ban', pass_context=True)
    @commands.has_role('Moderators')
    async def ban(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID')
        today = date.today()

        # Displays card in punishment log channel with info on ban
        embed_msg = discord.Embed(title='User Receiving Permanent Ban:', description=str(
            member.display_name), color=0xEE1717)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been banned from the Discord server. The reason for this ban is because {reason}.')
        await member.ban()
        await ctx.message.delete()

    # Warns user and sends a message to the user informing them of why they were warned
    @client.command(name='warn', pass_context=True)
    @commands.has_role('Moderators')
    async def warn(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID')
        today = date.today()

        # Displays card in punishment log channel with info on warn
        embed_msg = discord.Embed(title='User Receiving Warning:', description=str(
            member.display_name), color=0xEE7E17)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You are receiving a warning for {reason}. Please do not do this again. Thank you!')
        await ctx.message.delete()

    # Mutes users from being able to talk in normal chat channels
    @client.command(name='mute', pass_context=True)
    @commands.has_role('Moderators')
    async def therapy(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel("CHANNEL_ID")
        today = date.today()

        # Removes chat role and adds mute role
        role = discord.utils.get(member.guild.roles, name='approved')
        await member.remove_roles(role)
        role = discord.utils.get(member.guild.roles, name='mute')
        await member.add_roles(role)

        # Displays card in punishment log channel with info on mute
        embed_msg = discord.Embed(title='User Muted:', description=str(
            member.display_name), color=0x41ECDB)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been muted on the Discord server. Please speak with a mod to find out why.')
        await ctx.message.delete()

    # Removes mute from user and sends them message informing them they were unmuted
    @client.command(name='removemute', pass_context=True)
    @commands.has_role('Moderators')
    async def removetherapy(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID')
        today = date.today()

        role = discord.utils.get(member.guild.roles, name='mute')
        await member.remove_roles(role)
        role = discord.utils.get(member.guild.roles, name='approved')
        await member.add_roles(role)

        embed_msg = discord.Embed(title='User unmuted:', description=str(
            member.display_name), color=0xD84DFF)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been unmuted and should have access to general chat now. Have a nice day!')
        await ctx.message.delete()

    # Allows users to add roles to themselves in discord server
    @client.command(name='addrole', pass_context=True)
        @commands.has_role('approved')
        async def addrole(ctx, role: discord.Role):
            member = ctx.author
            await member.add_roles(role)
            await ctx.send('Role added to user ' + str(member) + ': ' + str(role))

    # Allows user to remove roles from themselves in discord server
    @client.command(name='removerole', pass_context=True)
    @commands.has_role('approved')
    async def removerole(ctx, role: discord.Role):
        member = ctx.author
        await member.remove_roles(role)
        await ctx.send('Role removed from user ' + str(member) + ': ' + str(role))

    # Command for moderating. Allows mods to verify users and grants access to normal chatting channels
    @client.command(name='approve', pass_context=True)
    # @commands.has_role('Moderators')
    @commands.has_permissions(manage_roles=True)
    async def approve(ctx, *members: discord.Member): # *members lets you add multiple users in 1 command to the approved role
        await ctx.message.delete()
        role_id = 'ROLE_ID'
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        i = 0

        # Counter for all users needing approved role added
        for member in members:
            i += 1

        await ctx.send('Adding the approved role to ' + str(i) + ' users. Please wait!')
        await asyncio.sleep(1)

        # Adds role to each member and displays message verifying role was added
        for member in members:
            await member.add_roles(role)
            await ctx.send(str(member) + ' has been approved!')
            await asyncio.sleep(1)

    #Beginning of the role reaction commands
    reaction_title = ""
    reactions = {}
    reaction_message_id = ""

    # Creates card with emoji reacts on it which allows users to add different roles to themselves
    @client.command(name="createreactpost")
    async def createreactpost(ctx):
        embed_msg = discord.Embed(title='Add your roles here!', color=0x6d49d0)
        embed_msg.add_field(
            name="Set Title", value="$setreactiontitle \"New Title\"", inline=False)
        embed_msg.add_field(
            name="Add Role", value="$addrolereaction @Role EMOJI_HERE", inline=False)
        embed_msg.add_field(
            name="Remove Role", value="$removerolereaction @Role", inline=False)
        embed_msg.add_field(
            name="Send Creation Post", value="$sendreactionpost", inline=False)

        await ctx.send(embed=embed_msg)
        await ctx.message.delete()

    @client.command(name="setreactiontitle")
    async def setreactiontitle(ctx, new_title):

        global reaction_title
        reaction_title = new_title
        await ctx.send("The title for the message is now `" + reaction_title + "`!")
        await ctx.message.delete()

    @client.command(name="addrolereaction")
    async def addrolereaction(ctx, role: discord.Role, reaction):

        if role != None:
            reactions[role.name] = reaction
            await ctx.send("Role `" + str(role.name) + "` has been added with the emoji " + str(reaction))
            await ctx.message.delete()
        else:
            await ctx.send("Please try again!")

    @client.command(name="removerolereaction")
    async def removerolereaction(ctx, role: discord.Role):

        if role.name in reactions:
            del reactions[role.name]
            await ctx.send("Role `" + str(role.name) + "` has been deleted!")
            await ctx.message.delete()
        else:
            await ctx.send("That role was not added!")

    @client.command(name="sendreactionpost")
    async def sendreactionpost(ctx):
        global reaction_title

        description = "React to add your roles here!\n\n"

        for role in reactions:
            description += "`" + str(role) + "` - " + \
                str(reactions[role]) + "\n"

        embed_msg = discord.Embed(
            title=reaction_title, description=description, color=0x6d49d0)

        message = await ctx.send(embed=embed_msg)

        global reaction_message_id
        reaction_message_id = str(message.id)

        for role in reactions:
            await message.add_reaction(reactions[role])

        await ctx.message.delete()

    @client.event
    async def on_reaction_add(reaction, user):
        global reaction_message_id

        if not user.bot:
            message = reaction.message

            if str(message.id) == reaction_message_id:
                role_to_give = ""

                for role in reactions:
                    if reactions[role] == reaction.emoji:
                        role_to_give = role

                role_for_reaction = discord.utils.get(
                    user.guild.roles, name=role_to_give)
                await user.add_roles(role_for_reaction)

    #End of the role reaction commands
    
    @ client.event
    async def on_message(message):
        if message.content == 'hello octus':
            await message.channel.send(f'Hello {message.author}!')

        await client.process_commands(message)

    client.run('YOUR_API_KEY_HERE')

if __name__ == '__main__':
    main()