import asyncio
import telebot
from App import Event
from loguru import logger
from telebot import util
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


class BotRunner(object):
    def __init__(self, config):
        self.bot = config.bot
        self.proxy = config.proxy
        self.config = config

    def botcreate(self):
        bot = AsyncTeleBot(self.bot.botToken, state_storage=StateMemoryStorage())
        return bot, self.bot

    def run(self):
        logger.success("Bot Start")
        bot, _config = self.botcreate()
        if self.proxy.status:
            from telebot import asyncio_helper
            asyncio_helper.proxy = self.proxy.url
            logger.success("Proxy Set")

        @bot.message_handler(commands=["start", "help"], chat_types=['private'])
        async def handle_command(message):
            await Event.start(bot, message, self.config.ip)

        @bot.message_handler(commands=['ip'])
        async def handle_ip(message):
            command_args = message.text.split()
            if len(command_args) == 1:
                await bot.reply_to(message, "格式错误, 格式应为 /ip [IP/Domain]")
            elif len(command_args) == 2:
                await Event.handle_ip(bot, message, self.config.ip)
            else:
                await bot.reply_to(message, "格式错误, 格式应为 /ip [IP/Domain]")

        @bot.message_handler(commands=['ip_ali'])
        async def handle_ip(message):
            command_args = message.text.split()
            if len(command_args) == 1:
                await bot.reply_to(message, "格式错误, 格式应为 /ip_ali [IP/Domain]")
            elif len(command_args) == 2:
                await Event.handle_ip_ali(bot, message, self.config.ip)
            else:
                await bot.reply_to(message, "格式错误, 格式应为 /ip_ali [IP/Domain]")

        @bot.message_handler(commands=['icp'])
        async def handle_icp(message):
            command_args = message.text.split()
            if len(command_args) == 1:
                await bot.reply_to(message, "格式错误, 格式应为 /icp [Domain]")
            elif len(command_args) == 2:
                await Event.handle_icp(bot, message)
            else:
                await bot.reply_to(message, "格式错误, 格式应为 /icp [Domain]")

        @bot.message_handler(commands=['whois'])
        async def handle_whois(message):
            command_args = message.text.split()
            if len(command_args) == 1:
                await bot.reply_to(message, "格式错误, 格式应为 /whois [Domain]")
            elif len(command_args) == 2:
                await Event.handle_whois(bot, message)
            else:
                await bot.reply_to(message, "格式错误, 格式应为 /whois [Domain]")

        @bot.message_handler(commands=['dns'])
        async def handle_dns(message):
            command_args = message.text.split()
            if len(command_args) == 1:
                await bot.reply_to(message, "格式错误, 格式应为 /dns [Domain](Record_Type)")
            elif len(command_args) == 2:
                await Event.handle_dns(bot, message, "A")
            elif len(command_args) == 3:
                await Event.handle_dns(bot, message, command_args[2])
            else:
                await bot.reply_to(message, "格式错误, 格式应为 /dns [Domain](Record_Type)")

        from telebot import asyncio_filters
        bot.add_custom_filter(asyncio_filters.IsAdminFilter(bot))
        bot.add_custom_filter(asyncio_filters.ChatFilter())
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))

        async def main():
            await asyncio.gather(bot.polling(non_stop=True, allowed_updates=util.update_types))

        asyncio.run(main())
