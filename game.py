from player import RandomPlayer


class Game:
    def __init__(self, cc_score=3, cd_score=5, dc_score=0, dd_score=1, game_count=10):
        self._players = {}
        self.cc_score = cc_score
        self.cd_score = cd_score
        self.dc_score = dc_score
        self.dd_score = dd_score
        self.game_count = game_count

        self._score_board = {}

    def return_score_board(self):
        return self._score_board

    def add_player(self, Player):
        self._players[Player.name] = Player

    def sort_by_score(self):
        self._score_board = sorted(
            self._players.items(), key=lambda x: x[1].score, reverse=True
        )

    def play_game(self, Player1, Player2):
        res1 = Player1.play()
        res2 = Player2.play()

        Player1.after_play(res1, res2)
        Player2.after_play(res2, res1)
        # win win
        if res1 is True and res2 is True:
            Player1.add_score(self.cc_score)
            Player2.add_score(self.cc_score)
        # p1 lose
        elif res1 is True and res2 is False:
            Player1.add_score(self.dc_score)
            Player2.add_score(self.cd_score)
        # p2 lose
        elif res1 is False and res2 is True:
            Player1.add_score(self.cd_score)
            Player2.add_score(self.dc_score)
        # lose lose
        else:
            Player1.add_score(self.dd_score)
            Player2.add_score(self.dd_score)

    # 참가자들끼리 차례로 붙어 전체 점수 측정
    def run1(self):
        players = list(self._players.values())
        for i in range(len(players)):
            p1 = players[i]
            for j in range(i, len(players)):
                p2 = players[j]
                if p1.uuid == p2.uuid:
                    continue
                for _ in range(self.game_count):
                    self.play_game(p1, p2)
                p1.before_play()
                p2.before_play()
        self.sort_by_score()

    # 참가자들끼리 game 후 미러전 game + 랜덤봇과 game
    def run2(self):
        players = list(self._players.values())
        for i in range(len(players)):
            p1 = players[i]
            for j in range(i, len(players)):
                p2 = players[j]
                if p1.uuid == p2.uuid:
                    continue
                for _ in range(self.game_count):
                    self.play_game(p1, p2)
                p1.before_play()
                p2.before_play()

        for p in self._players.values():
            m = p.init_for_mirror()
            r = RandomPlayer()

            for _ in range(self.game_count):
                self.play_game(p, r)
            p.before_play()

            for _ in range(self.game_count):
                self.play_game(p, m)
            p.before_play()
            del r, m

        self.sort_by_score()
