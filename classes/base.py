from typing import Optional

from classes.unit import EnemyUnit, PlayerUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: PlayerUnit = None
    enemy: EnemyUnit = None
    game_is_running = False
    battle_result: str = None

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        if self.player.hp == 0 < self.enemy.hp:
            self.battle_result = 'Вы проиграли'
        elif self.enemy.hp == 0 < self.player.hp:
            self.battle_result = 'Вы выиграли'
        elif self.player.hp == 0 == self.enemy.hp:
            self.battle_result = 'Ничья'
        return self.battle_result

    def _stamina_regeneration(self) -> None:
        self.player.add_stamina(self.STAMINA_PER_ROUND)
        self.enemy.add_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self) -> str:
        result = self._check_players_hp()

        if result is not None:
            return result

        self._stamina_regeneration()
        self.enemy.hit(self.player)
        return f'{self.player.name} пропустил ход'

    def player_hit(self) -> str:
        result = self._check_players_hp()

        if result is not None:
            return result

        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self) -> str:
        result = self._check_players_hp()

        if result is not None:
            return result

        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result

    def _end_game(self) -> None:
        self._instances = {}
        self.game_is_running = False
