from mcp.server.fastmcp import FastMCP
# from iot import (
#     turn_on_light,
#     turn_off_light,
#     turn_on_humidifier,
#     turn_off_humidifier,
#     get_humidifier_status
# )

# 创建 MCP 服务器
mcp = FastMCP("IoT Server")

@mcp.tool()
def control_humidifier(action: str) -> dict:
    """
    控制加湿器的开关
    
    Args:
        action: 控制动作，可以是 "on" 或 "off"
    
    Returns:
        dict: 包含操作状态和消息的字典
    """
    try:
        if action not in ["on", "off"]:
            return {
                "status": "error",
                "message": "Invalid action. Must be 'on' or 'off'"
            }
        
        success = False
        if action == "on":
            print("开启加湿器")
            # success = turn_on_humidifier()
        else:
            print("关闭加湿器")
            # success = turn_off_humidifier()
        
        if not success:
            return {
                "status": "error",
                "message": "Failed to control humidifier"
            }
        
        return {
            "status": "success",
            "message": f"Humidifier turned {action}",
            "current_state": action == "on"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error controlling humidifier: {str(e)}"
        }

@mcp.tool()
def control_grow_light(action: str) -> dict:
    """
    控制植物补光灯的开关
    
    Args:
        action: 控制动作，可以是 "on" 或 "off"
    
    Returns:
        dict: 包含操作状态和消息的字典
    """
    try:
        if action not in ["on", "off"]:
            return {
                "status": "error",
                "message": "Invalid action. Must be 'on' or 'off'"
            }
        
        success = False
        if action == "on":
            print("开启植物补光灯")
            success=True
            # success = turn_on_light()
        else:
            print("关闭植物补光灯")
            success=True
            # success = turn_off_light()
        
        if not success:
            return {
                "status": "error",
                "message": "Failed to control grow light"
            }
        
        return {
            "status": "success",
            "message": f"Grow light turned {action}",
            "current_state": action == "on"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error controlling grow light: {str(e)}"
        }

@mcp.tool()
def get_environment_data() -> dict:
    """
    获取环境数据（温度和湿度）
    
    Returns:
        dict: 包含环境数据的字典
    """
    try:
        # humidifier_status = get_humidifier_status()
        humidifier_status = "on"
        if humidifier_status is None:
            return {
                "status": "error",
                "message": "Failed to get humidifier status"
            }
        
        # 这里可以添加获取温度和湿度的具体实现
        # 目前返回模拟数据
        return {
            "status": "success",
            "temperature": 25.0,
            "humidity": 45.0,
            "unit": {
                "temperature": "°C",
                "humidity": "%"
            },
            "humidifier_status": humidifier_status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting environment data: {str(e)}"
        }

# 启动 MCP 服务器
if __name__ == "__main__":
    mcp.run() 