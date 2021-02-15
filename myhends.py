from reg import bot, dp
from aiogram.types import Message, CallbackQuery
#from mykeyboards import menu, sub_menu 
from aiogram.dispatcher.filters import Command, Text
from bs4 import BeautifulSoup as bs
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
#from keyboardwb import menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import pyowm
import requests
import asyncio

x = 0

class Translater(StatesGroup):
	T1 = State()

@dp.message_handler(Command('start'))
async def welcome(message: Message):
	await bot.send_message(chat_id=message.from_user.id, text=f'Привет {message.from_user["first_name"]}, напиши /search и я переведу тебе текст 😄')

@dp.message_handler(Command('search'))
async def quizz(message: Message):
	await message.answer("Выбери тип товара:")
	await Translater.T1.set()

@dp.message_handler(state=Translater.T1)
async def ans1(message: Message, state: FSMContext):
	await state.update_data(answer1=message.text)
	data = await state.get_data()
	answer1 = data.get("answer1")
	await message.answer("Выберите товар")
	await state.finish()
	global host
	host = 'https://www.wildberries.ru'
	global tURL
	tURL = f'https://www.wildberries.ru/catalog/0/search.aspx?search={answer1}&sort-popular'
	HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
	response = requests.get(tURL, headers = HEADERS)
	soup = bs(response.content, 'html.parser')
	global cardname
	cardname = soup.findAll('div', class_ = 'dtList i-dtList j-card-item')
	global cardprice
	cardprice = soup.findAll('div', class_ = 'j-cataloger-price')
	global names
	global brands
	global links
	global prices
	global lastpr
	names = []
	brands = []
	links = []
	prices = []
	lastpr = []


	
	for item1 in cardname:
		names.append({'name': item1.find('span', class_ = 'goods-name c-text-sm').get_text(strip = True)})

	for item2 in cardname:
		brands.append({'brand': item2.find('strong', class_ = 'brand-name c-text-sm').get_text(strip = True)})


	for item3 in cardname:
		links.append({'link': item3.find('a', class_ = 'ref_goods_n_p j-open-full-product-card').get('href')})

	for item4 in cardprice:
		prices.append({'price': item4.find('ins', class_ = 'lower-price')})
		

	for item5 in cardname:
		lastpr.append({'lastprice': item5.find('span', class_ = 'price-sale active')})

	name = names[x]
	name = str(name)
	name = name[10:-2]

	#достаем бренд товара
	brand = brands[x]
	brand = str(brand)
	brand = brand[11:-3]

	#достаем ссылку на карточку товара
	#for link in links[x]:
	global link
	link = links[x]
	link = str(link)
	link = link[10:-2]
	link = host + link

	#достаем цену товара
	price = prices[x]
	price = str(price)
	price = price[36:-7]
	#достаем скидку на товар
	lastprice = lastpr[x]
	lastprice = str(lastprice)
	lastprice = lastprice[47:-8]
	buy_menu = InlineKeyboardMarkup(
		inline_keyboard=[
		[
		InlineKeyboardButton(text = " ⬅️ Назад ", callback_data = "back"),
		InlineKeyboardButton(text = " Вперед ➡️ ", callback_data = "next"),
		],
		[
		InlineKeyboardButton(text = "✅ Перейти", url = link)
		],
		[
		InlineKeyboardButton(text = "❌ Отменить ❌", callback_data = "cancel")
		]
		])
	await message.answer(link + "\n" + brand + " - " + name + "\n" + "Цена: " + price + "\n" + "Скидка: " + lastprice, reply_markup=buy_menu)
ans1(Message, FSMContext)

print(x)

