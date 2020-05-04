import io
from PIL import Image

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async

from gan import GAN


def transform_pil_image_to_bytes(image: Image):
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    buffer.seek(0)
    return buffer


token = '229213507:AAG_Bp8PCvg1fcbdwKVJH2rNV7LEI_boeTM'

REQUEST_KWARGS = {
    'proxy_url': 'socks5://51.15.119.190:1080',
    'urllib3_proxy_kwargs': {
        'username': 'bots_proxy',
        'password': 'inna_made',
    }
}

checkpoint = GAN('../checkpoints')


def get_image_bytes(bot, update):
    if not update.message.photo:
        file_id = update.message.document['file_id']
    else:
        file_id = update.message.photo[-1]['file_id']
    file = bot.getFile(file_id)
    image = file.download_as_bytearray()
    image_path = f'image_{file_id}.jpg'
    file.download(image_path)
    return image_path


def start(bot, update):
    text = 'Привет, я бот, показывающий контура распознаваний с кибаны. Пришли мне url изображения с мониты.\n' \
           'Распознавания показываются по final_recognition, чтобы изменить на raw_recognition напишите команду /switch'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def unknown_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command")


@run_async
def handle_image(bot, update):
    image_path = get_image_bytes(bot, update)
    checkpoint.predict(image_path)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
    # bot.send_message(chat_id=update.message.chat_id, text=text)


def temp(bot, update):
    print(bot)
    print(update)
    bot.send_sticker(update.message.chat_id, 'CAACAgIAAxkBAAIpOl6pQxvHCAN3X7JuXXV2uM9-RazAAAJcAANBqK4GoHz0eN-ZjpMZBA')


if __name__ == '__main__':
    updater = Updater(token=token,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(['start', 'help'], start))
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, handle_image))
    dp.add_handler(MessageHandler(Filters.sticker, temp))

    print('initializing completed')
    updater.start_polling()
