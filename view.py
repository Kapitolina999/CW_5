from typing import Dict

from flask import Flask, render_template, request, redirect

from classes.base import Arena
from classes.classes import unit_classes
from classes.equipment import Equipment
from classes.unit import PlayerUnit, EnemyUnit, BaseUnit

app = Flask(__name__)


heroes: Dict[str, BaseUnit] = {}

arena = Arena()
equipment = Equipment()


@app.route('/')
def menu_page():
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        header = 'Выбор вашего героя'
        classes = unit_classes
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        return render_template('hero_choosing.html', result={
            'header': header,
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        })

    if request.method == 'POST':
        name = request.form['name']
        unit = request.form['unit_class']
        weapon = equipment.get_weapon(request.form['weapon'])
        armor = equipment.get_armor(request.form['armor'])
        new_player = PlayerUnit(name, unit_classes[unit])
        new_player.equip_armor(armor)
        new_player.equip_weapon(weapon)
        heroes['player'] = new_player
        return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    if request.method == 'GET':
        header = 'Выбор героя компьютера'
        classes = unit_classes
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        return render_template('hero_choosing.html', result={
            'header': header,
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        })

    if request.method == 'POST':
        name = request.form['name']
        unit = request.form['unit_class']
        weapon = equipment.get_weapon(request.form['weapon'])
        armor = equipment.get_armor(request.form['armor'])
        new_player = EnemyUnit(name, unit_classes[unit])
        new_player.equip_armor(armor)
        new_player.equip_weapon(weapon)
        heroes['enemy'] = new_player
        return redirect('/fight/')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes, result='Начало боя')


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/end-fight/')
def end_fight():
    """
    Конец игры, и переход на кнопку начала игры
    """
    arena._end_game()
    return redirect('/')
