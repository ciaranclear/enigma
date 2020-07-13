
from core_enigma.enigma.enigma import Enigma
from core_enigma.keyboard.keyboard import Keyboard
from core_enigma.plugboard.plugboard import Plugboard
from core_enigma.rotor_group.rotor_group import RotorGroup
from core_enigma.rotor_group_collection.rotor_group_collection import RotorGroupCollection
from core_enigma.stecker_cable.stecker_cable import SteckerCable
from core_enigma.connector.connector import Connector
from core_enigma.uhr_box.uhr_box import UhrBox
from core_enigma.settings.settings import (NUMBERS,
                                           LETTERS,
                                           QWERTZ,
                                           EQUIPMENT_DICT,
                                           KEYBOARD_DICT,
                                           ENIGMA_LAYOUT,
                                           UHR_DICT,
                                           MORSE_CODE)


def machines():
  machines = []
  for machine in EQUIPMENT_DICT:
    machines.append(machine)
  return machines

def makeMachine(machine_type):

  def machine_init(self):
    super(type(self), self).__init__()

  machine = type(machine_type,(Enigma,),{"__init__": machine_init})
  machine = machine()
  # add keyboard
  machine.keyboard = Keyboard(KEYBOARD_DICT)
  # add plugboard
  plugboard_type = EQUIPMENT_DICT[machine_type]["PLUGBOARD"]
  if (plugboard_type == "STECKER"):
    machine.plugboard = Plugboard()
  elif (plugboard_type == "UHR"):
    machine.uhr_box = UhrBox(UHR_DICT)
    machine.plugboard = Plugboard()
  # add rotor group
  entry_wheel_chars = EQUIPMENT_DICT[machine_type]["ENTRY_WHEEL"]
  rotor_group_cells = EQUIPMENT_DICT[machine_type]["ROTOR_GROUP_CELLS"]
  machine.rotor_group = RotorGroup(entry_wheel_chars,
                                   rotor_group_cells)
  # add rotor group items
  rotors = EQUIPMENT_DICT[machine_type]["ROTORS"]
  reflectors = EQUIPMENT_DICT[machine_type]["REFLECTORS"]
  ring_characters = EQUIPMENT_DICT[machine_type]["RING_CHARACTERS"]
  machine.rotor_group_collection = RotorGroupCollection(rotors,
                                                        ring_characters,
                                                        reflectors)
  return machine


if __name__ == "__main__":

  machines = machines()
  for machine in machines:
    machine = makeMachine(machine)
    print(machine.machine_type)
    print(machine.valid_enigma())
    print(dir(machine))
    #print(machine.rotor_group_collection.rotors_list())
    #print(machine.rotor_group_collection.reflectors_list())