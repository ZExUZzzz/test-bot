import discord
import discord.voice_client
import traceback
import requests
import time
import ffmpeg


from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from random import randint

with open('dict.txt', 'r', encoding='Windows-1251') as dictos:
    replics = dictos.read().split(';')

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))

def got_anekdot(type):
    request_anekdot = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=' + type)
    return request_anekdot.text[12:-2]

def apexapirequest(whois):
    try:
        player = requests.get(
            'https://public-api.tracker.gg/v2/apex/standard/profile/origin/'+whois,
            params={'TRN-Api-Key': 'e8072754-58a4-4c23-9663-de9d1feeee88'}).json()

        player = player['data']
        player_stats = player['segments'][0]['stats']

    except KeyError:
        #print('Ошибка. Возможно неверно введен ник')
        return 'error'

    player_active_legend = player['metadata']['activeLegendName']
    if player_stats.get('level'):
        player_level = int(player_stats['level']['value'])
    else:
        player_level = 'Нет данных'
    if player_stats.get('kills'):
        player_kills = int(player_stats['kills']['value'])
    else:
        player_kills = 'Нет данных'
    if player_stats.get('damage'):
        player_damage = int(player_stats['damage']['value'])
    else:
        player_damage = 'Нет данных'
    if player_stats.get('rankScore'):
        player_rank = player_stats['rankScore']['metadata']['rankName']
    else:
        player_rank = 'Нет данных'

    #print(player_level, player_kills, player_damage, player_active_legend, player_rank)

    whois = [whois, player_level, player_active_legend, player_kills, player_damage, player_rank]
    return whois

Bot = commands.Bot(command_prefix='!')

@Bot.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await connect.channel()
        await ctx.send(f'Бот присоединился к каналу')

@Bot.command()
async def Привет(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет {author.mention}')

@Bot.command()
async def Reboot(ctx):
    await ctx.send(f'Анус себе ребутни, пёс')

@Bot.command()
async def SudoReboot(ctx):
    await ctx.send(f'I will be back...')
    time.sleep(randint(1,3))
    await ctx.send(f'Я вернулся, кожанные ублюдки')

@Bot.command()
async def reboot(ctx):
    await ctx.send(f'Анус себе ребутни, пёс')

@Bot.command()
async def DieStupiudBot(ctx):
    await ctx.send(f'Дохнешь только ты через наносекунду после высадки. А я тебя ещё переживу')

@Bot.command()
async def Rank(ctx, arg):
    await ctx.send('Секундочку... веду поиск')
    player_data = apexapirequest(arg)
    if player_data != 'error':
        await ctx.send(embed=discord.Embed(description=f'** {ctx.author.name}, информация по вашему запросу:**' + '\n Имя игрока: ' + str(player_data[0]) + '\n Текущий уровень: ' + str(player_data[1]) + '\n Текущая легенда: ' + str(player_data[2]) + '\n Убийств: ' + str(player_data[3]) + '\n Нанес урона: ' + str(player_data[4]) + '\n Текущий ранг: ' + str(player_data[5]),color=0x0c0c0c))
        print('Игрок:', player_data[0])
        print('Текущий уровень:', player_data[1])
        print('Текущая легенда:', player_data[2])
        print('Убийств:', player_data[3])
        print('Нанес урона:', player_data[4])
        print('Текущий ранг:', player_data[5])
    else:
        print(player_data)
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, игрок не найден.**'+'\n Попробуй ещё', color=0x0c0c0c))

@Bot.command()
async def Анекдот(ctx):
    await ctx.send(got_anekdot('1'))

@Bot.command()
async def Анекдот18(ctx):
    await ctx.send(got_anekdot('18'))

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))
    if isinstance(error, commands.MissingRequiredArgument ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, необходимо ввести имя пользователя после команды через пробел.**', color=0x0c0c0c))

@Bot.event
async def on_message(ctx):
    for attach in ctx.attachments:
        await ctx.channel.send(replics[randint(0,len((replics))-1)])
    await Bot.process_commands(ctx)
@Bot.event
async def on_voice_state_update(member, before, after):
    member = str(member)
    before = str(before).split(' ')
    after = str(after).split(' ')
    channel_message = Bot.get_channel(777477363847921677)
    if before[4][8:] == 'None>':
        channel_input_output = Bot.get_channel(int(after[5][3:]))
        await channel_message.send(member[0:-5]+' зашёл на канал ' + channel_input_output.name)
    if after[4][8:] == 'None>':
        channel_input_output = Bot.get_channel(int(before[5][3:]))
        await channel_message.send(member[0:-5] + ' покинул канал ' + channel_input_output.name)

Bot.run('Nzc3Nzc2ODA2MTEwOTUzNDc0.X7IXGA.DPnSs0ytPtLznRgSokB6y8okdCQ')

#Keyes:
#Nzc3Nzc2ODA2MTEwOTUzNDc0.X7IXGA.DPnSs0ytPtLznRgSokB6y8okdCQ TESTBOTSERVER
#Nzc3NDc2NjU5NjExODI4MjM1.X7D_kA.FGxXfHPnWSIqUWBshGqXlDObHbs MNO_BOT