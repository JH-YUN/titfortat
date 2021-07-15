import uuid
import random


class Player:
    count = 0

    def __init__(self, name=None):
        self.score = 0
        self.uuid = uuid.uuid4()
        if name is None:
            self.name = self.__class__.__name__ + "-" + str(self.__class__.count)
            self.__class__.count += 1

    def add_score(self, score):
        self.score += score

    @classmethod
    def get_count(cls):
        return cls.count

    @classmethod
    # 미러전을 위한 임시 클래스 추가
    def init_for_mirror(cls):
        return cls()


# 팃포탯
# 선제 협력
# 상대방이 협력할 경우 협력, 배신할 경우 배신
class TitForTat(Player):
    def __init__(self, name=None):
        super().__init__()
        self.before_play()

    def before_play(self):
        self._prev_game = None

    def play(self):
        if self._prev_game or self._prev_game is None:
            return True
        else:
            return False

    def after_play(self, my_result, opponent_result):
        self._prev_game = opponent_result


# 팃2포탯
# 선제 협력
# 상대방의 한번의 배신은 용서 두번 연속 배신할 경우 배신
class TitFor2Tat(Player):
    def __init__(self, name=None):
        super().__init__()
        self.before_play()

    def before_play(self):
        self._prev_game = None
        self._prev_prev_game = None

    def play(self):
        if self._prev_game is None or self._prev_prev_game:
            return True
        elif self._prev_game is False and self._prev_prev_game is False:
            return False
        else:
            return True

    def after_play(self, my_result, opponent_result):
        self._prev_prev_game = self._prev_game
        self._prev_game = opponent_result


# 무관용
# 선제 협력
# 상대가 협력할 경우 협력
# 상대가 한번이라도 배신할 경우 무조건 배신
class FriedMan(Player):
    def __init__(self, name=None):
        super().__init__()
        self.before_play()

    def before_play(self):
        self.flag = True

    def play(self):
        return self.flag

    def after_play(self, my_result, opponent_result):
        if opponent_result is False:
            self.flag = False


# 확률배반 팃포탯
# n%의 랜덤확률로 배신
# n%가 아닐 경우 팃포탯을 따름
class Joss(Player):
    def __init__(self, name=None, probability=10):
        super().__init__()
        self.before_play()
        self._probability = probability

    def before_play(self):
        self._prev_game = None

    def play(self):
        if random.choices(
            [True, False], weights=[self._probability, 100 - self._probability]
        )[0]:
            return False
        elif self._prev_game or self._prev_game is None:
            return True
        else:
            return False

    def after_play(self, my_result, opponent_result):
        self._prev_game = opponent_result


# 무조건 협력
class AllC(Player):
    def __init__(self, name=None):
        super().__init__()

    def before_play(self):
        pass

    def play(self):
        return True

    def after_play(self, my_result, opponent_result):
        pass


# 무조건 배신
class AllD(Player):
    def __init__(self, name=None):
        super().__init__()

    def before_play(self):
        pass

    def play(self):
        return False

    def after_play(self, my_result, opponent_result):
        pass


# 탐정
# 첫 4게임을 협력-배신-협력-배신 고정
# 첫 4게임중 배신이 감지될 경우 팃포탯처럼 행동
# 첫 4게임중 배신이 감지되지 않을 경우 AllD 처럼 행동
class Detective(Player):
    def __init__(self, name=None):
        super().__init__()
        self.before_play()

    def before_play(self):
        self.game_count = 0
        self.d_flag = True
        self.first_four_games = [True, False, True, False]
        self.prev_game = None

    def play(self):
        if self.game_count < 4:
            return self.first_four_games[self.game_count]
        else:
            if self.d_flag:
                return False
            else:
                return self.prev_game

    def after_play(self, my_result, opponent_result):
        self.prev_game = opponent_result
        if self.game_count < 4:
            if opponent_result is False:
                self.d_flag = False


# 파블로프
# 선제 협력
# 상대방이 협력할 경우 본인 마지막 수 그대로
# 상대방이 배신할 경우 본인 마지막 수 반대로
class Pavlov(Player):
    def __init__(self, name=None):
        super().__init__()
        self.before_play()
        
    def before_play(self):
        self.prev_game = None
        self.prev_my_result = None

    def play(self):
        if self.prev_game is None:
            return True
        elif self.prev_game:
            return self.prev_my_result
        else:
            return not self.prev_my_result

    def after_play(self, my_result, opponent_result):
        self.prev_game = opponent_result
        self.prev_my_result = my_result


# 무작위
class RandomPlayer(Player):
    def __init__(self, name=None):
        super().__init__()

    def before_play(self):
        pass

    def play(self):
        return random.choices([True, False], weights=[50, 50])[0]

    def after_play(self, my_result, opponent_result):
        pass
