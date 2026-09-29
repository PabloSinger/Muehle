import Stein


class Spielfeld:
    felder: list[list[list[int]]]
    steine: list[Stein.Stein]
    def __init__(self) -> None:
        for i in range(2):  # Steine-Liste initialisieren, neun schwarze und neun weiße.
            for _ in range(9):
                self.steine.append(Stein.Stein(farbe=bool(i)))

    def is_on_field(self, pos: tuple([int,int,int]) -> bool:
        if not all([i in range(3) for i in pos]) or pos[1] = pos[2] = 1 :
            return true
        

    def check_move(self, start: tuple[int, int, int], ziel: tuple[int, int, int], spielphase: int) -> bool:
        assert spielphase in range(3)   # Spielphasen: 0=Setzphase, 1=Zugphase, 2=Endphase
        for stein in self.steine:
            if stein.pos == ziel:
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
