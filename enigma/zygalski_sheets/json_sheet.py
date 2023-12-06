"""
{
    "reflector":"UKW-B",
    "rotor_types":{"RS":"III","RM":"II","RF":"I"},
	"rotor_settings":{"RS":"A","RM":"A","RF":"A"}
}
"""
from zygalski_sheets1.sheet_data import SheetDataGenerator
import json


def make_json_sheet(settings):
    """
    
    """
    generator = SheetDataGenerator()
    data = generator.data(settings)
    data = json.dumps(data)
    return data