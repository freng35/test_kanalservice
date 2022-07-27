import asyncio
from aiogram import Bot, Dispatcher, executor, types
import db_script

bot = Bot(token='5433024809:AAGPgc4u39zWCXZ_wwCfdtYwrk8hpBzpjTU')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer('Бот, который отправляет сообщения о поставках, которые прошли')


async def main():
    sleep_time = 60 * 60 * 24
    records_sent = []
    await asyncio.sleep(10)

    while True:
        records = db_script.get_records()
        for record in records:
            if record not in records_sent:
                await bot.send_message(427825467, f'Срок поставки заказа №{record[1]} прошел')
                records_sent.append(record)

        await asyncio.sleep(sleep_time)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(executor.start_polling(dp))
    loop.run_forever()
