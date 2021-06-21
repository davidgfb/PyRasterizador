from numpy import array
from pygame import init
from pygame.draw import polygon
from pygame.display import set_mode, flip
    
def ptoInterseccion(n, ptoPlano, d, ptoRayo):
    anguloIncidencia = n @ d

    if abs(anguloIncidencia) < 1e-6:
        raise RuntimeError("error: el rayo es paralelo al plano")

    direccionPlanoRayo = ptoRayo - ptoPlano
    
    return -n @ direccionPlanoRayo / anguloIncidencia * d + ptoPlano + direccionPlanoRayo

def main():
    ptosTri, z, ptosInterseccion = [[0,1,0],
                                      [1,0,0],
                                      [0,0,1]],\
                                     array([0, 0, 1]), [] 
    
    n, ptoPlano, ptoRayo,  = z, -5 * z, 10 * z

    for ptoTri in ptosTri:
        rayDirection = ptoTri - ptoRayo
        x,y,z = ptoInterseccion(n, ptoPlano, rayDirection, ptoRayo) # conversion a enteros

        ptosInterseccion.append([x,y,z]) # conversion a array de enteros
    
    init()
     
    NEGRO, BLANCO, AZUL, VERDE, ROJO, pantalla, ptosPantalla, escala = (0, 0, 0),\
                                       (255, 255, 255), (0, 0, 255),\
                                       (0, 255, 0), (255, 0, 0),\
                                        set_mode((300, 300)), [], 100  # tupla no mutable

    distanciasPtos = []

    from math import sqrt
    
    for pto in ptosInterseccion:
        x,y,z=pto
        #ptosPantalla.append([escala * (x + 1), -escala * (y - 2)])
        ptosPantalla.append([escala * (x + 1), -escala * (y - 2)])

        xR, yR, zR = ptoRayo
        dx = x-xR
        dy = y-yR
        dz = z-zR
        
        distanciasPtos.append(sqrt(dx ** 2 + dy ** 2 + dz ** 2))

    print("ptosInterseccion =", ptosInterseccion,
          ", \nptosPantalla =", ptosPantalla,
          ", \ndistanciasPtos =", distanciasPtos)
    
    polygon(pantalla, BLANCO, ptosPantalla, 0)

    flip()

main()

# TODO:
    # da la vuelta al eje Y
    # no hay profundidad
    # añade shader plano dep anguloIncidencia cos?
