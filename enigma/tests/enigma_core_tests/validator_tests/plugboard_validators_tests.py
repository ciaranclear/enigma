import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.plugboard_validators import *


class TestPlugboardValidators(unittest.TestCase):

    def test_valid_stecker_pb_settings(self):
        """
        
        """
        passing = [
            {
                "input":"ab cd ef gh ij kl mn op qr st",
                "output":{
                    "A":"B","B":"A","C":"D","D":"C","E":"F",
                    "F":"E","G":"H","H":"G","I":"J","J":"I",
                    "K":"L","L":"K","M":"N","N":"M","O":"P",
                    "P":"O","Q":"R","R":"Q","S":"T","T":"S",
                    "U":"U","V":"V","W":"W","X":"X","Y":"Y",
                    "Z":"Z"
                },
                "charset_flag":"L"
            },
            {
                "input":"01,02 03,04 05,06 07,08 09,10 11,12 13,14 15,16 17,18 19,20",
                "output":{
                    "01":"02","02":"01","03":"04","04":"03","05":"06",
                    "06":"05","07":"08","08":"07","09":"10","10":"09",
                    "11":"12","12":"11","13":"14","14":"13","15":"16",
                    "16":"15","17":"18","18":"17","19":"20","20":"19",
                    "21":"21","22":"22","23":"23","24":"24","25":"25",
                    "26":"26"
                },
                "charset_flag":"N"
            }
        ]

        failing = [
            {"input":"#a cd ef gh ij kl mn op qr st","charset_flag":"L"}
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output"], PlugboardValidators.valid_stecker_pb_settings(test_dict["input"], test_dict["charset_flag"]))

        for test_dict in failing:
            with self.assertRaises(SteckerPlugboardSettingsError):
                PlugboardValidators.valid_stecker_pb_settings(test_dict["input"], test_dict["charset_flag"]) 

    def test_valid_uhr_box_pb_settings(self):
        """
        
        """
        passing = [
            {
                "input":"a b c d e f g h i j",
                "output":{
                    "01A":"A","02A":"B","03A":"C","04A":"D","05A":"E",
                    "06A":"F","07A":"G","08A":"H","09A":"I","10A":"J"
                },
                "group":"A",
                "charset_flag":"L"
            },
            {
                "input":"01 02 03 04 05 06 07 08 09 10",
                "output":{
                    "01A":"01","02A":"02","03A":"03","04A":"04","05A":"05",
                    "06A":"06","07A":"07","08A":"08","09A":"09","10A":"10"
                },
                "group":"A",
                "charset_flag":"N"
            }
        ]

        failing = [
            {
                "input":"# b c d e f g h i j",
                "group":"A",
                "charset_flag":"L"
            }
        ]

        for test_dict in passing:
            self.assertEqual(test_dict["output"], PlugboardValidators.valid_uhr_box_pb_settings(test_dict["input"], test_dict["charset_flag"], test_dict["group"]))

        for test_dict in failing:
            with self.assertRaises(UhrBoxPlugboardSettingsError):
                PlugboardValidators.valid_uhr_box_pb_settings(test_dict["input"], test_dict["charset_flag"], test_dict["group"])

    def test_valid_stecker_pb_dict(self):
        """
        
        """
        pass

    def test_valid_uhr_box_pb_dict(self):
        """
        
        """
        pass