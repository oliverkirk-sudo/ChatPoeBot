# ChatPoeBot

[QChatGPT](https://github.com/RockChinQ/QChatGPT)的插件,用于将QQ机器人与[Poe](https://poe.com)上的机器人连接

## 1、前置工作

- 首先在[Poe](https://poe.com)注册账号，并登录。
- 获取token
    - Chrome: 开发者工具 > 应用 > Cookies > poe.com
    - Firefox: 开发者工具 > 存储 > Cookies
    - Safari: 开发者工具 > 存储 > Cookies

## 2、修改配置文件

- 下载本插件`!plugin https://github.com/oliverkirk-sudo/ChatPoeBot.git`
- 在config文件夹中将poe_config_temp.py修改为poe_config.py,格式如下：

```python
# Sage = 'capybara'
# GPT4 = 'beaver'
# Claude = 'a2_2'
# ClaudeInstant = 'a2'
# ChatGPT = 'chinchilla'
# Dragonfly = 'nutria'
poe_config = {
    'default_bot_type': PoeBots.ChatGPT,  # 默认机器人类型
    'proxy': '',  # 代理，'http://127.0.0.1:7890',
    'tokens': [],  # 填入获取到的token，str格式逗号隔开
    'prefix': True  # 启用前缀POE
}

```

- 用`!relaod`重新加载插件

## 3、包含的指令

- `!poe help` 显示本帮助
- `!poe type <BotType>` 切换机器人类型<br>
  机器人类型: Sage，GPT4，Claude，ClaudeInstant，ChatGPT，Dragonfly<br>
  其中GPT4与Claude,免费版每天只有一次对话机会
- `!poe purg [count]` count为可选值，默认为回滚一次
- `!poe reset` 重置对话
- `!poe history [count]` count为可选值，默认返回最近5条历史