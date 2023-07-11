# -*- coding: utf-8 -*-
# @Time： 2023/7/11 9:09 
# @FileName: API.py
# @Software： PyCharm
# @GitHub: KimmyXYC
def ip_api(target, ip_addr, data, _is_url):
    if _is_url:
        ip_info = f"""查询目标： `{target}`\n解析地址： `{ip_addr}`\n"""
    else:
        ip_info = f"""查询目标： {target}\n"""
    if data["regionName"]:
        ip_info += f"""地区： `{data["country"]}` - `{data["regionName"]}` - `{data["city"]}`\n"""
    else:
        ip_info += f"""地区： `{data["country"]}`\n"""
    ip_info += f"""经纬度： `{data["lon"]}, {data["lat"]}`\nISP： `{data["isp"]}`\n组织： `{data["org"]}`\n`{data["as"]}`"""
    return ip_info
