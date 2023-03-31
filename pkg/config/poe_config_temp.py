from plugins.ChatPoeBot.pkg.poe_bot import PoeBots

# Sage = 'capybara'
# GPT4 = 'beaver'
# Claude = 'a2_2'
# ClaudeInstant = 'a2'
# ChatGPT = 'chinchilla'
# Dragonfly = 'nutria'
poe_config = {
    'default_bot_type': PoeBots.ChatGPT,
    'proxy': 'http://127.0.0.1:7890',  # 'http://127.0.0.1:7890',
    'tokens': [],  # 填入获取到的token
    'prefix': True  # 启用前缀POE
}
