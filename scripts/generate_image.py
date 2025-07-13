from PIL import Image, ImageDraw, ImageFont
import os

output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

font_path = os.path.join(os.getcwd(), "assets", "NotoSansTamil-Regular.ttf")
final_image = f"{output_dir}/question.png"


def create_image_styled(question_data: dict):

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

    img.save(final_image)
    print("🎨 Enhanced image saved:", final_image)


if __name__ == "__main__":
    # Example usage
    question_data = {
        "id": 1,
        "question": "இந்தியாவின் தலைநகரம் எது?",
        "options": [
            "சென்னை",
            "மும்பை",
            "டெல்லி",
            "கொல்கத்தா"
        ]
    }
    create_image_styled(question_data)
    print("Image created successfully.")