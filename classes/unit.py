from __future__ import annotations
from abc import ABC

from classes.equipment import Weapon, Armor
from classes.classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass) -> object:
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health  # здоровье
        self.stamina = unit_class.max_stamina
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _check_using_armor(self) -> bool:
        """
        Проверка достаточно ли выносливости для использования брони
        :return: bool
        """
        return self.stamina >= self.armor.stamina_per_turn

    def _check_using_weapon(self) -> bool:
        """
        Проверка достаточно ли выносливости для использования оружия
        :return: bool
        """
        return self.stamina >= self.weapon.stamina_per_hit

    def _count_damage(self, target: BaseUnit) -> float:
        """
        :param target: объект-цель атакующего
        :return: нанесенный цели урон
        """
        armor_target = round(target.armor.defence * target.unit_class.armor, 1) if target._check_using_armor() else 0
        damage = round(self.weapon.damage * self.unit_class.attack, 1) - armor_target

        self.stamina -= self.weapon.stamina_per_hit
        target.stamina -= target.armor.stamina_per_turn if target._check_using_armor() else 0

        target.get_damage(damage)
        return round(damage, 1)

    def get_damage(self, damage: float) -> None:
        if damage > 0:
            self.hp -= damage if self.hp >= damage else self.hp

    def hit(self, target: BaseUnit) -> str:

        if self._check_using_weapon():
            damage = self._count_damage(target)

            if damage > 0:
                return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} соперника и " \
                       f"наносит {damage} урона."
            return f"{self.name}, используя {self.weapon.name}, наносит удар {target.name}, " \
                   f"но {target.armor.name} cоперника его останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def use_skill(self, target: BaseUnit) -> str:
        """
        Использовать умение
        """
        if self._is_skill_used:
            return 'Умение уже использовано'
        self._is_skill_used = True
        return self.unit_class.skill.use(self, target)


    def add_stamina(self, const_regeneration: int) -> None:
        """
        Регенерация выносливости
        :param const_regeneration: базовое восстановление выносливости за ход
        """
        stamina_regeneration = const_regeneration * self.unit_class.stamina

        if self.stamina_points + stamina_regeneration > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_regeneration


class PlayerUnit(BaseUnit):
    pass


class EnemyUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        """
        Наносит удар или применяет умение с вероятностью 10%
        """
        if not self._is_skill_used and 10 == randint(1, 10):
            return self.use_skill(target)
        super().hit(target)
