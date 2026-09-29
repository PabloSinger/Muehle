




def draw( spielfeld):
  x = None
  y = None

  feld =   [[" " for _ in range(7)] for _ in range(7)] 
  for i in range(3):
            for j in range(3):
                for k in range(3):
                  
                    if j == 0:
                         x = i
                    elif j == 1:
                          x = 3
                    if j == 2:
                         x = 6-i
                      
                    if k == 0:
                         y = 6-i
                    elif k == 1:
                          y = 3
                    if k == 2:
                         y = i
                    if spielfeld[i][j][k] is not None:
                      feld[y][x] = int(spielfeld[i][j][k])
                    
     
  for f in feld:
       print(f)
    
        
