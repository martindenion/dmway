import json

class Verification:
    """Cette classe comporte les méthodes nécessaire à la vérification
    du format JSON des données reçues par les différents capteurs"""

    def __init__(self):
        """Par défaut, la vérification du format est un échec"""
        self.success_keys = False
        self.success_values = False

    def json_to_dict(self, raw_json):
        """Méthode qui permet de convertir un message JSON en dictionnaire python"""
        return json.loads(raw_json)

    def _get_ts(self, raw_json):
        raw_dict = self.json_to_dict(raw_json)
        return raw_dict["ts"]

    def get_keys(self, raw_json):
        """Méthode qui retourne une liste des key de la trame JSON"""
        raw_dict = self.json_to_dict(raw_json)
        keys_list = []
        for cle in raw_dict.keys():
            keys_list.append(cle)
        return keys_list

    def get_values(self, raw_json):
        """Méthode qui retourne une liste des valeurs de la trame JSON"""
        raw_dict = self.json_to_dict(raw_json)
        values_list = []
        for cle in raw_dict.values():
            values_list.append(cle)
        return values_list

    def verify_keys(self, raw_json):
        """"Méthode qui vérifie la validité des keys de la trame JSON"""
        keys_list = self._get_keys(raw_json)
        model_keys_list = ['name', 'type', 'ts', 'temperature', 'humidity', 'pressure', 'luminosity', 'sound']
        if 'name' in keys_list and 'type' in keys_list:
            for key in keys_list:
                print('key : {}'.format(key))
                if key in model_keys_list:
                    self.success_keys = True
                else:
                    self.success_keys = False
                    break
        else:
            self.success_keys = False
        return self.success_keys

    def verify_values(self, raw_json):
        """Méthode qui vérifie la validité des values de la trame JSON"""
        raw_dict = self.json_to_dict(raw_json)
        values_list = self._get_values(raw_json)
        for key, value in raw_dict.items():
            if (key == 'name' or key == 'type') and isinstance(value, str):
                self.success_values = True
            elif isinstance(value, int) or isinstance(value, float):
                self.success_values = True
            else:
                self.success_values = False
                break
        return self.success_values