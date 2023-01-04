
import requests


#Text Part
async def get_surah(number):
    url = f"https://al-quran1.p.rapidapi.com/{number}"

    headers = {
        "X-RapidAPI-Key": "5fc30762abmshf92a6b1c9bccbfcp12ea17jsn8524abcc0ea0",
        "X-RapidAPI-Host": "al-quran1.p.rapidapi.com",
    }

    r = requests.get(url, headers=headers)

    res = r.json()

    verses = res["total_verses"]
    # name_en = res["surah_name"]
    # name_ar = res["surah_name_ar"]
    # translation_name = res["translation"]
    # desc = res["description"]
    # verse = res["verses"]["1"]["content"]
    full_arabic = []
    # _full_arabic = []
    # __full_arabic = []

    for i in range(1, verses + 1):
        full_arabic.append(res["verses"][str(i)]["content"])

    return full_arabic


async def get_ayah(num1, num2, num3):
    url = f"https://al-quran1.p.rapidapi.com/{num1}/{num2}-{num3}"

    headers = {
        "X-RapidAPI-Key": "5fc30762abmshf92a6b1c9bccbfcp12ea17jsn8524abcc0ea0",
        "X-RapidAPI-Host": "al-quran1.p.rapidapi.com",
    }

    res = requests.get(url, headers=headers)
    r = res.json()
    ayahs = []

    for i in range(int(num2), int(num3) + 1):

        ayahs.append(r[str(i)]["content"])

    row = "\n".join(ayahs)
    return row


async def quran_uzbek_text(number):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{number}.json"

    res = requests.get(url)
    r = res.json()

    total_verses = len(r["chapter"])
    full = []

    for i in range(0, total_verses):
        full.append((r["chapter"][i]["text"]))

    row = "\n".join(full)
    return row


async def quran_uzbek_text_total(number):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{number}.json"

    res = requests.get(url)
    r = res.json()

    total_verses = len(r["chapter"])
    # full = []

    return total_verses


async def quran_uzbek_text_ayah(num, num2):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{num}/{num2}.json"

    res = requests.get(url)
    r = res.json()

    verse = []
    verse.append(r["text"])

    return verse[0]


#Audio part

async def send_full_audio(number):

    if int(number) > 0 and int(number) < 10:
        number = str(0) + str(0) + str(number)
    elif int(number) >= 10 and int(number) < 100:
        number = str(0) + str(number)
    else:
        number = number

    link = f"https://server8.mp3quran.net/afs/{number}.mp3"

    response = requests.get(link, allow_redirects=True)

    open("file/audio.mp3", "wb").write(response.content)

    return True


# async def send_verse_audio(surah, ayah):
#     if int(surah) > 0 and int(surah) < 10:
#         surah = str(0) + str(0) + str(surah)
#     elif int(surah) > 9 and int(surah) < 100:
#         surah = str(0) + str(surah)
#     elif int(surah) > 99 and int(surah) < 115:
#         surah = str(surah)
#     else:
#         return "Invalid input!"

#     if int(ayah) > 0 and int(ayah) < 10:
#         ayah = str(0) + str(0) + str(ayah)
#     elif int(ayah) > 9 and int(ayah) < 100:
#         ayah = str(0) + str(ayah)
#     elif int(ayah) > 99 and int(ayah) < 115:
#         ayah = str(ayah)
#     else:
#         return "Invalid input!"

#     link = f"http://www.everyayah.com/data/Alafasy_128kbps/{surah}{ayah}.mp3"

#     resp = requests.get(link, allow_redirects=True)

#     open("verse/verse.mp3", "wb").write(resp.content)

#     return True


# def search_music(name):
#     url = "https://spotify23.p.rapidapi.com/search/"
#     querystring = {
#         "q": f"{name}",
#         "type": "multi",
#         "offset": "2",
#         "limit": "2",
#         "numberOfTopResults": "5",
#     }

#     headers = {
#         "X-RapidAPI-Key": "5fc30762abmshf92a6b1c9bccbfcp12ea17jsn8524abcc0ea0",
#         "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)

#     r = response.json()

#     music = r["tracks"]["items"][0]["data"]["uri"]

#     open("file/music.mp3", "wb").write(response.content)

#     # playsound.playsound("music.mp3")

#     return name
