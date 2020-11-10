from aiohttp import web

async def index(request):
    return web.Response(text='Hello Aiohttp!')

async def home(request):
    return web.Response('./views/home')