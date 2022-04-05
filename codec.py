import time


class GPS_Element:
    def __init__(self):
        self.longitude = None
        self.latitude = None
        self.altitude = None
        self.angle = None
        self.satellites = None
        self.speed = None


class IO_Element:
    def __init__(self):
        self.event_ID = None
        self.element_count = None
        self.one_byte_element_count = None
        self.list_one_byte_elements = []
        self.two_byte_element_count = None
        self.list_two_byte_elements = []
        self.four_byte_element_count = None
        self.list_four_byte_elements = []
        self.eight_byte_element_count = None
        self.list_eight_byte_elements = []
        self.x_byte_element_count = None
        self.list_x_byte_elements = []
        self.origin_type =None


class AVL_Data:
    def __init__(self):
        self.timestamp = None
        self.priority = None
        self.gps_element = GPS_Element()
        self.io_element = IO_Element()


class IO_Element_object:
    def __init__(self):
        self.ID = None
        self.length = None
        self.value = None


class Codec8:
    def __init__(self, data, data_packet):
        self.data_packet = data_packet
        self.data = data
        self.avl_data = AVL_Data()

    def get_timestamp(self):
        self.avl_data.timestamp = time.strftime('%d.%m.%Y %H:%M:%S',
                                                time.gmtime(int(str(int(self.data[:16], 16))[:-3])))
        self.data = self.data[16:]

    def get_priority(self):
        self.avl_data.priority = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_gps_element_longitude(self):
        self.avl_data.gps_element.longitude = int(self.data[:8], 16)
        self.data = self.data[8:]

    def get_gps_element_latitude(self):
        self.avl_data.gps_element.latitude = int(self.data[:8], 16)
        self.data = self.data[8:]

    def get_gps_element_altitude(self):
        self.avl_data.gps_element.altitude = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_gps_element_angle(self):
        self.avl_data.gps_element.angle = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_gps_element_satellites(self):
        self.avl_data.gps_element.satellites = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_gps_element_speed(self):
        self.avl_data.gps_element.speed = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_event_ID(self):
        self.avl_data.io_element.event_ID = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_io_element_count(self):
        self.avl_data.io_element.element_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def get_io_element_one_byte_element_count(self):
        self.avl_data.io_element.one_byte_element_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def parse_one_byte_io_element(self):
        for j in range(self.avl_data.io_element.one_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:2], 16)
            self.data = self.data[2:]
            io_element_obj.value = int(self.data[:2], 16)
            self.data = self.data[2:]
            self.avl_data.io_element.list_one_byte_elements.append(io_element_obj)

    def parse_two_byte_io_element(self):
        for j in range(self.avl_data.io_element.two_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:2], 16)
            self.data = self.data[2:]
            io_element_obj.value = int(self.data[:4], 16)
            self.data = self.data[4:]
            self.avl_data.io_element.list_two_byte_elements.append(io_element_obj)

    def get_io_element_two_byte_element_count(self):
        self.avl_data.io_element.two_byte_element_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def parse_four_byte_io_element(self):
        for j in range(self.avl_data.io_element.four_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:2], 16)
            self.data = self.data[2:]
            io_element_obj.value = int(self.data[:8], 16)
            self.data = self.data[8:]
            self.avl_data.io_element.list_four_byte_elements.append(io_element_obj)

    def get_io_element_four_byte_element_count(self):
        self.avl_data.io_element.four_byte_element_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def parse_eight_byte_io_element(self):
        for j in range(self.avl_data.io_element.eight_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:2], 16)
            self.data = self.data[2:]
            io_element_obj.value = int(self.data[:16], 16)
            self.data = self.data[16:]
            self.avl_data.io_element.list_eight_byte_elements.append(io_element_obj)

    def get_io_element_eight_byte_element_count(self):
        self.avl_data.io_element.eight_byte_element_count = int(self.data[:2], 16)
        self.data = self.data[2:]

    def parse_avl_data(self):
        self.get_timestamp()
        self.get_priority()
        self.get_gps_element_longitude()
        self.get_gps_element_latitude()
        self.get_gps_element_altitude()
        self.get_gps_element_angle()
        self.get_gps_element_satellites()
        self.get_gps_element_speed()
        self.get_io_element_event_ID()
        self.get_io_element_count()

        self.get_io_element_one_byte_element_count()
        self.parse_one_byte_io_element()

        self.get_io_element_two_byte_element_count()
        self.parse_two_byte_io_element()

        self.get_io_element_four_byte_element_count()
        self.parse_four_byte_io_element()

        self.get_io_element_eight_byte_element_count()
        self.parse_eight_byte_io_element()

        self.data_packet.data.avl_data_list.append(self.avl_data)

    def view_data_packet(self):
        print("TCP AVL Data Packet -----------------")
        print("Preamble: ", self.data_packet.preamble)
        print("AVL Data Length: ", self.data_packet.avl_data_length)
        print("Data ----------------")
        print("    Codec ID: ", self.data_packet.data.codec_id)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count)
        for i in self.data_packet.data.avl_data_list:
            print("    AVL Data -----------------")
            print("        Timestamp: ", i.timestamp)
            print("        Priority: ", i.priority)
            print("        GPS Element ------------------")
            print("            Longitude: ", i.gps_element.longitude)
            print("            Latitude: ", i.gps_element.latitude)
            print("            Altitude: ", i.gps_element.altitude)
            print("            Angle: ", i.gps_element.angle)
            print("            Satellites: ", i.gps_element.satellites)
            print("            Speed: ", i.gps_element.speed)

            print("        I/O Element ------------------")
            print("            Event ID: ", i.io_element.event_ID)

            print("            Element count: ", i.io_element.element_count)
            print("            1b Element count: ", i.io_element.one_byte_element_count)
            for j in i.io_element.list_one_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            2b Element count: ", i.io_element.two_byte_element_count)
            for j in i.io_element.list_two_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            4b Element count: ", i.io_element.four_byte_element_count)
            for j in i.io_element.list_four_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            8b Element count: ", i.io_element.eight_byte_element_count)
            for j in i.io_element.list_eight_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count2)
        print("Crc: ", self.data_packet.crc)

    def convert_to_json(self):
        tcp_avl_data_packet = {}
        tcp_avl_data_packet["Preamble"] = self.data_packet.preamble
        tcp_avl_data_packet["AVL Data Length"] = self.data_packet.avl_data_length
        tcp_avl_data_packet["Data"] = {}
        tcp_avl_data_packet["Data"]["Codec ID"] = self.data_packet.data.codec_id
        tcp_avl_data_packet["Data"]["AVL Data Count"] = self.data_packet.data.avl_data_count
        tcp_avl_data_packet["Data"]["AVL Data List"] = []
        for i in self.data_packet.data.avl_data_list:
            obj = {}
            obj["Timestamp"] = i.timestamp
            obj["Priority"] = i.priority
            obj["GPS Element"] = {}
            obj["GPS Element"]["Longitude"] = i.gps_element.longitude
            obj["GPS Element"]["Latitude"] = i.gps_element.latitude
            obj["GPS Element"]["Altitude"] = i.gps_element.altitude
            obj["GPS Element"]["Angle"] = i.gps_element.angle
            obj["GPS Element"]["Satellites"] = i.gps_element.satellites
            obj["GPS Element"]["Speed"] = i.gps_element.speed
            obj["I/O Element"] = {}
            obj["I/O Element"]["Event ID"] = i.io_element.event_ID
            obj["I/O Element"]["Element count"] = i.io_element.element_count

            obj["I/O Element"]["1b Element count"] = i.io_element.one_byte_element_count
            obj["I/O Element"]["1b Elements"] = []
            for j in i.io_element.list_one_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["1b Elements"].append(obj2)

            obj["I/O Element"]["2b Element count"] = i.io_element.two_byte_element_count
            obj["I/O Element"]["2b Elements"] = []
            for j in i.io_element.list_two_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["2b Elements"].append(obj2)

            obj["I/O Element"]["4b Element count"] = i.io_element.four_byte_element_count
            obj["I/O Element"]["4b Elements"] = []
            for j in i.io_element.list_four_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["4b Elements"].append(obj2)

            obj["I/O Element"]["8b Element count"] = i.io_element.eight_byte_element_count
            obj["I/O Element"]["8b Elements"] = []
            for j in i.io_element.list_eight_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["8b Elements"].append(obj2)

            tcp_avl_data_packet["Data"]["AVL Data List"].append(obj)

        tcp_avl_data_packet["Data"]["AVL Data Count End"] = self.data_packet.data.avl_data_count2
        tcp_avl_data_packet["Crc"] = self.data_packet.crc

        return tcp_avl_data_packet


