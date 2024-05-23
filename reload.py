import requests
import urllib.parse
import logging
import colorlog

class bypass:
    def __init__(self, reload_url, anchor_url, bg_value):
        self.reload_url = reload_url.strip()
        self.anchor_url = anchor_url.strip()
        self.bg_value = bg_value.strip()
        self.site_key = self.anchor_url.split('k=')[1].split("&")[0]
        self.co = self.anchor_url.split("co=")[1].split("&")[0]
        self.v = self.anchor_url.split("v=")[1].split("&")[0]
        self.chr_value, self.vh_value = self.extract_chr_vh(bg_value)
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = colorlog.getLogger()
        logger.setLevel(logging.INFO)
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(handler)
        return logger

    def extract_chr_vh(self, bg_value):
        chr_start_index = bg_value.find("chr=") + 4
        chr_end_index = bg_value.find("&", chr_start_index)
        chr_value = urllib.parse.unquote(bg_value[chr_start_index:chr_end_index])

        vh_start_index = bg_value.find("vh=") + 3
        vh_end_index = bg_value.find("&", vh_start_index)
        vh_value = urllib.parse.unquote(bg_value[vh_start_index:vh_end_index])

        return chr_value, vh_value

    def send_get_request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def send_post_request(self, url, token):
        payload = {
            "v": self.v,
            "reason": "q",
            "c": token,
            "k": self.site_key,
            "co": self.co,
            "hl": "en",
            "size": "invisible",
            "chr": self.chr_value,
            "vh": self.vh_value,
            "bg": self.bg_value
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def bypass_recaptcha(self):
        request_text = self.send_get_request(self.anchor_url)
        if request_text:
            token = request_text.split('recaptcha-token" value="')[1].split('">')[0]
            response_text = self.send_post_request(self.reload_url, token)
            if response_text:
                try:
                    captcha_value = str(response_text.split('"rresp","')[1].split('"')[0])
                    print(captcha_value)
                    print(response.cookies)
                    return captcha_value
                except Exception as e:
                    return False
            else:
                return False
        else:
            return False

# Setting up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='recaptcha_bypasser.log',
                    filemode='a')

# Example usage:
#https://www.google.com/recaptcha/api2/reload?k=

reload_url = ""
anchor_url = ""
bg_value   = ""
bypasser = bypass(reload_url, anchor_url, bg_value)

