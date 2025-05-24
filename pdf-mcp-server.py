from mcp.server.fastmcp import FastMCP
from pdf import add_text_watermark  # 导入PDF水印函数

# Create an MCP server for PDF operations
mcp = FastMCP("PDF Watermark Service")

# Add a PDF watermark tool
@mcp.tool()
def add_pdf_watermark(input_pdf: str, output_pdf: str, text: str, font_size: int = 12, opacity: float = 0.2, angle: int = 30) -> str:
    """
    为PDF文件添加文字水印
    
    Args:
        input_pdf: 输入PDF文件路径
        output_pdf: 输出PDF文件路径
        text: 水印文字内容
        font_size: 字体大小，默认为12
        opacity: 透明度，0-1之间，默认为0.2
        angle: 旋转角度，默认为30度
    
    Returns:
        str: 处理结果信息
    """
    try:
        # 调用pdf.py中的水印功能
        add_text_watermark(input_pdf, output_pdf, text, font_size, opacity, angle)
        return f"已成功为 {input_pdf} 添加水印并保存为 {output_pdf}"
    except Exception as e:
        return f"添加水印失败: {str(e)}"

# 启动MCP server
if __name__ == "__main__":
    mcp.run()