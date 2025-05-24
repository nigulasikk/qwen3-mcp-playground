
#!/usr/bin/env python3
"""
Qwen-Agent客户端
用于连接到微信MCP服务器并调用send-message工具
支持三种运行模式：测试模式、TUI界面和GUI界面
"""
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
from qwen_agent.utils.output_beautify import typewriter_print

def init_agent_service():
    """初始化智能体服务"""
    llm_cfg = {
        'model': 'Qwen/Qwen3-14B',
        'model_server': 'http://localhost:1234/v1',  # api_base
        'api_key': 'EMPTY',
        # 'thought_in_content': False,
        # 或者使用DashScope服务
        # 'model': 'qwen3-32b',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY', '')  # 从环境变量获取API密钥
    }

    tools = [
        {
            'mcpServers': {  # You can specify the MCP configuration file
                'time': {
                    'command': 'uvx',
                    'args': ['mcp-server-time', '--local-timezone=Asia/Shanghai']
                },
                'chat-mcp': {
                    'command': 'python',
                    'args': ['chat-mcp-server.py']
                },
                'pdf-mcp': {
                    'command': 'python',
                    'args': ['pdf-mcp-server.py']
                },
                # 文件操作
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        "./",
                    ]
                },
               
                # 画流程图
                # "mermaid": {
                #     "command": "npx",
                #     "args": [
                #         "-y", 
                #         "@peng-shawn/mermaid-mcp-server",
                #         ""
                #     ]
                # }
                # "mcp-server-chart": {
                #     "command": "npx",
                #     "args": [
                #         "-y",
                #         "@antv/mcp-server-chart"
                #     ]
                # }
            },
        },
        'code_interpreter'
    ]

    bot = Assistant(
        llm=llm_cfg,
        function_list=tools,
        system_message="""你是一个能帮助用户发送消息的助手。当用户要求你发送消息时，请按照以下步骤操作：
    1. 先使用 get_contacts 工具获取联系人列表
    2. 从列表中找到目标联系人对象（包含id和name）
    3. 使用 send_message 工具，将联系人对象和消息内容作为参数发送消息
    请始终使用中文回复。"""
    )

    return bot


def test(query: str = '给张三发送一条消息，告诉他明天会议取消了'):
    """单次测试模式"""
    # 初始化智能体
    bot = init_agent_service()

    # 执行单次对话
    messages = [{'role': 'user', 'content': query}]
    response_plain_text = ''
    print(f"测试查询: {query}")
    print("助手回应:")
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)


def app_tui():
    """文本用户界面模式"""
    # 初始化智能体
    bot = init_agent_service()

    # 交互式对话
    print("=== 微信消息发送助手 ===")
    print("你可以要求助手发送消息，例如：'给张三发送一条消息，告诉他明天会议取消了'")
    print("输入'exit'退出程序")
    print("=====================")
    
    messages = []
    
    while True:
        query = input('\n用户请求: ')
        if query.lower() == 'exit':
            break
        
        messages.append({'role': 'user', 'content': query})
        
        response_plain_text = ''
        print('助手回应:')
        
        for response in bot.run(messages=messages):
            response_plain_text = typewriter_print(response, response_plain_text)
        
        messages.extend(response)


def app_gui():
    """图形用户界面模式"""
    # 初始化智能体
    bot = init_agent_service()
    
    # 配置聊天界面
    chatbot_config = {
        'prompt.suggestions': [
            '给张三发送一条消息，告诉他明天会议取消了',
            '获取我的联系人列表',
            '给老婆发一条消息说我今晚加班'
        ]
    }
    
    # 启动Web界面
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == "__main__":
    # 可以取消注释下面三行中的一行来选择运行模式
    # test()
    # app_tui()
    app_gui()