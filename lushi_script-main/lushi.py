import pyautogui
import cv2
import time
from PIL import ImageGrab, Image
import numpy as np

import win32api
from winguiauto import findTopWindow
import win32gui
import win32con


class Icons:
    def __init__(self):
        for k, v in Images.__dict__.items():
            if not k.startswith('_'):
                setattr(self, k, self.fname2img(v))

    @staticmethod
    def fname2img(fname):
        return cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2GRAY)


def find_lushi_window():
    hwnd = findTopWindow("炉石传说")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    rect = win32gui.GetWindowPlacement(hwnd)[-1]
    image = ImageGrab.grab(rect)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    return rect, image


def find_icon_location(lushi, icon):
    result = cv2.matchTemplate(lushi, icon, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    if maxVal > 0.8:
        (startX, startY) = maxLoc
        endX = startX + icon.shape[1]
        endY = startY + icon.shape[0]
        return True, (startX + endX) // 2, (startY + endY) // 2, maxVal
    else:
        return False, None, None, maxVal


class Images:
    yongbing = 'imgs/yongbing.png'
    travel = 'imgs/travel.png'
    air_element = 'imgs/air.png'
    # air_element = 'imgs/birdwoman.png'  # 修改点 我想打鸟人
    team_list = 'imgs/team_list.png'
    team_lock = 'imgs/team_lock.png'

    member_ready = 'imgs/member_ready.png'

    not_ready = 'imgs/not_ready.png'
    skill_select = 'imgs/skill_select.png'
    battle_ready2 = 'imgs/battle_ready2.png'
    surprise2 = 'imgs/surprise2.png'

    surprise = 'imgs/surprise.png'  # 看看哪一个效果好，我也会重新截图
    start_point = 'imgs/start_point.png'
    treasure_list = 'imgs/treasure_list.png'
    treasure_replace = 'imgs/treasure_replace.png'
    visitor_list = 'imgs/visitor_list.png'
    final_reward = 'imgs/final_reward.png'

    final_confirm = 'imgs/final_confirm.png'
    boom = 'imgs/boom.png'
    ice_berg = 'imgs/ice_berg.png'
    hero_name = 'imgs/LichKing.png'
    box = 'imgs/box.png'
    checkteam = 'imgs/checkteam.png'
    confirm2 = 'imgs/confirm2.png'
    giveup = 'imgs/giveup.png'
    boss = 'imgs/boss.png'


class Agent:
    # def __init__(self, skill_list=None, team_id=2):
    #     self.icons = Icons()
    #
    #     if skill_list is None:
    #         self.skill_list = [
    #             (1, -1), (0, 1), (0, 1)
    #         ]
    #     else:
    #         if len(skill_list) == 3 and isinstance(skill_list[0], tuple):
    #             self.skill_list = skill_list
    def __init__(self, team_id, heros_id, skills_id, targets_id):
        self.icons = Icons()
        self.team_id = team_id
        self.heros_id = heros_id
        self.skills_id = skills_id
        self.targets_id = targets_id

        self.hero_relative_locs = [
            (677, 632),
            (807, 641),
            (943, 641)
        ]

        # self.hero_relative_locs = [
        #     (807, 641),
        #     (677, 632),
        #     (943, 641)
        # ]

        self.enemy_mid_location = (850, 285)

        self.skill_relative_locs = [
            (653, 447),
            (801, 453),
            (963, 459),
        ]

        self.treasure_locs = [
            (707, 488), (959, 462), (1204, 474)
        ]
        self.treasure_collect_loc = (968, 765)

        self.visitor_locs = [
            (544, 426), (790, 420), (1042, 416)
        ]
        self.visitor_choose_loc = (791, 688)

        self.members_loc = [
            (620, 878), (690, 880), (774, 879),
            (811, 881), (880, 899), (954, 911)
        ]
        self.drag2loc = (1213, 564)

        self.locs = {
            'left': [(452, 464), (558, 461), (473, 465)],
            'right': [(777, 478), (800, 459), (903, 469)]
        }

        self.finial_reward_locs = [
            (660, 314), (554, 687), (1010, 794), (1117, 405), (806, 525)
        ]

        self.start_game_relative_loc = (1250, 732)

        self.select_travel_relative_loc = (1090, 674)

        self.team_locations = [(374, 324), (604, 330), (837, 324)]
        self.team_loc = self.team_locations[team_id]
        self.start_team_loc = (1190, 797)
        self.start_game_relative_loc = (1250, 732)
        self.start_point = (1114, 956)
        self.checkteam = (1134, 1118)
        self.start_point_relative_loc = (654, 707)

        self.options_loc = (1579, 920)
        self.surrender_loc = (815, 363)

        self.empty_loc = (1518, 921)

    def run(self, start_point_loc=None):
        # surprise_loc = None
        start_point_loc = None
        # start_game_loc = None
        # side = None
        battle_count = 0


        while True:
            time.sleep(.5)  # 修改点 flag
            states, rect = self.check_state()

            if 'box' in states or 'boss' in states:
                print('great')
                if battle_count:
                    pyautogui.click(self.checkteam)
                continue

            pyautogui.moveTo(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
            pyautogui.click()
            # pyautogui.moveTo(rect[0] + self.empty_loc[0], rect[1] + self.empty_loc[1])
            # pyautogui.click()
            # print(states, side, start_point_loc, surprise_loc, battle_count)
            print(states)

            if 'yongbing' in states:
                pyautogui.click(states['yongbing'][0])
                continue

            # if 'start_point' in states:
            #     start_point = states['start_point'][0]
            #     print(start_point)

            if 'travel' in states:
                pyautogui.click(states['travel'][0])
                pyautogui.click(rect[0] + self.select_travel_relative_loc[0],
                                rect[1] + self.select_travel_relative_loc[1])
                continue

            if 'air_element' in states:
                pyautogui.click(states['air_element'][0])
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                continue

            if 'team_list' in states:
                pyautogui.click(rect[0] + self.team_loc[0], rect[1] + self.team_loc[1])
                if 'team_lock' in states:
                    pyautogui.click(states['team_lock'][0])
                pyautogui.click(rect[0] + self.start_team_loc[0], rect[1] + self.start_team_loc[1])
                continue

            # if 'member_ready' in states:
            #     pyautogui.click(states['member_ready'][0])
            #     continue
            if 'member_ready' in states:
                # if 'boom' in states or 'ice_berg' in states:
                #     print("Surrendering")
                #     pyautogui.click(rect[0] + self.options_loc[0], rect[1] + self.options_loc[1])
                #     pyautogui.click(rect[0] + self.surrender_loc[0], rect[1] + self.surrender_loc[1])
                #     continue

                # for idx in self.heros_id:
                #     loc = self.members_loc[idx]
                #     pyautogui.click(rect[0] + loc[0], rect[1] + loc[1])
                #     pyautogui.click(rect[0] + self.drag2loc[0], rect[1] + self.drag2loc[1])

                pyautogui.click(states['member_ready'][0])
                continue

            if 'battle_ready2' in states:
                pyautogui.click(states['battle_ready2'][0])
                battle_count += 1
                continue

            if 'treasure_list' in states or 'treasure_replace' in states:
                treasure_loc_id = np.random.randint(0, 3)
                treasure_loc = self.treasure_locs[treasure_loc_id]
                pyautogui.click(rect[0] + treasure_loc[0], rect[1] + treasure_loc[1])
                pyautogui.click(rect[0] + self.treasure_collect_loc[0], rect[1] + self.treasure_collect_loc[1])
                continue

            if 'visitor_list' in states:
                if 'hero_name' in states:
                    pyautogui.click(states['hero_name'][0])
                    pyautogui.click(rect[0] + self.visitor_choose_loc[0], rect[1] + self.visitor_choose_loc[1])
                else:
                    # visitor_id = np.random.randint(0, 3)
                    visitor_id = np.random.randint(0, 2)  # 修改点 只需要前两个中任意
                    visitor_loc = self.visitor_locs[visitor_id]
                    pyautogui.click(rect[0] + visitor_loc[0], rect[1] + visitor_loc[1])
                    pyautogui.click(rect[0] + self.visitor_choose_loc[0], rect[1] + self.visitor_choose_loc[1])

                continue

            if 'final_reward' in states:
                for rew in self.finial_reward_locs:
                    pyautogui.moveTo(rect[0] + rew[0], rect[1] + rew[1])
                    pyautogui.click()
                continue

            if 'final_confirm' in states:
                pyautogui.click(states['final_confirm'][0])
                continue

            # if 'surprise' in states or 'surprise2' in states:
            #     time.sleep(.5)
            #     if 'surprise' in states:
            #         surprise_loc = states['surprise'][0]
            #     else:
            #         surprise_loc = states['surprise2'][0]
            #     if 'start_point' in states:
            #         pyautogui.click(surprise_loc)
            #     pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
            #
            #     if side is None:
            #         if surprise_loc[0] <= self.start_point_relative_loc[0] + rect[0]:
            if 'start_game' in states:
                pyautogui.click(states['start_game'][0])
                continue

            if 'surprise' in states or 'surprise2' in states:
                if 'surprise' in states:
                    surprise_loc = states['surprise'][0]
                    if 'start_point' not in states:
                        if surprise_loc[0] < self.start_point[0]:
                            side = 'left'
                        else:
                            side = 'right'
                    side_locs = self.locs[side]  # 到continue前左移了一个tab
                    for loc in side_locs:
                        pyautogui.moveTo(loc[0] + rect[0], loc[1] + rect[1])
                        pyautogui.click(clicks=2, interval=0.25)
                else:
                    surprise_loc = states['surprise2'][0]  # 此处else逻辑可能有问题
                    pyautogui.click(surprise_loc)
                #
                # if side is not None:
                # side_locs = self.locs[side]   # 到continue前左移了一个tab
                # for loc in side_locs:
                #     pyautogui.moveTo(loc[0] + rect[0], loc[1] + rect[1])
                #     pyautogui.click(clicks=2, interval=0.25)
                #     pyautogui.click(rect[0] + self.start_game_relative_loc[0],
                #                     rect[1] + self.start_game_relative_loc[1])
                # side = None
                # pyautogui.click(surprise_loc)
                continue

            if 'confirm2' in states:
                confirm2_loc = states['confirm2'][0]
                pyautogui.click(confirm2_loc)
                continue

            if 'giveup' in states:
                giveup_loc = states['giveup'][0]
                pyautogui.click(giveup_loc)
                continue

            if 'skill_select' in states or 'not_ready' in states:
                if 'boom' in states or 'ice_berg' in states:
                    print("Surrendering")
                    pyautogui.click(rect[0] + self.options_loc[0], rect[1] + self.options_loc[1])
                    pyautogui.click(rect[0] + self.surrender_loc[0], rect[1] + self.surrender_loc[1])
                    continue
                pyautogui.click(rect[0] + self.start_game_relative_loc[0], rect[1] + self.start_game_relative_loc[1])
                first_hero_loc = self.hero_relative_locs[0]
                pyautogui.click(rect[0] + first_hero_loc[0], rect[1] + first_hero_loc[1])

            for idx, skill_id, target_id in zip([0, 1, 2], self.skills_id, self.targets_id):
                hero_loc = (rect[0] + self.hero_relative_locs[idx][0], rect[1] + self.hero_relative_locs[idx][1])
                skill_loc = (
                    rect[0] + self.skill_relative_locs[skill_id][0],
                    rect[1] + self.skill_relative_locs[skill_id][1])
                pyautogui.click(*skill_loc)
                # for skill_id, target_id in self.skill_list:
                #     skill_loc = (
                #         rect[0] + self.skill_relative_locs[skill_id][0],
                #         rect[1] + self.skill_relative_locs[skill_id][1])
                #     pyautogui.click(*skill_loc)

                if target_id != -1:
                    enemy_loc = (rect[0] + self.enemy_mid_location[0], rect[1] + self.enemy_mid_location[1])
                    pyautogui.click(*enemy_loc)
                continue

    def check_state(self):
        lushi, image = find_lushi_window()
        output_list = {}
        for k, v in self.icons.__dict__.items():
            if not k.startswith('_'):
                success, click_loc, conf = self.find_icon_and_click_loc(v, lushi, image)
                if success:
                    output_list[k] = (click_loc, conf)
        return output_list, lushi

    def find_icon_and_click_loc(self, icon, lushi, image):
        success, X, Y, conf = find_icon_location(image, icon)
        if success:
            click_loc = (X + lushi[0], Y + lushi[1])
        else:
            click_loc = None
        return success, click_loc, conf


def find_relative_loc():
    pos = pyautogui.position()
    rect, _ = find_lushi_window()
    print((pos[0] - rect[0], pos[1] - rect[1]))


def main():
    pyautogui.PAUSE = 0.35
    if True:
        # pyautogui.confirm(text="请启动炉石，将炉石调至窗口模式，分辨率设为1600x900，画质设为高，语言设为简体中文")
        # pyautogui.confirm(text="程序默认副本为上次战斗的副本，本程序目前只支持H1-2，请将默认副本设为H1-2")
        # pyautogui.confirm(text="程序默认使用队伍为从左到右第三支队伍，且跳过英雄选择阶段，直接按准备就绪，所以请记下默认出场的英雄以及你想使用的技能，从左到右依次记下")
        # heros_id = pyautogui.prompt(text="请输入要选择出场英雄的序号用空格隔开，0为1号位，1为2号位，以此类推。默认为1 4 5")
        # team_id = pyautogui.prompt(text="请输入第一排队伍序号，0为第一支队伍，1为第一支，2为第三支")
        # skills = pyautogui.prompt(text="请输入默认出场英雄技能编号，用空格隔开: 0为第一技能，1为第二技能，2为第三技能, 如 1 1 0 代表第一英雄用第二技能，代表第二英雄用第二技能，代表第三英雄用第一技能")
        # skill_target = pyautogui.prompt(text="请输入已选择的三个技能的属性，用空格隔开: -1无需指定目标，0指定地方中间目标，如 -1 0 0")
        # if len(skills) == 0:
        #     skills = "0 0 0"
        # if len(skill_target) == 0:
        #     skill_target = "1 1 1"
        # if len(team_id) == 0:
        #     team_id = "1"
        # if heros_id == "":
        #     heros_id = "1 4 5"
        skills_id = "1 0 0"
        targets_id = "-1 0 0"
        heros_id = "0 1 2"
        team_id = "0"  # 这里将逻辑写死，不用再调试  修改点 flag

    #     skills = [int(s.strip()) for s in skills.strip().split(' ')]
    #     skill_target = [int(s.strip()) for s in skill_target.strip().split(' ')]
    #     team_id = int(team_id)
    #     assert (len(skills) == 3)
    #     assert (len(skill_target) == 3)
    #     assert (team_id in [0, 1, 2])
    #     skill_list = [(x, y) for x, y in zip(skills, skill_target)]
    # else:
    #     skill_list = None
    heros_id = [int(s.strip()) for s in heros_id.strip().split(' ')]
    skills_id = [int(s.strip()) for s in skills_id.strip().split(' ')]
    targets_id = [int(s.strip()) for s in targets_id.strip().split(' ')]
    team_id = int(team_id)

    assert (len(skills_id) == 3 and len(targets_id) == 3 and len(heros_id) == 3)
    assert (team_id in [0, 1, 2])

    agent = Agent(team_id=team_id, heros_id=heros_id, skills_id=skills_id, targets_id=targets_id)
    agent.run()

    # agent = Agent(skill_list=skill_list, team_id=team_id)
    # agent.run()


if __name__ == '__main__':
    main()
