from app.dependencies import settings

uri = f'{settings.MONGO_CONNECTION}://{settings.MONGO_ROOT_USERNAME}:{settings.MONGO_ROOT_PASSWORD}@{settings.MONGO_HOST}'

if settings.MONGO_CONNECTION != 'mongodb+srv':
    uri += f':{settings.MONGO_PORT}'

uri += f'/{settings.MONGO_DB}?authSource=admin'
