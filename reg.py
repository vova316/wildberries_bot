import asyncio
from aiogram import Bot, Dispatcher , executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot('1265769369:AAHLQMOAuEztBsioqwmtJbjRpby_47JAi2A', parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
	from myhends import dp
	#from npd import scheduled
	#dp.loop.create_task(scheduled(3))
	executor.start_polling(dp)
