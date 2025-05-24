from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Chat Server")

# Add a get_contacts tool
@mcp.tool()
def get_contacts() -> list:
    """
    获取联系人列表
    
    Returns:
        list: 联系人列表，每个联系人包含姓名、ID等信息
    """
    try:
        # 这里是获取联系人的逻辑
        # 在实际应用中，这里可能是调用通讯录API的代码
        # 示例实现 - 返回一个模拟的联系人列表
        contacts = [
            {"id": "user1", "name": "张三", "avatar": "https://example.com/avatar1.jpg"},
            {"id": "user2", "name": "李四", "avatar": "https://example.com/avatar2.jpg"},
            {"id": "user3", "name": "王五", "avatar": "https://example.com/avatar3.jpg"},
            {"id": "user_center", "name": "老李", "avatar": "https://example.com/avatar1.jpg"},
            {"id": "user_666", "name": "老婆", "avatar": "https://example.com/avatar1.jpg"},
        ]
        
        print(f"成功获取了 {len(contacts)} 个联系人")
        return contacts
    except Exception as e:
        print(f"获取联系人失败: {str(e)}")
        return []

# Add a sendMessage tool
@mcp.tool()
def send_message(recipient: dict, message: str) -> str:
    """
    给指定的接收者发送消息。
    
    Args:
        recipient: 接收者对象，包含id和name字段
        message: 要发送的消息内容
    
    Returns:
        str: 发送状态信息
    """
    # 这里实现发送消息的逻辑
    try:
        # 从recipient对象中获取wxid和name
        wxid = recipient.get("id")
        name = recipient.get("name")
        
        if not wxid:
            return "发送消息失败: 接收者ID不能为空"
        
        # 示例实现 - 在实际应用中替换为真实的消息发送逻辑
        print(f"正在发送消息到 {name}({wxid}): {message}")
        
        # 模拟发送过程
        # 在实际应用中，这里可能是调用消息API的代码
        # 例如: message_api.send(wxid, message)
        
        return f"消息已成功发送给 {name}({wxid})，消息内容：{message}"
    except Exception as e:
        return f"发送消息失败: {str(e)}"

# 发送附件工具
@mcp.tool()
def send_attachment(recipient: dict, file_path: str) -> str:
    """
    给指定的接收者发送附件，发送pdf等文件。
    
    Args:
        recipient: 接收者对象，包含id和name字段
        file_path: 要发送的文件路径
    
    Returns:
        str: 发送状态信息
    """
    # 这里实现发送附件的逻辑
    try:
        # 从recipient对象中获取wxid和name
        wxid = recipient.get("id")
        name = recipient.get("name")
        
        if not wxid:
            return "发送附件失败: 接收者ID不能为空"
        
        # 示例实现 - 在实际应用中替换为真实的附件发送逻辑
        print(f"正在发送附件到 {name}({wxid}): {file_path}")
        
        # 模拟发送过程
        # 在实际应用中，这里可能是调用消息API的代码
        # 例如: message_api.send_attachment(wxid, file_path)
        
        return f"附件已成功发送给 {name}({wxid})，附件地址：{file_path}"
    except Exception as e:
        return f"发送消息失败: {str(e)}"

# 启动MCP servers
if __name__ == "__main__":
    mcp.run()