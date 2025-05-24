import PyPDF2
import os
import tempfile
import random  # 添加随机数模块
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import gray, Color
# 添加TTF字体支持
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
def register_chinese_font():
    """注册中文字体，支持 Windows 和 Mac 系统"""
    # Windows 系统字体路径
    windows_font_paths = [
        r"C:\Windows\Fonts\simhei.ttf",  # 黑体
        r"C:\Windows\Fonts\simsun.ttc",  # 宋体
        r"C:\Windows\Fonts\msyh.ttc",    # 微软雅黑
    ]
    
    # Mac 系统字体路径
    mac_font_path = "/System/Library/Fonts/STHeiti Light.ttc"
    
    # 根据操作系统选择字体路径
    if os.name == 'nt':  # Windows 系统
        for font_path in windows_font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                    return "ChineseFont"
                except Exception as e:
                    print(f"注册字体 {font_path} 失败: {str(e)}")
                    continue
    else:  # Mac 或其他系统
        if os.path.exists(mac_font_path):
            try:
                pdfmetrics.registerFont(TTFont("STHeiti", mac_font_path))
                return "STHeiti"
            except Exception as e:
                print(f"注册字体 {mac_font_path} 失败: {str(e)}")
    
    # 如果所有字体都注册失败，返回 None
    print("警告：未能找到合适的中文字体，将使用默认字体")
    return None

def add_watermark(input_pdf, output_pdf, watermark_pdf):
    with open(input_pdf, 'rb') as input_file, open(watermark_pdf, 'rb') as watermark_file:
        input_reader = PyPDF2.PdfReader(input_file)
        watermark_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]
        writer = PyPDF2.PdfWriter()

        for page in input_reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def create_watermark_pdf(text, output_path, font_size=20, opacity=0.2, angle=30, watermark_count=3):
    """
    创建包含文字水印的PDF文件
    
    参数:
    text (str): 水印文字内容
    output_path (str): 输出的水印PDF路径
    font_size (int): 字体大小
    opacity (float): 透明度，0-1之间
    angle (int): 旋转角度
    watermark_count (int): 水印数量
    """
    # 注册中文字体
    chinese_font = register_chinese_font()
    
    # 创建画布
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # 设置透明度 - 降低默认值从0.3到0.2
    c.setFillColor(Color(0, 0, 0, alpha=opacity))
    
    # 设置字体和大小
    font_name = chinese_font if chinese_font else "Helvetica"
    c.setFont(font_name, font_size)
    
    # 计算文本宽度
    text_width = c.stringWidth(text, font_name, font_size)
    
    # 安全边距
    margin = max(text_width, font_size)
    
    # 将页面划分为网格，确保水印分布更均匀
    # 计算网格大小（根据水印数量）
    import math
    grid_count = math.ceil(math.sqrt(watermark_count))
    cell_width = (width - 2 * margin) / grid_count
    cell_height = (height - 2 * margin) / grid_count
    
    # 生成不重复的网格单元
    cells = []
    for i in range(grid_count):
        for j in range(grid_count):
            cells.append((i, j))
    
    # 随机打乱网格单元顺序
    random.shuffle(cells)
    
    # 在每个选中的网格单元内随机放置水印
    for idx in range(min(watermark_count, len(cells))):
        i, j = cells[idx]
        
        # 保存当前图形状态
        c.saveState()
        
        # 计算当前网格单元的边界
        cell_left = margin + i * cell_width
        cell_bottom = margin + j * cell_height
        
        # 在网格单元内随机选择位置（留出一些边距）
        inner_margin = margin * 0.5
        x = random.uniform(cell_left + inner_margin, cell_left + cell_width - inner_margin)
        y = random.uniform(cell_bottom + inner_margin, cell_bottom + cell_height - inner_margin)
        
      
        
        # 移动到随机位置并旋转
        c.translate(x, y)
        c.rotate(angle)
        
        # 绘制文本
        c.drawString(-text_width/2, 0, text)
        
        # 恢复图形状态
        c.restoreState()
    
    # 完成绘制并保存
    c.save()

def add_text_watermark(input_pdf, output_pdf, text, font_size=20, opacity=0.2, angle=30):
    """
    在PDF文件上添加文字水印
    
    参数:
    input_pdf (str): 输入PDF文件路径
    output_pdf (str): 输出PDF文件路径
    text (str): 水印文字内容
    font_size (int): 字体大小
    opacity (float): 透明度，0-1之间，默认值从0.3降低到0.2
    angle (int): 旋转角度
    """
    # 创建临时文件来存储水印PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_watermark_path = temp_file.name
    
    try:
        # 创建水印PDF
        create_watermark_pdf(text, temp_watermark_path, font_size, opacity, angle, 3)
        
        # 将水印应用到输入PDF
        add_watermark(input_pdf, output_pdf, temp_watermark_path)
    finally:
        print("正在清理临时文件...")
        # 清理临时文件
        if os.path.exists(temp_watermark_path):
            os.remove(temp_watermark_path)

# 示例用法
# 添加PDF水印
# add_watermark("deepseek.pdf", "output_with_watermark.pdf", "watermark.pdf")
# 添加文字水印
# add_text_watermark("deepseek.pdf", "output_with_text_watermark.pdf", "机密文件", font_size=40, opacity=0.3, angle=45)
# add_text_watermark("deepseek.pdf", "output_with_text_watermark.pdf", "机密文件", font_size=40, opacity=0.3, angle=45)