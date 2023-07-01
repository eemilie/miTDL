from dataclasses import dataclass
from typing import List, Any

from AL import Token
from constants import first, follow
from Errores import Error
from AL import Analizador_lexico
from TS import GestorTS, Tabla_de_simbolos
from tipo import Tipo


class temporales:
    valorStr = ''
    valorB = 0
    valorInt = 0
    nombre = 't'
    count = 0
    desp = 0  # desplazamiento en la ts

    def set_temporal(self, nombre, tipo):
        self.nombre = nombre + str(self.count)
        self.count += 1
        if tipo in {'t_int', 't_bool'}:
            self.desp = self.desp + 1
        elif tipo == 't_str':
            self.desp = self.desp + 32




class Nodo:
    '''Falta los .lugar y la lista de parametros de .lugar[i]'''
    tipo: List[Tipo]
    tipoRetorno: Tipo = None
    tipoParametros: List[Tipo] = None
    tam: int
    '''Parte de TdL'''
    lugarInt = 0
    lugarBool = 0
    lugarStr = ''
    long = 0
    paramInt = 0
    paramBool = 0
    paramStr = ''
    entro = ''
    asig = ''
    post = ''
    elems = 0
    siguiente = ''
    inicio = ''
    param: List[Any] = []  # .param 1 o para la lista
    lugar_lista: List[Any] = []  # lista de parametros de E2 que puede ser cualquier cosa creo
    lugar_if_id =  None
    lugar_pr_id =  None
    lugar_rt_id = None
    #entro_not = False
    id_func = ''
    pasar_param = None


    def __init__(self):
        self.tipo = []
        self.tam = 0
        self.lugarBool = None

    def set_tam(self, tam: int):
        self.tam = tam

    def get_tam(self):
        return self.tam

    def get_tipo(self):
        if len(self.tipo) == 0:
            return None
        return self.tipo[-1]

    def set_tipo(self, tipo: Tipo):
        self.tipo.append(tipo)

    def get_tipoRet(self):
        return self.tipoRetorno

    def set_tipoRet(self, tipo: Tipo):
        self.tipoRetorno = tipo

    '''Parte de TdL'''

    def get_lugarInt(self):
        if self.lugarInt is None:
            return None
        else:
            return self.lugarInt

    def set_lugarInt(self, lugarInt: int):
        self.lugarInt = lugarInt

    def get_lugarBool(self):
        if self.lugarBool is None:
            return None
        else:
            return self.lugarBool

    def set_lugarBool(self, lugarBool: int):
        self.lugarBool = lugarBool

    def get_lugarStr(self):
        if self.lugarStr is None:
            return None
        else:
            return self.lugarStr

    def set_lugarStr(self, lugarStr: str):
        self.lugarStr = lugarStr

    def get_long(self):
        return self.long

    def set_long(self, long: int):
        self.long = long

    def get_paramInt(self):
        return self.paramInt

    def set_paramInt(self, paramInt: int):
        self.paramInt = paramInt

    def get_paramBool(self):
        return self.paramBool

    def set_paramBool(self, paramBool: int):
        self.paramBool = paramBool

    def get_paramStr(self):
        return self.paramStr

    def set_paramStr(self, paramStr: str):
        self.paramStr = paramStr

    def get_entro(self):
        return self.entro

    def set_entro(self, entro: str):
        self.entro = entro

    def get_asig(self):
        return self.asig

    def set_asig(self, asig: str):
        self.asig = asig

    def get_post(self):
        return self.post

    def set_post(self, post: str):
        self.post = post

    def get_elems(self):
        return self.elems

    def set_elems(self, elems: int):
        self.elems = elems

    def get_siguiente(self):
        return self.siguiente

    def set_siguiente(self, siguiente: str):
        self.siguiente = siguiente

    def get_inicio(self):
        return self.inicio

    def set_inicio(self, inicio: str):
        self.inicio = inicio


class Registro_de_activacion:
    tamLocal: int
    tamTemp: int
    tamTotal: int
    temporal: {}  # mapa de temporales
    etiq: str  # ? hace falta ??
    tabla: {str, Tabla_de_simbolos}  # {str, Tabla_de_simbolos simbolo}
    locales: {} # mapa de locales del ra
    todos: List[Any] = []
    num_params_func: int
    cabeza_ra: []
    VD = None

    def __init__(self, tamLocal, tamTemp, tamTotal, temporal, etiq, tabla, locales, todos, num_params_func, cabeza_ra, VD): #todos
        self.tamLocal = tamLocal
        self.tamTemp = tamTemp
        self.tamTotal = tamTotal
        self.temporal = temporal
        self.etiq = etiq
        self.tabla = tabla
        self.locales = locales
        self.todos = todos              # ANHADIR EN ORDEN LAS COSAS EN EL MAPA TODOS
        self.num_params_func = num_params_func          #para el paso de los params
        self.cabeza_ra = cabeza_ra                      # para los pasos de los params
        self.VD = VD

    def __str__(self):
        return f"Registro_de_activacion(tamLocal={self.tamLocal}, tamTemp={self.tamTemp}, tamTotal={self.tamTotal}, temporal={self.temporal}, etiq={self.etiq}, tabla={self.tabla}, locales={self.locales}, todos={self.todos})"


class datos_estaticos:
    temps: List[Any] = []
    locales: {}

    def __init__(self, temps, locales):
        self.temps = temps
        self.locales = locales


