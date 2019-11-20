from unittest import TestCase

class TestVerification(TestCase):

    def test_init(self):
        raw_json_empty = {"device": "", "type": "", "values": {}}
        from src.format.format import Verification
        verif = Verification()
        self.assertEqual(verif.filtered_dict, raw_json_empty)

    def test_zwave_good_format(self):
        raw_json = '{"node_id":"zwave","label":"fibaro","energy":30,"power":30}'
        raw_dict_filtered = {'device': 'zwave', 'type': 'fibaro', 'values': {'energy': 30, 'power': 30}}
        from src.format.format import Verification
        verif = Verification()
        verif.filter_data("zwave/+/energy", raw_json)
        self.assertEqual(verif.filtered_dict, raw_dict_filtered)

