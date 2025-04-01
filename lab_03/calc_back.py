from PIL import Image

INCORRECT_IMAGE_FORMAT = Exception("Изображение имеет неправильный формат")
IMAGE_NOT_ACCESSIBLE = Exception("Изображение невозможно открыть")
STRING_TOO_LONG = Exception("Сообщение слишком длинное")
NO_STRING_ENCODED = Exception("Сообщение не содержит закодированной строки")

STRING_TERMINATOR = '#'

CHAR_BITS = 8


def get_bit(num, ind):
    return num & (1 << ind)


def set_bit(num, ind):
    return num | (1 << ind)


def unset_bit(num, ind):
    return num & ~(1 << ind)


class EncoderBack:
    def __init__(self, img_path):
        self.img_path = img_path
        self.saved = True
        img_ext = img_path.split(".")[-1]
        if img_ext != "bmp":
            raise INCORRECT_IMAGE_FORMAT
        try:
            img_data = Image.open(img_path)
        except Exception as _:
            raise IMAGE_NOT_ACCESSIBLE
        self.pixel_values = [list(i) for i in list(img_data.getdata())]
        self.channels_count = len(self.pixel_values[0])
        img_data.close()

    def save_image(self, path):
        img_data = Image.open(self.img_path)
        new_img = Image.new(img_data.mode, img_data.size)
        new_img.putdata([tuple(i) for i in self.pixel_values])
        new_img.save(path)
        self.saved = True

    def __encode_char(self, code, pixel_start):
        channel_ind = 0
        pixel_ind = pixel_start
        for bit in range(0, CHAR_BITS):
            if pixel_ind >= len(self.pixel_values):
                raise STRING_TOO_LONG
            if get_bit(code, bit):
                self.pixel_values[pixel_ind][channel_ind] = set_bit(self.pixel_values[pixel_ind][channel_ind], 0)
            else:
                self.pixel_values[pixel_ind][channel_ind] = unset_bit(self.pixel_values[pixel_ind][channel_ind], 0)
            channel_ind += 1
            if channel_ind == self.channels_count:
                channel_ind = 0
                pixel_ind += 1
        return channel_ind, pixel_ind

    def __decode_char(self, pixel_start):
        channel_ind = 0
        pixel_ind = pixel_start
        code = 0
        for bit in range(0, CHAR_BITS):
            if pixel_ind >= len(self.pixel_values):
                raise NO_STRING_ENCODED
            if get_bit(self.pixel_values[pixel_ind][channel_ind], 0):
                code = set_bit(code, bit)
            channel_ind += 1
            if channel_ind == self.channels_count:
                channel_ind = 0
                pixel_ind += 1
        return chr(code), channel_ind, pixel_ind

    def encode_message(self, message):
        pixel_ind = 0
        for c in message:
            c_code = ord(c)
            channel_ind, pixel_ind = self.__encode_char(c_code, pixel_ind)
            if channel_ind != 0:
                pixel_ind += 1
        term_code = ord(STRING_TERMINATOR)
        self.__encode_char(term_code, pixel_ind)
        self.saved = False

    def decode_message(self):
        pixel_ind = 0
        result = []
        current_char = ''
        while current_char != STRING_TERMINATOR:
            current_char, channel_ind, pixel_ind = self.__decode_char(pixel_ind)
            if ord(current_char) > 127:
                raise NO_STRING_ENCODED
            result.append(current_char)
            if channel_ind != 0:
                pixel_ind += 1
        return "".join(result[:len(result) - 1])
