from dataclasses import dataclass, field
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: float  # Защита
    stamina_per_turn: float  # Количество затрачиваемой выносливости за ход

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float  # Минимальный урон
    max_damage: float  # Максимальный урон
    stamina_per_hit: float  # Количество затрачиваемой выносливости за удар

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon] = field(default_factory=list)
    armors: List[Armor] = field(default_factory=list)


class Equipment:
    def __init__(self):
        self.equipment = Equipment._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        :param weapon_name:  название оружия
        :return: соответсвующий объект Weapon
        """
        return next(filter(lambda weapon: weapon.name in weapon_name, self.equipment.weapons))

    def get_armor(self, armor_name: str) -> Armor:
        """
        :param armor_name: название амуниции
        :return: соответсвующий объект Armor
        """
        return next(filter(lambda armor: armor.name in armor_name, self.equipment.armors))

    def get_weapons_names(self) -> list:
        """
        :return: список названий оружия
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """
        :return: список названий амуниции
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open('data/equipment.json', encoding='utf-8') as data:
            data = json.load(data)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
