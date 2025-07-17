from PIL import Image, ImageDraw, ImageFont
import os

output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

font_path = os.path.join(os.getcwd(), "assets", "NotoSansTamil-Regular.ttf")
final_image = f"{output_dir}/question.png"


def create_style_one(question_data: dict, name=f"question1.png"):

    img = Image.new("RGB", (1080, 1920), color="#f0f4f8")
    draw = ImageDraw.Draw(img)

    # Default sizes
    font_title = ImageFont.truetype(font_path, 72)
    font_question = ImageFont.truetype(font_path, 64)
    font_option = ImageFont.truetype(font_path, 52)
    font_channel = ImageFont.truetype(font_path, 48)
    font_subscribe = ImageFont.truetype(font_path, 48)

    margin_x = 80
    max_width = 920
    padding = 60
    line_height_title = 110
    line_height_q = 85
    line_height_opt = 65
    spacing_after_q = 40
    top_banner_height = 100
    bottom_banner_height = 100
    max_content_height = int(1920 * 0.85)

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    def calculate_content_height(q_lines, opt_lines, line_q, line_opt):
        opt_box_height = sum(len(opt) * line_opt + 30 for opt in opt_lines)
        return (
            top_banner_height + line_height_title +
            len(q_lines) * line_q + spacing_after_q +
            opt_box_height + padding * 2 + bottom_banner_height
        )

    # Initial wrapping
    wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width)
    wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 60) for opt in question_data["options"]]
    content_height = calculate_content_height(wrapped_q_lines, wrapped_opt_lines, line_height_q, line_height_opt)

    # 🔁 Shrink if needed
    if content_height > max_content_height:
        font_question = ImageFont.truetype(font_path, 54)
        font_option = ImageFont.truetype(font_path, 46)
        line_height_q = 70
        line_height_opt = 58
        padding = 40
        wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width)
        wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 60) for opt in question_data["options"]]
        content_height = calculate_content_height(wrapped_q_lines, wrapped_opt_lines, line_height_q, line_height_opt)

    # Coordinates
    box_x1 = margin_x
    box_x2 = 1080 - margin_x
    box_y1 = (1920 - content_height) // 2 + top_banner_height
    box_y2 = box_y1 + content_height - top_banner_height - bottom_banner_height

    # Draw UI: banners
    draw.rectangle([(0, 0), (1080, top_banner_height)], fill="#102b3f")
    draw.text((40, 20), "GK Tamil Academy", fill="white", font=font_channel)
    draw.rectangle([(0, 1920 - bottom_banner_height), (1080, 1920)], fill="#ff4d4d")
    draw.text((380, 1920 - 80), "Subscribe for daily TNPSC!", fill="white", font=font_subscribe)

    # Draw white content box
    draw.rounded_rectangle(
        [(box_x1, box_y1), (box_x2, box_y2)],
        radius=40, fill="#ffffff", outline="#dddddd", width=2
    )

    y = box_y1 + padding
    x = box_x1 + padding

    # Title
    title_bar_height = 90
    draw.rounded_rectangle([(x, y), (box_x2 - padding, y + title_bar_height)], radius=20, fill="#008ecc")
    draw.text((x + 20, y + 10), "QUESTION", fill="white", font=font_title)
    y += title_bar_height + 30

    # Question
    for line in wrapped_q_lines:
        draw.text((x, y), line, fill="#111111", font=font_question)
        y += line_height_q
    y += spacing_after_q

    # Options
    for opt_lines in wrapped_opt_lines:
        opt_box_y1 = y - 10
        opt_box_y2 = y + len(opt_lines) * line_height_opt + 20
        draw.rounded_rectangle(
            [(x, opt_box_y1), (box_x2 - padding, opt_box_y2)],
            radius=20, fill="#f2f2f2", outline="#cccccc", width=1
        )
        inner_y = y + 5
        for line in opt_lines:
            draw.text((x + 20, inner_y), line, fill="#333333", font=font_option)
            inner_y += line_height_opt
        y = opt_box_y2 + 20

    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)


