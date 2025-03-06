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
    today = datetime.today()
    tarih = today.strftime('%Y-%m-%d')
    guncel_saat = datetime.now().strftime('%H:%M')

    response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={tarih}&days=1&timezoneOffset=180&calculationMethod=Turkey')
    data = response.json()

    times = data["times"]
    prayer_times = list(times.values())[0]
    iftar_saati = prayer_times[4]  # İftar saati
    sahur_saati = prayer_times[0]  # Sahur saati

    zaman1 = datetime.strptime(guncel_saat, "%H:%M")
    zaman2_iftar = datetime.strptime(iftar_saati, "%H:%M")
    fark_iftar = zaman2_iftar - zaman1

    if fark_iftar.total_seconds() < 0:
        # İftar geçmiş, sıradaki günü al
        tomorrow = today + timedelta(days=1)
        tarih = tomorrow.strftime('%Y-%m-%d')
        response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={tarih}&days=1&timezoneOffset=180&calculationMethod=Turkey')
        data = response.json()
        prayer_times = list(data["times"].values())[0]
        iftar_saati = prayer_times[4]
        sahur_saati = prayer_times[0]
        zaman2_iftar = datetime.strptime(iftar_saati, "%H:%M")
        fark_iftar = zaman2_iftar - zaman1

    fark_dakika_iftar = int(fark_iftar.total_seconds() // 60)
    saat_iftar = fark_dakika_iftar // 60
    dakika_iftar = fark_dakika_iftar % 60

    # Sahura kalan süre hesaplama
    zaman2_sahur = datetime.strptime(sahur_saati, "%H:%M")
    fark_sahur = zaman2_sahur - zaman1

    if fark_sahur.total_seconds() < 0:
        # Sahur geçmiş, sıradaki günü al
        tomorrow = today + timedelta(days=1)
        tarih = tomorrow.strftime('%Y-%m-%d')
        response = requests.get(f'https://vakit.vercel.app/api/timesForPlace?id={city_id}&date={tarih}&days=1&timezoneOffset=180&calculationMethod=Turkey')
        data = response.json()
        prayer_times = list(data["times"].values())[0]
        sahur_saati = prayer_times[0]
        zaman2_sahur = datetime.strptime(sahur_saati, "%H:%M")
        fark_sahur = zaman2_sahur - zaman1

    fark_dakika_sahur = int(fark_sahur.total_seconds() // 60)
    saat_sahur = fark_dakika_sahur // 60
    dakika_sahur = fark_dakika_sahur % 60

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