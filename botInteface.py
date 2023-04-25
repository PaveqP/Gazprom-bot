import telebot
from telebot import types
import main
from config import group_names, domains_names, technologies_names, using_method_names

bot = telebot.TeleBot('6065747915:AAGWxo4frFKct-CXNXIA3Iqp0s5pj5_pkB4')

identifiers = {}
back_action = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать работу")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=
"Здравствуйте, {0.first_name}! \n\n\
Я бот компании Газпромнефть - Цифровые Решения".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['support'])
def support(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('форма для связи', url='https://forms.yandex.ru/u/64480ba584227c2ccdfe5df7/'))
    bot.send_message(message.chat.id, 'Свяжитесь с нами!', reply_markup=markup)

@bot.message_handler(commands=['info'])
def info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать!")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=
"<b>Инструкция:</b> \n\n\
Я выдаю актуальную информацию на основе выбранных вами данных. \n\n\
Для получения результата вам необходимо пошагово выбрать необходимые\
<b> параметры поиска:</b> \n\n\
\
1. Выбрать функциональную группу; \n\n\
2. Определиться с доменом; \n\n\
3. Указать технологию; \n\n\
4. Выбрать метод использования; \n\n\
5. Наконец, выбрать интересующий сценарий \n\n\
\
<b>Для навигации</b> вы можете использовать встроенное меню, кнопки, предложенные для выбора, а также писать команды вручную, если это потребуется. \n\n\
\
Если вы <b>обнаружили ошибку</b>, хотите <b>задать вопрос</b>, или предложить <b>идею по улучшению</b> сервиса - смело обращайтесь к разработчикам при помощи соответствующей кнопки в меню или команды /support \n\n\
\
Уверен, мы отлично сработаемся. <b>Желаю удачи!</b>".format(message.from_user),
reply_markup=markup, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if (message.chat.type == 'private'):

        # выдача кнопок с функциональными группами
        if (message.text == 'Начать работу' or message.text == "Начать!" or message.text == "◀️ Назад к выбору функциональной группы" or message.text == 'Начать сначала'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            items = main.get_funcGroups()
            for item in items:
                if (item['group_name_ru'] != 'Логистика'):
                    btn = types.KeyboardButton(item['group_name_ru'])
                    markup.add(btn)
            back_action.append('start')
            bot.send_message(message.chat.id, 'Пожалуйста, выберите функциональную группу, с которой хотите работать', reply_markup=markup)

        # выдача кнопок с доменами
        group_flag = 0
        for group in group_names:
            if message.text == group['name'] or message.text == '◀️ Назад к выбору домена':
                group_id = group['id']
                identifiers['group'] = group_id
                domens = main.get_domains(group_id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for domain in domens:
                    btn = types.KeyboardButton(domain['domain'])
                    markup.add(btn)
                back_action.append('group_names')
                btn_back = types.KeyboardButton('◀️ Назад к выбору функциональной группы')
                markup.add(btn_back)
                if group_flag == 0:
                    bot.send_message(message.chat.id, 'Выберите домен', reply_markup=markup)
                    group_flag += 1
                else: 
                    bot.send_message(message.chat.id,'', reply_markup=markup)

        # выдача кнопок с технологиями

        techno_flag = 0
        for dom in domains_names:
            if message.text == dom['name'] or message.text == '◀️ Назад к выбору технологии':
                if techno_flag == 0:
                    domen_id = dom['id']
                    identifiers['domen'] = domen_id
                technos = main.selectTechnos(identifiers['domen'], identifiers['group'])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for techno in technos:
                    btn = types.KeyboardButton(techno['name'])
                    markup.add(btn)
                back_action.append('domains')
                btn_back = types.KeyboardButton('◀️ Назад к выбору домена')
                markup.add(btn_back)
                if techno_flag == 0:
                    bot.send_message(message.chat.id, 'Выберите технологию', reply_markup=markup)
                    techno_flag += 1
                else: 
                    bot.send_message(message.chat.id,'', reply_markup=markup)

        # выдача кнопок с методами использования

        method_flag = 0
        for technology in technologies_names:
            if message.text == technology['name'] or message.text == '◀️ Назад к выбору метода использования':
                if method_flag == 0:
                    technology_id = technology['id']
                    identifiers['technology'] = technology_id
                methods = main.selectMethods(identifiers['technology'], identifiers['domen'], identifiers['group'])
                print(methods)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for method in methods:
                    btn = types.KeyboardButton(method['name'])
                    markup.add(btn)
                back_action.append('technologies')
                btn_back = types.KeyboardButton('◀️ Назад к выбору технологии')
                markup.add(btn_back)
                if method_flag == 0:
                    bot.send_message(message.chat.id, 'Выберите метод использования', reply_markup=markup)
                    method_flag += 1
                else: 
                    bot.send_message(message.chat.id,'', reply_markup=markup)

        # выдача кнопок с наименованиями сценариев

        scenaries_flag = 0
        for using_method in using_method_names:
            if message.text == using_method['name']:
                if scenaries_flag == 0:
                    method_id = using_method['id']
                    identifiers['meth'] = method_id
                scenarios = main.selectScenarios(identifiers['meth'], identifiers['technology'], identifiers['domen'],
                                                 identifiers['group'])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for scenario in scenarios:
                    btn = types.KeyboardButton(scenario['scenario_name_ru'])
                    markup.add(btn)
                back_action.append('using_method')
                btn_back = types.KeyboardButton('◀️ Назад к выбору метода использования')
                markup.add(btn_back)
                if scenaries_flag == 0:
                    bot.send_message(message.chat.id, 'Теперь выберите наименование сценария', reply_markup=markup)
                    scenaries_flag += 1
                else: 
                    bot.send_message(message.chat.id,'', reply_markup=markup)

        scNames = main.selectScenariosNames()

        # выдача всей инфы

        for scenary in scNames:
            if message.text == scenary['scenario_name_ru']:
                scen_id = scenary['id']
                identifiers['scen'] = scen_id
                info = main.getAllInfo(identifiers['scen'])
                print(info)

                for block in info:

                    name = block['scenario_name_ru']
                    descript = block['description_ru']
                    solution_potential_grade = block['solution_potential_grade']
                    solution_potential_ru = block['solution_potential_ru']
                    solution_maturity_grade = block['solution_maturity_grade']
                    solution_maturity_ru = block['solution_maturity_ru']
                    implemented_in_gazprom_ru = block['implemented_in_gazprom_ru']
                    readiness_of_the_company_grade = block['readiness_of_the_company_grade']
                    readiness_of_the_company_ru = block['readiness_of_the_company_ru']
                    benchmarking_name = block['benchmarking_name']
                    benchmarking_description = block['benchmarking_description']
                    benchmarking_company = block['benchmarking_company']
                    benchmarking_year_of_deploy = block['benchmarking_year_of_deploy']
                    rad_name = block['rad_name']
                    rad_description = block['rad_description']
                    tc_name = block['tc_name']

                    if tc_name == '':
                        tc_name = 'Проект отсутствует'

                    bot.send_message(message.chat.id, text=f'<b>Вы выбрали сценарий:</b> {name}', parse_mode='HTML')
                    bot.send_message(message.chat.id, text=f'<b>Описание:</b> {descript}', parse_mode='HTML')
                    bot.send_message(message.chat.id,
                                     text=f'<b >Потенциал решения(1-3) :</b> {solution_potential_grade} \n<b>Описание потенциала решения:</b> {solution_potential_ru}',
                                     parse_mode='HTML')
                    bot.send_message(message.chat.id,
                                     text=f'<b>Рыночная зрелость(1-5) :</b> {solution_maturity_grade} \n<b>Описание рыночной зрелости:</b> {solution_maturity_ru}',
                                     parse_mode='HTML')
                    bot.send_message(message.chat.id,
                                     text=f'<b>Организационная готовность(1-7) :</b> {readiness_of_the_company_grade} \n<b>Описание организационной готовности:</b> {readiness_of_the_company_ru}',
                                     parse_mode='HTML')
                    bot.send_message(message.chat.id, text=f'<b>Реализуется в Газпром:</b> {implemented_in_gazprom_ru}',
                                     reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')

                    benchmarking_text1 = benchmarking_name.split('\n\n')
                    benchmarking_text2 = benchmarking_description.split('\n\n')
                    benchmarking_text3 = benchmarking_company.split('\n\n')
                    benchmarking_text4 = benchmarking_year_of_deploy.split('\n\n')
                    rad_text1 = rad_name.split('\n\n')
                    rad_text2 = rad_description.split('\n\n')
                    benchmarking_result = ''

                    try:
                        check_result = 0
                        if (rad_text1[0] != 'Отсутствует' and benchmarking_text1[0] == 'Отсутствует'):
                            check_result = 1
                            for idx, line in enumerate(rad_text1):
                                benchmarking_result += f'{idx + 1}.\t<b>Проект в ГПН | НИОКР: </b> \
                                \n<b>Название: </b>{rad_text1[idx]} \n<b>Описание: </b>{rad_text2[idx]} \n\n'
                        else:
                            check_result = 2
                            for idx, line in enumerate(benchmarking_text1):
                                benchmarking_result += f'{idx + 1}.\t<b>Наименование: </b>{benchmarking_text1[idx]} \n<b>Описание: </b>{benchmarking_text2[idx]} \
                                \n<b>Компания: </b>{benchmarking_text3[idx]} \n<b>Год внедрения: </b>{benchmarking_text4[idx]} \n\n<b>Проект в ГПН | НИОКР: </b> \
                                \n<b>Название: </b>{rad_text1[idx]} \n<b>Описание: </b>{rad_text2[idx]} \n\n'

                        if (check_result == 1):
                            bot.send_message(message.chat.id,
                                        text=f'<b>Бенчмаркинг(внешний рынок) : Отсутствует</b> \n\n{benchmarking_result}',
                                        reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
                        if (check_result == 2):
                            bot.send_message(message.chat.id,
                                        text=f'<b>Бенчмаркинг(внешний рынок) :</b> \n\n{benchmarking_result}',
                                        reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
                        bot.send_message(message.chat.id, text=f'<b>Название проекта в ЦТ :</b> {tc_name}',
                                    reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
                    except:
                        
                        bot.send_message(message.chat.id, text = "<b>Бенчмаркинг(внешний рынок):</b> отсутствует", parse_mode="html")
                        bot.send_message(message.chat.id, text = "<b>Проект в ЦТ:</b> отсутствует", parse_mode="html")

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn_rebut = types.KeyboardButton('Начать сначала')
                    markup.add(btn_rebut)
                    bot.send_message(message.chat.id,'Выберите действие', reply_markup=markup)



bot.polling(none_stop=True)