@dp.callback_query_handler(text="back")
async def back(call: CallbackQuery):
	await call.message.edit_reply_markup()
	z = len(names) - 1
	global x
	if x == 0:
		x = z
		name = names[x]
		name = str(name)
		name = name[10:-2]

		#достаем бренд товара
		brand = brands[x]
		brand = str(brand)
		brand = brand[11:-3]

		#достаем ссылку на карточку товара
		#for link in links[x]:
		global link
		link = links[x]
		link = str(link)
		link = link[10:-2]
		link = host + link

		#достаем цену товара
		price = prices[x]
		price = str(price)
		price = price[36:-7]
		#достаем скидку на товар
		lastprice = lastpr[x]
		lastprice = str(lastprice)
		lastprice = lastprice[47:-8]
		buy_menu = InlineKeyboardMarkup(
			inline_keyboard=[
			[
			InlineKeyboardButton(text = " ⬅️ Назад ", callback_data = "back"),
			InlineKeyboardButton(text = " Вперед ➡️ ", callback_data = "next"),
			],
			[
			InlineKeyboardButton(text = "✅ Перейти", url = link)
			],
			[
			InlineKeyboardButton(text = "❌ Отменить ❌", callback_data = "cancel")
			]
			])
		await call.message.answer(link + "\n" + brand + " - " + name + "\n" + "Цена: " + price + "\n" + "Скидка: " + lastprice, reply_markup=buy_menu)
	else:
		x = x - 1
		name = names[x]
		name = str(name)
		name = name[10:-2]

		#достаем бренд товара
		brand = brands[x]
		brand = str(brand)
		brand = brand[11:-3]

		#достаем ссылку на карточку товара
		#for link in links[x]:
		link = links[x]
		link = str(link)
		link = link[10:-2]
		link = host + link

		#достаем цену товара
		price = prices[x]
		price = str(price)
		price = price[36:-7]
		#достаем скидку на товар
		lastprice = lastpr[x]
		lastprice = str(lastprice)
		lastprice = lastprice[47:-8]
		buy_menu = InlineKeyboardMarkup(
			inline_keyboard=[
			[
			InlineKeyboardButton(text = " ⬅️ Назад ", callback_data = "back"),
			InlineKeyboardButton(text = " Вперед ➡️ ", callback_data = "next"),
			],
			[
			InlineKeyboardButton(text = "✅ Перейти", url = link)
			],
			[
			InlineKeyboardButton(text = "❌ Отменить ❌", callback_data = "cancel")
			]
			])
		await call.message.answer(link + "\n" + brand + " - " + name + "\n" + "Цена: " + price + "\n" + "Скидка: " + lastprice, reply_markup=buy_menu)

back(CallbackQuery)
@dp.callback_query_handler(text="next")
async def next(call: CallbackQuery):
	await call.message.edit_reply_markup()
	z = len(names) - 1
	global x
	if x == z:
		x = 0
		name = names[x]
		name = str(name)
		name = name[10:-2]

		#достаем бренд товара
		brand = brands[x]
		brand = str(brand)
		brand = brand[11:-3]

		#достаем ссылку на карточку товара
		#for link in links[x]:
		global link
		link = links[x]
		link = str(link)
		link = link[10:-2]
		link = host + link

		#достаем цену товара
		price = prices[x]
		price = str(price)
		price = price[36:-7]
		#достаем скидку на товар
		lastprice = lastpr[x]
		lastprice = str(lastprice)
		lastprice = lastprice[47:-8]
		buy_menu = InlineKeyboardMarkup(
			inline_keyboard=[
			[
			InlineKeyboardButton(text = " ⬅️ Назад ", callback_data = "back"),
			InlineKeyboardButton(text = " Вперед ➡️ ", callback_data = "next"),
			],
			[
			InlineKeyboardButton(text = "✅ Перейти", url = link)
			],
			[
			InlineKeyboardButton(text = "❌ Отменить ❌", callback_data = "cancel")
			]
			])
		await call.message.answer(link + "\n" + brand + " - " + name + "\n" + "Цена: " + price + "\n" + "Скидка: " + lastprice, reply_markup=buy_menu)
	else:
		x = x + 1
		name = names[x]
		name = str(name)
		name = name[10:-2]

		#достаем бренд товара
		brand = brands[x]
		brand = str(brand)
		brand = brand[11:-3]

		#достаем ссылку на карточку товара
		#for link in links[x]:
		link = links[x]
		link = str(link)
		link = link[10:-2]
		link = host + link

		#достаем цену товара
		price = prices[x]
		price = str(price)
		price = price[36:-7]
		#достаем скидку на товар
		lastprice = lastpr[x]
		lastprice = str(lastprice)
		lastprice = lastprice[47:-8]
		buy_menu = InlineKeyboardMarkup(
			inline_keyboard=[
			[
			InlineKeyboardButton(text = " ⬅️ Назад ", callback_data = "back"),
			InlineKeyboardButton(text = " Вперед ➡️ ", callback_data = "next"),
			],
			[
			InlineKeyboardButton(text = "✅ Перейти", url = link)
			],
			[
			InlineKeyboardButton(text = "❌ Отменить ❌", callback_data = "cancel")
			]
			])
		await call.message.answer(link + "\n" + brand + " - " + name + "\n" + "Цена: " + price + "\n" + "Скидка: " + lastprice, reply_markup=buy_menu)
next(CallbackQuery)

@dp.callback_query_handler(text="cancel")
async def next(call: CallbackQuery):
	await call.answer('Вы отменили покупку', show_alert = True)
	await call.message.edit_reply_markup()
