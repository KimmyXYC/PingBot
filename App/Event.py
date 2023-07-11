import telebot
from loguru import logger
from Utils.IP import *
from Utils.API import *


async def start(bot, message):
    _url = "https://github.com/KimmyXYC/PingBot"
    _info = "/ip 查询IP地址\n/ip_ali 查询IP地址(阿里源)\n/icp 查询域名备案信息\n/whois 查询域名Whois信息\n"
    await bot.reply_to(
        message,
        f"{_info}开源地址: {_url}",
        disable_web_page_preview=True,
    )


async def handle_icp(bot, message):
    status, data = icp_record_check(message.text.split()[1])
    if not status:
        await bot.reply_to(message, f"请求失败: {data}")
        return
    if data["icp"] == "未备案":
        icp_info = f"""查询目标： `{message.text.split()[1]}`\n备案状态： `{data["icp"]}`\n"""
    else:
        icp_info = f"""查询目标： `{message.text.split()[1]}`\n备案号： `{data["icp"]}`\n备案主体： `{data["unitName"]}`\n备案性质： `{data["natureName"]}`\n"""
    await bot.reply_to(message, icp_info, parse_mode="MarkdownV2")


async def handle_whois(bot, message):
    status, result = whois_check(message.text.split()[1])
    if not status:
        await bot.reply_to(message, f"请求失败: {result}")
        return
    whois_info = f"`{result}`"
    await bot.reply_to(message, whois_info, parse_mode="MarkdownV2")


async def handle_ip_ali(bot, message, _config):
    ip_addr, ip_type = check_url(message.text.split()[1])
    _is_url = False
    if ip_type is None:
        ip_addr, ip_type = check_url(ip_addr)
        _is_url = True
    if ip_addr is None:
        await bot.reply_to(message, "格式错误, 格式应为 /ip [IP]")
        return
    elif ip_type == "v4":
        status, data = ali_ipcity_ip(ip_addr, _config.appcode)
        if not status:
            await bot.reply_to(message, f"请求失败: {data}")
            return
        if _is_url:
            ip_info = f"""查询目标： `{message.text.split()[1]}`\n解析地址： `{ip_addr}`\n"""
        else:
            ip_info = f"""查询目标： `{message.text.split()[1]}`\n"""
        if not data["country"]:
            status, data = kimmy_ip(ip_addr)
            if status:
                ip_info += f"""地区： `{data["country"]}`"""
        else:
            if data["prov"]:
                ip_info += f"""地区： `{data["country"]} - {data["prov"]} - {data["city"]}`\n"""
            else:
                ip_info += f"""地区： `{data["country"]}`\n """
            ip_info += f"""经纬度： `{data["lng"]}, {data["lat"]}`\nISP： `{data["isp"]}`\n组织： `{data["owner"]}`\n"""
            status, data = ipapi_ip(ip_addr)
            if status:
                ip_info += f"""`{data["as"]}`"""
        await bot.reply_to(message, f"{ip_info}", parse_mode="Markdown")
    elif ip_type == "v6":
        status, data = ipapi_ip(ip_addr)
        if status:
            ip_info = ip_api(message.text.split()[1], ip_addr, data, _is_url)
            await bot.reply_to(message, f"{ip_info}", parse_mode="Markdown")
        else:
            await bot.reply_to(message, f"请求失败: {data}")


async def handle_ip(bot, message, _config):
    ip_addr, ip_type = check_url(message.text.split()[1])
    _is_url = False
    if ip_type is None:
        ip_addr, ip_type = check_url(ip_addr)
        _is_url = True
    if ip_addr is None:
        await bot.reply_to(message, "格式错误, 格式应为 /ip [IP]")
        return
    else:
        status, data = ipapi_ip(ip_addr)
        if status:
            if not data["country"]:
                if _is_url:
                    ip_info = f"""查询目标： `{message.text.split()[1]}`\n解析地址： `{ip_addr}`\n"""
                else:
                    ip_info = f"""查询目标： `{message.text.split()[1]}`\n"""
                status, data = kimmy_ip(ip_addr)
                if status:
                    ip_info += f"""地区： `{data["country"]}`"""
            else:
                ip_info = ip_api(message.text.split()[1], ip_addr, data, _is_url)
            await bot.reply_to(message, f"{ip_info}", parse_mode="Markdown")
        else:
            if data == "reserved range":
                if _is_url:
                    ip_info = f"""查询目标： `{message.text.split()[1]}`\n解析地址： `{ip_addr}`\n"""
                else:
                    ip_info = f"""查询目标： `{message.text.split()[1]}`\n"""
                status, data = kimmy_ip(ip_addr)
                if status:
                    ip_info += f"""地区： `{data["country"]}`"""
                await bot.reply_to(message, f"{ip_info}", parse_mode="Markdown")
            else:
                await bot.reply_to(message, f"请求失败: {data}")
