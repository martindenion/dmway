from unittest import TestCase
import time

class TestVerificationZwave(TestCase):

    def test_init(self):
        raw_json_empty = {}
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false,"value":0}')
        self.assertEqual(verif.filtered_dict, raw_json_empty)

    #tests zwave to dmway standard

    def test_zwave_device(self):
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false,"value":0}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['device'], 'zwave_3-49-1-4')
        #self.assertAlmostEqual(verif.filtered_dict['ts'], int(round(time.time() * 1000)), 1)

    def test_zwave_type(self):
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false,"value":0}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['type'], 49)

    def test_zwave_value(self):
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false,"value":0}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['values']['Power'], 0)

    def test_zwave_without_key(self):
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power management","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false,"value":0}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict, {})

    def test_zwave_without_value(self):
        from src.format.format import Verification
        verif = Verification('{"value_id":"3-49-1-4","node_id":3,"class_id":49,"type":"decimal","genre":"user",'
                             '"instance":1,"index":4,"label":"Power","units":"W","help":"","read_only":true,'
                             '"write_only":false,"min":0,"max":0,"is_polled":false}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict, {})

    #tests rf433 to dmway

    def test_rf433_device(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_C" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['device'], 'RF433_103')

    def test_rf433_type(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_C" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['type'], 'THGR122N')

    def test_one_rf433_value(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_C" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['values']['temperature_C'], 20.400)

    def test_another_rf433_value(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_C" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict['values']['battery'], "OK")

    def test_rf433_without_key(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_F" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict, {})

    def test_rf433_without_type(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "id" : 103, '
                             '"channel" : 1, "battery" : "OK", "temperature_F" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict, {})

    def test_rf433_without_device(self):
        from src.format.format import Verification
        verif = Verification('{"time" : "2018-01-06 13:45:58", "brand" : "OS", "model" : "THGR122N", '
                             '"channel" : 1, "battery" : "OK", "temperature_F" : 20.400, "humidity" : 53}')
        verif.set_json_schema_default()
        verif.compare_rx_std()
        verif.check_value_to_send()
        verif.rx_to_dmway()
        self.assertEqual(verif.filtered_dict, {})
