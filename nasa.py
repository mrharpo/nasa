from fastapi import FastAPI
from config import NASA_API_KEY, NASA_API_URL
from datetime import date as dateType
from requests import get
from os import path
from json import dumps

app = FastAPI()
IMAGE_DIR = '/Users/ryan_harbert/Documents/Screen Savers'


def date_range(start_date: dateType, end_date: dateType):
    for ordinal in range(start_date.toordinal(), end_date.toordinal() + 1):
        yield dateType.fromordinal(ordinal)


async def get_apod_data(date: dateType):
    return get(
        NASA_API_URL + 'planetary/apod',
        params={
            'api_key': NASA_API_KEY,
            'date': date,
        },
    ).json()


def save_apod_data(apod, filename):
    with open(path.join(IMAGE_DIR, filename + '.json'), 'w') as j:
        j.write(dumps(apod))


async def save_apod_photo(apod, filename):
    if apod.get('media_type') == 'image':
        # get image
        image = get(apod.get('hdurl') or apod.get('url'))
        with open(path.join(IMAGE_DIR, filename + '.jpg'), 'wb') as i:
            i.write(image.content)


@app.get('/apod')
async def apod(date: dateType = None):
    if not date:
        date = dateType.today()
    response = await get_apod_data(date)
    print(response)
    # write metadata
    filename = str(date)
    save_apod_data(response, filename)
    await save_apod_photo(response, filename)


@app.get('/apods')
async def apods(startDate: dateType, endDate: dateType = None):
    if not endDate:
        endDate = dateType.today()
    days = (endDate - startDate).days
    if days > 31:
        print('date range too long')
    elif days < 1:
        print('end date must be after start date')
    else:
        for d in date_range(startDate, endDate):
            await apod(d)


if __name__ == '__main__':
    from uvicorn import run

    run(app)
