from format.format import Verification
from persistor.persist import Database
from publish.publish import Publish

json2 = '{"name":"device31","type":"capteur1","ts":1483228800000,"temperature":30,"humidity":50,"pressure":1015,' \
        '"luminosity":10000,"sound":55}'
json1 = '{"name":"device32","type":"capteur2","ts":1483228800000,"temperature":30,"humidity":50,"pressure":1015,' \
        '"luminosity":10000,"sound":55}'
json3 = '{"name":"device33","type":"capteur3","ts":1483228800000,"temperature":30,"humidity":50,"pressure":1015,' \
        '"luminosity":10000,"sound":55}'

def main_app():
    verif = Verification()
    data = Database()
    data.create_connection()
    data.create_table()
    pub = Publish()
    flag_for_pub = False
    while True:
        if verif.verify_keys(json1):
            if verif.verify_values(json1):
                data.insert_device(json1)
                flag_for_pub = True
            else:
                print("Error format from device : wrong value(s)")
        else:
            print("Error format from device : wrong key(s)")
        if flag_for_pub:
            data.create_connection()
            pub.create_device(json1, 1)
            pub.send_telemetry(json1, 1)

if __name__ == '__main__':
    main_app()