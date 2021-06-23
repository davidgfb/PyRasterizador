from pygame         import init
from pygame.display import set_mode, update
from pygame.draw    import aaline
from numpy          import array
from math           import sin, cos, radians
from time           import sleep

PANTALLA, NEGRO, BLANCO, xOrigenLinea, nFotogramas, sentido, refresca,\
          anguloG = set_mode((300, 300)), array((0, 0, 0)),\
          255 * array((1, 1, 1)), 150, 400, 0, True, 0 #False # 0 antihorario, 1 horario

def gira(): # en un solo eje o plano (z = 0)
    '''devuelve d normalizada'''
    global anguloG

    anguloR = radians(anguloG)

    if sentido == 0:
        d = (cos(anguloR), -sin(anguloR), 0) # sentido antihorario

    elif sentido == 1:
        d = (cos(anguloR), sin(anguloR), 0) # sentido horario

    if anguloG < 360:
        anguloG += 1

    return d

init()

for nFotograma in range(nFotogramas):
    d = gira()
    dx, dy, dz = d

    pto = xOrigenLinea * array(((dx + 1), (dy + 1)))
    ptoX, ptoY = pto
    ptoLinea = (ptoX, ptoY)
    
    if refresca:
        PANTALLA.fill(NEGRO)
        
    aaline(PANTALLA, BLANCO, (xOrigenLinea, xOrigenLinea), ptoLinea, 1) 
    update()

    sleep(1 / 60)

    #print("d =", d, ", anguloG =", anguloG)



