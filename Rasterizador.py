from numpy import array, cross
from numpy.linalg import norm
from pygame import init
from pygame.draw import polygon
from pygame.display import set_mode, flip
from math import sqrt
    
def devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo):
    anguloIncidencia = n @ d # n * d * cos(n^d)

    if abs(anguloIncidencia) < 1e-6:
        raise RuntimeError("error: el rayo es paralelo al plano")

    dPlanoRayo = ptoRayo - ptoPlano
    
    return -n @ dPlanoRayo / anguloIncidencia * d + ptoPlano + dPlanoRayo

def main():
    x, y, z, ptosInterseccion, dFocal = array((1,0,0)), array((0,1,0)),\
                                        array((0,0,1)), [], 1 #1m (1000mm), 0.1 #1dm (10cm, 100mm), 0.05 #5cm (50 mm)
    ptosTri = (x, y, z)    
    n, ptoRayo = z, 3/2 * z 

    ptoPlano = ptoRayo - array((0, 0, dFocal))

    # saca la normal del plano del triangulo a partir de dos vectores entre puntos
    dTri_12, dTri_23 = x - y, z - x
    nTri = abs(cross(dTri_12, dTri_23))   

    for ptoTri in ptosTri:        
        d = ptoTri - ptoRayo

        x, y, z = devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo) # conversion a enteros
        ptosInterseccion.append((x,y,z)) # conversion a array de enteros
            
    init()
     
    NEGRO, BLANCO, AZUL, VERDE, ROJO, pantalla, ptosPantalla, escala, \
           distanciasPtos = (0, 0, 0), (255, 255, 255), (0, 0, 255),\
                            (0, 255, 0), (255, 0, 0),\
                            set_mode((300, 300)), [], 100, []  # tupla no mutable
   
    for ptoInterseccion in ptosInterseccion: #ptoPantalla != ptoInterseccion
        x, y, z = ptoInterseccion
        ptosPantalla.append((escala * (x + 1), -escala * (y - 2)))
        
        distanciasPtos.append(norm(ptoInterseccion - ptoRayo))

    print("nTri =",                 nTri,
          ", \nptoRayo =",          ptoRayo,
          ", \nptoPlano =",         ptoPlano,
          ", \nptosInterseccion =", ptosInterseccion,
          ", \nptosPantalla =",     ptosPantalla,
          ", \ndistanciasPtos =",   distanciasPtos)

    sinRelleno = 0 # < 0 nada, 0 relleno, > 0 wireframe 
    
    polygon(pantalla, BLANCO, ptosPantalla, sinRelleno) 

    flip()

main()

# TODO:
    # da la vuelta al eje Y
    # no hay profundidad
    # añade shader plano dep anguloIncidencia cos?
