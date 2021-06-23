from numpy          import array, cross
from numpy.linalg   import norm
from pygame         import init
from pygame.draw    import polygon, aaline, circle
from pygame.display import set_mode, update
from time           import sleep
from math           import sin, cos, radians
from time           import time

seMueveLuz = False #True
estaDepurado = False

CERO, Z, Y, X, UNITARIO, dFocal = array((0, 0, 0)), array((0, 0, 1)),\
                                  array((0, 1, 0)), array((1, 0, 0)),\
                                  array((1, 1, 1)), 1

NEGRO, ROJO, VERDE, AZUL, BLANCO, PANTALLA, escala =\
       CERO, 255 * X, 255 * Y, 255 * Z, 255 * UNITARIO, set_mode((300, 300)), 100

ptosInterseccion, distanciasPtos, ptosPantalla = [], [], [] 

ptoLuz, dLuz = 10 * Y, -Y # cenital hacia abajo
ptosTri = (X, Y, Z)    
n, ptoRayo = Z, 3/2 * Z 
ptoPlano = ptoRayo - array((0, 0, dFocal))

# saca la normal del plano del triangulo a partir de dos vectores entre puntos
dTri_12, dTri_23 = X - Y, Z - X
nTri = cross(dTri_12, dTri_23) # regla mano derecha # abs
  
def devuelveInterseccionPlanoRayo(n, d, ptoPlano, ptoRayo):
    '''n y d deben estar normalizados'''
    pEscalarN_Y_D = n @ d 
    
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

def sombreaPlano(): # sombreador cara # la posicion por si sola no afecta a la luz. solo la dRotacion
    global dLuz

    if seMueveLuz:
        dLuz = devuelveD_Sol() # dLuz = normaliza(ptoLuz, y) si estuviera orbitando alrededor y mirando a camara 

    dxLuz, dyLuz, dzLuz = dLuz
    xOrigenLinea = 150 # y largo linea
    ptoLinea = (xOrigenLinea * (dxLuz + 1), -xOrigenLinea * dyLuz)
    aaline(PANTALLA, BLANCO, (xOrigenLinea, 0), ptoLinea, 1) 
    circle(PANTALLA, BLANCO, ptoLinea, 5) 

    pEscalarN_Tri_Y_D_Luz = cosAnguloEntreVectores(nTri, dLuz) # pEscalarN_Tri_Y_D_Luz = abs(nTri @ dLuz / norm(nTri - dLuz)) # y = 1er ptoTri # -1 < pEscalarN_Tri_Y_D_Luz < 1 # cos 180º = -1 # backface culling
    # si positivo no esta mirando a camara (no render). si negativo esta mirando (render)

    if pEscalarN_Tri_Y_D_Luz < 0:
        pEscalarN_Tri_Y_D_Luz = 0

    elif pEscalarN_Tri_Y_D_Luz > 1:
        pEscalarN_Tri_Y_D_Luz = 1

    cTri = VERDE
    colorTriAtenuado = cTri * pEscalarN_Tri_Y_D_Luz # gris

    if estaDepurado: # afecta grav rendimiento
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
        
    polygon(PANTALLA, colorTriAtenuado, ptosPantalla, noTieneRelleno)

# main
for ptoTri in ptosTri:    #ptos o ptosEscena    
    d = normaliza(ptoTri, ptoRayo)  
    xI, yI, zI = devuelveInterseccionPlanoRayo(n, d, ptoPlano, ptoRayo) # conversion a enteros

    distanciasPtos.append(norm(ptoTri - ptoRayo)) # ptoInterseccion - ptoRayo)) # zdepth desde pRayo o desde pInterseccion?
    ptosInterseccion.append((xI, yI, zI)) # conversion a array de enteros
        
for ptoInterseccion in ptosInterseccion: 
    xI, yI, zI = ptoInterseccion
    ptosPantalla.append((escala * (xI + 1), -escala * (yI - 2)))
    
# aqui para sombreador vertices / aristas?

noTieneRelleno = 0 # < 0 nada, = 0 relleno, > 0 wireframe

t = time()
fps = 60

init()

nFotogramas = 200
for nFotograma in range(nFotogramas):
    PANTALLA.fill(NEGRO)

    #ptoLuz += array((0.1, 0, 0)) # para mover la camara en sentido positivo del eje X

    sombreaPlano()
    update()

    sleep(1 / fps) 
  
dt = time() - t
print("\nhan pasado", round(dt, 2), "segundos para", nFotogramas, "fotogramas\n",\
      round(nFotogramas / dt, 2), "fotogramas por segundo") #round(dt / nFotogramas, 2), "segundos por fotograma")

