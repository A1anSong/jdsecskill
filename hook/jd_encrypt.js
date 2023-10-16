let result;

function encrypt(functionId, body, uuid, client, clientVersion) {
    Java.perform(() => {
        console.log("start")
        const BitmapkitUtils = Java.use('com.jingdong.common.utils.BitmapkitUtils')
        const context = Java.use('android.app.ActivityThread').currentApplication().getApplicationContext()
        const str = Java.use('java.lang.String')
        const jfunctionId = str.$new(functionId)
        const jbody = str.$new(body)
        const juuid = str.$new(uuid)
        const jclient = str.$new(client)
        const jclientVersion = str.$new(clientVersion)
        result = BitmapkitUtils.getSignFromJni(context, jfunctionId, jbody, juuid, jclient, jclientVersion)
    });
    return result
}

rpc.exports = {
    encrypt: encrypt
}