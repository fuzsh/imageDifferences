from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from ImageProcess import image_process
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOICE, PHOTO, RESULT = range(3)


def start(bot, update):
    reply_keyboard = [['Send Images', 'How It Works'], ['Author']]

    update.message.reply_text('سلام \n'
                              'من یه ربات پردازش تصویر نه چندان قوی هستم که برای درس کارگاه کامپیوتر ساخته شده ام.\n'
                              'کار اصلی من اینه که یه عکس از این بازیایی که دو تصویر میدن و میگن اختلافشون رو هست بهم بدی و من به صورت عمودی اونو نصف میکنم'
                              ' و بعدش میام اختلاف ها رو بهت میگم تا جایی که میتونم ....! \n\n'
                              'حالا از من چی میخوای ؟',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return CHOICE


def getImage(bot, update):
    user = update.message.from_user
    logger.info("getImage")
    update.message.reply_text('خب به به قسمت اصلی کار! یه عکس برای من بفرست',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def ERRORgetImage(bot, update):
    user = update.message.from_user
    logger.info("getImage")
    update.message.reply_text('نه دگ نمیشه !\n'
                              ' چیزی که میفرستی باید حتما عکس باشه نه چیز دگ ....\n '
                              'یبار دگ برام عکس بفرست\n',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)

    photo_file.download(str(update.message.chat.id) + '.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('خب خیلیم عالی ....\n'
                              'کمی منتظر بمون تا من برات نتیجه رو بفرستم')

    result(bot, update)
    return CHOICE


def author(bot, update):
    print(update.message.chat.id)
    user = update.message.from_user
    reply_keyboard = [['Send Images', 'How It Works']]
    logger.info("author of")
    update.message.reply_text('ساخته شده با قلب توسط فرزاد شامی و مهدی امینی',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True))


def description(bot, update):
    user = update.message.from_user
    reply_keyboard = [['Send Images', 'Author']]
    logger.info("describtion")
    update.message.reply_text('نحوه ی کار کرد',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True))


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def result(bot, update):
    user_id = update.message.chat.id

    score = image_process(user_id)

    bot.send_photo(user_id, photo=open('./ToUserSend/First-' + str(user_id) + ".jpg", 'rb'))
    bot.send_photo(user_id, photo=open('./ToUserSend/Second-' + str(user_id) + ".jpg", 'rb'))
    bot.send_photo(user_id, photo=open('./ToUserSend/Different-' + str(user_id) + ".jpg", 'rb'))
    bot.send_photo(user_id, photo=open('./ToUserSend/Thresh-' + str(user_id) + ".jpg", 'rb'))

    reply_keyboard = [['Send Images', 'How It Works'], ['Author']]

    update.message.reply_text(
        'SSIM: {}'.format(score),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))


def main():
    updater = Updater("759262213:AAGlPJipFkMVS-UhzmLMijHzTDhumWa5ZVk")

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOICE: [RegexHandler('^(Send Images)$', getImage),
                     RegexHandler('^(How It Works)$', description),
                     RegexHandler('^(Author)$', author)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    MessageHandler(not Filters.photo, ERRORgetImage)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
