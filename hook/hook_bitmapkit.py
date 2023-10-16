import sys

import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


jscode = """
Java.perform(() => {
  console.log("Inside java perform function");
  // Function to hook is defined here
  const my_class = Java.use('com.jingdong.common.utils.BitmapkitUtils');
  console.log("Java.Use.Successfully!");

  my_class.getSignFromJni.implementation = function (p0, p1, p2, p3, p4, p5){
    console.log(p0);
    console.log(p1);
    console.log(p2);
    console.log(p3);
    console.log(p4);
    console.log(p5);
    var ret_value = this.getSignFromJni(p0, p1, p2, p3, p4, p5);
    console.log(ret_value);
    return ret_value;
  };
});
"""

if __name__ == '__main__':
    host = '192.168.2.124:9999'
    manager = frida.get_device_manager()
    device = manager.add_remote_device(host)
    process = device.attach('京东')
    script = process.create_script(jscode)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()