class Analizador_sintactico:
    sig_token: Token
    analizador_lexico: Analizador_lexico
    indice = int
    parse = 'DescendenteR '
    linea: int
    gestor_errores: Error
    gTS: GestorTS
    count_tempBool = 0
    count_tempInt = 0
    count_tempStr = 0
    tabla = 0
    hashmap = {}
    primer = 0
    r: Registro_de_activacion
    lista_temp: List[temporales] = []
    de: datos_estaticos
    etiq_cadenas: List[Any] = []
    ras: List[Any] = []
    #emite: emites
    count_sig = 1
    count_ini = 1
    num_buc = 1
    entro_not = False
    entro_not_asig = False
    viene_while = False
    num_reg = 1
    count_diret = 1
    nummm = 1


    def __init__(self, analizador_lexico: Analizador_lexico, gestor_errores, g_TS: GestorTS):
        self.analizador_lexico = analizador_lexico
        self.indice = 0
        self.linea = 0
        self.gestor_errores = gestor_errores
        self.gTS = g_TS

    def error(self, chars_esperados):
        token = self.sig_token
        token_str = token.codigo
        self.gestor_errores.addError_sintactico(f"caracter recibido '{token_str}', se esperaba {chars_esperados}",
                                                self.analizador_lexico.contador_linea)

    def helper_error_msg(self, fstfllw):
        list_follow = []
        ret = ''
        for i, conjunto in enumerate(fstfllw):
            for j, elem in enumerate(conjunto):
                if elem == 'lambda':
                    continue
                list_follow.append(elem)
        return list_follow

    def register(self, num_regla):
        self.parse += str(num_regla) + ' '

    def get_token(self):
        self.sig_token = self.analizador_lexico.get_token()

    def equipara(self, token):
        if self.sig_token.codigo == token:
            self.get_token()
        else:
            self.error(f"['{token}']")

    def get_lugar_id(self, id_pos) -> Any:
        clave = self.gTS.get_simbolo(int(id_pos[1:]), int(id_pos[0])).nombre
        valor = self.hashmap[clave]
        return self.hashmap[clave]

    def set_lugar_id(self, id_pos, valor):
        clave = self.gTS.get_simbolo(int(id_pos[1:]), int(id_pos[0])).nombre
        self.hashmap[clave] = valor
        # se podria meter aqui las temporales en la lista de temporales del registro de activacion

    def buscarEtiqTs(self, id_pos):  # no va no devuleve nada
        return self.gTS.get_simbolo(int(id_pos[1:]), self.tabla).nombre

    def buscarVarTs(self, id_pos):
        return self.gTS.get_simbolo(int(id_pos[1:]), int(id_pos[0])).nombre

    def verificar_elemento(self,elemento):
        if isinstance(elemento, tuple) and len(elemento) == 2:
            return True
        else:
            return False

    def asig_func(self, tipo, func, id_ig):
        # ns.set_lugarInt() -> poner el .lugar al tipo de retorno de la func ??
        # se pone la llamada en una temp
        tempCall = temporales()
        # anadimos al mapa de temps y a todos
        tempCall.valorInt = 'call_' + str(func)
        tempCall.count = len(self.ra.temporal) + 1
        tempCall.nombre = tempCall.nombre + str(tempCall.count + 1)
        tempCall.desp = len(self.ra.todos) + 1
        self.ra.todos.append(tempCall)
        if tipo == Tipo.t_int:
            self.ra.temporal[tempCall.nombre] = tempCall.valorInt
        elif tipo == Tipo.t_bool:
            self.ra.temporal[tempCall.nombre] = tempCall.valorB
        elif tipo == Tipo.t_str:
            self.ra.temporal[tempCall.nombre] = tempCall.valorStr
        encontrado_ra = False
        cosa = 'ra'

        for i in range(len(self.ra.todos)):
            if isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_int and self.ra.todos[i].valorInt == tempCall.valorInt:
                despT = i
                break
            elif isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_bool and self.ra.todos[i].valorInt == tempCall.valorB:
                despT = i
                break
            elif isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_bool and self.ra.todos[i].valorInt == tempCall.valorStr:
                despT = i
                break

        for i in range(len(self.ra.todos)):
            if self.verificar_elemento(self.ra.todos[i]) and self.ra.todos[i][0] == id_ig:
                despV = i
                encontrado_ra = True
                break

        if encontrado_ra == False:
            for i in range(len(self.de.temps)):
                if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == id_ig:
                    despV = i
                    cosa = 'de'
                    break

        # ponemos la temp a nuestro id
        self.emite('callAsig1', cosa, id_ig, func, despV, despT)  # aqui busca la etiqueta/nombre de la funcion


    def cosa_para_pr_rt(self, tipo, lugar, lugar_id, pr_rt):
        si = 0
        if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
            desp = 0
            encontrado_ra = 0
            de = 'no'
            name = None

            for i in range(len(self.ra.todos)):
                id_o_temp = self.ra.todos[i]
                if self.verificar_elemento(id_o_temp) and lugar_id != None and id_o_temp[0] == lugar_id[0]:
                    name = id_o_temp[0]
                    encontrado_ra = 1
                    break
                desp += 1

            if encontrado_ra == 0:
                de = 'si'
                desp = 0
                for i in range(len(self.de.temps)):
                    id_o_temp = self.de.temps[i]
                    if self.verificar_elemento(id_o_temp) and lugar_id != None and id_o_temp[0] == lugar_id[0]:
                        name = id_o_temp[0]
                        desp = i
                        break

            # si i,prime o returnea directamente un entero/cad/bool
            if name == None: #not('name' in locals() and isinstance(name, str)):
                de = 'no'
                desp = 0
                for i in range(len(self.ra.todos)):
                    id_o_temp = self.ra.todos[i]
                    if tipo == Tipo.t_int and isinstance(id_o_temp, temporales) and id_o_temp.valorInt == lugar:
                        temp_selec = id_o_temp
                        desp = i
                        si = 1
                        encontrado_ra = 1
                        break
                    elif tipo == Tipo.t_bool and isinstance(id_o_temp, temporales) and id_o_temp.valorB == lugar:
                        temp_selec = id_o_temp
                        desp = i
                        si = 1
                        encontrado_ra = 1
                        break
                    elif tipo == Tipo.t_str and isinstance(id_o_temp, temporales) and id_o_temp.valorStr == lugar:
                        temp_selec = id_o_temp
                        desp = i
                        si = 1
                        encontrado_ra = 1
                        break


            if si == 1:
                name = temp_selec.nombre

            if de == 'si':
                self.emite(pr_rt, name, 'ra_de', tipo, lugar, desp)
            else:
                self.emite(pr_rt, name, 'ra', tipo, lugar, desp)


        else:
            desp = 0
            name = None
            for i in range(len(self.de.temps)):
                id_o_temp = self.de.temps[i]
                if self.verificar_elemento(id_o_temp) and lugar_id != None and id_o_temp[0] == lugar_id[0]:
                    name = id_o_temp[0]
                    desp = i
                    break

            if name == None: #not('name' in locals() and isinstance(name, str)):
                for i in range(len(self.de.temps)):
                    id_o_temp = self.de.temps[i]
                    if tipo == Tipo.t_int and isinstance(id_o_temp, temporales) and id_o_temp.valorInt == lugar:
                        temp_selec = id_o_temp
                        si = 1
                        desp = i
                        break
                    elif tipo == Tipo.t_bool and isinstance(id_o_temp, temporales) and id_o_temp.valorB == lugar:
                        temp_selec = id_o_temp
                        si = 1
                        desp = i
                        break
                    elif tipo == Tipo.t_str and isinstance(id_o_temp, temporales) and id_o_temp.valorStr == lugar:
                        temp_selec = id_o_temp
                        si = 1
                        desp = i
                        break

            if si == 1:
                name = temp_selec.nombre

            self.emite(pr_rt, name, 'de', '', lugar, desp)



    def id_if_while(self, lista, siguiente, ra_o_de, lug_if_id, if_o_while):
        for i in range(len(lista)):
            if ra_o_de == 'de' and self.verificar_elemento(lista[i]):
                if lista[i][0] == lug_if_id:
                    desp = i
                    break
            elif ra_o_de == 'ra' and self.verificar_elemento(lista[i]):
                if lista[i][0] == lug_if_id:
                    desp = i
                    break

        if self.entro_not:
            condicion = 1
        elif not self.entro_not:
            condicion = 0

        self.emite(if_o_while, lug_if_id, condicion, ra_o_de, desp, siguiente)


    def asig_casos(self, parid, lugar_tipo, id_pos, tipo):
        self.ra.locales[self.buscarVarTs(id_pos)] = lugar_tipo
        # self.ra.todos.append(self.buscarVarTs(id_pos))
        ponte = 1
        encontrado = 0
        de = 'no'
        for i in range(len(self.ra.todos)):
            # si no existe el id  se anhade
            if self.verificar_elemento(self.ra.todos[i]) == True and self.ra.todos[i][0] == parid[0]:
                self.ra.todos[i] = parid
                encontrado = 1
                desp = i
                ponte = 0
                break

        if encontrado == 0:     # si no lo hemos encontrado en el ra se busca en los de
            for i in range(len(self.de.temps)):
                if self.verificar_elemento(self.de.temps[i]) == True and self.de.temps[i][0] == parid[0]:
                    self.de.temps[i] = parid
                    desp = i
                    de = 'si'
                    break

        claves = list(self.ra.temporal.keys())

        for i in range(len(claves)):
            key = claves[i]
            if self.ra.temporal[key] == lugar_tipo:
                valorT = key
                temp = self.ra.temporal[key]
                break


        for i in range(len(self.ra.todos)):
            if isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_int and self.ra.todos[i].valorInt == parid[1]:
                despTempI = i
                break
            elif isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_bool and self.ra.todos[i].valorB == parid[1]:
                despTempI = i
                break
            elif isinstance(self.ra.todos[i], temporales) and tipo == Tipo.t_str and self.ra.todos[i].valorStr == parid[1]:
                despTempI = i
                break

        if de == 'si':
            self.emite('tempde', '2', self.buscarVarTs(id_pos), valorT, despTempI, desp)
        else:
            self.emite('temp', '2', self.buscarVarTs(id_pos), valorT, despTempI, desp)

        # self.emite('temp', '2', self.buscarVarTs(id_pos), valorT, temp, despTempI)

    def es_ra(self):
        if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
            return True
        else: return False


    # Concatena varios <
    def e1(self) -> Nodo:
        ne = Nodo()

        # Caso <
        if self.sig_token.codigo == 'less':
            # Sintactico
            self.register(48)
            self.equipara('less')
            nr = self.r()
            ne1 = self.e1()

            # Semantico
            if nr.get_tipo() != Tipo.t_int:
                ne.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(5, self.analizador_lexico.contador_linea)

            if nr.get_tipo() == Tipo.t_int and ne1.get_tipo() in {Tipo.t_ok, Tipo.t_bool}:
                ne.set_tipo(Tipo.t_bool)
                ''' TDL '''
                if ne1.get_elems() == 0:
                    '''revisar porque me esta dando un unexpected argument'''
                    ne.set_lugarBool(nr.get_lugarBool())
                    # creo que tambien se añade a la lista
                    # lista de parametros de E2 que puede ser cualquier cosa creo
                    ne.lugar_lista
                    ne.set_elems(1)
                else:
                    '''como vergas se hace una concatenacion de booleanos'''
                    ne.lugar = nr.lugar + ne1.lugar
                    ne.set_elems(1 + ne1.get_elems())
                ''' TDL '''



            else:
                ne.set_tipo(Tipo.t_error)

        elif self.sig_token.codigo in follow['E1']:  # caso lambda
            # Sintactico
            self.register(47)
            # Semantico
            ne.set_tipo(Tipo.t_ok)
            ''' TDL '''
            # ne.set_lugarBool(self, null) revisar si se puede poner a null y como afecta a la generacion de codigo
            ne.set_lugarInt(None)
            ne.set_lugarBool(None)
            ne.set_lugarStr(None)

            ne.set_elems(0)
            '''TDL '''
        else:
            self.error(self.helper_error_msg([first['E1'], follow['E1']]))

        return ne

    # Condicionales, interior de parentesis y derecha de la asignacion
    def e(self) -> Nodo:
        # Sintactico
        self.register(46)
        nr = self.r()
        ne1 = self.e1()

        # Semantico
        ne = Nodo()

        if ne1.get_tipo() == Tipo.t_error or nr.get_tipo() == Tipo.t_error:
            ne.set_tipo(Tipo.t_error)
            return ne

        if nr.get_tipo() == Tipo.t_bool and ne1.get_tipo() != Tipo.t_ok:
            ne.set_tipo(Tipo.t_error)
            self.gestor_errores.addError(11,
                                         self.analizador_lexico.contador_linea)  # cuando r es bool e1 tiene que ser lamba
            return ne

        elif nr.get_tipo() == Tipo.t_bool and ne1.get_tipo() == Tipo.t_ok:
            ne.set_tipo(Tipo.t_bool)
            ''' TDL '''
            ne.set_lugarBool(nr.get_lugarBool())  # E.lugar := R.lugar
            ne.lugar_if_id = nr.lugar_if_id
            ne.lugar_pr_id = nr.lugar_pr_id
            ne.lugar_rt_id = nr.lugar_rt_id
            ne.pasar_param = nr.pasar_param
            ''' TDL '''

        elif nr.get_tipo() == Tipo.t_int and ne1.get_tipo() == Tipo.t_ok:  # cuando r es int y no hay nada mas
            ne.set_tipo(Tipo.t_int)
            ''' TDL '''
            ''' TDL '''
            if ne1.get_elems() == 0:
                ne.set_lugarInt(nr.get_lugarInt())
                ne.set_post(nr.get_post())
                ne.lugar_pr_id = nr.lugar_pr_id
                ne.lugar_rt_id = nr.lugar_rt_id
                ne.pasar_param = nr.pasar_param
                ne.set_elems(1)
            else:
                # self.emite(ne.get_lugarBool(), ':=', nr.get_lugarInt(), '<', E2.lugar[1])
                if ne.get_lugarBool() == 1:
                    for i in range(2, ne1.get_elems()):  # esto esta mal escrito
                        print('dehfbouqewfhyceug', i)
                        self.emite(ne.get_lugarBool(), ':=', ne.get_lugarBool(), '<', ne1.lugar_lista[i], '')
            ''' TDL '''
            # self.nuevaTempInt()  # nuevatempInt() -> nos crea una nueva temporal de tipo int
            # ne.set_lugarInt(nr.get_lugarInt())  # solo pondriamos E.lugar = R.lugar
            ''' TDL '''

        elif nr.get_tipo() == Tipo.t_int and ne1.get_tipo() == Tipo.t_bool:  # cuando r es int y esta seguido de <
            ne.set_tipo(Tipo.t_bool)
            ''' TDL '''
            if ne1.get_elems() == 0:
                ne.set_lugarBool(nr.get_lugarInt())
            else:
                # self.emite(ne.get_lugarBool(), ':=', nr.get_lugarInt(), '<', E2.lugar[1])
                if ne.get_lugarBool() == 1:
                    for i in range(2, ne1.get_elems()):  # esto esta mal escrito
                        print('dehfbouqewfhyceug', i)
                        self.emite(ne.get_lugarBool(), ':=', ne.get_lugarBool(), '<', ne1.lugar_lista[i], '')
            ''' TDL '''

        elif nr.get_tipo() == Tipo.t_str and ne1.get_tipo() == Tipo.t_ok:  # cuando es un string
            ne.set_tipo(Tipo.t_str)
            ne.set_lugarStr(nr.lugarStr)
            ne.lugar_pr_id = nr.lugar_pr_id
            ne.lugar_rt_id = nr.lugar_rt_id
            ne.pasar_param = nr.pasar_param
            ''' CAMBIO MIOOOO NO SE SI ESTARA BIEBN'''

        elif nr.get_tipo() == Tipo.t_funcion and ne1.get_tipo() == Tipo.t_ok:
            ne.set_tipo(nr.get_tipo())
            ne.set_tipoRet(nr.get_tipoRet())
            ne.id_func = nr.id_func


        else:
            self.gestor_errores.addError(11,
                                         self.analizador_lexico.contador_linea)  # cuando r es int e1 puede ser lamba o <
        return ne

    # Concatena varios -
    def r1(self) -> Nodo:
        nr = Nodo()
        if self.sig_token.codigo == 'subtraction':
            # Sintactico
            self.register(45)
            self.equipara('subtraction')
            nu = self.u()
            nr2 = self.r1()

            # Semantico
            if nu.get_tipo() == Tipo.t_int and nr2.get_tipo() in {Tipo.t_int, Tipo.t_ok}:
                nr.set_tipo(Tipo.t_int)
                ''' TDL '''
                if nr2.get_elems() == 0:  # if R2’.elems = 0 then begin
                    nr2.set_elems(1)  # R2.elems := 1
                    nr.set_elems(nr2.get_elems())
                    nr2.set_lugarInt(nu.get_lugarInt())
                    nr2.lugar_lista.append(
                        nu.get_lugarInt())  # o lo pongo en la lista de lugares ??????????????????????????????????????????????????????????????????????????????????????????????
                else:
                    #nr.lugar_lista += nu.get_lugarInt() # NO SERIA APPEND ?
                    id_pos = self.sig_token.atributo
                    if id_pos == '':
                        nr.lugar_lista.append(nr2.get_lugarInt())  # nr.lugar_lista += nr2.get_lugarInt()
                    else:
                        iddddd = self.buscarVarTs(id_pos)
                        par_id_valor_r2 = (iddddd, nr2.get_lugarInt())
                        nr.lugar_lista.append(par_id_valor_r2)#nr.lugar_lista += nr2.get_lugarInt()
                    nr.elems = 1 + nr2.get_elems()

                    ''' esto  no va aqui 
                    tempResta = temporales()
                    valorResta = nr2.get_lugarInt() - nu.get_lugarInt()
                    tempResta.valorInt = valorResta

                    tempResta.desp = self.gTS.get_last_simbolo().get_desp()
                    nr2.set_lugarInt(valorResta)
                    esto  no va aqui '''

                    ''' TDL ANTES SIGUIENTE EL EDT 
                    if nr2.get_elems() == 0:  # if R2’.elems = 0 then begin
                        nr.set_lugarInt(nu.get_lugarInt())  # R2.lugar := U.lugar
                        nr.set_elems(1)  # R2.elems := 1
                    else:  # else begin
                        # R2.lugar := U.lugar ⊕ R2’.lugar
                        nr.set_elems(1 + nr2.get_elems())  # R2.elems := 1 + R2’.elems
                    TDL ANTES SIGUIENTE EL EDT '''

            else:
                nr.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(5, self.analizador_lexico.contador_linea)

        elif self.sig_token.codigo in follow['R1']:  # lambda
            # Sintactico
            self.register(44)
            # Semantico
            nr.set_tipo(Tipo.t_ok)
            ''' TDL '''
            #nr.set_elems(0)  # R2.elems := 0
            #nr.set_lugarInt(None)
            ''' R2. lugar := null  # como es lambda el lugar de bool no existe pero se tendria que ponerse a null 

            '''
            ''' TDL '''
        else:
            self.error(self.helper_error_msg([follow['R1'], first['R1']]))
            nr.set_tipo(Tipo.t_error)
        return nr

    # Juntar varias variables con -
    def r(self) -> Nodo:
        # Sintactico
        self.register(43)
        nu = self.u()
        nr2 = self.r1()

        # Semantico
        nr = Nodo()
        if nu.get_tipo() == Tipo.t_error or nr2.get_tipo() == Tipo.t_error:  # caso de resta
            nr.set_tipo(Tipo.t_error)

        elif nu.get_tipo() == Tipo.t_int and nr2.get_tipo() not in {Tipo.t_int, Tipo.t_ok}:  # caso de resta
            nr.set_tipo(Tipo.t_error)
            self.gestor_errores.addError(5, self.analizador_lexico.contador_linea)

        elif nu.get_tipo() == Tipo.t_int and nr2.get_tipo() in {Tipo.t_int, Tipo.t_ok}:
            nr.set_tipo(Tipo.t_int)
            ''' TDL '''
            # creamos la nuevaTempInt() R.lugar
            if nr2.elems == 0:  # if R2.elems = 0
                nr.set_lugarInt(nu.get_lugarInt())  # then R.lugar := U.lugar
                nr.set_post(nu.get_post())
                nr.lugar_pr_id = nu.lugar_pr_id
                nr.lugar_rt_id = nu.lugar_rt_id
                nr.pasar_param = nu.pasar_param
                #nr.lugar_lista.append(nu.get_lugarInt())
                # o lo pongo en la lista
            else:  # else begin
                #nr2.lugar_lista.append(nu.get_lugarInt())
                #nr.lugar_lista.extend(nr2.lugar_lista)
                nr.lugar_lista.append(nu.get_lugarInt())

                tempResta = temporales()
                nulo = False
                id_sum1 = None
                id_sum2 = None
                if self.verificar_elemento(nr2.lugar_lista[len(nr2.lugar_lista)-1]):
                    elem1 = nr2.lugar_lista[len(nr2.lugar_lista)-1][1]
                    id_sum1 = nr2.lugar_lista[len(nr2.lugar_lista) - 1][0]
                else:
                    elem1 = nr2.lugar_lista[len(nr2.lugar_lista) - 1]
                if self.verificar_elemento(nr2.lugar_lista[len(nr2.lugar_lista) - 2]):
                    elem2 = nr2.lugar_lista[len(nr2.lugar_lista)-2][1]
                    id_sum2 = nr2.lugar_lista[len(nr2.lugar_lista)-2][0]
                else:
                    elem2 = nr2.lugar_lista[len(nr2.lugar_lista) - 2]

                if elem1 == None:
                    elem1 = 000
                    nulo = True
                    tempResta.valorInt = -10000
                elif elem2 == None:
                    elem2 = 000
                    nulo = True
                    tempResta.valorInt = -10000
                elif elem2 == None and elem2 == None:
                    elem1 = 000
                    elem2 = 000
                    nulo = True
                    tempResta.valorInt = -10000
                else:
                    tempResta.valorInt = int(elem1) - int(elem2)

                nr.set_lugarInt(tempResta.valorInt)


                if self.es_ra():
                    #anadir la temporal al ra: en todos y temps
                    self.ra.todos.append(tempResta)
                    #para poner la temp bien
                    for i in range(len(self.ra.todos)):
                        teemp = self.ra.todos[i]
                        if isinstance(teemp, temporales) and teemp.valorInt == tempResta.valorInt or isinstance(teemp, temporales) and nulo and teemp.valorInt == tempResta.valorInt:
                            desp = i
                            count = len(self.ra.temporal)
                            nombre = tempResta.nombre + str(count)
                            tempAux = temporales()
                            tempAux.nombre = nombre
                            tempAux.desp = desp
                            tempAux.count = count
                            tempAux.valorInt = tempResta.valorInt
                            self.ra.todos[i] = tempAux
                            self.ra.temporal[tempAux.nombre] = tempAux.valorInt
                            break
                    # buscamos el desp de elem1
                    resta_de_o_ra = 'RESTARA'
                    encontrado1 = False
                    encontrado2 = False
                    for i in range(len(self.ra.todos)):
                        temid = self.ra.todos[i]
                        if self.verificar_elemento(temid) and temid[1] == elem1 or self.verificar_elemento(temid) and id_sum1 != None and temid[0] == id_sum1:
                            despE1 = i
                            encontrado1 = True
                            elem1 = temid[0]
                            break

                    if not encontrado1:
                        for i in range(len(self.de.temps)):
                                if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][1] == elem1 or self.verificar_elemento(self.de.temps[i]) and id_sum1 != None and self.de.temps[i][0] == id_sum1:
                                    despE1 = i
                                    resta_de_o_ra = 'RESTARADE1'
                                    encontrado1 = True
                                    elem1 = self.de.temps[i][0]
                                    break
                    if not encontrado1:
                        for i in range(len(self.ra.todos)):
                            if isinstance(self.ra.todos[i], temporales) and self.ra.todos[i].valorInt == elem1:
                                despE1 = i
                                elem1 = self.todos[i].nombre
                                break

                    # buscamos el desp de elem2
                    for i in range(len(self.ra.todos)):
                        temid = self.ra.todos[i]
                        if self.verificar_elemento(temid) and temid[1] == elem2 or self.verificar_elemento(temid) and id_sum2 != None and temid[0] == id_sum2:
                            despE2 = i
                            encontrado2 = True
                            elem2 = temid[0]
                            break

                    if not encontrado2:
                        for i in range(len(self.de.temps)):
                            if  self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][1] == elem2 or self.verificar_elemento(self.de.temps[i]) and id_sum2 != None and self.de.temps[i][0] == id_sum2:
                                despE2 = i
                                encontrado2 = True
                                elem2 = self.de.temps[i][0]
                                if resta_de_o_ra == 'RESTARADE1':
                                    resta_de_o_ra = 'RESTARADE3'
                                else:
                                    resta_de_o_ra = 'RESTARADE2'
                                break
                    if not encontrado2:
                        for i in range(len(self.ra.todos)):
                            if isinstance(self.ra.todos[i], temporales) and self.ra.todos[i].valorInt == elem2:
                                despE2 = i
                                elem2 = self.ra.todos[i].nombre
                                break

                    #self.ra.temporal[]
                    # emitir la temporal de la rest
                    self.emite(tempAux.nombre, 'igResta', elem1, desp , elem2, '')
                    self.cuarteto(despE1,despE2, resta_de_o_ra,'',24)
                    self.cuarteto('RESTARA', desp, '','', 25)
                else:
                    #anadir la temporal en todos y en temps
                    #tempResta.count = tempResta.count + 1
                    self.de.temps.append(tempResta)
                    for i in range(len(self.de.temps)):
                        if isinstance(self.de.temps[i], temporales) and self.de.temps[i] == tempResta.valorInt:
                            desp = i
                            count = len(self.de.temps) + 1
                            nombre = tempResta.nombre + str(count)
                            tempAux = temporales()
                            tempAux.nombre = nombre
                            tempAux.desp = desp
                            tempAux.count = count
                            tempAux.valorInt = tempResta.valorInt
                            self.de.temps[i] = tempAux
                    # emitir la temporal de la rest
                    self.emite(tempAux.nombre, 'igResta', elem1, '-', elem2, 'RESTADE')
                    #self.cuarteto()

                for i in range(2,nr2.get_elems()):  # nr2.lugar_lista(): ????????????????????
                    # emite(R.lugar, ‘:=’, U.lugar, ‘-’, R2.lugar[1]) ??????????????????????????????????????????????
                    quevale = i % 2
                    if i % 2 == 0:
                        self.emite(tempResta.nombre, 'igResta', nr.get_lugarInt(), '-', nr2.lugar_lista[i], 'RESTA')


                        '''
                        # si existe el RA
                        if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion) or getattr(self, 'ra',None) is not None and isinstance(self.ra, Registro_de_activacion):
                            tempResta.count = self.ra.tamTemp
                            tempResta.nombre = tempResta.nombre + str(tempResta.count)
                            self.ra.tamTemp = self.ra.tamTemp + 1
                            self.ra.tamTotal = self.ra.tamTotal + 1

                            tempResta.desp = self.ra.tamTotal

                            self.ra.todos.append(tempResta)

                            self.emite(tempResta.nombre, ':=', nu.get_lugarInt(), '-', nr2.lugar_lista[i], '')
                            self.emite(tempResta.nombre, 'igResta', nr.get_lugarInt(), 'hhh', nr2.lugar_lista[i], 'RESTA')
                            tempResta.valorInt = int(nu.get_lugarInt()) - int(nr2.lugar_lista[i])
                            # ponerlo en x tambien
                            # buscamos la x
                            clavesLoc = list(self.ra.locales.keys())
                            for i in range(self.ra.tamLocal):
                                key = clavesLoc[i]
                                if self.ra.locales[key] == nu.get_lugarInt():
                                    loc = key   # aqui tengo el nombre de la local
                                    self.ra.locales[key] = tempResta.valorInt
                                    break

                            claves = list(self.ra.todos.keys())
                            tamBueno = self.ra.tamLocal + self.ra.tamTemp
                            for i in range(tamBueno):
                                key = claves[i]
                                if self.ra.todos[key] == loc:
                                    self.ra.todos[key] = tempResta.valorInt


                    else:
                        tempResta.count = len(self.de.temps)
                        tempResta.nombre = tempResta.nombre + str(tempResta.count)
                        tempResta.desp = len(self.de.temps)

                        self.de.temps.append(tempResta)
                        print('DEEEEEEEEEEEEE:  ', self.de.temps)

                        self.emite(nr.get_lugarInt(), ':=', nr.get_lugarInt(), '-', nr2.lugar_lista[i], '')
                        self.emite(tempResta.nombre, 'igResta', nr.get_lugarInt(), '-', nr2.lugar_lista[i], 'RESTA')

                        '''


            ''' TDL '''

        elif nu.get_tipo() == Tipo.t_bool and nr2.get_tipo() != Tipo.t_ok:  # caso de booleano
            nr.set_tipo(Tipo.t_error)
            self.gestor_errores.addError(11, self.analizador_lexico.contador_linea)

        elif nu.get_tipo() == Tipo.t_bool and nr2.get_tipo() == Tipo.t_ok: # caso bool
            #if nu.entro_not:

            nr.set_tipo(Tipo.t_bool)
            nr.set_lugarBool(nu.get_lugarBool())
            nr.lugar_if_id = nu.lugar_if_id
            nr.lugar_rt_id = nu.lugar_rt_id
            nr.lugar_pr_id = nu.lugar_pr_id
            nr.pasar_param = nu.pasar_param



            # R.lugar := U.lugar

        elif nu.get_tipo() == Tipo.t_str and nr2.get_tipo() == Tipo.t_ok:
            nr.set_tipo(Tipo.t_str)
            nr.set_lugarStr(nu.get_lugarStr())  # se pilla bien tmb
            nr.lugar_rt_id = nu.lugar_rt_id
            nr.lugar_pr_id = nu.lugar_pr_id
            nr.pasar_param = nu.pasar_param

        elif nu.get_tipo() == Tipo.t_funcion and nr2.get_tipo() == Tipo.t_ok:
            nr.set_tipo(nu.get_tipo())
            nr.set_tipoRet(nu.get_tipoRet())
            nr.id_func = nu.id_func


        else:
            nr.set_tipo(Tipo.t_error)

        return nr

    # puede dejar una variable como esta o negarla
    def u(self) -> Nodo:
        u = Nodo()

        # negacion
        if self.sig_token.codigo == 'not':
            # Sintactico
            self.register(42)
            self.equipara('not')
            self.entro_not = True
            self.entro_not_asig = True
            v = self.v()

            # Semantico
            if v.get_tipo() == Tipo.t_bool:
                u.set_tipo(Tipo.t_bool)

                u.set_lugarBool(v.get_lugarBool())
                u.lugar_if_id = v.lugar_if_id
                u.lugar_pr_id = v.lugar_pr_id
                u.lugar_rt_id = v.lugar_rt_id

                if not self.viene_while:
                    if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
                        for i in range(len(self.ra.todos)):
                            item = self.ra.todos[i]
                            if self.verificar_elemento(item) and item[0] == v.lugar_if_id[0]:
                                self.ra.todos[i] = v.lugar_if_id
                                desp = i
                                break
                        self.emite(v.lugar_if_id[0], ':=', 'not', v.get_lugarBool(), desp, 'ra')
                    else:
                        for i in range(len(self.de.temps)):
                            item = self.de.temps[i]
                            if self.verificar_elemento(item) and item[0] == v.lugar_if_id[0]:
                                self.de.temps[i] = v.lugar_if_id
                                desp = i
                                break
                        self.emite(v.lugar_if_id[0], ':=', 'not', v.get_lugarBool(), desp, 'de')


                ''' TDL '''
                #self.viene_while = False


            else:
                u.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(4, self.analizador_lexico.contador_linea)
        else:
            # Sintactico
            self.register(41)
            v = self.v()

            # Semantico
            u.set_tipo(v.get_tipo())
            ''' TDL '''
            if u.get_tipo() == Tipo.t_bool:
                u.set_lugarBool(v.get_lugarBool())  # U.lugar := V.lugar
                u.lugar_if_id = v.lugar_if_id
                u.lugar_pr_id = v.lugar_pr_id
                u.lugar_rt_id = v.lugar_rt_id
                u.pasar_param = v.pasar_param

            if u.get_tipo() == Tipo.t_int:
                u.set_lugarInt(v.get_lugarInt())  # U.lugar := V.lugar
                u.set_post(v.get_post())
                u.lugar_pr_id = v.lugar_pr_id
                u.lugar_rt_id = v.lugar_rt_id
                u.pasar_param = v.pasar_param


            if u.get_tipo() == Tipo.t_str:
                u.set_lugarStr(v.get_lugarStr())  # U.lugar := V.lugar
                u.lugar_pr_id = v.lugar_pr_id
                u.lugar_rt_id = v.lugar_rt_id
                u.pasar_param = v.pasar_param

            if v.get_tipo() == Tipo.t_funcion:
                #u.set_tipo(v.get_tipo())
                u.set_tipoRet(v.get_tipoRet())
                u.id_func = v.id_func
            ''' TDL '''

        return u

    # Puede autoincrementar una variable o pasar parametros a una funcion
    def v1(self, v: Nodo) -> Nodo:
        nv1 = Nodo()

        # Caso de autoincremento
        if self.sig_token.codigo == 'postIncrement':
            # Semantico (heredado)
            if v.get_tipo() == Tipo.t_int:
                nv1.set_tipo(Tipo.t_ok)

                ''' TDL '''
                nv1.set_post('post')  # v1.post = post
                ''' TDL '''

            else:
                nv1.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(5, self.analizador_lexico.contador_linea)

            # Sintactico
            self.register(38)
            self.equipara('postIncrement')


        # Caso de pasar parametros a una funcion
        elif self.sig_token.codigo == 'openParenthesis':
            # Sintactico
            self.register(40)
            self.equipara('openParenthesis')

            # Semantico comprueba que es tipo funcion
            if v.get_tipo() != Tipo.t_funcion:
                nv1.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(7, self.analizador_lexico.contador_linea)
                return nv1

            # Sinactico
            nl = self.l()
            nl.tipo.pop()
            self.equipara('closeParenthesis')

            # Semantico comprueba que los parametros son correctos
            nv1.set_tipo(Tipo.t_ok)
            antes = 0
            for i, tipo in enumerate(nl.tipo):
                if tipo != v.tipoParametros[i]:
                    nv1.set_tipo(Tipo.t_error)
                    self.gestor_errores.addError(8, self.analizador_lexico.contador_linea)
                else:
                    #buscamos el ra de la funcion que llamamos:
                    #buscamos lo que viene antes del param:
                    miPARAM = nl.param[i]
                    desp_param = 0
                    donde = 'ra'
                    encontrado_en_ra = False
                    if i == 0:
                        antes = 1
                    else:
                        for m in range(len(self.ras)):
                            if self.ras[m][0] == v.id_func:
                                raf = self.ras[m][1]
                                antes += raf.cabeza_ra[i][1]

                    #buscamos el desp del param:
                    for p in range(len(self.ra.todos)):
                        elem = self.ra.todos[p]
                        if self.verificar_elemento(elem) and elem[0] == miPARAM:
                            desp_param = p
                            encontrado_en_ra = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_int and elem.valorInt == miPARAM:
                            desp_param = p
                            encontrado_en_ra = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_bool and elem.valorB == miPARAM:
                            desp_param = p
                            encontrado_en_ra = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_str and elem.valorStr == miPARAM:
                            desp_param = p
                            encontrado_en_ra = True

                    if not encontrado_en_ra:
                        for j in range(len(self.de.temps)):
                            idd = self.de.temps[j]
                            if self.verificar_elemento(idd) and idd[0] == nl.param[i]:
                                desp_param = j
                                donde = 'ra_de'

                    self.emite('param', nl.param[i], desp_param, antes, donde,'')

        # Caso de lambda
        elif self.sig_token.codigo in follow['V1']:
            self.register(39)
            nv1.set_tipo(Tipo.t_ok)
        else:
            self.error(self.helper_error_msg([follow['V1'], first['V1']]))
        return nv1

    # Puede ser inicializacion de una variable o una llamada a una funcion o una operacion entre parentesis
    def v(self) -> Nodo:  # Comprobar los casos que empiecen por id
        nv = Nodo()

        # Caso de llamada a funcion o postincremento
        if self.sig_token.codigo == 'id':
            # Sintactico
            id_pos = self.sig_token.atributo
            self.equipara('id')

            # Semantico comprueba que la variable existe y pasa su tipo a nv1
            id_tipo = self.gTS.buscarTipo(id_pos)
            if id_tipo == '':
                id_pos = self.set_id_tipo_global(id_pos)
                id_tipo = self.gTS.buscarTipo(id_pos)
            nv.set_tipo(id_tipo)

            '''
            for w in range(len(self.ras)):
                if self.buscarEtiqTs(id_pos) == self.ras[w][0]:
                    nv.id_func = self.buscarEtiqTs(id_pos)
            '''

            # pasa los tipos de parametros a nv1
            if nv.get_tipo() == Tipo.t_funcion:
                nv.tipoParametros = self.gTS.buscarTipoParam(id_pos)
                nv.id_func = self.buscarEtiqTs(id_pos)

            # Sintactico
            self.register(37)  # no habiamos registrado lo de V-> idV2
            nv1 = self.v1(nv)

            # Semantico
            # establece como tipo a nv el tipo de retorno la funcion o el tipo de la variable si no es una funcion
            if nv.get_tipo() == Tipo.t_funcion:
                retorno = self.gTS.buscarTipoRet(id_pos)
                #nv.set_tipo(retorno)
                nv.set_tipoRet(retorno)
            elif nv1.get_tipo() != Tipo.t_error:
                nv.set_tipo(self.gTS.buscarTipo(id_pos))
                ''' TDL '''
                if nv1.get_post() == 'post':
                    ''' TDL '''
                    # antiguo valor de id
                    antiguo_valor = self.get_lugar_id(id_pos)

                    tempPostInt = temporales()
                    if antiguo_valor != None:
                        valorPost = int(antiguo_valor) + 1
                    else:
                        valorPost = 'INC PARAM'#self.buscarVarTs(id_pos)
                        antiguo_valor = self.buscarVarTs(id_pos)
                    # valorPost = self.buscarLugarTS(id_pos) + 1
                    tempPostInt.valorInt = valorPost
                    tempPostInt.desp = len(self.ra.temporal) #self.ra.tamTemp
                    #self.ra.tamTemp += 1
                    tempPostInt.nombre = tempPostInt.nombre + str(tempPostInt.desp)


                    nv1.set_lugarInt(valorPost)
                    nv.set_lugarInt(valorPost)

                    #ANHADIR AL RA O AL DE:
                    if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
                        self.ra.todos.append(tempPostInt)
                        self.ra.temporal[tempPostInt.nombre] = valorPost
                        #ponemos bien el desp de la temporal.
                        for i in range(len(self.ra.todos)):
                            if isinstance(self.ra.todos[i], temporales) and self.ra.todos[i].nombre == tempPostInt.nombre:
                                #despBien = i
                                self.ra.todos[i].desp = i
                                break

                        parid = (self.buscarVarTs(id_pos), valorPost)
                        for i in range(len(self.ra.todos)):
                            if self.verificar_elemento(self.ra.todos[i]) and self.ra.todos[i][0] == parid[0]:
                                desp = i
                                self.ra.todos[i] = parid
                                break

                        self.cuarteto(desp,'ra','','',13)


                    else:
                        self.de.temps.append(tempPostInt)

                        parid = (self.buscarVarTs(id_pos), valorPost)
                        for i in range(len(self.de.temps)):
                            if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == parid[0]:
                                desp = i
                                self.de.temps[i] = parid
                                break

                        self.cuarteto(desp, 'de', '', '', 13)

                    nv.lugar_pr_id = self.buscarVarTs(id_pos)

                    self.set_lugar_id(id_pos, valorPost)  # seteamos el nuevo valor de id

                    self.emite(self.buscarVarTs(id_pos), '=', antiguo_valor, '+', 1, '')

                    nv1.set_post('')
                    nv.set_post('postAsig')
                    ''' TDL '''

                elif nv.get_tipo() == Tipo.t_funcion:
                    if nv.get_tipo() == Tipo.t_int:
                        self.emite(nv.get_lugarInt(), '=', 'call', self.buscarEtiqTs(id_pos), '', '')
                    if nv.get_tipo() == Tipo.t_bool:
                        self.emite(nv.get_lugarBool(), '=', 'call', self.buscarEtiqTs(id_pos), '', '')
                    if nv.get_tipo() == Tipo.t_str:
                        self.emite(nv.get_lugarStr(), '=', 'call', self.buscarEtiqTs(id_pos), '', '')

                elif nv1.get_tipo() == Tipo.t_ok:
                    miIDD = self.buscarVarTs(id_pos)
                    if nv.get_tipo() == Tipo.t_int:
                        par_id_valor = (miIDD, self.get_lugar_id(id_pos))
                        nv.set_lugarInt(par_id_valor)
                        nv.lugar_pr_id = par_id_valor
                        nv.lugar_rt_id = par_id_valor
                        nv.pasar_param = par_id_valor   # para los parametros

                    if nv.get_tipo() == Tipo.t_bool:
                        valor_id = self.get_lugar_id(id_pos)


                        if self.entro_not and not self.viene_while:
                            if valor_id == 0:
                                valor_id =1
                            elif valor_id == 1:
                                valor_id = 0
                            self.set_lugar_id(id_pos, valor_id)
                            #self.entro_not = False

                        nv.set_lugarBool(valor_id)
                        par_id_valor = (miIDD, valor_id)
                        nv.lugar_if_id = par_id_valor   # para guardar el valor del id del if si solo tiene un id dentro
                        nv.lugar_pr_id = par_id_valor   # guarda el valor del print si printea un id
                        nv.lugar_rt_id = par_id_valor
                        nv.pasar_param = par_id_valor   # para los parametros

                    if nv.get_tipo() == Tipo.t_str:
                        nv.set_lugarStr(self.get_lugar_id(id_pos))
                        par_id_valor = (miIDD, self.get_lugar_id(id_pos))
                        nv.lugar_pr_id = par_id_valor
                        nv.lugar_rt_id = par_id_valor
                        nv.pasar_param = par_id_valor   # para los parametros

            else:
                nv.set_tipo(Tipo.t_error)

        # Caso de operacion entre parentesis
        elif self.sig_token.codigo == 'openParenthesis':
            # Sintactico
            self.register(36)
            self.equipara('openParenthesis')
            ne = self.e()

            # Semantico
            nv.set_tipo(ne.get_tipo())

            ''' TDL '''
            '''
            V_lugar = E_lugar 
            '''
            if ne.get_tipo() == Tipo.t_int:
                nv.set_lugarInt(ne.get_lugarInt())
                nv.lugar_pr_id = ne.lugar_pr_id
                nv.lugar_rt_id = ne.lugar_rt_id
            if ne.get_tipo() == Tipo.t_bool:
                nv.set_lugarBool(ne.get_lugarBool())
                nv.lugar_pr_id = ne.lugar_pr_id
                nv.lugar_rt_id = ne.lugar_rt_id
                nv.lugar_if_id = ne.lugar_if_id
            if ne.get_tipo() == Tipo.t_str:
                nv.set_lugarStr(ne.get_lugarStr())
                nv.lugar_pr_id = ne.lugar_pr_id
                nv.lugar_rt_id = ne.lugar_rt_id

            ''' TDL '''

            # Sintactico
            self.equipara('closeParenthesis')

        # Caso de inicializacion de variable
        elif self.sig_token.codigo == 'CTEEntero':
            # Sintactico
            self.register(34)
            valor = self.sig_token.atributo  # se pilla bien !!!
            self.equipara('CTEEntero')

            ''' TDL '''

            tempE = temporales()
            tempE.valorInt = valor


            if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):

                tempE.count = self.ra.tamTemp
                tempE.nombre = tempE.nombre + str(tempE.count)

                self.ra.temporal[tempE.nombre] = tempE.valorInt
                self.ra.tamTemp = self.ra.tamTemp + 1
                self.ra.tamTotal = self.ra.tamTotal + 1

                tempE.desp = len(self.ra.todos)

                self.emite('temp', '1', tempE.nombre, tempE.valorInt, '', tempE.desp)

                self.ra.todos.append(tempE)

                print(self.ra.__str__())


            else:
                tempE.count = len(self.de.temps)
                tempE.nombre = tempE.nombre + str(tempE.count)
                tempE.desp = len(self.de.temps)

                self.de.temps.append(tempE)
                print('DEEEEEEEEEEEEE:  ', self.de.temps)
                self.emite('temp', '4', tempE.nombre, tempE.valorInt, '', tempE.desp)

            self.lista_temp.append(tempE)

            nv.set_lugarInt(valor)  # SE PONE BIEN TAMBIEN



            ''' TDL '''

            # Semantico
            nv.set_tipo(Tipo.t_int)


        elif self.sig_token.codigo == 'CTECadena':
            # Sintactico
            self.register(33)
            valor = self.sig_token.atributo  # pilla bien la cadena
            self.equipara('CTECadena')

            ''' TDL '''

            tempStr = temporales()
            tempStr.valorStr = valor


            if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):

                tempStr.count = self.ra.tamTemp
                tempStr.nombre = tempStr.nombre + str(tempStr.count)

                self.ra.temporal[tempStr.nombre] = tempStr.valorStr
                self.ra.tamTemp = self.ra.tamTemp + 1
                self.ra.tamTotal = self.ra.tamTotal + 1

                tempStr.desp = len(self.ra.todos)

                etiq_cadena = 'etiq_cad' + str(self.nummm)
                self.nummm += 1


                #ayuda = (tempStr.valorStr, nummm)

                #par = (etiq_cadena, ayuda)
                par = (etiq_cadena, tempStr.valorStr)

                self.etiq_cadenas.append(par)

                self.emite('tempcad', '1', tempStr.nombre, etiq_cadena, valor, tempStr.desp)

                etiq_buc = 'bucle'+str(self.num_buc)
                etiq_fin = 'fin'+str(self.num_buc)
                self.num_buc += 1


                self.cuarteto(tempStr.desp, etiq_cadena, etiq_buc, etiq_fin, 20)


                self.ra.todos.append(tempStr)

                print(self.ra.__str__())


            else:
                tempStr.count = len(self.de.temps)
                tempStr.nombre = tempStr.nombre + str(tempStr.count)
                tempStr.desp = len(self.de.temps)


                etiq_cadena = 'etiq_cad'+ str(self.nummm)
                self.nummm += 1

                par = (etiq_cadena,tempStr.valorStr)

                self.etiq_cadenas.append(par)


                self.de.temps.append(tempStr)

                self.emite('temp', '5', tempStr.nombre, etiq_cadena, valor, tempStr.desp)

                etiq_buc = 'bucle' + str(self.num_buc)
                etiq_fin = 'fin' + str(self.num_buc)
                self.num_buc += 1


                #self.cuarteto(tempStr.desp, etiq_cadena, etiq_buc, etiq_fin, 21)


                print('DEEEEEEEEEEEEE:  ', self.de.temps)

            self.lista_temp.append(tempStr)


            nv.set_lugarStr(par)

            ''' TDL '''

            # Semantico
            nv.set_tipo(Tipo.t_str)

        elif self.sig_token.codigo == 'CTEBooleano':  # Parte nueva con lo de V -> bool
            # Sintactico
            self.register(35)
            valor = self.sig_token.atributo
            self.equipara('CTEBooleano')

            ''' TDL '''
            tempB = temporales()
            if valor == 'false':
                valor = 0
            if valor == 'true':
                valor = 1
            tempB.valorB = valor


            if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion) or getattr(self, 'ra', None) is not None and isinstance(self.ra, Registro_de_activacion):

                tempB.count = self.ra.tamTemp
                tempB.nombre = tempB.nombre + str(tempB.count)

                self.ra.temporal[tempB.nombre] = tempB.valorB
                self.ra.tamTemp = self.ra.tamTemp + 1
                self.ra.tamTotal = self.ra.tamTotal + 1

                tempB.desp = len(self.ra.todos)

                self.ra.todos.append(tempB)

                print(self.ra.__str__())

                self.emite('temp', '1', tempB.nombre, tempB.valorB, '', tempB.desp)


            else:
                tempB.count = len(self.de.temps)
                tempB.nombre = tempB.nombre + str(tempB.count)
                tempB.desp = len(self.de.temps)

                self.de.temps.append(tempB)
                print('DEEEEEEEEEEEEE:  ', self.de.temps)

                self.emite('temp', '4', tempB.nombre, tempB.valorB, '', tempB.desp)

            nv.set_lugarBool(valor)


            self.lista_temp.append(tempB)



            ''' TDL '''

            # Semantico
            nv.set_tipo(Tipo.t_bool)
        else:
            self.error(self.helper_error_msg([first['V']]))
            # nv.set_tipo(Tipo.t_error)
        return nv

    # Puede ser una lista de parametros de funcion
    def l(self) -> Nodo:
        nl = Nodo()

        # Caso de lista de parametros de funcion
        if self.sig_token.codigo in first['E']:
            # Sintactico
            es_id = False
            self.register(32)
            for posible in first['E']:
                if self.sig_token.codigo == posible:
                    if posible == 'id':
                        id_pos = self.sig_token.atributo
                        es_id = True
                    nl = self.e()
                    break

            ''' TDL '''
            nl.param.clear()
            #nl.param.append(self.get_lugar_id(id_pos))
            if es_id:
                nl.param.append(self.buscarVarTs(id_pos))
            else:
                if nl.tipo[0] == Tipo.t_int:
                    nl.param.append(nl.get_lugarInt())
                elif nl.tipo[0] == Tipo.t_bool:
                    nl.param.append(nl.get_lugarBool())
                elif nl.tipo[0] == Tipo.t_str:
                    nl.param.append(nl.get_lugarStr())

            nl.long = 1

            '''
            A_param = BuscarLugarTS(id_pos) + (concatenacion) A_param
            A_long = 1
            '''
            # Semantico
            # nl.tipo += self.q().tipo

            ''' cambiado mio '''
            nq = self.q()
            nl.tipo += nq.tipo

            nl.param = nq.param
            nl.long = nl.long + nq.long

            ''' TDL '''

        # Caso funcion sin parametros
        elif self.sig_token.codigo in follow['L']:
            # Sintactico
            self.register(31)

            # Semantico
            nl.set_tipo(Tipo.t_null)
        else:
            self.error(self.helper_error_msg([first['E'], follow['L']]))
            # nl.set_tipo(Tipo.t_error)
        return nl

    # Elementos de la lista de parametros de la funcion
    def q(self) -> Nodo:
        nq = Nodo()
        # nuevo elemento
        if self.sig_token.codigo == 'coma':
            # Sintactico
            self.register(30)

            self.equipara('coma')
            id_pos = self.sig_token.atributo
            ne = self.e()

            ''' TDL '''

            #nq.param.append(self.get_lugar_id(id_pos))
            nq.param.append(ne.pasar_param[0])
            nq.long += 1
            ''' TDL '''

            # Semantico
            nq.set_tipo(ne.get_tipo())
            nq1 = self.q()
            nq.tipo += nq1.tipo

            ''' TDL '''
            nq.long = nq.long + nq1.long            # aqui pasa algo raro nq1.long tendria que ser 1 y es 0
            nq.param = nq1.param                   # CREO QUE ESTO ES INUTIL Y SOLO HABRAI QUE IGUALARLASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
            ''' TDL '''


        # No mas elementos
        elif self.sig_token.codigo in follow['Q']:
            # Sintactico
            self.register(29)

            # Semantico
            nq.set_tipo(Tipo.t_null)
        else:
            self.error(self.helper_error_msg([follow['Q'], first['Q']]))
            # nq.set_tipo(Tipo.t_error)
        return nq

    # Puede ser una asignacion o una llamada a funcion
    def s1(self, s: Nodo) -> Nodo:
        ns1 = Nodo()
        # Caso de asignacion
        if self.sig_token.codigo == 'assignment':
            # Sintactico
            self.register(28)
            self.equipara('assignment')
            ne = self.e()

            # Semantico
            # Comprueba que los tipos a ambos lados de la asignacion sean iguales
            if ne.get_tipo() == Tipo.t_error:
                ns1.set_tipo(Tipo.t_error)
            elif s.get_tipo() == ne.get_tipo() or s.get_tipo() == ne.get_tipoRet():
                if ne.get_tipo() == Tipo.t_funcion:
                    ns1.set_tipo(ne.get_tipo())
                    ns1.set_tipoRet(ne.get_tipoRet())
                    ns1.id_func = ne.id_func
                else:
                    ns1.set_tipo(Tipo.t_ok)
                    ''' TDL '''
                    if ne.get_tipo() == Tipo.t_int:
                        ns1.set_lugarInt(ne.get_lugarInt())
                    if ne.get_tipo() == Tipo.t_bool:
                        ns1.set_lugarBool(ne.get_lugarBool())
                    if ne.get_tipo() == Tipo.t_str:
                        ns1.set_lugarStr(ne.get_lugarStr())

                ns1.set_asig('asig')
                ns1.set_post(ne.get_post())
                ''' TDL '''
            else:
                ns1.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(10, self.analizador_lexico.contador_linea)

        # Caso de llamada a funcion
        elif self.sig_token.codigo == 'openParenthesis':
            # Sintactico
            self.register(27)

            # Semantico
            # Comprueba que el tipo de la variable sea una funcion
            if s.get_tipo() != Tipo.t_funcion:
                ns1.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(7, self.analizador_lexico.contador_linea)
                return ns1

            # Sinantico
            self.equipara('openParenthesis')
            nl = self.l()
            self.equipara('closeParenthesis')

            # Semantico
            # Comprueba que los tipos de los parametros de la llamada a funcion sean iguales a los de la funcion
            nl.tipo.pop()
            ns1.set_tipo(Tipo.t_ok)
            antes = 0
            for i, tipo in enumerate(nl.tipo):
                if tipo != s.tipoParametros[i]:
                    ns1.set_tipo(Tipo.t_error)
                    self.gestor_errores.addError(8, self.analizador_lexico.contador_linea)
                else:
                    miParam2 = nl.param[i]
                    desp_param2 = 0
                    donde2 = 'ra'
                    encontrado_ra_2 = False
                    if i == 0:
                        antes = 1
                    else:
                        for m in range(len(self.ras)):
                            if self.ras[m][0] == s.id_func:
                                raf = self.ras[m][1]
                                antes += raf.cabeza_ra[i][1]
                    #busacmos el desp del param
                    for p in range(len(self.ra.todos)):
                        elem = self.ra.todos[p]
                        if self.verificar_elemento(elem) and elem[0] == miParam2:
                            desp_param2 = p
                            encontrado_ra_2 = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_int and elem.valorInt == miParam2:
                            desp_param2 = p
                            encontrado_ra_2 = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_bool and elem.valorB == miParam2:
                            desp_param2 = p
                            encontrado_ra_2 = True
                        elif isinstance(elem, temporales) and nl.tipo[i] == Tipo.t_str and elem.valorStr == miParam2:
                            desp_param2 = p
                            encontrado_ra_2 = True

                    if not encontrado_ra_2:
                        for j in range(len(self.de.temps)):
                            idd = self.de.temps[j]
                            if self.verificar_elemento(idd) and idd[0] == nl.param[i]:
                                desp_param2 = j
                                donde2 = 'ra_de'

                    #self.emite('param', nl.param[i], '', '', '', '')
                    self.emite('param', nl.param[i], desp_param2, antes, donde2, '')

                ''' TDL '''

                # TENDRIA QUE ESTAR EN FOR DE 1 HASTA L.LONG, AQUI NO SE SI ESTA BIEN PUESTO

        # Caso lamda
        elif self.sig_token.codigo in follow['S1']:
            # Sintactico
            self.register(26)

            # Semantico
            ns1.set_tipo(Tipo.t_ok)
        else:
            self.error(self.helper_error_msg([follow['S1'], first['S1']]))
            # ns1.set_tipo(Tipo.t_error)
        return ns1

    # Sentencias
    def s(self) -> Nodo:
        ns = Nodo()

        # Caso de llamada a funcion o asignacion de variable
        if self.sig_token.codigo == 'id':
            # Sintactico

            id_pos = self.sig_token.atributo
            self.equipara('id')

            # Semantico

            # Comprueba que la variable exista y pasa el tipo de la variable a la funcion s1
            id_tipo = self.gTS.buscarTipo(id_pos)
            if id_tipo == '':
                self.set_id_tipo_global(id_pos)
                id_tipo = self.gTS.buscarTipo(id_pos)
            ns.set_tipo(id_tipo)

            # Si es una funcion asigna el tipo de la variable al retorno de la funcion
            if ns.get_tipo() == Tipo.t_funcion:
                ns.tipoParametros = self.gTS.buscarTipoParam(id_pos)
                ns.id_func = self.buscarEtiqTs(id_pos)

            # Sintactico
            self.register(25)
            ns1 = self.s1(ns)
            self.equipara('semicolon')

            # Semantico
            ''' TDL '''
            if ns.get_tipo() == Tipo.t_funcion:
                valor = self.buscarEtiqTs(id_pos)
                self.emite('call', ns.id_func, '', '', '','')

            elif ns1.get_asig() == 'asig' and ns1.get_post() != 'postAsig' and not self.entro_not_asig:
                if ns1.get_tipo() == Tipo.t_funcion:
                    func = ns1.id_func
                    id_ig = self.buscarVarTs(id_pos)

                    if ns.get_tipo() == Tipo.t_int:
                        self.asig_func(ns.get_tipo(), func, id_ig)

                    if ns.get_tipo() == Tipo.t_bool:
                        self.asig_func(ns.get_tipo(), func, id_ig)

                    if ns.get_tipo() == Tipo.t_str:
                        self.asig_func(ns.get_tipo(), func, id_ig)



                elif ns.get_tipo() == Tipo.t_int:
                    valorHH = ns1.get_lugarInt()
                    self.set_lugar_id(id_pos, valorHH)

                    self.emite(self.buscarVarTs(id_pos), ':=', ns1.get_lugarInt(), '', '','')

                    parid = (self.buscarVarTs(id_pos),ns1.get_lugarInt())   # par con el nd del id y lo que vale

                    if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):

                        self.ra.locales[self.buscarVarTs(id_pos)] = ns1.get_lugarInt()
                        self.ra.tamLocal = self.ra.tamLocal +1


                        self.asig_casos(parid, ns1.get_lugarInt(), id_pos, ns.get_tipo())


                    else:
                        for i in range(len(self.de.temps)):
                            if isinstance(self.de.temps[i], temporales):
                                if self.de.temps[i].valorInt == self.get_lugar_id(id_pos):
                                    despT = i
                                    temppp = self.de.temps[i].nombre
                                    break
                            else:
                                if self.de.temps[i] == self.get_lugar_id(id_pos):
                                    despT = i
                                    temppp = self.de.temps[i]
                                    break

                        for i in range(len(self.de.temps)):
                            if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == parid[0]:
                                despV = i
                                valorV = self.de.temps[i][0]
                                self.de.temps[i] = parid
                                break

                        #self.de.temps.append(parid)

                        self.emite('temp', '3', valorV, temppp, despT, despV)




                elif ns.get_tipo() == Tipo.t_bool:

                    valora = ns1.get_lugarBool()
                    self.set_lugar_id(id_pos, valora)
                    self.emite(self.buscarVarTs(id_pos), ':=', ns1.get_lugarBool(), '', '', '')
                    parid = (self.buscarVarTs(id_pos), ns1.get_lugarBool() )

                    if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):

                        self.ra.locales[self.buscarVarTs(id_pos)] = valora
                        self.ra.tamLocal = self.ra.tamLocal +1

                        self.asig_casos(parid, ns1.get_lugarBool(), id_pos, ns.get_tipo())


                    else:
                        #self.de.temps.append(parid)
                        valorF = self.get_lugar_id(id_pos)
                        for i in range(len(self.de.temps)):
                            if isinstance(self.de.temps[i], temporales):
                                if self.de.temps[i].valorB == self.get_lugar_id(id_pos):
                                    despT = i
                                    temppp = self.de.temps[i].nombre
                                    break
                            else:
                                if self.de.temps[i] == self.get_lugar_id(id_pos):
                                    despT = i
                                    temppp = self.de.temps[i]
                                    break

                        for i in range(len(self.de.temps)):
                            if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == parid[0]:
                                despV = i
                                valorV = self.de.temps[i][0]
                                self.de.temps[i] = parid
                                break

                        self.emite('temp', '3', valorV, temppp, despT, despV)



                elif ns.get_tipo() == Tipo.t_str:
                    self.set_lugar_id(id_pos, ns1.get_lugarStr())
                    self.emite(self.buscarVarTs(id_pos), ':=', ns1.get_lugarStr(), '', '', '')

                    parid = (self.buscarVarTs(id_pos), ns1.get_lugarStr() )


                    if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):

                        self.ra.tamLocal = self.ra.tamLocal + 1
                        #self.ra.locales[self.buscarVarTs(id_pos)] = ns.get_lugarStr()

                        encontrado_ra = False

                        prim = 'temp'

                        #encuentro mi temp:
                        for i in range(len(self.ra.todos)):
                            if isinstance(self.ra.todos[i], temporales) and self.ra.todos[i].valorStr == ns1.get_lugarStr()[1]:
                                despT = i
                                temppp = self.ra.todos[i].nombre
                                break
                        #encuntro mi id en ra
                        for i in range(len(self.ra.todos)):
                            if self.verificar_elemento(self.ra.todos[i]) and self.ra.todos[i][0] == parid[0]:
                                despV = i
                                valorV = self.ra.todos[i]
                                nuevopar = (parid[0], ns1.get_lugarStr()[1])
                                self.ra.todos[i] = nuevopar
                                self.ra.locales[parid[0]] = ns1.get_lugarStr()[1]
                                encontrado_ra = True
                                break

                        #si no esta en ra lo busco en de
                        if not encontrado_ra:
                            for i in range(len(self.de.temps)):
                                valorV = self.de.temps[i]
                                if self.verificar_elemento(valorV) and valorV[0] == parid[0]:
                                    despV = i
                                    nuevopar = (parid[0], ns1.get_lugarStr()[1])
                                    self.de.temps[i] = nuevopar
                                    otroPar = (self.de.locales[parid[0]][0], ns1.get_lugarStr()[1])
                                    self.de.locales[parid[0]] = otroPar
                                    prim = 'tempde'
                                    break

                        self.emite(prim, '2', self.buscarVarTs(id_pos), temppp, despT, despV)

                        #self.asig_casos(parid, ns1.get_lugarStr(), id_pos, ns1.get_tipo())

                    else:
                        #self.de.temps.append(self.buscarVarTs(id_pos))
                        for i in range(len(self.de.temps)):
                            if isinstance(self.de.temps[i], temporales):
                                if self.de.temps[i].valorStr == ns1.get_lugarStr()[1]:
                                    despT = i
                                    temppp = self.de.temps[i].nombre
                                    break
                            else:
                                if self.de.temps[i] == ns1.get_lugarStr()[1]:
                                    despT = i
                                    temppp = self.de.temps[i]
                                    break

                        for i in range(len(self.de.temps)):
                            if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == parid[0]:
                                despV = i
                                valorV = self.de.temps[i][0]
                                nuevopar = (parid[0], ns1.get_lugarStr()[1])
                                self.de.temps[i] = nuevopar
                                otroPar = (self.de.locales[parid[0]][0], ns1.get_lugarStr()[1])
                                self.de.locales[parid[0]] = otroPar
                                break

                        self.emite('temp', '3', valorV, temppp, despT, despV)
                ns1.set_asig('')

            elif ns.get_tipo() == Tipo.t_ok:  #
                if ns.get_tipo() == Tipo.t_int:
                    # no estoy seguraaa
                    ns.set_lugarInt(self.get_lugar_id(id_pos))
                if ns.get_tipo() == Tipo.t_bool:
                    # no estoy seguraaa
                    ns.set_lugarBool(self.get_lugar_id(id_pos))
                if ns.get_tipo() == Tipo.t_str:
                    # no estoy seguraaa
                    ns.set_lugarStr(self.get_lugar_id(id_pos))
            ''' TDL '''

            ns.set_tipo(ns1.get_tipo())


        # print
        elif self.sig_token.codigo == 'print':
            # Sintactico
            self.register(24)
            self.equipara('print')
            ne = self.e()  # lo puse a ne
            self.equipara('semicolon')

            # Semantico
            ns.set_tipo(Tipo.t_ok)
            ''' TDL '''
            if ne.get_tipo() == Tipo.t_int:
                self.cosa_para_pr_rt(ne.get_tipo(),ne.get_lugarInt(), ne.lugar_pr_id, 'print')

            if ne.get_tipo() == Tipo.t_bool:
                self.cosa_para_pr_rt(ne.get_tipo(), ne.get_lugarBool(), ne.lugar_pr_id, 'print')

            if ne.get_tipo() == Tipo.t_str:
                #self.cosa_para_pr_rt(ne.get_tipo(), ne.get_lugarStr(), ne.lugar_pr_id, 'print')
                if self.es_ra():
                    if ne.lugar_pr_id == None:
                        for i in range(len(self.ra.todos)):
                            if isinstance(self.ra.todos[i], temporales) and self.ra.todos[i].valorStr == ne.get_lugarStr()[1]:
                                prrr = self.ra.todos[i].nombre
                                break
                    else:
                        prrr = ne.lugar_pr_id[0]
                    self.emite('printcad', ne.get_lugarStr()[0], 'ra', prrr, 'string', '')
                else:
                    self.emite('printcad', ne.get_lugarStr()[0],'de',ne.lugar_pr_id[0],'string','')

            ''' TDL '''


        elif self.sig_token.codigo == 'input':
            # Sintactico
            self.register(23)
            self.equipara('input')
            id_pos = self.sig_token.atributo
            self.equipara('id')
            self.equipara('semicolon')

            # Semantico
            ns.set_tipo(Tipo.t_ok)

            ''' TDL '''
            #id_pos = self.sig_token.atributo
            nombre_reg = 'R'+str(self.num_reg)
            self.num_reg += 1

            if self.es_ra():
                for i in range(len(self.ra.todos)):
                    if self.verificar_elemento(self.ra.todos[i]) and self.ra.todos[i][0] == self.buscarVarTs(id_pos):
                        desp = i
                        break
                for clave in self.ra.locales:
                    if clave == self.buscarVarTs(id_pos):
                        tipo = self.ra.locales[clave][0]
                        break

                self.emite('input', self.buscarVarTs(id_pos), desp, 'ra', tipo, nombre_reg)

            else:
                for i in range(len(self.de.temps)):
                    if self.verificar_elemento(self.de.temps[i]) and self.de.temps[i][0] == self.buscarVarTs(id_pos):
                        desp = i
                        break
                for clave in self.de.locales:
                    if clave == self.buscarVarTs(id_pos):
                        tipo = self.de.locales[clave][0]
                        break

                self.emite('input', self.buscarVarTs(id_pos), desp, 'de', tipo, nombre_reg)

            ''' TDL '''


        elif self.sig_token.codigo == 'return':
            # Sintactico
            self.register(22)
            self.equipara('return')
            nx = self.x()
            self.equipara('semicolon')

            # Semantico
            if nx.get_tipo() != Tipo.t_error:
                ns.set_tipo(Tipo.t_ok)

                ''' TDL '''
                if nx.get_tipo() == Tipo.t_int:
                    self.cosa_para_pr_rt(nx.get_tipo(), nx.get_lugarInt(), nx.lugar_rt_id, 'return')
                    self.ra.VD = nx.get_lugarInt()

                if nx.get_tipo() == Tipo.t_bool:
                    self.cosa_para_pr_rt(nx.get_tipo(), nx.get_lugarBool(), nx.lugar_rt_id, 'return')
                    self.ra.VD = nx.get_lugarBool()

                if nx.get_tipo() == Tipo.t_str:
                    self.cosa_para_pr_rt(nx.get_tipo(), nx.get_lugarStr(), nx.lugar_rt_id, 'return')
                    self.ra.VD = nx.get_lugarStr()
                ''' TDL '''

            else:
                ns.set_tipo(Tipo.t_error)

            # establece el tipo de retorno
            ns.tipoRetorno = nx.get_tipo()

        else:
            self.error(self.helper_error_msg(first['S']))
            ns.set_tipo(Tipo.t_error)
            ns.tipoRetorno = ns.get_tipo()

        self.entro_not_asig = False
        self.entro_not = False

        return ns

    # Lo que sigue a un return
    def x(self) -> Nodo:
        nx = Nodo()

        # Caso de expresion
        if self.sig_token.codigo in first['E']:
            # Sintactico
            self.register(21)
            for posible in first['E']:
                if self.sig_token.codigo == posible:
                    ne = self.e()
                    # semantico
                    nx.set_tipo(ne.get_tipo())
                    ''' TDL '''
                    if ne.get_tipo() == Tipo.t_int:
                        nx.set_lugarInt(ne.get_lugarInt())
                        nx.lugar_pr_id = ne.lugar_pr_id
                        nx.lugar_rt_id = ne.lugar_rt_id
                    if ne.get_tipo() == Tipo.t_bool:
                        nx.set_lugarBool(ne.get_lugarBool())
                        nx.lugar_pr_id = ne.lugar_pr_id
                        nx.lugar_rt_id = ne.lugar_rt_id
                    if ne.get_tipo() == Tipo.t_str:
                        nx.set_lugarStr(ne.get_lugarStr())
                        nx.lugar_pr_id = ne.lugar_pr_id
                        nx.lugar_rt_id = ne.lugar_rt_id
                    ''' TDL '''

                    break

        # Caso de lambda
        elif self.sig_token.codigo in follow['X']:
            self.register(20)
            nx.set_tipo(Tipo.t_ok)
        else:
            self.error(self.helper_error_msg([first['E'], follow['X']]))
        return nx

    # Tipos
    def t(self) -> Nodo:
        nt = Nodo()
        if self.sig_token.codigo == 'int':
            # Sintactico
            self.register(19)
            self.equipara('int')

            # Semantico
            nt.set_tipo(Tipo.t_int)
            nt.set_tam(1)

        elif self.sig_token.codigo == 'boolean':
            # Sintactico
            self.register(18)
            self.equipara('boolean')

            # Semantico
            nt.set_tipo(Tipo.t_bool)
            nt.set_tam(1)

        elif self.sig_token.codigo == 'string':
            # Sintactico
            self.register(17)
            self.equipara('string')

            # Semantico
            nt.set_tipo(Tipo.t_str)
            nt.set_tam(64)


        else:
            self.error(self.helper_error_msg([first['T']]))
            # nt.set_tipo(Tipo.t_error)
        return nt

    # While, if, declaraciones y sentencias
    def b(self) -> Nodo:
        nb = Nodo()

        if self.sig_token.codigo == 'if':
            # Sintactico
            self.register(16)
            self.equipara('if')
            self.viene_while = True

            self.equipara('openParenthesis')
            ne = self.e()
            self.equipara('closeParenthesis')

            self.viene_while = False

            # Semantico

            ''' TDL '''
            nb.set_siguiente('B_siguiente'+str(self.count_sig))
            self.count_sig += 1

            ''' TDL '''

            if (ne.get_tipo() != Tipo.t_bool):
                nb.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(4, self.analizador_lexico.contador_linea)
                ''' TDL '''
            else:
                if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
                    self.id_if_while(self.ra.todos, nb.get_siguiente(), 'ra', ne.lugar_if_id[0], 'if')


                else:   # si solo son datos estaticos
                    self.id_if_while(self.de.temps, nb.get_siguiente(), 'de', ne.lugar_if_id[0], 'if')

                ''' TDL '''
            self.entro_not = False
            ns = self.s()
            nb.set_tipo(ns.get_tipo())

            ''' TDL '''
            self.emite(nb.get_siguiente(), ':', '', '', '', '')
            ''' TDL '''


        elif self.sig_token.codigo == 'let':
            self.gTS.zonadec = True
            # Sintactico
            self.register(15)
            self.equipara('let')
            id_pos = self.sig_token.atributo
            self.equipara('id')
            nt = self.t()

            # Semantico
            self.gTS.zonadec = False
            self.gTS.insertarTipo(id_pos, nt.get_tipo())
            self.gTS.insertarDesp(id_pos, nt.get_tam())
            self.equipara('semicolon')
            nb.set_tipo(nt.get_tipo())

            ''' TDL'''
            parTipoLocal = (nt.get_tipo(), None)
            paridlet = (self.buscarVarTs(id_pos),None)  # creamos el par que acabmos de leer
            if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
                self.ra.locales[self.buscarVarTs(id_pos)] = parTipoLocal # lo anhadimos a los locales
                self.ra.todos.append(paridlet)# lo anhadimos a todos
            else:
                self.de.temps.append(paridlet)
                self.de.locales[self.buscarVarTs(id_pos)] = parTipoLocal

            #self.emite('let', '', '', self.buscarVarTs(id_pos), '', '')
            ''' TDL '''

        elif self.sig_token.codigo in first['S']:
            # Sintactico
            self.register(14)
            for posible in first['S']:
                if self.sig_token.codigo == posible:
                    ns = self.s()

                    # Semantico

                    nb.set_tipo(ns.get_tipo())
                    nb.set_tipoRet(ns.get_tipoRet())

                    ''' TDL '''
                    nb.set_entro('entro')

                    if ns.get_tipo() == Tipo.t_int:
                        nb.set_lugarInt(ns.get_lugarInt())
                    if ns.get_tipo() == Tipo.t_bool:
                        nb.set_lugarBool(ns.get_lugarBool())
                    if ns.get_tipo() == Tipo.t_str:
                        nb.set_lugarStr(ns.get_lugarStr())
                    ''' TDL '''

                    break


        elif self.sig_token.codigo == 'while':
            # Sintactico
            self.register(13)
            self.equipara('while')

            ''' TDL '''
            nb.set_inicio('B_inicio'+str(self.count_ini))
            self.count_ini += 1

            nb.set_siguiente('B_siguiente'+str(self.count_sig))
            self.count_sig += 1

            self.emite(nb.get_inicio(), ':', '', '', '', '')
            ''' TDL '''

            self.viene_while = True

            # Sintactico
            self.equipara('openParenthesis')
            ne = self.e()
            self.equipara('closeParenthesis')
            self.viene_while = False


            # Semantico
            if ne.get_tipo() == Tipo.t_bool:
                nb.set_tipo(Tipo.t_ok)

                if hasattr(self, 'ra') and isinstance(self.ra, Registro_de_activacion):
                    self.id_if_while(self.ra.todos, nb.get_siguiente(), 'ra', ne.lugar_if_id[0], 'while')
                else:   # si solo son datos estaticos
                    self.id_if_while(self.de.temps, nb.get_siguiente(), 'de', ne.lugar_if_id[0], 'while')

                ''' TDL '''
                #self.emite('if', ne.get_lugarBool(), '=', '0', 'goto', nb.get_siguiente())
                ''' TDL '''

            else:
                nb.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(4, self.analizador_lexico.contador_linea)

            # Sintactico
            self.equipara('openCurly')
            ns = self.s()
            self.equipara('closeCurly')

            # Semantico
            if ns.get_tipo() == Tipo.t_error:
                nb.set_tipo(Tipo.t_error)
            else:
                nb.set_tipo(Tipo.t_ok)

                ''' TDL '''
                self.emite('goto', nb.get_inicio(), '', '', '', '')
                self.emite(nb.get_siguiente(), ':', '', '', '', '')
                ''' TDL '''

        else:
            self.error(self.helper_error_msg([first['B']]))
            # nb.set_tipo(Tipo.t_error)
        return nb

    # Definicion de funcion
    def f(self) -> Nodo:
        self.linea += 1
        nf = Nodo()
        if self.sig_token.codigo == 'function':
            self.gTS.zonadec = True
            # Sintactico
            self.register(12)
            self.equipara('function')
            id_pos = self.sig_token.atributo
            id_funcion = id_pos
            self.equipara('id')
            nh = self.h()

            tipo_H = nh.get_tipo()

            # Semantico
            self.gTS.insertarTipo(id_pos, Tipo.t_funcion)
            self.gTS.insertarTipoParam(id_pos, Tipo.t_null)
            self.gTS.crearTabla()
            self.gTS.insertarTipoRet(id_pos, nh.get_tipo())

            # Sintactico
            self.equipara('openParenthesis')
            na = self.a()
            self.equipara('closeParenthesis')

            # Semantico
            self.gTS.zonadec = False
            self.gTS.insertarTipoParam(id_pos, na.tipo)

            ''' TDL '''
            self.ra = Registro_de_activacion(0,0,1,{},self.buscarEtiqTs(id_funcion),{}, {},[],0,[], None)
            par_EM = ('EM', 1)
            self.ra.todos.append('EM')
            self.ra.cabeza_ra.append(par_EM)
            for i in range(len(na.param)):
                self.ra.locales[na.param[i]] = None
                par_param = (na.param[i], None)
                self.ra.todos.append(par_param)
                self.ra.tamLocal += 1
                self.hashmap[na.param[i]] = None
                if na.tipo[i] == Tipo.t_str:
                    desp_tipo = 32
                else:
                    desp_tipo = 1
                par_cab = (na.param[i], desp_tipo)
                self.ra.cabeza_ra.append(par_cab)

            self.ra.tamTotal = self.ra.tamLocal + self.ra.tamTotal
            iduhwd = id_funcion
            print('tabla r:' ,iduhwd)
            self.ra.tabla[self.buscarEtiqTs(id_funcion)] = self.gTS.getTabla()

            print('RAAAAAAAAAAAAAA: ', self.ra.__str__())


            # id_pos = self.sig_token.atributo
            self.emite(self.buscarEtiqTs(id_funcion), ':', '', '', '', '')

            ''' TDL '''

            # Sintactico
            self.equipara('openCurly')
            nc = self.c()
            self.gTS.destruirTabla()
            self.equipara('closeCurly')

            # Semantico
            ''' TDL '''
            if nc.get_tipoRet() == Tipo.t_null or nh.get_tipo() == Tipo.t_ok:
                self.emite('return', '_', '_', '_', '_', '_')
            ''' TDL '''

            self.ra.tamTotal = self.ra.tamLocal + self.ra.tamTemp
            print( 'RA FINAAAL : ' ,self.ra.__str__())

            par = (self.ra.etiq, self.ra)

            self.ras.append(par)

            ''' REINICILIZAR EL RA '''
            self.ra = None
            na.param = []

            if nc.get_tipoRet() == nh.get_tipo():
                nf.set_tipo(Tipo.t_ok)
            else:
                nf.set_tipo(Tipo.t_error)
                self.gestor_errores.addError(9, self.analizador_lexico.contador_linea)
        else:
            self.error(self.helper_error_msg([first['F']]))
        return nf

    # Tipo de retorno funcion
    def h(self) -> Nodo:
        nh = Nodo()

        # tipo no nulo
        if self.sig_token.codigo in first['T']:
            # Sintactico
            self.register(11)
            for posible in first['T']:
                if self.sig_token.codigo == posible:
                    nt = self.t()

                    # Semantico
                    nh.set_tipo(nt.get_tipo())
                    break
        # tipo nulo
        elif self.sig_token.codigo in follow['H']:
            # Sintactico
            self.register(10)

            # Semantico
            nh.set_tipo(Tipo.t_ok)
        else:
            self.error(self.helper_error_msg([first['T'], follow['H']]))
            # nh.set_tipo(Tipo.t_error)
        return nh

    # Lista de parametros
    def a(self) -> Nodo:
        na = Nodo()

        # lista no vacia
        na.param = []
        if self.sig_token.codigo in first['T']:
            # Sintactico
            self.register(9)
            for posible in first['T']:
                if self.sig_token.codigo == posible:
                    nt = self.t()
                    id_pos = self.sig_token.atributo
                    self.equipara('id')

                    # Semantico
                    ''' TDL '''
                    na.param.append(self.buscarVarTs(id_pos))
                    na.long = 1

                    self.gTS.insertarTipo(id_pos, nt.get_tipo())
                    self.gTS.insertarDesp(id_pos, nt.get_tam())
                    # na.tipo = nt.tipo + self.k().tipo

                    ''' cambiado mio '''
                    nk = self.k()
                    na.tipo = nt.tipo + nk.tipo
                    ''' TDL -> INITILLLLLLLLLLLLLLLLLLLLLLLLLLLLL ??????????????????'''
                    # na.param += nk.param  # concatenación de las listas
                    # na.set_long(na.get_long() + nk.get_long())
                    na.param.extend(nk.param)
                    na.long = na.long + nk.long
                    na.long = len(na.param)
                    nk.param.clear()

                    break

        # lista vacia
        elif self.sig_token.codigo in follow['A']:
            self.register(8)
            na.set_tipo(Tipo.t_null)
        else:
            self.error(self.helper_error_msg([first['T'], follow['A']]))
            na.set_tipo(Tipo.t_error)
        return na

    # Lista de parametros
    def k(self) -> Nodo:
        nk = Nodo()
        # otro parametro
        if self.sig_token.codigo == 'coma':
            # Sintactico
            self.register(7)
            self.equipara('coma')
            nt = self.t()
            id_pos = self.sig_token.atributo
            self.equipara('id')

            # Semantico
            self.gTS.insertarTipo(id_pos, nt.get_tipo())
            self.gTS.insertarDesp(id_pos, nt.get_tam())

            nk.param.append(self.buscarVarTs(id_pos))
            nk.long += 1

            # Sintactico
            nk1 = self.k()

            # Semantico
            nk.tipo = nt.tipo + nk1.tipo

            if nk1.get_tipo() != Tipo.t_null:
                nk.param = nk.param.extend(nk1.param)
                nk.long += nk1.long

        # no hay mas parametros
        elif self.sig_token.codigo in follow['K']:
            self.register(6)
            nk.set_tipo(Tipo.t_null)
        else:
            self.error(self.helper_error_msg([first['K'], follow['K']]))
            nk.set_tipo(Tipo.t_error)
        return nk

    # Lista de sentencias en la funcion
    def c(self) -> Nodo:
        nc = Nodo()
        # lista no vacia
        if self.sig_token.codigo in first['B']:
            # Sintactico
            self.register(5)
            for posible in first['B']:
                if self.sig_token.codigo == posible:
                    nb = self.b()

                    # Semantico
                    nc.set_tipo(nb.get_tipo())
                    nc.set_tipoRet(nb.get_tipoRet())

                    ''' TDL '''
                    if nb.get_entro() == 'entro':
                        if nb.get_tipo() == Tipo.t_int:
                            # self.nuevaTempInt()
                            nc.set_lugarInt(nb.get_lugarInt())
                        if nb.get_tipo() == Tipo.t_bool:
                            # self.nuevaTempBool()
                            nc.set_lugarBool(nb.get_lugarBool())
                        if nb.get_tipo() == Tipo.t_str:
                            # self.nuevaTempStr()
                            nc.set_lugarStr(nb.get_lugarStr())
                    nb.set_entro('')
                    ''' TDL '''

                    # Sintactico
                    nc1 = self.c()

                    # Semantico
                    if nc.tipoRetorno is None and (nc1.get_tipo() != Tipo.t_error or nc1.get_tipo() != Tipo.t_ok):
                        nc.set_tipoRet(nc1.get_tipoRet())
                    break

        # lista vacia
        # C -> lambda
        elif self.sig_token.codigo in follow['C']:
            self.register(4)
            nc.set_tipo(Tipo.t_ok)

        else:
            self.error(self.helper_error_msg([first['B'], follow['C']]))
        return nc

    # Axioma
    def p(self):
        np = Nodo()
        # B
        if self.sig_token.codigo in first['B']:
            # Sintactico
            self.register(3)

            if not hasattr(self, 'de') :
                self.de = datos_estaticos([], {})


            for posible in first['B']:
                if self.sig_token.codigo == posible:
                    self.b()
                    self.p()
                    break

        # Funcion
        elif self.sig_token.codigo in first['F']:
            # Sintactico
            self.register(2)
            for posible in first['F']:
                if self.sig_token.codigo == posible:
                    self.f()
                    self.p()
                    break

        # Fin
        elif self.sig_token.codigo in follow['P']:
            self.register(1)
            self.equipara('eof')

            self.cuarteto('','','','', 100)
            for i in range(len(self.etiq_cadenas)):
                self.cuarteto(self.etiq_cadenas[i][1], self.etiq_cadenas[i][0], '', '', 101)
            for i in range(len(self.ras)):
                naame = "tam_RA_"+str(self.ras[i][0])
                tam = 0
                ra_now = self.ras[i][1]
                if ra_now.VD != None:
                    par_VD = ('VD',(1, ra_now.VD))
                    ra_now.todos.append(par_VD)
                    tam += 1

                for i in range(len(ra_now.cabeza_ra)):
                    tam += ra_now.cabeza_ra[i][1]

                claves_loc = list(ra_now.locales)
                p = 0
                lista_aux = []
                for i in range(len(ra_now.cabeza_ra)-1, len(claves_loc)):
                    lista_aux.append(claves_loc[i])
                    p += 1

                for i in range(len(lista_aux)):
                    clave = lista_aux[i]
                    valor = ra_now.locales[clave]
                    if isinstance(valor, str) and valor.isdigit() or isinstance(valor, int):
                        tam += 1
                    else:
                        tam += 32

                for clave in ra_now.temporal:
                    temp_valor = ra_now.temporal[clave]
                    if isinstance(temp_valor, str) and temp_valor.isdigit() or isinstance(temp_valor, int):
                        tam += 1
                    else:
                        tam += 32


                self.cuarteto(naame, tam, '', '', 103)
                #self.ras[i][1]

            if hasattr(self, 'de') and isinstance(self.de, datos_estaticos):
                tam_de = 0
                for i in range(len(self.de.temps)):
                    elem = self.de.temps[i]
                    if self.verificar_elemento(elem) and isinstance(elem[1], int) or self.verificar_elemento(elem) and isinstance(elem[1], str) and elem[1].isdigit():
                        tam_de += 1
                    elif isinstance(elem, temporales) and elem.valorStr == '' or isinstance(elem, temporales) and elem.valorStr == None:
                        tam_de += 1
                    else:
                        tam_de += 32
                self.cuarteto(tam_de, '', '', '', 102)
            else:
                self.cuarteto('', '', '', '', 102)


        else:
            self.error(self.helper_error_msg([first['F'], first['B'], follow['P']]))

        return np

    def main(self):
        self.gTS.crearTabla()
        self.get_token()
        self.p()
        self.gestor_errores.lanzarError()
        self.gTS.destruirTabla()
        if self.sig_token.codigo != 'eof':
            self.error('eof')

    def set_id_tipo_global(self, id_pos: int) -> int:
        self.gTS.insertarTipo(id_pos, Tipo.t_int)
        self.gTS.insertarDesp(id_pos, 1)

        return id_pos

    def emite(self, string, string2, string3, string4, string5, string6):

        # con triples comillas sencillas comentas como si fuese lo de java de /* */

        # 0 -> ERROR
        # 1 -> emitir etiqueta
        # 2 -> emitir un if con goto
        # 3 -> emitir un return

        # emite de una etiqueta
        if string2 == ':' and string3 == '' and string4 == '':
            # creamos el cuarteto de una etiqueta
            # Asi metemos las cosas en el fichero
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(:,_,_, {string})\n")
            cod = 1  # para entender que queremos emitir una etiqueta
            # printeamos en un fich
            # llamamos a la funcion cuarteto

            ''' GCI '''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string}: \n")

            self.cuarteto(':', string, '', '', cod)

        if string == 'if' or string == 'while':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(if, {string2}, {string3},{ string6})\n")  # esta mal hecho
            cod = 2

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"if {string2} := {string3} goto {string6}\n")

            # cuarteto
            self.cuarteto(string4, string3, string5, string6, cod)

        if string == 'return':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(return,_,_,{string2})\n")

            if string2 != '_':
                ''' GCI'''
                with open('./output/GCI.txt', 'a') as f:
                    f.write(f"return {string2} \n")
                # llamamos a cuarteto
                cod = 3
                self.cuarteto(string, '', string6, string2, cod)
            else:
                ''' GCI'''
                with open('./output/GCI.txt', 'a') as f:
                    f.write(f"return \n")
                cod = 32

                self.cuarteto(string, '', string6, string2, cod)

        if string == 'print' or string == 'printcad':
            if string == 'printcad':
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(print,_,_, {string4})\n")
            else:
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(print,_,_, {string2})\n")            # aqui me imprime una temporal pero quiero x ARREGLAR

            cod = 4

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"print  {string2}  \n")

            # llamamos a cuarteto
            if string5 == 'string':
                self.cuarteto(string3, string2, string5, string6, cod)
            else:
                self.cuarteto(string3, string4, string5, string6, cod)

        if string == 'input':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(input,_,_, {string2})\n")

            cod = 5
            self.cuarteto(string3, string4, string5, string6, cod)

        if string == 'callAsig1' or string == 'callAsig32':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(call,{string4},_, {string3})\n")

            cod = 6

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string3} (o temp nose) := {string4} /  TENDRIA QUE SER UNA TEMP -> VER LUEGO COMO HACER )\n")

            # llamamos a cuarteto
            if string == 'callAsig1':
                cod = 61
            else:
                cod = 632

            self.cuarteto(string5, string6, string4 , string2, cod)

        if string == 'param':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"({string},{string2},_,_)\n")

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"param {string2} ( o temp no se) )\n")

            cod = 7
            self.cuarteto(string, string2, string3, string4, cod)

        if string2 == '<':
            cod = 8
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(<,{string},{string3},_)\n")

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string} <  {string3} ( o temp no se) \n")

            self.cuarteto('<', string, string3, '_', cod)

        if string3 == 'not':
            cod = 9
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(:= ,not,_,{string})\n")

            ''' GCI '''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f" {string3} not  {string3} ( o temp no se) \n")

            self.cuarteto(string6, string5, '', '', cod)

        if string2 == ':=' and string4 == '-':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"({string4},{string3},{string5},{string})\n")
            # self.cuartetos += '(-,' + string3 + ',' + string5 + ',' + string + ')'
            cod = 10

            ''' GCI '''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"temp := {string3} -  {string5} \n")
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string} := temp )\n")
            # llamamos a cuarteto
            self.cuarteto('-', string3, string5, string, cod)

        if string2 == 'igResta':
            cod = 24
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(-,{string3},{string5},{string})\n")

            #self.cuarteto(string3, string4, string5, string6, cod)


        if string2 == ':=' and string4 == '<':
            cod = 11
            with open('./output/emites.txt', 'a') as f:
                f.write(f"({string4},{string3},{string5},{string})\n")

            ''' GCI '''
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"temp := {string3} <  {string5}\n")
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"  {string} := temp\n")

            self.cuarteto(string4, string3, string5, string, cod)

        '''
        if string2 == ':=':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(:=,{string3},_, {string})\n")
            cod = 12

            # llamamos a cuarteto
            self.cuarteto(':=', string3, '_', string, cod)
        '''

        if string4 == '+':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(+,{string3},{string5}, {string})\n")
            cod = 13

            with open('./output/GCI.txt', 'a') as f:
                f.write(f"temp := {string3} + 1   \n")
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string} := temp \n")


            #self.cuarteto(string4, string3, string5, string, cod)

        if string == 'goto':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(goto,_,_,{string2}\n")
            cod = 14

            with open('./output/GCI.txt', 'a') as f:
                f.write(f" goto {string3} \n")

            # llamamos a cuarteto
            self.cuarteto('goto', '', '', string2, cod)

        if string == 'call' and string3 == '':
            print('ENTRAS DONDE YO QUIERO ????')
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(call,{string2},_,_)\n")

            cod = 15

            ''' GCI'''
            with open('./output/GCI.txt', 'a') as f:
                f.write(
                    f" call {string2}  \n")

            # llamamos a cuarteto
            self.cuarteto('call', string2, '_', '_', cod)

        if string == 'temp' and string2 == '1' or string == 'tempcad' and string2 == '1':
            if string == 'tempcad':
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(:=, {string5},_,{string3})\n")
            else:
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(:=, {string4},_,{string3})\n")

            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string3} := {string4}   \n")

            cod = 16

            #if string5 != 'cad':
            self.cuarteto(string3, string4,'_',string6,cod)

        if string2 == '2' and string == 'temp' or string == 'tempde':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(:=, {string4},_,{string3})\n")

            if string == 'temp':
                cod = 17
                with open('./output/GCI.txt', 'a') as f:
                    f.write(f"{string3} := {string4}   \n")
                self.cuarteto(string3, string4, string5, string6, cod)

            else:
                cod = 172
                with open('./output/GCI.txt', 'a') as f:
                    f.write(f"{string3} := {string4}   \n")
                self.cuarteto(string3, string4, string5, string6, cod)


        if string == 'temp' and string2 == '3':
            cod = 18
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(:=, {string4},_,{string3})\n")
            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string3} := {string4}   \n")

            self.cuarteto(string3, string4, string5, string6, cod)

        if string == 'temp' and string2 == '4' or string == 'temp' and string2 == '5':
            cod = 19
            if string2 == '5':
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(:=, {string5},_,{string3})\n")
            else:
                with open('./output/emites.txt', 'a') as f:
                    f.write(f"(:=, {string4},_,{string3})\n")

            with open('./output/GCI.txt', 'a') as f:
                f.write(f"{string3} := {string4}   \n")

            #if string5 != 'cad':
            self.cuarteto(string3, string4, string5, string6, cod)

        '''
        if string == 'while':
            with open('./output/emites.txt', 'a') as f:
                f.write(f"(if,{string2},:=,)\n")
        '''





    #def GCI(self, ):

    def cuarteto(self, string1, string2, string3, string4, cod):
        if self.primer == 0:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  ORG 0\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #inicio_estaticas, .IY\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #inicio_pila, .IX\n")
                f.write(f"\n \n")
            self.primer = 1

        if cod == 1:
            # co de emitir una etiqueta:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"{string2}:\n")

        if cod == 2:
            if string1 == 'de':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  CMP #{string3}[.IY], #{string2}\n")
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  BZ ${string4}\n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  CMP #{string3}[.IX], #{string2}\n")
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  BZ ${string4}\n")


        if cod == 3:
            # return
            if string3 == 'string':
                tipo = 32
            else:
                tipo = 1

            with open('./output/CO.ens', 'a') as f:
                f.write(f"  SUB #tam_RA_{self.ra.etiq}, #{tipo}\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  ADD .A, .IX\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string3}[.IX], [.A]\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  BR[.IX]\n")

        if cod == 32:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  BR [.IX]\n")

        if cod == 4:
            # print
            if string1 == 'de' or string1 == 'ra_de':
                if string3 == 'string':
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  WRSTR /{string2}\n")

                elif isinstance(string3, str) and string3[0].isdigit() or isinstance(string3, int) or string2 == Tipo.t_int or string2 == Tipo.t_bool:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  WRINT #{string4}[.IY]\n")


            else:
                if string3 == 'string' or string2 == Tipo.t_str:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  WRSTR /{string2}\n")

                elif isinstance(string3, str) and string3[0].isdigit() or isinstance(string3, int) or string2 == Tipo.t_int or string2 == Tipo.t_bool:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  WRINT #{string4}[.IX]\n")


        if cod == 5:
            if string2 == 'ra':
                if string3[0].isdigit():
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  ININT .{string4}\n")
                        f.write(f"  MOVE .[{string4}], #{string1}[.IX]\n")
                else:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  INSTR #{string1}[.IX]\n")
            else:
                if string3 == Tipo.t_int or string3 == Tipo.t_bool:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  ININT .{string4}\n")
                        f.write(f"  MOVE .[{string4}], #{string1}[.IY]\n")
                else:
                    with open('./output/CO.ens', 'a') as f:
                        f.write(f"  INSTR #{string1}[.IY]\n")

        if cod == 6 or cod == 61 or cod == 632:
            # call y asignacion
            if cod == 61:
                tipo = 1
            elif cod == 623:
                tipo = 32

            with open('./output/CO.ens', 'a') as f:
                dirr = "dir_ret"+str(self.count_diret)
                self.count_diret += 1

                f.write(f"  MOVE #{dirr}, #tam_RA_{self.ra.etiq}[.IX]\n")
                f.write(f"  ADD #tam_RA_{self.ra.etiq}, .IX\n")
                f.write(f"  MOVE .A, .IX\n")
                f.write(f"  BR ${string3}\n")
                f.write(f"{dirr}: \n")
                f.write(f"  SUB #tam_RA_{self.ra.etiq}, #{tipo} \n")
                f.write(f"  ADD .A, .IX \n")
                f.write(f"  MOVE [.A], [.R9] \n")
                f.write(f"  SUB .IX, #tam_RA_{self.ra.etiq} \n")
                f.write(f"  MOVE .A, .IX         \n")
                f.write(f"  MOVE .R9, #{string2}[.IX]        \n")
            if string4 == 'de':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  MOVE #{string2}[.IX], #{string1}[.IY]        \n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  MOVE #{string2}[.IX], #{string1}[.IX]        \n")


        if cod == 7:
            # param
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  ADD #tam_RA_{self.ra.etiq}, .IX             ; params \n")
                f.write(f"  ADD #{string4}, .A                          ; params  \n")
                f.write(f"  MOVE #{string3}[.IX], [.A]                  ; params  \n")

        if cod == 8:
            # menor
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  CMP {string2},{string3}\n")

        if cod == 9:
            # NOT
            if string1 == 'ra':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  NOT #{string2}[.IX]\n")
                    #f.write(f"MOVE .A, {string4}\n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  NOT #{string2}[.IY]\n")


        if cod == 10:
            # resta
            with open('./output/CO.ens', 'a') as f:
                f.write(f"SUB {string2},{string3}\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"MOVE .A, {string4}\n")

        if cod == 11:
            # menor y asignacion
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  CMP {string2},{string3}\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  BP /mayor\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #1,{string4}\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  BR /sig\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  mayor: MOVE #0,{string4}\n")
            with open('./output/CO.ens', 'a') as f:
                f.write(f"sig:\n")

        if cod == 12:
            # asignacion
            '''
            with open('./output/CO.ens', 'a') as f:
                f.write(f"MOVE #{string2}, {string4}\n")
            '''


        if cod == 13:
            # ++
            if string2 == 'ra':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  INC #{string1}[.IX] \n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  INC #{string1}[.IY] \n")

        if cod == 14:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"BR ${string4}\n")

        if cod == 15:
            dirr2 = 'dir_ret'+str(self.count_diret)
            self.count_diret += 1

            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{dirr2}, #tam_RA_{self.ra.etiq}[.IX]          ; call \n")
                f.write(f"  ADD #tam_RA_{self.ra.etiq}, .IX\n")
                f.write(f"  MOVE .A, .IX \n")
                f.write(f"  BR ${string2}\n")

                f.write(f"{dirr2}: \n")
                f.write(f"  SUB #tam_RA_{self.ra.etiq}, .IX\n")
                f.write(f"  MOVE .A, .IX\n")


        if cod == 16:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string2}, #{string4}[.IX] \n")

        if cod == 17:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string3}[.IX], #{string4}[.IX]\n")

        if cod == 172:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string3}[.IX], #{string4}[.IY]\n")

        if cod == 18:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string3}[.IY], #{string4}[.IY] \n") # aqui seriaaa he inversado los desp

        if cod == 19:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string2}, #{string4}[.IY] \n")

        if cod == 24:
            if string3 == 'RESTARA':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  SUB #{string1}[.IX], #{string2}[.IX] \n")
            if string3 == 'RESTARADE1':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  SUB #{string1}[.IY], #{string2}[.IX] \n")
            if string3 == 'RESTARADE2':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  SUB #{string1}[.IX], #{string2}[.IY] \n")
            if string3 == 'RESTARADE3':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  SUB #{string1}[.IY], #{string2}[.IY] \n")

        if cod == 25:
            if string1 == 'RESTARA':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  MOVE .A, #{string2}[.IX] \n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"  MOVE .A, #{string2}[.IY] \n")



        '''
        if cod == 20:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string1}[.IX], .R2 \n")
                f.write(f"  MOVE #{string2}, .R3 \n")
                f.write(f"{string3}: \n")
                f.write(f"  CMP [.R3], #0\n")
                f.write(f"  BZ ${string4} \n")
                f.write(f"  MOVE [.R3], [.R2] \n")
                f.write(f"  INC .R2 \n")
                f.write(f"  INC .R3 \n")
                f.write(f"  BR ${string3} \n")
                f.write(f"{string4}: \n")
                f.write(f"  MOVE [.R3], [.R2] \n")
                #f.write(f"  BR [.IX] \n")
                #f.write(f"  MOVE #{string1}[.IX], #NOSEEE?[.R2] \n")
        '''


        ''' ESO ES PARA EL INPUT DEL STRING CREOO 
        if cod == 21:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"  MOVE #{string1}[.IY], .R2 \n")
                f.write(f"  MOVE #{string2}, .R3 \n")
                f.write(f"{string3}: \n")
                f.write(f"  CMP [.R3], #0\n")
                f.write(f"  BZ ${string4} \n")
                f.write(f"  MOVE [.R3], [.R2] \n")
                f.write(f"  INC .R2 \n")
                f.write(f"  INC .R3 \n")
                f.write(f"  BR ${string3} \n")
                f.write(f"{string4}: \n")
                f.write(f"  MOVE [.R3], [.R2] \n")
                #f.write(f"  BR [.IY] ;??? \n")
                #f.write(f"  MOVE #{string1}[.IY], #NOSEEE?[.R2] \n")
        '''



        if cod == 100:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"\n \n")
                f.write(f"  ORG 1000\n")
                f.write(f"\n \n")
                f.write(f"; cadenas y Tam_RAs \n")

        if cod == 101:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"{string2}:    DATA {string1} \n")

        if cod == 103:
            with open('./output/CO.ens', 'a') as f:
                f.write(f"{string1}:    EQU {string2} \n")

        if cod == 102:
            if string1 == '':
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"\n \n")
                    f.write(f"inicio_estaticas:     RES 0 \n")
                    f.write(f"inicio_pila:          NOP \n")
                    f.write(f"                      END\n")
            else:
                with open('./output/CO.ens', 'a') as f:
                    f.write(f"\n \n")
                    f.write(f"inicio_estaticas:     RES {string1} \n")
                    f.write(f"inicio_pila:          NOP \n")
                    f.write(f"                      END\n")

