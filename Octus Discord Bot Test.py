# Need to run "pip install discord" for packages to work

import discord
import datetime
from discord import player
from discord.ext import commands
from datetime import date
import time
import asyncio
import random
from displayCard import displayCard
from getBlackJackTotal import getBlackJackTotal


def main():
    client = commands.Bot(command_prefix='$')

    @client.event
    async def on_ready():
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')

        await channel.send('Bot online!')

    @client.command(name='blackjack', pass_context=True)
    @commands.has_role('Admin')
    async def blackjack(ctx):
        await ctx.message.delete()
        num_of_cards_in_hand = 0
        play_game = True
        card_to_draw = random.randint(1, 52)
        player_blackjack_count = 0
        dealer_blackjack_count = 0
        dealer_has_busted = False
        player_will_stay = False
        card_number = ''

        list_of_cards = ['Aclub.png', '2club.png', '3club.png', '4club.png', '5club.png', '6club.png', '7club.png', '8club.png',
                         '9club.png', 'Tclub.png', 'Jclub.png', 'Qclub.png', 'Kclub.png', 'Adiamonds.png', '2diamonds.png', '3diamonds.png', '4diamonds.png', '5diamonds.png', '6diamonds.png', '7diamonds.png', '8diamonds.png', '9diamonds.png', 'Tdiamonds.png', 'Jdiamonds.png', 'Qdiamonds.png', 'Kdiamonds.png', 'Ahearts.png', '2hearts.png', '3hearts.png', '4hearts.png', '5hearts.png', '6hearts.png', '7hearts.png', '8hearts.png', '9hearts.png', 'Thearts.png', 'Jhearts.png', 'Qhearts.png', 'Khearts.png', 'Aspades.png', '2spades.png', '3spades.png', '4spades.png', '5spades.png', '6spades.png', '7spades.png', '8spades.png', '9spades.png', 'Tspades.png', 'Jspades.png', 'Qspades.png', 'Kspades.png']

        card_names = ['Ace of club', '2 of club', '3 of club', '4 of club', '5 of club', '6 of club', '7 of club', '8 of club', '9 of club', '10 of club', 'Jack of club', 'Queen of club', 'King of club', 'Ace of diamonds', '2 of diamonds', '3 of diamonds', '4 of diamonds', '5 of diamonds', '6 of diamonds', '7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', 'Jack of diamonds', 'Queen of diamonds', 'King of diamonds',
                      'Ace of hearts', '2 of hearts', '3 of hearts', '4 of hearts', '5 of hearts', '6 of hearts', '7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'Jack of hearts', 'Queen of hearts', 'King of hearts', 'Ace of spades', '2 of spades', '3 of spades', '4 of spades', '5 of spades', '6 of spades', '7 of spades', '8 of spades', '9 of spades', '10 of spades', 'Jack of spades', 'Queen of spades', 'King of spades', ]

        cards_in_hand = []

        cards_in_deck = len(list_of_cards)

        await ctx.send('------------------------------------------------')

        await ctx.send('The dealer will play first')

        while play_game == True:
            card_to_draw = random.randint(1, cards_in_deck)

            # await displayCard(ctx, list_of_cards, card_to_draw)
            cards_in_hand.append(card_names[card_to_draw])

            #print(f'Value for card_to_draw: {card_to_draw}')
            card_name = list_of_cards[card_to_draw]
            list_of_cards.remove(card_name)
            #print(f'Length of list_of_cards: {len(list_of_cards)}')
            card_number = list_of_cards[card_to_draw][0]

            num_of_cards_in_hand += 1
            cards_in_deck -= 1

            if cards_in_deck > 0:
                await ctx.send('The dealer will now play')

                if player_blackjack_count <= 21:
                    await ctx.send('Here is my card')
                    await displayCard(ctx, list_of_cards, card_to_draw)
                    dealer_blackjack_count = await getBlackJackTotal(card_number, dealer_blackjack_count)
                    await ctx.send(f'Cards left in deck: {cards_in_deck}\n\nPlayer Blackjack count: {player_blackjack_count}\nDealer Blackjack count: {dealer_blackjack_count}\n')

                    if player_will_stay == False:
                        await ctx.send('What would you like to do?\nA. Hit\nB. View cards in hand\nC. Stand\nD. Quit')
                    else:
                        # Need to possibly make all this a function that can be called
                        continue

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['a', 'b', 'c', 'd']

                    msg = await client.wait_for('message', check=check)

                    if msg.content.lower() == 'a':
                        await ctx.send('Here is your card')
                        await displayCard(ctx, list_of_cards, card_to_draw)
                        player_blackjack_count = await getBlackJackTotal(card_number, player_blackjack_count)
                        await asyncio.sleep(2)
                    elif msg.content.lower() == 'b':
                        stay_in_menu = True
                        await ctx.send('Cards in hand currently:')
                        for i in range(num_of_cards_in_hand):
                            await ctx.send(f'{cards_in_hand[i]}')

                        while stay_in_menu == True:
                            await ctx.send('What would you like to do?\nA. Hit\nB. View cards in hand again\nC. Stay')
                            player_will_stay = True

                            def check(msg):
                                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['a', 'b', 'c']

                            msg = await client.wait_for('message', check=check)

                            if msg.content.lower() == 'a':
                                stay_in_menu == False
                                break
                            elif msg.content.lower() == 'b':
                                await ctx.send('Cards in hand currently:')
                                for i in range(num_of_cards_in_hand):
                                    await ctx.send(f'{cards_in_hand[i]}')
                            elif msg.content.lower() == 'c':
                                stay_in_menu == False
                                break
                    elif msg.content.lower() == 'c':
                        # Need to possibly make all this a function that can be called
                        player_will_stay = True
                        await ctx.send('I will continue to hit')
                        while player_will_stay == True:
                            await ctx.send('Here is my card')
                            await displayCard(ctx, list_of_cards, card_to_draw)
                            dealer_blackjack_count = await getBlackJackTotal(card_number, dealer_blackjack_count)
                            await ctx.send(f'Cards left in deck: {cards_in_deck}\n\nPlayer Blackjack count: {player_blackjack_count}\nDealer Blackjack count: {dealer_blackjack_count}\n')

                            if dealer_blackjack_count >= 21:
                                player_will_stay == False
                                await ctx.send('The dealer hit over 21. That\'s a bust for me. You win!')
                                play_game = False

                    elif msg.content.lower() == 'd':
                        await ctx.send('Have a good day!')
                        play_game = False
                        break
                elif dealer_blackjack_count > 21:
                    await ctx.send('The dealer hit over 21. That\'s a bust for me. You win!')
                    play_game == False
                    break
                elif player_blackjack_count > 21:
                    await ctx.send('You hit over 21. That\'s a bust for you. You lose!')
                    play_game == False
                    break
            else:
                await ctx.send('The deck is empty.')
                await ctx.send('Have a good day!')
                play_game = False
                break

    @client.command(name='tempban', pass_context=True)
    @commands.has_role('Admin')
    async def tempban(ctx, member: discord.Member, duration: int, *, reason=None):
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')
        # num_of_days = duration * 86400  # converts number you enter from seconds to days
        num_of_minutes = duration * 60
        time_banned = duration
        today = date.today()

        embed_msg = discord.Embed(title='User Receiving Temporary Ban:', description=str(
            member.display_name), color=0xF1E94B)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Number of days banned:',
                            value=int(time_banned), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been temporarily banned from the server for {time_banned} day(s). The reason for this ban is because {reason}.')
        await member.ban()
        await ctx.message.delete()
        # await client.delete_message(ctx.message)
        await asyncio.sleep(num_of_minutes)
        await member.unban()
        await channel.send(f'User {member.display_name} has been unbanned.')

    @client.command(name='ban', pass_context=True)
    @commands.has_role('Admin')
    async def ban(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')
        today = date.today()

        embed_msg = discord.Embed(title='User Receiving Permanent Ban:', description=str(
            member.display_name), color=0xEE1717)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been banned from the server. The reason for this ban is because {reason}.')
        await member.ban()
        await ctx.message.delete()

    @client.command(name='warn', pass_context=True)
    @commands.has_role('Admin')
    async def warn(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')
        today = date.today()

        embed_msg = discord.Embed(title='User Receiving Warning:', description=str(
            member.display_name), color=0xE6DF2E)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You are receiving a warning for {reason}. Please do not do this again. Thank you!')
        await ctx.message.delete()

    @client.command(name='detain', pass_context=True)
    @commands.has_role('Admin')
    async def detain(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')
        today = date.today()

        #role = discord.utils.get(member.guild.roles, name='approved')
        # await member.remove_roles(role)
        role = discord.utils.get(member.guild.roles, name='Muted')
        await member.add_roles(role)

        embed_msg = discord.Embed(title='User sent to cell:', description=str(
            member.display_name), color=0x41ECDB)
        embed_msg.add_field(name='Reason:',
                            value=str(reason), inline=False)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been detained on the server. Please see the channel so a mod can discuss the reason why you were sent there. Thank you!')
        await ctx.message.delete()

    @client.command(name='undetain', pass_context=True)
    @commands.has_role('Admin')
    async def undetain(ctx, member: discord.Member, *, reason=None):
        channel = client.get_channel('CHANNEL_ID_TO_POST_MESSAGE_IN')
        today = date.today()

        role = discord.utils.get(member.guild.roles, name='Muted')
        await member.remove_roles(role)
        #role = discord.utils.get(member.guild.roles, name='approved')
        # await member.add_roles(role)

        embed_msg = discord.Embed(title='User removed from cell:', description=str(
            member.display_name), color=0xD84DFF)
        embed_msg.add_field(name='Date:',
                            value=str(today), inline=False)
        await channel.send(embed=embed_msg)
        await member.send(f'You have been undetained on the us-politixxxs server and should have access to general chat now. Have a nice day!')
        await ctx.message.delete()

    @client.command(name='addrole', pass_context=True)
    # @commands.has_role('Admin')
    async def addrole(ctx, role: discord.Role):
        member = ctx.author

        if (role.id == 'Administrator' or role.id == 'Moderator'):
            await ctx.send('Unable to add role ' + str(role) + ' to user ' + str(member) + '.')
        else:
            await member.add_roles(role)
            await ctx.send('Role added to user ' + str(member) + ': ' + str(role))

    @client.command(name='removerole', pass_context=True)
    # @commands.has_role('Admin')
    async def removerole(ctx, role: discord.Role):
        member = ctx.author

        if (role.id == 'Administrator' or role.id == 'Moderator'):
            await ctx.send('Unable to remove role ' + str(role) + ' from user ' + str(member) + '.')
        else:
            await member.remove_roles(role)
            await ctx.send('Role removed from user ' + str(member) + ': ' + str(role))

    @client.command(name='approve', pass_context=True)
    # @commands.has_role('Moderators')
    @commands.has_permissions(manage_roles=True)
    async def approve(ctx, *members: discord.Member):
        await ctx.message.delete()
        role_id = 'ROLE_ID_HERE'
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        i = 0

        for member in members:
            i += 1

        await ctx.send('Adding the approved role to ' + str(i) + ' users. Please wait!')
        await asyncio.sleep(1)

        for member in members:
            await member.add_roles(role)
            await ctx.send(str(member) + ' has been approved!')
            await asyncio.sleep(1)

    @client.command(name='shutdown', pass_context=True)
    @commands.has_role('Admin')
    async def shutdown(ctx):
        await ctx.send('I am logging off now. Goodbye!')
        await client.close()

    # Beginning of the role reaction commands
    reaction_title = ""
    reactions = {}
    reaction_message_id = ""

    @client.command(name="createreactpost")
    async def createreactpost(ctx):
        embed_msg = discord.Embed(title='Add your roles here!', color=0x6d49d0)
        embed_msg.add_field(
            name="Set Title", value="$setposttitle \"New Title\"", inline=False)
        embed_msg.add_field(
            name="Add Role", value="$addrolereact @Role EMOJI_HERE", inline=False)
        embed_msg.add_field(
            name="Remove Role", value="$removerolereact @Role", inline=False)
        embed_msg.add_field(
            name="Send Creation Post", value="$sendreactpost", inline=False)

        await ctx.send(embed=embed_msg)
        await ctx.message.delete()

    @client.command(name="setposttitle")
    async def setreactiontitle(ctx, new_title):

        global reaction_title
        reaction_title = new_title
        await ctx.send("The title for the message is now `" + reaction_title + "`!")
        await ctx.message.delete()

    @client.command(name="addrolereact")
    async def addrolereaction(ctx, role: discord.Role, reaction):

        if role != None:
            reactions[role.name] = reaction
            await ctx.send("Role `" + str(role.name) + "` has been added with the emoji " + str(reaction))
            await ctx.message.delete()
        else:
            await ctx.send("Please try again!")

    @client.command(name="removerolereact")
    async def removerolereaction(ctx, role: discord.Role):

        if role.name in reactions:
            del reactions[role.name]
            await ctx.send("Role `" + str(role.name) + "` has been deleted!")
            await ctx.message.delete()
        else:
            await ctx.send("That role was not added!")

    @client.command(name="sendreactpost")
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

    @client.command(name="playgame")
    async def playgame(ctx):
        await ctx.send('What game would you like to play?')
        await asyncio.sleep(1)
        await ctx.send('A. Pick a number\nB. Heads or tails\nC. Quit\nType a letter to select an option!')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['a', 'b', 'c']

        msg = await client.wait_for('message', check=check)

        if msg.content.lower() == 'a':
            user_did_win = False
            correct_number = random.randint(1, 10)

            await ctx.send('Enter a number between 1 and 10.\nIf you guess the right number you win!')

            while user_did_win == False:
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

                msg = await client.wait_for('message', check=check)

                if int(msg.content) == correct_number:
                    await ctx.send('You guess right! You win.')
                    user_did_win = True
                else:
                    await ctx.send('You guessed wrong. Try again!')
                    await asyncio.sleep(1)
        elif msg.content.lower() == 'b':
            correct_number = random.randint(1, 2)
            await ctx.send('I will flip a coin and you will guess if it landed on heads or tails.')
            await ctx.send('Flipping coin now')
            await asyncio.sleep(3)
            await ctx.send('Alright, guess which side landed face up!')
            await asyncio.sleep(1)
            await ctx.send('A. Heads\nB. Tails\nType a letter to select an option!')

            #user_did_win = False

            # while user_did_win == False:
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['a', 'b']

            msg = await client.wait_for('message', check=check)

            if correct_number == 1:
                if msg.content.lower() == 'a':
                    await ctx.send('You guessed right! You win.')
                    user_did_win = True
                else:
                    await ctx.send('You guessed wrong. You lose!')
                    await asyncio.sleep(1)
            elif correct_number == 2:
                if msg.content.lower() == 'b':
                    await ctx.send('You guessed right! You win.')
                    user_did_win = True
                else:
                    await ctx.send('You guessed wrong. You lose!')
                    await asyncio.sleep(1)
        elif msg.content.lower() == "c":
            await ctx.send('Well I didn\'t want to play anymore games with you anyways!')
        else:
            await ctx.send('I\'m sorry, I don\'t understand what you said.')

    # End of the role reaction commands

    @client.event
    async def on_message(message):
        channel = message.channel
        if message.content == 'hello octus' or message.content == 'Hello octus' or message.content == 'Hello Octus':
            await message.channel.send(f'Hello {message.author}!')

        await client.process_commands(message)

    client.run('YOUR_API_KEY_HERE')


if __name__ == '__main__':
    main()