class Codec16(Codec8):
    def get_io_element_event_ID(self):
        self.avl_data.io_element.event_ID = int(self.data[:4], 16)
        self.data = self.data[4:]

    def parse_one_byte_io_element(self):
        for j in range(self.avl_data.io_element.one_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:2], 16)
            self.data = self.data[2:]
            self.avl_data.io_element.list_one_byte_elements.append(io_element_obj)

    def parse_two_byte_io_element(self):
        for j in range(self.avl_data.io_element.two_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:4], 16)
            self.data = self.data[4:]
            self.avl_data.io_element.list_two_byte_elements.append(io_element_obj)

    def parse_four_byte_io_element(self):
        for j in range(self.avl_data.io_element.four_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:8], 16)
            self.data = self.data[8:]
            self.avl_data.io_element.list_four_byte_elements.append(io_element_obj)

    def parse_eight_byte_io_element(self):
        for j in range(self.avl_data.io_element.eight_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:16], 16)
            self.data = self.data[16:]
            self.avl_data.io_element.list_eight_byte_elements.append(io_element_obj)

    def get_origin_type(self):
        self.avl_data.io_element.origin_type = int(self.data[:2], 16)
        self.data = self.data[2:]

    def parse_avl_data(self):
        self.get_timestamp()
        self.get_priority()
        self.get_gps_element_longitude()
        self.get_gps_element_latitude()
        self.get_gps_element_altitude()
        self.get_gps_element_angle()
        self.get_gps_element_satellites()
        self.get_gps_element_speed()
        self.get_io_element_event_ID()
        self.get_origin_type()
        self.get_io_element_count()

        self.get_io_element_one_byte_element_count()
        self.parse_one_byte_io_element()

        self.get_io_element_two_byte_element_count()
        self.parse_two_byte_io_element()

        self.get_io_element_four_byte_element_count()
        self.parse_four_byte_io_element()

        self.get_io_element_eight_byte_element_count()
        self.parse_eight_byte_io_element()

        self.data_packet.data.avl_data_list.append(self.avl_data)

    def view_data_packet(self):
        print("TCP AVL Data Packet -----------------")
        print("Preamble: ", self.data_packet.preamble)
        print("AVL Data Length: ", self.data_packet.avl_data_length)
        print("Data ----------------")
        print("    Codec ID: ", self.data_packet.data.codec_id)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count)
        for i in self.data_packet.data.avl_data_list:
            print("    AVL Data -----------------")
            print("        Timestamp: ", i.timestamp)
            print("        Priority: ", i.priority)
            print("        GPS Element ------------------")
            print("            Longitude: ", i.gps_element.longitude)
            print("            Latitude: ", i.gps_element.latitude)
            print("            Altitude: ", i.gps_element.altitude)
            print("            Angle: ", i.gps_element.angle)
            print("            Satellites: ", i.gps_element.satellites)
            print("            Speed: ", i.gps_element.speed)

            print("        I/O Element ------------------")
            print("            Event ID: ", i.io_element.event_ID)
            print("            Origin Type: ", i.io_element.origin_type)
            print("            Element count: ", i.io_element.element_count)
            print("            1b Element count: ", i.io_element.one_byte_element_count)
            for j in i.io_element.list_one_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            2b Element count: ", i.io_element.two_byte_element_count)
            for j in i.io_element.list_two_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            4b Element count: ", i.io_element.four_byte_element_count)
            for j in i.io_element.list_four_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            8b Element count: ", i.io_element.eight_byte_element_count)
            for j in i.io_element.list_eight_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count2)
        print("Crc: ", self.data_packet.crc)

    def convert_to_json(self):
        tcp_avl_data_packet = {}
        tcp_avl_data_packet["Preamble"] = self.data_packet.preamble
        tcp_avl_data_packet["AVL Data Length"] = self.data_packet.avl_data_length
        tcp_avl_data_packet["Data"] = {}
        tcp_avl_data_packet["Data"]["Codec ID"] = self.data_packet.data.codec_id
        tcp_avl_data_packet["Data"]["AVL Data Count"] = self.data_packet.data.avl_data_count
        tcp_avl_data_packet["Data"]["AVL Data List"] = []
        for i in self.data_packet.data.avl_data_list:
            obj = {}
            obj["Timestamp"] = i.timestamp
            obj["Priority"] = i.priority
            obj["GPS Element"] = {}
            obj["GPS Element"]["Longitude"] = i.gps_element.longitude
            obj["GPS Element"]["Latitude"] = i.gps_element.latitude
            obj["GPS Element"]["Altitude"] = i.gps_element.altitude
            obj["GPS Element"]["Angle"] = i.gps_element.angle
            obj["GPS Element"]["Satellites"] = i.gps_element.satellites
            obj["GPS Element"]["Speed"] = i.gps_element.speed
            obj["I/O Element"] = {}
            obj["I/O Element"]["Event ID"] = i.io_element.event_ID
            obj["I/O Element"]["Origin type"] = i.io_element.origin_type
            obj["I/O Element"]["Element count"] = i.io_element.element_count

            obj["I/O Element"]["1b Element count"] = i.io_element.one_byte_element_count
            obj["I/O Element"]["1b Elements"] = []
            for j in i.io_element.list_one_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["1b Elements"].append(obj2)

            obj["I/O Element"]["2b Element count"] = i.io_element.two_byte_element_count
            obj["I/O Element"]["2b Elements"] = []
            for j in i.io_element.list_two_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["2b Elements"].append(obj2)

            obj["I/O Element"]["4b Element count"] = i.io_element.four_byte_element_count
            obj["I/O Element"]["4b Elements"] = []
            for j in i.io_element.list_four_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["4b Elements"].append(obj2)

            obj["I/O Element"]["8b Element count"] = i.io_element.eight_byte_element_count
            obj["I/O Element"]["8b Elements"] = []
            for j in i.io_element.list_eight_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["8b Elements"].append(obj2)

            tcp_avl_data_packet["Data"]["AVL Data List"].append(obj)

        tcp_avl_data_packet["Data"]["AVL Data Count End"] = self.data_packet.data.avl_data_count2
        tcp_avl_data_packet["Crc"] = self.data_packet.crc

        return tcp_avl_data_packet


