from format.format import Verification
from persistor.persist import Database
from publish.publish import Publish
from subscribe.subscribe import SubThread
import var


json2 = '{"name":"device31","type":"capteur1","ts":1483228800000,"temperature":30,"humidity":50,"pressure":1015,' \
        '"luminosity":10000,"sound":55}'
json1 = '{"name":"device32","type":"capteur2","ts":1483228800000,"temperature":30,"humidity":50,"pressure":1015,' \
        '"luminosity":10000,"sound":55}'
json3 = '{"addr":"uneadresse","name":"device2001","type":"capteur3","ts":1483228800000,"temperature":30,"humidity":50,' \
        '"pressure":1015,' \
        '"luminosity":10000,"sound":55}'


def main_app():
    verif = Verification()
    data = Database()
    sub = SubThread()
    data.create_connection()
    data.create_table()
    pub = Publish()
    flag_for_pub = False
    raw_json_rg = ""
    nb_devices = 0
    var.init()
    while True:
        # Reading serial port
        sub.start()
        raw_json = var.raw_json
        # raw_json = json3
        # Comparing previous and current raw JSON to not send several times the same frame
        if raw_json is not None and raw_json != raw_json_rg:
            raw_json_rg = raw_json
            raw_json_sent = verif.modify_ts(raw_json)
            # Verifying the format of the JSON frame
            if verif.verify_keys(raw_json_sent):
                print("Good keys")
                if verif.verify_values(raw_json_sent):
                    print("Good values")
                    # Saving JSON frame in the SQLite database
                    data.create_connection()
                    data.insert_device(raw_json_sent)
                    nb_devices += 1
                    flag_for_pub = True
                else:
                    print("Error format from device : wrong value(s)")
            else:
                print("Error format from device : wrong key(s)")
            if nb_devices > 0 and flag_for_pub:
                pub.create_devices()
                pub.send_telemetry_all_devices()
                data.create_connection()
                data.delete_all_devices()
        nb_devices = 0
        flag_for_pub = False


if __name__ == '__main__':
    main_app()