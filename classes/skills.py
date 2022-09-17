from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # что выполняет это условие? Проверка типов
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user: Optional[BaseUnit]
    target: Optional[BaseUnit]

    @property
    @abstractmethod
    def name(self):
        raise NotImplemented

    @property
    @abstractmethod
    def stamina(self):  # требуемая выносливость
        raise NotImplemented

    @property
    @abstractmethod
    def damage(self):  # наносимый урон
        raise NotImplemented

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} применил умение {self.name} и нанес {self.target.name} {self.damage} урона"

    def _is_stamina_enough(self) -> bool:
        """
        True если выносливость атакующего больше требуемой выносливости для применения умения
        """
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости."


class FuryPunch(Skill):
    name = 'Свирепый пинок'
    stamina = 6
    damage = 12


class HardShot(Skill):
    name = 'Мощный укол'
    stamina = 5
    damage = 15

