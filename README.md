# PingBot
## 功能 / Features
```
ip - 查询 IP 地址
ip_ali - 查询 IP 地址(阿里云)
icp - 查询域名 ICP 备案信息
whois - 查询域名 Whois 信息
dns - 查询域名 DNS 信息
```
## 安装 / Installation

- 安装依赖。Install dependencies.
```shell
git clone https://github.com/KimmyXYC/PingBot.git
pip3 install -r requirements.txt
```

- 复制配置文件。Copy configuration file.
```shell
cp Config/app_exp.toml Config/app.toml
```
- 填写配置文件。Fill out the configuration file.
```toml
[bot]
master = [100, 200]
botToken = 'key' # Required, Bot Token


[proxy]
status = false
url = "socks5://127.0.0.1:7890"

[ip]
appcode = "1234567890" # Required, Aliyun AppCode
```