def create_style_two(question_data: dict, name="question2.png"):
    img = Image.new("RGB", (1080, 1920), color="#fdfdfd")
    draw = ImageDraw.Draw(img)


    # Fonts
    font_title = ImageFont.truetype(font_path, 64)
    font_question = ImageFont.truetype(font_path, 58)
    font_option = ImageFont.truetype(font_path, 48)
    font_channel = ImageFont.truetype(font_path, 42)
    font_subscribe = ImageFont.truetype(font_path, 44)

    # Dimensions
    margin_x = 80
    max_width = 920
    padding = 50
    line_height_q = 75
    line_height_opt = 60
    spacing_after_q = 40
    top_banner_height = 90
    bottom_banner_height = 100

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width - 60)
    wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 100) for opt in question_data["options"]]

    # Draw Background Grid Pattern
    for x in range(0, 1080, 80):
        for y in range(0, 1920, 80):
            draw.ellipse((x, y, x + 6, y + 6), fill="#e8e8e8")

    # Top Banner
    draw.rectangle([(0, 0), (1080, top_banner_height)], fill="#1a365d")
    draw.text((40, 18), "GK Tamil Academy", fill="white", font=font_channel)

    # Bottom Banner
    draw.rectangle([(0, 1920 - bottom_banner_height), (1080, 1920)], fill="#ff6666")
    draw.text((330, 1920 - 72), "Subscribe for daily TNPSC!", fill="white", font=font_subscribe)

    # Question box
    box_x1 = margin_x
    box_x2 = 1080 - margin_x
    y = top_banner_height + 80

    draw.rounded_rectangle([(box_x1, y), (box_x2, y + 120)], radius=30, fill="#ffd966")
    draw.text((box_x1 + 30, y + 20), "கேள்வி", fill="#1a1a1a", font=font_title)
    y += 150

    for line in wrapped_q_lines:
        draw.text((box_x1, y), line, fill="#111111", font=font_question)
        y += line_height_q
    y += spacing_after_q

    # Pastel option colors
    pastel_colors = ["#e0f7fa", "#fce4ec", "#fff9c4", "#e8f5e9"]
    border_colors = ["#4dd0e1", "#f06292", "#fbc02d", "#81c784"]

    for i, opt_lines in enumerate(wrapped_opt_lines):
        opt_y1 = y
        opt_y2 = y + len(opt_lines) * line_height_opt + 30
        draw.rounded_rectangle(
            [(box_x1, opt_y1), (box_x2, opt_y2)],
            radius=20,
            fill=pastel_colors[i % len(pastel_colors)],
            outline=border_colors[i % len(border_colors)],
            width=2
        )
        inner_y = y + 15
        for line in opt_lines:
            draw.text((box_x1 + 30, inner_y), line, fill="#333333", font=font_option)
            inner_y += line_height_opt
        y = opt_y2 + 20

    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)


def create_style_three(question_data: dict, name="question3.png"):
    img = Image.new("RGB", (1080, 1920), color="#101820")
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(font_path, 66)
    font_question = ImageFont.truetype(font_path, 58)
    font_option = ImageFont.truetype(font_path, 48)
    font_subscribe = ImageFont.truetype(font_path, 44)

    margin_x, padding = 70, 50
    max_width = 920
    line_height_q = 76
    line_height_opt = 58
    spacing_after_q = 40

    def wrap_text(text, font, max_width):
        lines, line = [], ""
        for word in text.split():
            test_line = f"{line}{word} "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = f"{word} "
        lines.append(line.strip())
        return lines

    wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width)
    wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 40) for opt in question_data["options"]]

    y = 150
    draw.text((margin_x, y), "TNPSC QUESTION", font=font_title, fill="#00ffff")
    y += 110

    # Shadow effect
    content_bg = Image.new("RGB", (920, 1600), "#ffffff")
    content_draw = ImageDraw.Draw(content_bg)
    content_y = 30
    for line in wrapped_q_lines:
        content_draw.text((20, content_y), line, fill="#000000", font=font_question)
        content_y += line_height_q
    content_y += spacing_after_q

    for opt_lines in wrapped_opt_lines:
        box_y1, box_y2 = content_y - 5, content_y + len(opt_lines) * line_height_opt + 20
        content_draw.rounded_rectangle([(10, box_y1), (910, box_y2)], radius=15, fill="#f0f0f0")
        inner_y = content_y + 5
        for line in opt_lines:
            content_draw.text((30, inner_y), line, font=font_option, fill="#111111")
            inner_y += line_height_opt
        content_y = box_y2 + 25

    # Paste with drop shadow
    img.paste(content_bg, (margin_x, y))
    draw.text((280, 1850), "Subscribe for Daily GK Tamil", font=font_subscribe, fill="#ffffff")

    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)
    

