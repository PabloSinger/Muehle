import Stein
type position = tuple[int, int, int]

class Spielfeld:
    felder: list[list[list[bool|None]]]
    # steine: list[Stein.Stein]
    def __init__(self) -> None:
        self.reset()

    def is_on_field(self, pos: position) -> bool:
        return all(i in range(3) for i in pos) or not (pos[1] == pos[2] == 1)


    def check_move(self, start: position, ziel: position, spielphase: int) -> bool:
        assert spielphase in range(3)   # Spielphasen: 0=Setzphase, 1=Zugphase, 2=Endphase
        if self.felder[ziel[0]][ziel[1]][ziel[2]] != None:
                return False        # Es darf nicht bereits ein Stein auf dem Zielfeld liegen.
        if spielphase == 1:
            if start[0] != ziel[0]:
                if (start[1] + start[2]) % 2 != 1 or abs(start[0]-ziel[0]) != 1 or start[1] != ziel[1] or start[2] != ziel[2]:
                    return False
            else:
                diff = 0
                for i in range(2):
                    diff += abs(start[i+1]-ziel[i+1])
                if diff != 1: return False  # in der Zugphase muss genau ein Feld weiter gerückt werden.
        return True

    def reset(self) -> None:
        self.felder = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def check_for_piece(self, pos: position) -> bool|None: # None=nix, False=weiß, True=schwarz
        return self.felder[pos[0]][pos[1]][pos[2]]

    def move_piece(self, start: position, ziel: position, spielphase: int) -> None:
        if spielphase == 0:
            self.felder[ziel[0]][ziel[1]][ziel[2]] = bool(start[0])
        else:
            self.felder[ziel[0]][ziel[1]][ziel[2]] = self.felder[start[0]][start[1]][start[2]]
            self.felder[start[0]][start[1]][start[2]] = None

    def get_piece_count(self, spieler: bool) -> int:
        count = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if (not (j == k == 1)) and self.felder[i][j][k] is spieler:
                        count += 1
        return count
