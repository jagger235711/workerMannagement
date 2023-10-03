import random
import string

from PIL import Image, ImageDraw, ImageFont


def generate_captcha(width=120, height=30, char_num=5):
    """
    生成给定大小的验证码图片和验证码文字
    """

    # 随机生成验证码文本,包含数字和字母
    chars = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choices(chars, k=char_num))

    # 生成空白图片模板
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # 根据图片大小计算合适的字体大小
    font_size = int(height * 0.9)
    font = ImageFont.truetype(font='arial.ttf', size=font_size)

    # 计算每个字符所占的宽度
    # font_width, font_height = font.getsize(captcha_text[0])
    left, top, right, bottom = font.getbbox(captcha_text[0])
    font_width = right - left
    font_height = bottom - top

    # 绘制每个字符,并随机微调位置和字体大小
    posi = 25
    for i in range(char_num):
        x = i * font_width + random.randint(-3, 5) + posi
        y = random.randint(0, int(0.3 * height))
        font = ImageFont.truetype(font='arial.ttf', size=random.randint(font_size - 3, font_size + 3))
        draw.text((x, y), captcha_text[i], fill=random_color(), font=font)

    # 绘制干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=random_color())

        # 绘制干扰线条
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    return img, captcha_text


# 随机颜色生成函数
def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


if __name__ == '__main__':
    img, captcha_text = generate_captcha()
    print(captcha_text)
    img.show()
