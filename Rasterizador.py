from numpy          import array, cross
from numpy.linalg   import norm
from pygame         import init
from pygame.draw    import polygon, line
from pygame.display import set_mode, update
from time           import sleep
from math           import sin, cos, radians
    
def devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo):
    pEscalarN_Y_D = n @ d # pEscalar = cos 90º = 0 (vectores perps, no hace falta norm)
    
    if abs(pEscalarN_Y_D) < 1e-6:
        raise Exception("error: el rayo es perpendicular al plano")
    
    dPlanoRayo = ptoRayo - ptoPlano
    
    return -n @ dPlanoRayo / pEscalarN_Y_D * d + ptoPlano + dPlanoRayo

def normaliza(u, v):
    return (u - v) / norm(u - v)

def cosAnguloEntreVectores(u, v):
    return u @ v / norm(u - v)

anguloG = 0
def devuelveD_Sol():
    global anguloG

    anguloR = radians(anguloG)

    d = (-cos(anguloR), -sin(anguloR), 0)

    if anguloG < 180:
        anguloG += 1

    return d

def sombreaPlano(): # sombreador cara # la posicion unicamente no afecta a la luz. solo la dRotacion
    dLuz = devuelveD_Sol() # dLuz = (ptoLuz-y) / norm(ptoLuz-y) # si estuviera orbitando y mirando a camara 

    dxLuz, dyLuz, dzLuz = dLuz
    xLinea = 150
    line(pantalla, BLANCO, (xLinea, 0), (xLinea * (dxLuz + 1), -xLinea * dyLuz), 1) 

    pEscalarN_Tri_Y_D_Luz = cosAnguloEntreVectores(nTri, dLuz) # pEscalarN_Tri_Y_D_Luz = abs(nTri @ dLuz / norm(nTri - dLuz)) # y = 1er ptoTri # -1 < pEscalarN_Tri_Y_D_Luz < 1 # cos 180º = -1 # backface culling
    # si positivo no esta mirando a camara (no render). si negativo esta mirando (render)

    if pEscalarN_Tri_Y_D_Luz < 0:
        pEscalarN_Tri_Y_D_Luz = 0

    elif pEscalarN_Tri_Y_D_Luz > 1:
        pEscalarN_Tri_Y_D_Luz = 1

    cTri = BLANCO
    colorTriAtenuado = cTri * pEscalarN_Tri_Y_D_Luz # gris

    print(40 * "#",
          "\n\nTri {nTri =", nTri, ", ptosTri =", ptosTri,
          
          "},\n\nRayo {ptoRayo =", ptoRayo, ", d =", d,
                    
          "},\n\nPlano {ptoPlano =", ptoPlano, ", n =", n,
          "},\n", 

          "\nInterseccion {ptosInterseccion =", ptosInterseccion,
          "},\n", 

          "\nPantalla {ptosPantalla =", ptosPantalla,
          "},\n", 

          "\nDistancia {distanciasPtos =", distanciasPtos,

          "},\n\nLuz {ptoLuz =", ptoLuz, ", dLuz =", dLuz, ", anguloG =", anguloG,
          
          "},\n\nSombreador {pEscalarN_Tri_Y_D_Luz =", pEscalarN_Tri_Y_D_Luz,
          ", cTri =", cTri, ", colorTriAtenuado =", colorTriAtenuado,
          "}\n")
   
    polygon(pantalla, colorTriAtenuado, ptosPantalla, noTieneRelleno)
    
#def main():
x, y, z, dFocal = array((1, 0, 0)), array((0.0, 1.0, 0.0)),\
                                    array((0, 0, 1)), 1 #1u = 1m (1000mm), 0.1 #1dm (10cm, 100mm), 0.05 #5cm (50 mm)

ptosInterseccion, distanciasPtos = [], [] # ptosInterseccion = distanciasPtos = []

ptoLuz, dLuz = 10 * y, -y # cenital hacia abajo
ptosTri = (x, y, z)    
n, ptoRayo = z, 3/2 * z 
ptoPlano = ptoRayo - array((0, 0, dFocal))

# saca la normal del plano del triangulo a partir de dos vectores entre puntos
dTri_12, dTri_23 = x - y, z - x
nTri = cross(dTri_12, dTri_23) # regla mano derecha # abs

for ptoTri in ptosTri:        
    d = normaliza(ptoTri, ptoRayo)  
    xI, yI, zI = devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo) # conversion a enteros

    distanciasPtos.append(norm(ptoTri - ptoRayo)) # ptoInterseccion - ptoRayo)) # zdepth desde pRayo o desde pInterseccion?
    ptosInterseccion.append((xI, yI, zI)) # conversion a array de enteros
        
init()
 
NEGRO, BLANCO, AZUL, VERDE, ROJO, pantalla, ptosPantalla, escala =\
       array((0.0, 0.0, 0.0)), array((255.0, 255.0, 255.0)),      \
       array((0.0, 0.0, 255.0)), array((0.0, 255.0, 0.0)),        \
       array((255.0, 0.0, 0.0)), set_mode((300, 300)), [], 100  # tuplas no mutables

for ptoInterseccion in ptosInterseccion: #ptoPantalla != ptoInterseccion
    xI, yI, zI = ptoInterseccion
    ptosPantalla.append((escala * (xI + 1), -escala * (yI - 2)))
    
# aqui para sombreador vertices / aristas?

noTieneRelleno = 0 # < 0 nada, = 0 relleno, > 0 wireframe

for x in range(200):
    pantalla.fill(NEGRO)

    ptoLuz += array((0.1, 0, 0))

    sombreaPlano()
    update()
    sleep(0.01) # 1/100 hz = 100 fps

#main()
