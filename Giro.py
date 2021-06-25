from pygame         import init
from pygame.display import set_mode, update
from pygame.draw    import aaline
from numpy          import array
from numpy.linalg   import norm
from math           import sin, cos, radians, acos, degrees 
from time           import sleep

CERO = array((0, 0, 0))
PANTALLA, NEGRO, BLANCO, xOrigenLinea, nFotogramas, sentido, refresca,\
          anguloG = set_mode((300, 300)), CERO,\
          255 * array((1, 1, 1)), 150, 400, 0, True, 0 #False # 0 antihorario, 1 horario

Z, Y, X = array((0, 0, 1)), array((0, 1, 0)), array((1, 0, 0))
ptosTri = [X, Y, Z] # el tri tendra un solo angulo local para todos sus puntos
# tri.gira() tri.angulo # orientacion, rotacion

'''
def giraPlano(nombrePlano): # en un solo eje o plano (z = 0)
    pto = (x,y,z)

    if plano == "alfa": # xy 
         z = 0 # pto = (x,y,0)
    elif plano == "beta": # xz 
         y = 0 # pto = (x,0,z)
    elif plano == "gamma": # yz 
         x = 0 # pto = (0,y,z)

    return pto
               
def giraEje(nombreEje):
    if eje == "x": # plano gamma yz (x=0)
        pto = giraPlano(gamma)
    elif eje == "y": # plano beta xz (y=0)
        pto = giraPlano(beta)
    elif eje == "z": # plano alfa xy (z=0)
        pto = giraPlano(alfa)

    return pto
''' 

def gira(anguloG): # en un solo eje o plano (z = 0)
    '''devuelve direccion normalizada correspondiente al angulo entre [0, 360)'''
    anguloR = radians(anguloG)

    if sentido == 0:
        d = (cos(anguloR), -sin(anguloR), 0) # sentido antihorario

    elif sentido == 1:
        d = (cos(anguloR), sin(anguloR), 0) # sentido horario

    '''
    if anguloG < 359: # [0,359)
        anguloG += 1

    else: # anguloG >= 359 [359, inf)
        anguloG = 0
    '''

    return d

#def gira1():
    
init()

def devuelveAnguloEntreVectores(u, v):
    '''devuelve angulo entre vectores normalizados (en un mismo plano o eje)'''
    sonIgualesU_V = (u == v).all()

    if sonIgualesU_V:
        angulo = 0

    else: # u != v 
        angulo = degrees(acos(u @ v / norm(u - v)))
    
    return angulo 



''' PROBADOR
print(devuelveAnguloEntreVectores(X, X), "debe ser 0º\n",
      devuelveAnguloEntreVectores(Y, X), "debe ser 90º\n",
      devuelveAnguloEntreVectores(Z, X), "debe ser 90º")

print(devuelveAnguloEntreVectores(-X, X), "debe ser 180º\n",
      devuelveAnguloEntreVectores(-Y, Y), "debe ser 180º\n",
      devuelveAnguloEntreVectores(-Z, Z), "debe ser 180º") # error
'''

'''
def gira1(d): # rota. vector de rotacion
    #devuelve direccion girada a partir de d normalizada
    return cos(radians(1)) / d # en q plano o eje?

#PROBADOR
print(gira1(X), "debe ser ")
'''

while True:
    #'''
    angulosPtosTri = []
    
    for posPtoArray in range(len(ptosTri)):     
        anguloPtoTri = devuelveAnguloEntreVectores(ptosTri[posPtoArray], X)
        anguloPtoTri1 = anguloPtoTri + 1 # - 1
        angulosPtosTri.append(anguloPtoTri1) 
        ptosTri[posPtoArray] = gira(radians(anguloPtoTri1)) 
        
    print("\nangulosPtosTri =", angulosPtosTri, "\nptosTri =", ptosTri)    
    #'''
    
    #reloj
    d = gira(anguloG)

    if anguloG < 359: # [0,359)
        anguloG += 1

    else: # anguloG >= 359 [359, inf)
        anguloG = 0
    
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