def create_style_four(question_data: dict, name="question4.png"):
    img = Image.new("RGB", (1080, 1920), color="#fcfcfc")
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(font_path, 66)
    font_question = ImageFont.truetype(font_path, 60)
    font_option = ImageFont.truetype(font_path, 50)
    font_subscribe = ImageFont.truetype(font_path, 46)

    margin_x, padding = 80, 50
    line_height_q = 80
    line_height_opt = 60
    spacing_after_q = 30
    max_width = 880

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width)
    wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 40) for opt in question_data["options"]]

    # Add vertical side color bar
    draw.rectangle([(0, 0), (60, 1920)], fill="#e63946")

    # Add watermark-style faded text
    draw.text((200, 80), "GK தமிழ் Academy", font=font_title, fill="#dddddd")

    y = 240
    # Bordered question section with shadow illusion
    draw.rounded_rectangle(
        [(margin_x - 10, y - 20), (1080 - margin_x + 10, y + len(wrapped_q_lines) * line_height_q + 40)],
        radius=25, fill="#f1f1f1", outline="#aaaaaa")

    for line in wrapped_q_lines:
        draw.text((margin_x, y), line, font=font_question, fill="#222222")
        y += line_height_q
    y += spacing_after_q

    # Options with alternating background colors
    opt_colors = ["#edf2fb", "#e2ece9"]
    for i, opt_lines in enumerate(wrapped_opt_lines):
        box_y1 = y - 10
        box_y2 = y + len(opt_lines) * line_height_opt + 20
        draw.rounded_rectangle(
            [(margin_x, box_y1), (1080 - margin_x, box_y2)],
            radius=20, fill=opt_colors[i % 2], outline="#bbbbbb")
        inner_y = y + 5
        for line in opt_lines:
            draw.text((margin_x + 20, inner_y), line, font=font_option, fill="#111111")
            inner_y += line_height_opt
        y = box_y2 + 20

    # Bottom subscription tag with background
    draw.rectangle([(0, 1820), (1080, 1920)], fill="#1d3557")
    draw.text((260, 1860), "Subscribe for Daily TNPSC Quiz", font=font_subscribe, fill="#ffffff")

    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)


def create_style_five(question_data: dict, name="question5.png"):
    img = Image.new("RGB", (1080, 1920), color="#e0f7fa")  # Light blue background
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(font_path, 66)
    font_question = ImageFont.truetype(font_path, 60)
    font_option = ImageFont.truetype(font_path, 50)
    font_subscribe = ImageFont.truetype(font_path, 46)

    margin_x, padding = 80, 50
    line_height_q = 80
    line_height_opt = 60
    spacing_after_q = 40
    max_width = 920 # Increased max width for more text per line

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    wrapped_q_lines = wrap_text(question_data["question"], font_question, max_width)
    wrapped_opt_lines = [wrap_text(opt, font_option, max_width - 40) for opt in question_data["options"]]

    # Header with a subtle gradient effect (simulated)
    draw.rectangle([(0, 0), (1080, 180)], fill="#00796b") # Dark teal
    draw.text((margin_x, 80), "GK தமிழ் Academy", font=font_title, fill="#ffffff") # White text

    y = 240
    # Question box with a border and light shadow
    question_box_height = len(wrapped_q_lines) * line_height_q + padding * 2
    draw.rectangle([(margin_x - 10, y - 20), (1080 - margin_x + 10, y + question_box_height - 20)],
                   fill="#ffffff", outline="#a7d9d2", width=3) # White with teal border

    for line in wrapped_q_lines:
        draw.text((margin_x, y), line, font=font_question, fill="#263238") # Dark grey text
        y += line_height_q
    y += spacing_after_q

    # Options with distinct, slightly darker background and rounded corners
    opt_colors = ["#b2dfdb", "#80cbc4"] # Lighter and slightly darker teal shades
    for i, opt_lines in enumerate(wrapped_opt_lines):
        box_y1 = y - 10
        box_y2 = y + len(opt_lines) * line_height_opt + 20
        draw.rounded_rectangle(
            [(margin_x, box_y1), (1080 - margin_x, box_y2)],
            radius=30, fill=opt_colors[i % 2]) # No outline for a cleaner look
        inner_y = y + 5
        for line in opt_lines:
            draw.text((margin_x + 30, inner_y), line, font=font_option, fill="#263238") # Dark grey text
            inner_y += line_height_opt
        y = box_y2 + 25 # Increased spacing between options

    # Bottom footer with a dark, solid color
    draw.rectangle([(0, 1820), (1080, 1920)], fill="#004d40") # Even darker teal
    draw.text((260, 1860), "Subscribe for Daily TNPSC Quiz", font=font_subscribe, fill="#ffffff")

    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)


