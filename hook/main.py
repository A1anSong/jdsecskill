import sys

import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


if __name__ == '__main__':
    pass
    # new_user_info(users.sxz)
    # with open('jd_encrypt.js') as js_file:
    #     jscode = js_file.read()
    # host = '192.168.2.124:9999'
    # manager = frida.get_device_manager()
    # device = manager.add_remote_device(host)
    # process = device.attach('京东')
    # script = process.create_script(jscode)
    # script.on('message', on_message)
    # print('[*] Running CTF')
    # script.load()
    # res = script.exports_sync.encrypt(
    #     'newUserInfo',
    #     '{"flag":"nickname","fromSource":1,"sourceLevel":1}',
    #     'eae36be37144ad31',
    #     'android',
    #     '12.1.4'
    # )
    # print(res)
    # sys.stdin.read()