"""

Reload URL: redacted
Anchor URL : redacted
BG : redacted~~~R4-lYdDr6YMaJ0Gg2oQoOafyuH6bHFV0kW8ODQN8Ho7rxvX5q0mPEBESEz69vQEbs2MFUu6AP1_eUHnypzKfAM6rOvDd2mOBDhuEYOSJEkadR-zp0eUmVeRDbGZyHc2zIxTd5UQtaldQSDWStNw1V3W8JPpyqxcFb3JJu_2n5-9Vsoyh1js0Xeuy2QFG0EuyTSXDxAY_V5vqymoApH64r9qJkUarXEtDGAGEyqxgrPYjMfQrTIWx8IrWaaHsIkwb948ADkYbychuderYyHra9_gyzVVvqNjuiV8_WynSIyzOqvr6AaOqKPsfhzkiOKb8Pa0huHv4DBczSZ3heLL_5eA3vdVGwxZ3F-udV3Yf55gTFsiXnd4anP-5GD2G2z4HJKklNV65ezVQqOBgW5HWiEO-MDbPaoAWtleo1ZP2AUcp2VlOighDZti5crQO5JuAUZOg2zZMjxcCAcJzX3oRhKExgZkJlU0YeBw5FnD6ew04XmasNSbewgQ8LAJojb93uRLgvDjqtynACFopKWshX0YcXVasSSr5IRnXwR4s6PNRyTgjsdunT67Pnxsa0ZTNRGS3DTQBsgPLDH0YKk91b4z5rvSlP34MKqQjtBF69da7CsStVahER634fetfpEj17SPOwZIYuGgfiV8zxhBhyL10kzixZnLXggh38cfGcP7RUt9XekDLj9tO9ApEo-iQ
2024-05-02 21:34:51 - INFO - GET request sent successfully
2024-05-02 21:34:51 - INFO - POST request sent successfully
2024-05-02 21:34:51 - INFO - Recaptcha Bypassed: 03AFcWeA6T7IW2SsL7mAfxPBRTHxR_B6GHIXQ0aTsK9Q-LjUyJb5redacted~~~t5wNab4vUTZa35O4_VnOMm71kZGGm14xc47bfs1c9anqM3t_jnjsredacted~~~x47OciBoXhqeDgvXSVl89qUhnp9R9299JgHb7-UyL9flomfgSyCJDPDg5fZ6xGPfagredacted~~~m3xIZxLGEVqI4_NCgmHnSjfOsPFZ4iTZCZTD1z4q5qMa4gZvV_tZselYP01QDBOJOPiDbUYVCVQYtIMJ5Ovce7W-2awYW7uLV0NJP-LTMd-4K9nGK9CJUXzW_XufLmjUruyunvOLGkUHWw_1E20Z40cej6M435ftpjFgArmZlWyM2W5pSlN4tcrBKZPPCRuLy-UuvyexR8MvEMEgm1plvRmOq0ShRuF85_NW58SjSXvOsqdXFnbYUnzSfyDnowLLvOCEvnKbTNsUaOhtGLJZfncOdTdQchdgbUO4eQFHab32j1LOpJV76ETV09ec__bO3CNUWJtWsfJ-0fj_et5xfxcAQCdR-Ln7KH5bb_kzfJj-yGhKdzvHmoagiyieURHWzS-ZWLH9LiSdbCOQ20W8jyuJ3oVVBpqy1STdiX6PeIot5wanN7AaxiRPUs6ClVupjcrBK43h166sT2c4QpjwswfMqbbtAixaD1ceBah23aiJLLUsuXK5pPXpAYebz9U9-a6whgn2ls0y0fe_GGPCxFcwkTn3HKMuVw8jAjUQP6jCTZ6YbsLL_w-orjxLMQHTj2qdIdF5Z0vM4lP3BAlzUI0QtVUbBPWH3oU6w7sNDkKBYKgJ2pKJ-25AIO4E9Tn0-3PQtbeJaF4WAgHfZv2hhy6jDhktBQXXUYbmqfRGPn03ZtR_VSGGCTTSlX4-e19QiRzZ7lSg12TCmMUxItnaGHo9hWlW7cQb8XcuMT9Xyapxo3rPCRi7bhDDiiOPv3-EC_mdJ7NN5PVbMZZDMbITLyYRjkOxkALN-d0d6WNZCFmhIYc-5YErRCi1cwbaLpgUADUF-tqmrhiGyLx8nZg9S2ddA023Mv_oiKiXWVshjSkosK7BqlSveQ339b5Voxscr_CauXnJeVZ__nZIp9SUcp70--hCMh9dKTulTYXChLcQGJZqjeexAX4WJXH4lxIBPO0m48cn5IxCYsa42Axoc5hcRdXEBnG6gSXtmDsYAhuHU7swTf5GhZPSq3Jtm87QSu3iT0dXc8SYiFTX0O0XYRbuqyZzk81lQWOaPcZBPd5DRziXOMkfDBnXnCzWILiEE_WE6awHSBchj6mZM15QsaCPcUBV1Mxlas7NTJkfKmcM15PZb4OTdnyAYYVMkjm-aK30QIgSAbs0jlyzZK8EIFK3W-c35D6VA0faNig_cWbv1WY65d6hoyJUiB3XFXQN9xg1IbaiseA_FrwAF7p9sVYcagCI73wHzxXtO2dIBIr2sEmeUkDBuvhGggTKb1SJeRx_mGDN_37yxnFRtypUO1qt6yamC79YiUeU9utELrxTiPGr9WbNJ2_a3Drad55Nf19RSZQwvVbhhbt92GndFjyBLXKWY14yFW-iGrQl5F47Pltl-i7y2etojmYSnxefJzq1qYE5UQtFgmJww5Rmem1wPTN34-ItTqz528MEM5BT45mZMFEAZl_4SVMb-89J-kz30-9JYz5v9QOi3X8bci9TSy8b0z1C-MNTZfF8NUKGbh0RraXmk7hCO-rCocgcZZZz8fBInuz3nKpveEZOwxIA0UMuwcyiBte3DB2pspbgJ4zEg6oSMYsvD4GpUp9zVPS3eedTKc2-VYRMAk0lSDlX-bP97t4hYTdrqYxtJRexgg4LlQst-_aWxWFVnImAt57XQhtthJJaoBuVcsjIInuXCXt_1k0nP70s_hA9jfV86MiFO0ea4IdZ5AbVounRHO3XCw2FeV4ygVAGJYtroxixF0siO3c3nFrC

"""""
