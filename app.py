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
    print("开始配置LLM参数...")
    llm_cfg = {
        'model': 'Qwen/Qwen3-14B',
        'model_server': 'http://127.0.0.1:1234/v1',  # api_base
        'api_key': 'EMPTY',
        'thought_in_content': False,
        # 或者使用DashScope服务
        # 'model': 'qwen3-32b',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY', '')  # 从环境变量获取API密钥
    }
    print("LLM参数配置完成")

    print("开始配置工具列表...")
    tools = [
        {
            'mcpServers': {  
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
                        r"C:\Users\1\Desktop",
                    ]
                },
               
                "mermaid": {
                # 画流程图
                    "command": "npx",
                    "args": [
                        "-y", 
                        "@peng-shawn/mermaid-mcp-server",
                        r"C:\Users\1\Desktop",
                    ]
                },
                "iot-mcp": {
                    "command": "python",
                    "args": ["iot-mcp-server.py"]
                }
                # "mcp-server-chart": {
                #     "command": "npx",
                #     "args": [
                #         "-y",
                #         "@antv/mcp-server-chart"
                #     ]
                # }
            },
        },
        # 'code_interpreter'
    ]
    print("工具列表配置完成")

    print("Assistant 开始初始化")
    try:
        bot = Assistant(
            llm=llm_cfg,
            function_list=tools,
            system_message="""你是我的工作助手，能帮我处理各种任务，包括 给PDF加水印，发送信息，画流程图,控制加湿器，控制植物补光灯等。以下是一些你掌握的知识：
        1.发送消息流程： 先使用 get_contacts 工具获取联系人列表，再从列表中找到目标联系人对象（包含id和name），最后使用 send_message 工具，将联系人对象和消息内容作为参数发送消息
        2.当前电脑桌面路径为：C:\\Users\\1\\Desktop"""
        
        )
        print("初始化智能体完成")
        return bot
    except Exception as e:
        print(f"初始化过程中出现错误: {str(e)}")
        raise


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
            '我需要把我桌面上的qwen-vl.pdf发给老婆和张三，并且发给他们的pdf都需要加上他们名字的水印(如“共享给某某某的学习资料”)。最后用 mermaind画一张本次任务完整的流程图放在桌面上”),所有任务完成后回复“任务完成”',
            '执行任务前先用 mermaind画一张本次任务完整的流程图放在桌面上',
            '开启加湿器',
            '关闭加湿器',
            "开启植物补光灯",
            "关闭植物补光灯",
        ]
    }
    
    # 启动Web界面
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == "__main__":
    print("开始运行")
    # 可以取消注释下面三行中的一行来选择运行模式
    # test()
    # app_tui()
    app_gui()