from tsbot import TSBot, TSCtx, query
from unidecode import unidecode
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import asyncio
import os

load_dotenv()

username = os.getenv("TS3_USERNAME")
password = os.getenv("TS3_PASSWORD")
address = os.getenv("TS3_ADDRESS")

bot = TSBot(
    username=username,
    password=password,
    address=address,
)

cities = ["Istanbul", "Ankara", "Elazığ", "Eskişehir"]  # Buraya istediğin şehirleri ekleyebilirsin.
cities.reverse()

def check_city_id(CityName):
    normalized_city_name = unidecode(CityName.lower())
    response = requests.get(f'https://vakit.vercel.app/api/searchPlaces?q={CityName}&lang=tr')
    data = response.json()

    for city in data:
        city_name = unidecode(city["name"].lower())
        if city_name == normalized_city_name:
            return city["id"]

    return None

def check_iftar_and_sahur(city_id):
    # Şu anki TAM TARİH ve SAAT (timezone-aware olmalı, API ile aynı olmalı)
    current_datetime = datetime.now()
    
    # Bugünün tarihini al
    today_date = current_datetime.strftime('%Y-%m-%d')
    
    # Bugünün vakitlerini çek
    response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={today_date}&days=1&timezoneOffset=180&calculationMethod=Turkey')
    data = response.json()
    
    # Bugünün iftar ve sahur saatleri (TARİH ile birlikte)
    bugun_times = list(data["times"].values())[0]
    iftar_bugun = datetime.strptime(f"{today_date} {bugun_times[4]}", "%Y-%m-%d %H:%M")
    sahur_bugun = datetime.strptime(f"{today_date} {bugun_times[0]}", "%Y-%m-%d %H:%M")
    
    # İftar kontrolü
    if current_datetime < iftar_bugun:
        iftar_zamani = iftar_bugun
    else:
        # Yarının iftarını çek
        yarin_date = (current_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
        response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={yarin_date}&days=1&timezoneOffset=180&calculationMethod=Turkey')
        data = response.json()
        yarin_times = list(data["times"].values())[0]
        iftar_zamani = datetime.strptime(f"{yarin_date} {yarin_times[4]}", "%Y-%m-%d %H:%M")
    
    # Sahur kontrolü (DİKKAT: Yarının sahuru bugünün gecesine ait!)
    yarin_date = (current_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
    response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={yarin_date}&days=1&timezoneOffset=180&calculationMethod=Turkey')
    data = response.json()
    yarin_times = list(data["times"].values())[0]
    sahur_yarin = datetime.strptime(f"{yarin_date} {yarin_times[0]}", "%Y-%m-%d %H:%M")
    
    # Süre hesaplamaları
    fark_iftar = iftar_zamani - current_datetime
    fark_sahur = sahur_yarin - current_datetime
    
    # Formatlama
    saat_iftar = fark_iftar.seconds // 3600
    dakika_iftar = (fark_iftar.seconds % 3600) // 60
    
    saat_sahur = fark_sahur.seconds // 3600
    dakika_sahur = (fark_sahur.seconds % 3600) // 60
    
    return f"{saat_iftar} saat {dakika_iftar} dakika", f"{saat_sahur} saat {dakika_sahur} dakika"

@bot.on("connect")
async def on_connect(bot: TSBot, ctx: TSCtx):
    print("Bot başarıyla bağlandı!")

    await create_channel(bot, ctx, "[cspacerr]╚═══════════════════╝", 0)
    
    for city in cities:
        city_id = check_city_id(city)
        if city_id is None:
            print(f"Şehir bulunamadı: {city}")
            continue

        kalan_sure_iftar, kalan_sure_sahur = check_iftar_and_sahur(city_id)

        sahur_channel_name = f"[cspacer]{city} | {kalan_sure_sahur}"
        sahur_channel_id = await create_channel(bot, ctx, sahur_channel_name, 0)

        async def sahur_task(channel_id, cityname, cityid):
            while True:
                await asyncio.sleep(60)

                _, kalan_sure_sahur = check_iftar_and_sahur(cityid)
                sahur_channel_name = f"[cspacer]{cityname} | {kalan_sure_sahur}"

                await update_channel(bot, ctx, channel_id, sahur_channel_name)

        asyncio.create_task(sahur_task(sahur_channel_id, city, city_id))

    await create_channel(bot, ctx, "[cspacer] Sahur Saatleri", 0)
    await create_channel(bot, ctx, "[cspacerrrr]╔═══════════════════╗", 0)
    await create_channel(bot, ctx, "[cspacerrrrr]╚═══════════════════╝", 0)

    for city in cities:
        city_id = check_city_id(city)
        if city_id is None:
            print(f"Şehir bulunamadı: {city}")
            continue

        kalan_sure_iftar, kalan_sure_sahur = check_iftar_and_sahur(city_id)

        iftar_channel_name = f"[cspacer]{city} | {kalan_sure_iftar}"
        iftar_channel_id = await create_channel(bot, ctx, iftar_channel_name, 0)

        async def iftar_task(channel_id, cityname, cityid):
            while True:
                await asyncio.sleep(60)

                kalan_sure_iftar, _, = check_iftar_and_sahur(cityid)
                iftar_channel_name = f"[cspacer]{cityname} | {kalan_sure_iftar}"

                await update_channel(bot, ctx, channel_id, iftar_channel_name)

        asyncio.create_task(iftar_task(iftar_channel_id, city, city_id))

    await create_channel(bot, ctx, "[cspacer] Iftar Saatleri", 0)
    await create_channel(bot, ctx, "[cspacerrr]╔═══════════════════╗", 0)

async def create_channel(bot: TSBot, ctx: TSCtx, channel_name: str, order: int):
    channels_list = await bot.send(query("channellist"))
    for channel in channels_list:
        if channel_name.lower() == channel["channel_name"].lower():
            print(f"Oda zaten var: {channel_name}")
            return

    response = await bot.send(query("channelcreate").params(
        channel_name=channel_name,
        channel_flag_permanent=1,
        channel_order=order
    ))
    channel_id = response["cid"]

    await bot.send(query("channeladdperm").params(
        cid=channel_id,
        permsid="i_channel_needed_join_power",
        permvalue=999999999
    ))

    print(f"Kanal oluşturuldu: {channel_name} | {channel_id}")
    
    return channel_id

async def update_channel(bot: TSBot, ctx: TSCtx, channel_id: int, channel_name: str):
    await bot.send(query("channeledit").params(cid=channel_id, channel_name=channel_name))
    print(f"{channel_id} kanalı güncellendi: {channel_name}")
    return

asyncio.run(bot.run())