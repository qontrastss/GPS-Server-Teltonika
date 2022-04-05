import json
from codec import Codec8, Codec16, Codec8Ex


class Data:
    def __init__(self):
        self.codec_id = 0
        self.avl_data_count = 0
        self.avl_data_list = []
        self.avl_data_count2 = 0


class TCP_AVP_Data_Packet:
    def __init__(self):
        self.preamble = 0
        self.avl_data_length = 0
        self.data = Data()
        self.crc = 0


class Parse_Data:
    def __init__(self, data):
        self.data_packet = TCP_AVP_Data_Packet()
        self.data = data

    def get_preamble(self):
        self.data_packet.preamble = int(self.data[:8], 16)
        self.data = self.data[8:]

    def get_avl_length(self):
        self.data_packet.avl_data_length = int(self.data[:8], 16)
        self.data = self.data[8:]

    def get_codec_id(self):
        self.data_packet.data.codec_id = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_avl_data_count(self):
        self.data_packet.data.avl_data_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_avl_data_count2(self):
        self.data_packet.data.avl_data_count2 = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_crc(self):
        self.data_packet.crc = int(self.data[:8], 16)
        self.data = self.data[8:]

    def parse_data(self):
        self.get_preamble()
        self.get_avl_length()
        self.get_codec_id()
        self.get_avl_data_count()

        if self.data_packet.data.codec_id == 8:  # Codec 8
            for i in range(self.data_packet.data.avl_data_count):
                avl_obj = Codec8(self.data, self.data_packet)
                avl_obj.parse_avl_data()
                self.data = avl_obj.data
                self.data_packet = avl_obj.data_packet
        elif self.data_packet.data.codec_id == 16:  # Codec 16
            for i in range(self.data_packet.data.avl_data_count):
                avl_obj = Codec16(self.data, self.data_packet)
                avl_obj.parse_avl_data()
                self.data = avl_obj.data
                self.data_packet = avl_obj.data_packet
        elif self.data_packet.data.codec_id == 142:  # Codec 8 Extended
            for i in range(self.data_packet.data.avl_data_count):
                avl_obj = Codec8Ex(self.data, self.data_packet)
                avl_obj.parse_avl_data()
                self.data = avl_obj.data
                self.data_packet = avl_obj.data_packet
        else:
            raise ValueError("Corrupted Data Inserted!")

        self.get_avl_data_count2()
        self.get_crc()
        return self.data_packet, self.data.encode('utf-8')

    def save_data(self):
        json_data = {}
        if self.data_packet.data.codec_id == 8:  # Codec 8
            avl_obj = Codec8(self.data, self.data_packet)
            json_data = avl_obj.convert_to_json()
        elif self.data_packet.data.codec_id == 16:  # Codec 16
            avl_obj = Codec16(self.data, self.data_packet)
            json_data = avl_obj.convert_to_json()
        elif self.data_packet.data.codec_id == 142:  # Codec 8 Extended
            avl_obj = Codec8Ex(self.data, self.data_packet)
            json_data = avl_obj.convert_to_json()

        with open("data.json", 'r') as j:
            data_list = json.load(j)

        with open("data.json", 'w') as w:
            data_list.append(json_data)
            json_string = json.dumps(data_list)
            w.write(json_string)

    def view_data(self):
        if self.data_packet.data.codec_id == 8:  # Codec 8
            avl_obj = Codec8(self.data, self.data_packet)
            avl_obj.view_data_packet()
        elif self.data_packet.data.codec_id == 16:  # Codec 16
            avl_obj = Codec16(self.data, self.data_packet)
            avl_obj.view_data_packet()
        elif self.data_packet.data.codec_id == 142:  # Codec 8 Extended
            avl_obj = Codec8Ex(self.data, self.data_packet)
            avl_obj.view_data_packet()
