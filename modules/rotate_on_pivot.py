import math


def rotate_on_pivot(pivot, direction, image, sample_image):
    offset_x = sample_image.get_rect().w // 2 - pivot[0]
    offset_y = sample_image.get_rect().h // 2 - pivot[1]
    dist = math.sqrt(offset_x ** 2 + offset_y ** 2)
    angle = (-90 - (180 / math.pi *
                    -math.atan2(offset_y, offset_x))) % 360
    angle += direction - 90
    angle %= 360
    real_center = image.get_rect().w // 2, image.get_rect().h // 2
    image_y = +(round(math.cos(angle * math.pi / 180) * dist))
    image_x = +(round(math.sin(-angle * math.pi / 180) * dist))
    image_x -= real_center[0] - pivot[0]
    image_y -= real_center[1] - pivot[1]
    image_offset = image_x, image_y
    return image_offset