def create_style_six(question_data: dict, name="question6.png"):
    img = Image.new("RGB", (1080, 1920), color="black")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_question = ImageFont.truetype(font_path, 56)
    font_option = ImageFont.truetype(font_path, 48)
    font_label = ImageFont.truetype(font_path, 46)
    font_channel = ImageFont.truetype(font_path, 40)
    font_subscribe = ImageFont.truetype(font_path, 42)

    # Constants
    neon_color = (140, 82, 255)
    margin_x = 80
    question_box_width = 920
    option_box_width = 920
    option_box_height_min = 130
    top_banner_height = 100
    bottom_banner_height = 100
    inner_width = 1080

    def wrap_text(text, font, max_width):
        lines, line = [], ""
        for word in text.split():
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    # --- Top Banner ---
    draw.rectangle([(0, 0), (inner_width, top_banner_height)], fill="#1a365d")
    draw.text((50, 25), "GK Tamil Academy", fill="white", font=font_channel)

    y = top_banner_height + 60  # space below banner

    # --- Question Box ---
    wrapped_q_lines = wrap_text(question_data["question"], font_question, question_box_width - 60)
    q_box_height = 60 + len(wrapped_q_lines) * 68
    q_x1 = margin_x
    q_x2 = inner_width - margin_x
    q_y2 = y + q_box_height

    draw.rounded_rectangle([(q_x1, y), (q_x2, q_y2)], radius=80, outline=neon_color, width=4)

    # Connector circle
    circle_center = (540, q_y2)
    r = 36
    draw.ellipse([(circle_center[0] - r, circle_center[1] - r), (circle_center[0] + r, circle_center[1] + r)],
                 outline=neon_color, width=4)
    draw.text((circle_center[0] - 12, circle_center[1] - 24), "?", fill=neon_color, font=font_label)

    # Draw wrapped question text
    text_y = y + 30
    for line in wrapped_q_lines:
        line_w = draw.textlength(line, font=font_question)
        draw.text(((inner_width - line_w) / 2, text_y), line, fill="white", font=font_question)
        text_y += 68

    y = q_y2 + r + 60  # space after connector

    # --- Options as vertical boxes ---
    wrapped_opt_lines = [wrap_text(opt, font_option, option_box_width - 100) for opt in question_data["options"]]
    labels = ["A", "B", "C", "D"]

    for i, opt_lines in enumerate(wrapped_opt_lines):
        box_height = max(option_box_height_min, 40 + len(opt_lines) * 60)
        box_y2 = y + box_height

        draw.rounded_rectangle([(margin_x, y), (inner_width - margin_x, box_y2)],
                               radius=60, outline=neon_color, width=3)

        draw.text((margin_x - 50, y + 30), labels[i], fill=neon_color, font=font_label)

        text_y = y + 25
        for line in opt_lines:
            draw.text((margin_x + 40, text_y), line, fill="white", font=font_option)
            text_y += 60

        y = box_y2 + 40


    img.save(os.path.join(output_dir, name))
    print("🎨 Enhanced image saved:", name)


if __name__ == "__main__":
    # Example usage
    question_data = {
    "id": 11,
    "question": "இந்திய சுதந்திரப் போராட்டத்தின் போது, 'மகாத்மா' என்ற பட்டம் காந்திஜிக்கு யாரால் வழங்கப்பட்டது, மேலும் அதன் முக்கியத்துவம் என்னவாக இருந்தது?",
    "options": [
        "A. ரவீந்திரநாத் தாகூர், தேசத்தின் ஆன்மீகத் தலைவராக அங்கீகரிக்கப்பட்டது",
        "B. சுபாஷ் சந்திர போஸ், இந்தியாவின் தேசத் தந்தையாக அறிவிக்கப்பட்டது",
        "C. ஜவஹர்லால் நேரு, சுதந்திர இந்தியாவின் முதல் பிரதமராக பரிந்துரைக்கப்பட்டது",
        "D. சர்தார் வல்லபாய் படேல், இந்திய மாநிலங்களை ஒருங்கிணைத்ததற்காக கௌரவிக்கப்பட்டது"
    ]
}
    create_style_one(question_data)
    create_style_two(question_data)
    create_style_three(question_data)
    create_style_four(question_data)
    create_style_five(question_data)
    create_style_six(question_data)
    