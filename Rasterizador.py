from numpy          import array, cross
from numpy.linalg   import norm
from pygame         import init
from pygame.draw    import polygon, aaline, circle
from pygame.display import set_mode, update
from time           import sleep
from math           import sin, cos, radians
from time           import time
  
def devuelveInterseccionPlanoRayo(n, ptoPlano, d, ptoRayo):
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

seMueveLuz = False # True

def sombreaPlano(): # sombreador cara # la posicion unicamente no afecta a la luz. solo la dRotacion
    global dLuz

    if seMueveLuz:
        dLuz = devuelveD_Sol() # dLuz = normaliza(ptoLuz, y) si estuviera orbitando alrededor y mirando a camara 

    dxLuz, dyLuz, dzLuz = dLuz
    xOrigenLinea = 150 # y largo linea
    ptoLinea = (xOrigenLinea * (dxLuz + 1), -xOrigenLinea * dyLuz)
    aaline(pantalla, BLANCO, (xOrigenLinea, 0), ptoLinea, 1) 
    circle(pantalla, BLANCO, ptoLinea, 5) 

    pEscalarN_Tri_Y_D_Luz = cosAnguloEntreVectores(nTri, dLuz) # pEscalarN_Tri_Y_D_Luz = abs(nTri @ dLuz / norm(nTri - dLuz)) # y = 1er ptoTri # -1 < pEscalarN_Tri_Y_D_Luz < 1 # cos 180º = -1 # backface culling
    # si positivo no esta mirando a camara (no render). si negativo esta mirando (render)

    if pEscalarN_Tri_Y_D_Luz < 0:
        pEscalarN_Tri_Y_D_Luz = 0

    elif pEscalarN_Tri_Y_D_Luz > 1:
        pEscalarN_Tri_Y_D_Luz = 1

    cTri = VERDE
    colorTriAtenuado = cTri * pEscalarN_Tri_Y_D_Luz # gris

    ''' debug (afecta grav rendimiento)
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
    '''
    
    polygon(pantalla, colorTriAtenuado, ptosPantalla, noTieneRelleno)

# main    
x, y, z, dFocal = array((1, 0, 0)), array((0.0, 1.0, 0.0)),\
                  array((0, 0, 1)), 1 # 1u = 1m (1000mm), 0.1 #1dm (10cm, 100mm), 0.05 #5cm (50 mm)

ptosInterseccion, distanciasPtos, ptosPantalla = [], [], [] # ptosInterseccion = distanciasPtos = []

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
 
NEGRO, BLANCO, AZUL, VERDE, ROJO, pantalla, escala =        \
       array((0.0, 0.0, 0.0)), array((255.0, 255.0, 255.0)),\
       array((0.0, 0.0, 255.0)), array((0.0, 255.0, 0.0)),  \
       array((255.0, 0.0, 0.0)), set_mode((300, 300)), 100  # tuplas no mutables

for ptoInterseccion in ptosInterseccion: 
    xI, yI, zI = ptoInterseccion
    ptosPantalla.append((escala * (xI + 1), -escala * (yI - 2)))
    
# aqui para sombreador vertices / aristas?

noTieneRelleno = 0 # < 0 nada, = 0 relleno, > 0 wireframe

t = time()
fps = 60

nFotogramas = 200
for nFotograma in range(nFotogramas):
    pantalla.fill(NEGRO)

    ptoLuz += array((0.1, 0, 0))

    sombreaPlano()
    update()

    sleep(1 / fps) 
  
dt = time() - t
print("\nhan pasado", round(dt, 2), "segundos para", nFotogramas, "fotogramas\n",\
      round(nFotogramas / dt, 2), "fotogramas por segundo") #round(dt / nFotogramas, 2), "segundos por fotograma")

