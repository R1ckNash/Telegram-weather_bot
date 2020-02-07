import telebot
import config
import pyowm

def bot_start():

    owm = pyowm.OWM(config.weatherToken, language='ru')
    bot = telebot.TeleBot(config.token)

    keyboard_weather = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_weather.row('Погода Москва','Погода Питер','Погода Волгоград')

    def get_wind_direction(deg):
        l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
        for i in range(0,8):
            step = 45.
            min = i*step - 45/2.
            max = i*step + 45/2.
            if i == 0 and deg > 360-45/2.:
                deg = deg - 360
            if deg >= min and deg <= max:
                res = l[i]
                break
        return res

    def show_weather(message):
        try:
            city_name = message.text.lower()[7:]
            observation = owm.weather_at_place(city_name)
            w = observation.get_weather()
            l = observation.get_location()
            name = l.get_name()
            country = l.get_country()
            reference_time = w.get_reference_time(timeformat='iso')
            sunset_time = w.get_sunset_time(timeformat='iso')
            sunrise_time = w.get_sunrise_time(timeformat='iso')
            status = w.get_detailed_status()
            temp = w.get_temperature('celsius')['temp']
            wind = w.get_wind('meters_sec')['speed']
            wind_deg = w.get_wind('meters_sec')['deg']

            answer = 'В городе ' + name + ', ' + country + ' в данный момент ' + status + '\n' \
                     + 'Температура в районе ' + str(round(temp)) + ' градусов' + '\n' \
                     + 'Ветер ' + str(wind) + 'м/с ' + get_wind_direction(wind_deg) + '\n' \
                     + 'Время ' + reference_time + '\n' \
                     + 'Время восхода солнца ' + sunrise_time + '\n' \
                     + 'Время захода солнца ' + sunset_time
            if 'снег' in status:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAIBMF49TETrs98_SE3jWo-JUQIOCpfOAAJ1AQACpkRICzV41ue6d7zZGAQ')
            elif 'дожд' in status:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAIBMl49THdzAAFSL68UmrOIwvobxCMswgACJAEAAqZESAsL5_Fz7_gGkBgE')
            elif 'солн' in status:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAIBM149TIkXR0flisSfBDasnlD1E9UmAAIiAQACpkRICxH1ucyPFfRmGAQ')
            elif 'облачно' in status:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAIBQV49Tj9saESnFdukwWLBUeK-RBMrAAJpAQACpkRIC3_d3Ey8De8JGAQ')
            else:
                bot.send_message(message.chat.id, 'Странная погода')

            bot.send_message(message.chat.id, answer)
        except pyowm.exceptions.api_response_error.NotFoundError:
            bot.send_message(message.chat.id, 'Город не найден, повторите попытку')

    @bot.message_handler(commands=['web'])
    def default_test(message):
        keyboard_web = telebot.types.InlineKeyboardMarkup()
        url_button_1 = telebot.types.InlineKeyboardButton(text="Yandex", url="https://yandex.ru/")
        url_button_2 = telebot.types.InlineKeyboardButton(text="YouTube", url="https://www.youtube.com/")
        url_button_3 = telebot.types.InlineKeyboardButton(text="Google", url="https://www.google.com/")
        keyboard_web.add(url_button_1, url_button_2, url_button_3)
        bot.send_message(message.chat.id, "Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard_web)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет, я могу показывать погоду, введи:' + '\n'
                                          '/help если нужна помощь' + '\n'
                                          '/web если нужны ссылки для быстрого перехода', reply_markup=keyboard_weather)

    @bot.message_handler(commands=['help'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Если хочешь получить прогноз погоды просто введи: погода <название города> '
                                          'или воспользуйся клавиатурой')

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'Доброго времени суток')
        elif message.text.lower() == 'пока':
            bot.send_message(message.chat.id, 'До встречи')
        elif message.text.lower() == 'как дела бот?':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMaXjwWFOiBULQKjSSIfoEILw-o5IcAAlcJAAJ5XOIJKyQBwA8ZVV4YBA')
        elif 'погода' in message.text.lower():
            show_weather(message)

    @bot.message_handler(content_types=['sticker'])
    def send_sticker(message):
        print(message)

    bot.polling()