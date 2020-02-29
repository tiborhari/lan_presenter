import ctypes
from argparse import ArgumentParser
from logging import basicConfig, getLogger
from pkg_resources import resource_string
from platform import system

from aiohttp.web import Application, Response, run_app

logger = getLogger()
is_windows = system() == 'Windows'


INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
VK_LEFT = 0x25
VK_RIGHT = 0x27

# Key code source:
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
WINDOWS_KEY_MAP = {
    'period': 0xBE,
    'F5': 0x74,
    'up': 0x26,
    'pageUp': 0x21,
    'left': 0x25,
    'right': 0x27,
    'down': 0x28,
    'pageDown': 0x22,
}

# Key code source:
# > dumpkeys --keys-only
LINUX_KEY_MAP = {
    'period': 52,
    'F5': 63,
    'up': 103,
    'pageUp': 104,
    'left': 105,
    'right': 106,
    'down': 108,
    'pageDown': 109,
}

if is_windows:
    from ctypes import wintypes

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = (
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", wintypes.WPARAM)
        )

    class MOUNSEINPUT(ctypes.Structure):
        _fields_ = (
            ("dx", wintypes.LONG),
            ("dy", wintypes.LONG),
            ("mouseData", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", wintypes.WPARAM)
        )

    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = (
            ("uMsg", wintypes.DWORD),
            ("wParamL", wintypes.WORD),
            ("wParamH", wintypes.WORD)
        )

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = (
                ('ki', KEYBDINPUT),
                ('mi', MOUNSEINPUT),
                ('hi', HARDWAREINPUT)
            )

        _anonymous_ = ('_input',)
        _fields_ = (
            ('type', wintypes.DWORD),
            ('_input', _INPUT)
        )


def press_key(hex_key_code):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hex_key_code))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hex_key_code,
                                                 dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def click_linux(key_name):
    from keyboard import send

    key_code = LINUX_KEY_MAP[key_name]
    send(key_code)


def click_windows(key_name):
    key_code = WINDOWS_KEY_MAP[key_name]
    press_key(key_code)
    release_key(key_code)


def click_key(key_name):
    click_windows(key_name) if is_windows else click_linux(key_name)


async def index(request):
    return Response(body=resource_string(__name__, 'index.html'),
                    content_type='text/html')


async def press(request):
    params = await request.json()
    click_key(params['key'])
    return Response(body='')


def create_app():
    app = Application()
    app.router.add_post('/press', press)
    app.router.add_get('/', index)
    return app


def parse_args(argv=None):
    parser = ArgumentParser(
        description='Presenter remote control over local network connection.')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default='54321')
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    basicConfig(level='DEBUG' if args.verbose else 'INFO')
    app = create_app()
    run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
