from selenium_stealth.selenium_stealth import stealth
from selenium import webdriver
from urllib.parse import unquote

def init_base_cap(options):
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-impl-side-painting")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-accelerated-jpeg-decoding")
    options.add_argument("--test-type=ui")
    options.add_argument("--ignore-certificate-errors")

    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'permissions.default.stylesheet': 2,
        }
    }
    options.add_experimental_option("prefs", prefs)


def add_stealth_js(driver):
    stealth(driver,
            languages=["en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Google Inc. (NVIDIA)",
            renderer="ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.7005)",
            fix_hairline=True,
            )


def get_driver():
    options = webdriver.ChromeOptions()
    init_base_cap(options)

    driver = webdriver.Chrome(options=options)
    add_stealth_js(driver)

    return driver


def get_letters():
    """Frence letters"""
    letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
    return letters.split(' ')


def str_filter(text):
    if not text:
        return ''

    decode_text = unquote(text)

    return decode_text.replace('+', ' ')
