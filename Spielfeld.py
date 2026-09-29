import Stein


class Spielfeld:
    felder: list[list[list[int]]]
    steine: list[Stein.Stein]

    def reset(self):
        
        for i in range(3):
            for k in range(3):
                for l in range(3):
                    if not l == k == 1:
                        self.felder[i][k][l] = None

    
    def __init__(self) -> None:
        for i in range(2):  # Steine-Liste initialisieren, neun schwarze und neun weiße.
            for _ in range(9):
                self.steine.append(Stein.Stein(farbe=bool(i)))

    def is_on_field(self, pos: tuple[int,int,int]) -> bool:
        if not all([i in range(3) for i in pos]) or pos[1] == pos[2] == 1:
            return False
        else:
            return True
        

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


    def check_mühle(self,pos: tuple[int,int,int]):
        
        if (pos[1] + pos[2]) % 2 == 1:
            if all([self.felder[i,pos[1],pos[2]] == self.felder[pos[0],pos[1],pos[2]] for i in range(3)]):
                 return True
            elif pos[1] == 1 and self.check_col(pos):
                return True
            elif pos[2] == 1 and self.check_row(pos):
                return True
            
        else: 
            if self.check_row(pos) or self.check_col(pos):
                return True
        return False
            
    def check_row(self, pos: tuple[int,int,int]):
        if all(self.felder[pos[0],i,pos[2]] == self.felder[pos[0],pos[1],pos[2]] for i in range(3)):
            return True
        return False
    def check_col(self, pos: tuple[int,int,int]):
        if all([self.felder[pos[0],pos[1],i] == self.felder[pos[0],pos[1],pos[2]] for i in range(3)]):
                return True
        return False


        
        
