type position = tuple[int, int, int]


class Spielfeld:
    felder: list[list[list[bool|None]]]
    # steine: list[Stein.Stein]
    def __init__(self) -> None:
        self.reset()


    def __iter__(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if not (j == k == 1):
                        yield self.felder[i][j][k], (i,j,k)

    def field_exists(self, pos: position) -> bool:
        return all(i in range(3) for i in pos) and not (pos[1] == pos[2] == 1)


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

    def get_field_state(self, pos: position) -> bool|None: # None=nix, False=weiß, True=schwarz
        return self.felder[pos[0]][pos[1]][pos[2]]

    def move_piece(self, start: position, ziel: position, spielphase: int) -> None:
        if spielphase == 0:
            self.felder[ziel[0]][ziel[1]][ziel[2]] = bool(start[0])
        else:
            self.felder[ziel[0]][ziel[1]][ziel[2]] = self.felder[start[0]][start[1]][start[2]]
            self.felder[start[0]][start[1]][start[2]] = None

    def get_piece_count(self, spieler: bool) -> int:
        return len([feld == spieler for feld,coord in self])

    def remove_piece(self, pos: position) -> None:
        self.felder[pos[0]][pos[1]][pos[2]] = None

    def check_mühle(self,pos: tuple[int,int,int]):

        if (pos[1] + pos[2]) % 2 == 1:
            if all(self.felder[i][pos[1]][pos[2]] == self.felder[pos[0]][pos[1]][pos[2]] for i in range(3)):
                return True
            elif pos[2] == 1 and self.check_col(pos):
                return True
            elif pos[1] == 1 and self.check_row(pos):
                return True

        else:
            if self.check_row(pos) or self.check_col(pos):
                return True
        return False

    def check_row(self, pos: tuple[int,int,int]):
        if all(self.felder[pos[0]][i][pos[2]] == self.felder[pos[0]][pos[1]][pos[2]] for i in range(3)):
            return True
        return False
    def check_col(self, pos: tuple[int,int,int]):
        if all(self.felder[pos[0]][pos[1]][i] == self.felder[pos[0]][pos[1]][pos[2]] for i in range(3)):
                return True
        return False
        
    def is_removable(self,remove_pos):
        remove_state = self.get_field_state(remove_pos)
        if self.check_mühle(remove_pos):
            return all(map(self.check_mühle,  [coord for feld, coord in self if feld == remove_state ] ))
 
        return True

    