class Codec8Ex(Codec8):
    def get_io_element_event_ID(self):
        self.avl_data.io_element.event_ID = int(self.data[:4], 16)
        self.data = self.data[4:]

    def parse_one_byte_io_element(self):
        for j in range(self.avl_data.io_element.one_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:2], 16)
            self.data = self.data[2:]
            self.avl_data.io_element.list_one_byte_elements.append(io_element_obj)

    def parse_two_byte_io_element(self):
        for j in range(self.avl_data.io_element.two_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:4], 16)
            self.data = self.data[4:]
            self.avl_data.io_element.list_two_byte_elements.append(io_element_obj)

    def parse_four_byte_io_element(self):
        for j in range(self.avl_data.io_element.four_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:8], 16)
            self.data = self.data[8:]
            self.avl_data.io_element.list_four_byte_elements.append(io_element_obj)

    def parse_eight_byte_io_element(self):
        for j in range(self.avl_data.io_element.eight_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:16], 16)
            self.data = self.data[16:]
            self.avl_data.io_element.list_eight_byte_elements.append(io_element_obj)

    def get_io_element_count(self):
        self.avl_data.io_element.element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_one_byte_element_count(self):
        self.avl_data.io_element.one_byte_element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_two_byte_element_count(self):
        self.avl_data.io_element.two_byte_element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_four_byte_element_count(self):
        self.avl_data.io_element.four_byte_element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_eight_byte_element_count(self):
        self.avl_data.io_element.eight_byte_element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def get_io_element_x_byte_element_count(self):
        self.avl_data.io_element.x_byte_element_count = int(self.data[:4], 16)
        self.data = self.data[4:]

    def parse_x_byte_io_element(self):
        for j in range(self.avl_data.io_element.x_byte_element_count):
            io_element_obj = IO_Element_object()
            io_element_obj.ID = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.length = int(self.data[:4], 16)
            self.data = self.data[4:]
            io_element_obj.value = int(self.data[:(io_element_obj.length*2)], 16)
            self.data = self.data[(io_element_obj.length*2):]
            self.avl_data.io_element.list_x_byte_elements.append(io_element_obj)

    def parse_avl_data(self):
        self.get_timestamp()
        self.get_priority()
        self.get_gps_element_longitude()
        self.get_gps_element_latitude()
        self.get_gps_element_altitude()
        self.get_gps_element_angle()
        self.get_gps_element_satellites()
        self.get_gps_element_speed()
        self.get_io_element_event_ID()
        self.get_io_element_count()

        self.get_io_element_one_byte_element_count()
        self.parse_one_byte_io_element()

        self.get_io_element_two_byte_element_count()
        self.parse_two_byte_io_element()

        self.get_io_element_four_byte_element_count()
        self.parse_four_byte_io_element()

        self.get_io_element_eight_byte_element_count()
        self.parse_eight_byte_io_element()

        self.get_io_element_x_byte_element_count()
        self.parse_x_byte_io_element()

        self.data_packet.data.avl_data_list.append(self.avl_data)

    def view_data_packet(self):
        print("TCP AVL Data Packet -----------------")
        print("Preamble: ", self.data_packet.preamble)
        print("AVL Data Length: ", self.data_packet.avl_data_length)
        print("Data ----------------")
        print("    Codec ID: ", self.data_packet.data.codec_id)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count)
        for i in self.data_packet.data.avl_data_list:
            print("    AVL Data -----------------")
            print("        Timestamp: ", i.timestamp)
            print("        Priority: ", i.priority)
            print("        GPS Element ------------------")
            print("            Longitude: ", i.gps_element.longitude)
            print("            Latitude: ", i.gps_element.latitude)
            print("            Altitude: ", i.gps_element.altitude)
            print("            Angle: ", i.gps_element.angle)
            print("            Satellites: ", i.gps_element.satellites)
            print("            Speed: ", i.gps_element.speed)

            print("        I/O Element ------------------")
            print("            Event ID: ", i.io_element.event_ID)
            print("            Origin Type: ", i.io_element.origin_type)
            print("            Element count: ", i.io_element.element_count)
            print("            1b Element count: ", i.io_element.one_byte_element_count)
            for j in i.io_element.list_one_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            2b Element count: ", i.io_element.two_byte_element_count)
            for j in i.io_element.list_two_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            4b Element count: ", i.io_element.four_byte_element_count)
            for j in i.io_element.list_four_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            8b Element count: ", i.io_element.eight_byte_element_count)
            for j in i.io_element.list_eight_byte_elements:
                print("            ID: ", j.ID)
                print("            Value: ", j.value)

            print("            Xb Element count: ", i.io_element.x_byte_element_count)
            for j in i.io_element.list_x_byte_elements:
                print("            ID: ", j.ID)
                print("            Length: ", j.length)
                print("            Value: ", j.value)
        print("    AVL Data Count: ", self.data_packet.data.avl_data_count2)
        print("Crc: ", self.data_packet.crc)

    def convert_to_json(self):
        tcp_avl_data_packet = {}
        tcp_avl_data_packet["Preamble"] = self.data_packet.preamble
        tcp_avl_data_packet["AVL Data Length"] = self.data_packet.avl_data_length
        tcp_avl_data_packet["Data"] = {}
        tcp_avl_data_packet["Data"]["Codec ID"] = self.data_packet.data.codec_id
        tcp_avl_data_packet["Data"]["AVL Data Count"] = self.data_packet.data.avl_data_count
        tcp_avl_data_packet["Data"]["AVL Data List"] = []
        for i in self.data_packet.data.avl_data_list:
            obj = {}
            obj["Timestamp"] = i.timestamp
            obj["Priority"] = i.priority
            obj["GPS Element"] = {}
            obj["GPS Element"]["Longitude"] = i.gps_element.longitude
            obj["GPS Element"]["Latitude"] = i.gps_element.latitude
            obj["GPS Element"]["Altitude"] = i.gps_element.altitude
            obj["GPS Element"]["Angle"] = i.gps_element.angle
            obj["GPS Element"]["Satellites"] = i.gps_element.satellites
            obj["GPS Element"]["Speed"] = i.gps_element.speed
            obj["I/O Element"] = {}
            obj["I/O Element"]["Event ID"] = i.io_element.event_ID
            obj["I/O Element"]["Origin type"] = i.io_element.origin_type
            obj["I/O Element"]["Element count"] = i.io_element.element_count

            obj["I/O Element"]["1b Element count"] = i.io_element.one_byte_element_count
            obj["I/O Element"]["1b Elements"] = []
            for j in i.io_element.list_one_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["1b Elements"].append(obj2)

            obj["I/O Element"]["2b Element count"] = i.io_element.two_byte_element_count
            obj["I/O Element"]["2b Elements"] = []
            for j in i.io_element.list_two_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["2b Elements"].append(obj2)

            obj["I/O Element"]["4b Element count"] = i.io_element.four_byte_element_count
            obj["I/O Element"]["4b Elements"] = []
            for j in i.io_element.list_four_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["4b Elements"].append(obj2)

            obj["I/O Element"]["8b Element count"] = i.io_element.eight_byte_element_count
            obj["I/O Element"]["8b Elements"] = []
            for j in i.io_element.list_eight_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Value"] = j.value
                obj["I/O Element"]["8b Elements"].append(obj2)

            obj["I/O Element"]["xb Element count"] = i.io_element.x_byte_element_count
            obj["I/O Element"]["xb Elements"] = []
            for j in i.io_element.list_x_byte_elements:
                obj2 = {}
                obj2["ID"] = j.ID
                obj2["Length"] = j.length
                obj2["Value"] = j.value
                obj["I/O Element"]["xb Elements"].append(obj2)

            tcp_avl_data_packet["Data"]["AVL Data List"].append(obj)

        tcp_avl_data_packet["Data"]["AVL Data Count End"] = self.data_packet.data.avl_data_count2
        tcp_avl_data_packet["Crc"] = self.data_packet.crc

        return tcp_avl_data_packet