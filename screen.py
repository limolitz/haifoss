import network
import time
import ntptime
import socket
import json
import sys

from inkplate10 import Inkplate


# COLS 825
# ROWS 1200


class Haifoss:
    display = None
    ip = None
    tab_width = 200
    tab_height = 50
    tab_left_margin = 12

    pictures_seconds = None

    config_file = "config.json"

    def __init__(self):
        self.display = Inkplate(Inkplate.INKPLATE_1BIT)
        self.display.begin()
        self.display.clearDisplay()
        self.display.setRotation(3)

    def read_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def get_config(self, key):
        if not(hasattr(self, 'config')):
            self.read_config()
        return self.config[key]

    def init_screen(self):
        self.display.clearDisplay()

    def fill(self, number):
        if number < 10:
            return "0"+str(number)
        return str(number)

    def get_time_str(self, seconds):
        year, month, mday, hour, minute, second, weekday, yearday = time.localtime(seconds)
        return str(year)+"-"+self.fill(month)+"-"+self.fill(mday)+" " \
            + self.fill(hour)+":"+self.fill(minute)+":"+self.fill(second)

    def http_get(self, url):
        _, _, host, path = url.split("/", 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect(addr)
        except OSError:
            return

        s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))

        last_four = "0000"
        headers = ""

        while True:
            data = s.recv(1)
            if data:
                # read headers byte by byte and parse as str
                headers += str(data, "utf8")
                # keep a sliding window on the last four characters to find body start
                last_four = last_four[1:] + str(data, "utf8")
                if last_four == "\r\n\r\n":
                    break
            else:
                break

        line_count = self.tab_height
        carryover = ""

        # TODO: parse header for content-length, and keep track of amount of received data
        # TODO: check if the file changed at all

        while True:
            print("Fetching data")
            try:
                data = s.recv(1024)
            except OSError:
                break

            if data:
                data_str = carryover + str(data, "utf8")

                # split by lines
                lines = data_str.splitlines()

                lines_use = lines

                # don't process last line if it is not complete and merge before next data
                if data_str[-1] != '\n':
                    carryover = lines[-1]
                    lines_use = lines[:-1]
                else:
                    carryover = ""

                for line in lines_use:
                    # if line has any data
                    # TODO: live progress bar?

                    print("Drawing col {}, len {}".format(line_count - self.tab_height, len(line)))
                    if len(line) > 0:
                        # draw immediately to conserve RAM
                        self.draw_line(line_count, line)
                    line_count += 1

            else:
                print("No data left")
                break
        s.close()

        return headers

    def draw_line(self, line_count, data):
        for h_line in data.split(','):
            start, end = h_line.split('-')
            # TODO: use grayscale?
            self.display.drawFastHLine(int(start), line_count, int(end) - int(start), self.display.BLACK)

    def get_pictures(self, count=1):
        start = time.time()
        path = self.get_config("pictures_url").format(count)

        # TODO: use max_height
        max_height = 1200 - self.tab_height

        start_get = time.time()
        self.http_get(path)
        end_get = time.time()
        print("HTTP/Write took {}s".format(end_get - start_get))
        self.pictures_seconds = time.time() - start

    def update_screen(self):
        self.draw_tabs()
        self.draw_statusbar()

        # self.draw_grid()
        self.display.display()

    def draw_tabs(self):
        for x in range(self.tab_left_margin, self.display.width() - self.tab_width, self.tab_width):
            self.display.drawRect(x, 0, self.tab_width, self.tab_height, self.display.BLACK)

    def draw_statusbar(self):
        self.display.drawFastHLine(0, self.display.height() - 15, self.display.width(), self.display.BLACK)
        last_line_y = self.display.height() - 12
        self.display.printText(10, last_line_y, "IP: {}".format(self.ip))
        self.display.printText(
            200, last_line_y,
            "Last update: {}, I/O took {}s".format(self.get_time_str(time.time()), self.pictures_seconds)
        )

    def draw_grid(self):
        for width in range(100, self.display.width(), 100):
            self.display.drawLine(width, 0, width, self.display.height(), self.display.BLACK)

        for height in range(100, self.display.height(), 100):
            self.display.drawLine(0, height, self.display.width(), height, self.display.BLACK)

    def connect_wifi(self):
        sta_if = network.WLAN(network.STA_IF)

        if not sta_if.isconnected():
            print("connecting to network...")
            sta_if.active(True)
            sta_if.connect(self.get_config("ssid"), self.get_config("password"))
            while not sta_if.isconnected():
                pass
        ip, netmask, gateway, dns = sta_if.ifconfig()
        self.ip = ip

        try:
            ntptime.settime()
        except OSError:
            pass

    def loop(self):

        while True:
            self.connect_wifi()

            self.init_screen()

            self.get_pictures()

            self.update_screen()

            print("Sleeping...")

            time.sleep(300)


def main():
    try:
        haifoss = Haifoss()
        haifoss.loop()
    except Exception as e:
        print("An exception occured: {}".format(e))
        sys.print_exception(e)


if __name__ == "__main__":
    main()
