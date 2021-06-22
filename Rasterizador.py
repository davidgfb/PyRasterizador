from numpy import array, cross
from numpy.linalg import norm
from pygame import init
from pygame.draw import polygon
from pygame.display import set_mode, update
from math import sqrt, sin, acos, degrees
from time import sleep
    
def devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo):
    anguloIncidencia = n @ d # n * d * cos(n^d)

    if abs(anguloIncidencia) < 1e-6:
        raise RuntimeError("error: el rayo es paralelo al plano")

    dPlanoRayo = ptoRayo - ptoPlano
    
    return -n @ dPlanoRayo / anguloIncidencia * d + ptoPlano + dPlanoRayo

def sombreaPlano():
    # sombreador plano cara
    moduloN_Tri, moduloD_Luz = nTri / norm(y), dLuz / norm(ptoLuz)

    pEscalar = moduloN_Tri @ moduloD_Luz

    anguloIncidenciaLuz = degrees(acos(pEscalar))

    pColor = sin(anguloIncidenciaLuz)

    if pColor < 0:
        pColor = 0

    colorTri = BLANCO * pColor # gris

    print(40 * "#",
          "\n\nnTri =",                  nTri,
          ", \nptoRayo =",             ptoRayo,
          ", \nptoPlano =",            ptoPlano,
          "\n", 40 * "-",
          "\nptosInterseccion =",      ptosInterseccion,
          "\n", 40 * "-",
          "\nptosPantalla =",          ptosPantalla,
          "\n", 40 * "-",
          "\ndistanciasPtos =",        distanciasPtos,
          "\nmoduloN_Tri =",           moduloN_Tri,
          ", \nmoduloD_Luz =",         moduloD_Luz,
          ", \npEscalar =",            pEscalar,
          ", \nanguloIncidenciaLuz =", anguloIncidenciaLuz,
          ", \npColor =",              pColor,
          ", \ncolorTri =",            colorTri,
          "\n")
   
    polygon(pantalla, colorTri, ptosPantalla, noTieneRelleno)
    
#def main():
x, y, z, ptosInterseccion, dFocal = array((1,0,0)), array((0,1,0)),\
                                    array((0,0,1)), [], 1 #1u = 1m (1000mm), 0.1 #1dm (10cm, 100mm), 0.05 #5cm (50 mm)

ptoLuz, dLuz = 10 * y, -y # cenital hacia abajo
ptosTri = (x, y, z)    
n, ptoRayo = z, 3/2 * z 

ptoPlano = ptoRayo - array((0, 0, dFocal))

# saca la normal del plano del triangulo a partir de dos vectores entre puntos
dTri_12, dTri_23 = x - y, z - x
nTri = abs(cross(dTri_12, dTri_23)) # regla mano derecha 

for ptoTri in ptosTri:        
    d = ptoTri - ptoRayo

    xI, yI, zI = devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo) # conversion a enteros
    ptosInterseccion.append((xI,yI,zI)) # conversion a array de enteros
        
init()
 
NEGRO, BLANCO, AZUL, VERDE, ROJO, pantalla, ptosPantalla, escala, \
       distanciasPtos = (0, 0, 0), array((255, 255, 255)), (0, 0, 255),\
                        (0, 255, 0), (255, 0, 0),\
                        set_mode((300, 300)), [], 100, []  # tupla no mutable

for ptoInterseccion in ptosInterseccion: #ptoPantalla != ptoInterseccion
    xI, yI, zI = ptoInterseccion
    ptosPantalla.append((escala * (xI + 1), -escala * (yI - 2)))
    
    distanciasPtos.append(norm(ptoInterseccion - ptoRayo))

    # aqui para sombreador plano vertices (arista?) 

noTieneRelleno = 0 # < 0 nada, = 0 relleno, > 0 wireframe

for x in range(20):
    pantalla.fill(NEGRO)

    ptoLuz += array((1, 0, 0))
    
    sombreaPlano()
    update()
    sleep(1)

#main()

# TODO:
    # da la vuelta al eje Y
    # no hay profundidad
    # añade shader plano dep anguloIncidencia cos?
