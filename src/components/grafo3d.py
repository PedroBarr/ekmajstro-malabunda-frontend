import flet as ft
import flet.canvas as fc

import asyncio
import math
import random as rd
import time
from typing import Dict, List

from themes import estilos_config

class Grafo3D(ft.Container):

    class Nodo:
        def __init__(
            self,
            id: str,
            x: float,
            y: float,
            z: float,
            d: float = 1, # distancia al nodo central
            c: ft.Colors = ft.Colors.BLUE, # color del nodo
            s: float = 10, # tamaño del nodo
            i: Dict = {}, # información adicional del nodo
        ):
            self.id = id
            self.x = x
            self.y = y
            self.z = z
            self.d = d
            self.c = c
            self.s = s
            self.i = i
    
    class Lazo:
        def __init__(
            self,
            nodo: "Grafo3D.Nodo",
            nodo_conectado: "Grafo3D.Nodo",
            c: ft.Colors = ft.Colors.GREY, # color del lazo
            i: Dict = {}, # información adicional del lazo
        ):
            self.nodo = nodo
            self.nodo_conectado = nodo_conectado
            self.c = c
            self.i = i
        
    def __init__(
        self,
        grafo: Dict[str, List],
        dimensiones_iniciales=(800, 600),
        escala_inicial: float = 100,
        angulo_acimut_inicial: float = 45,
        angulo_elevacion_inicial: float = 30,
        al_repintar=lambda: None,
        **parametros
    ):
        super().__init__(**parametros)
        self._personas = grafo.get('nodos', [])
        self._relaciones = grafo.get('enlaces', [])
        
        self._dimensiones = dimensiones_iniciales

        self._canvas = fc.Canvas(
            width=self._dimensiones[0],
            height=self._dimensiones[1],
            on_resize=lambda e: self._actualizar_dimensiones(e.control.width, e.control.height),
        )
        self._centro = (self._dimensiones[0] / 2, self._dimensiones[1] / 2)

        self._escala_inicial = escala_inicial
        self._angulo_acimut_inicial = angulo_acimut_inicial
        self._angulo_elevacion_inicial = angulo_elevacion_inicial

        self._escala = escala_inicial
        self._angulo_acimut = angulo_acimut_inicial
        self._angulo_elevacion = angulo_elevacion_inicial

        self._nodos = {}
        self._nodo_central = None
        self._lazos = []

        self._al_repintar = al_repintar
        self._ultimo_dibujo = 0
        self._ms_entre_dibujos = 1000

        self._calcular_nodos()
        self._calcular_zona_acercamiento()

        self._bocadillo = ft.Container(
            content=ft.Text("", color=ft.Colors.WHITE, size=12),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            border_radius=8,
            padding=10,
            visible=False,
            animate_position=150, # Suaviza el movimiento
        )

    def _calcular_nodos(self):
        personas = {}
        for persona in self._personas:
            if persona.get('prior', False):
                self._nodo_central = self.Nodo(
                    id=persona.get('id'),
                    x=0,
                    y=0,
                    z=0,
                    s=15,
                    c='#FF9984',
                    i=persona.get('personaId', {})
                )
            else:
                personas[persona.get('id')] = persona
        
        assert self._nodo_central is not None, \
            "No se encontró un nodo central en el grafo."
        
        self._contador_tipos_relaciones = {}

        for relacion in self._relaciones:
            tipo = relacion.get('tipo', 'desconocido')
            self._contador_tipos_relaciones[tipo] = self._contador_tipos_relaciones.get(tipo, 0) + 1
            persona_conectada = personas[relacion.get('target')]
            nodo_conectado = self.Nodo(
                id=persona_conectada.get('id'),
                x=0,
                y=0,
                z=0,
                s=10,
                c=estilos_config['tipos_relacion'].get(tipo, {}).get('color', ft.Colors.GREY),
                i=persona_conectada.get('personaId', {})
            )
            lazo = self.Lazo(
                nodo=self._nodo_central,
                nodo_conectado=nodo_conectado,
                c=estilos_config['tipos_relacion'].get(tipo, {}).get('borde', ft.Colors.GREY),
                i=relacion
            )
            self._lazos.append(lazo)
            self._nodos[nodo_conectado.id] = nodo_conectado
        
        self._conteo_tipos_relaciones = len(self._contador_tipos_relaciones.keys())

        self._posicionar_nodos()
        self._colisiones = {}

    def _posicionar_nodos(self):
        self._posiciones = {}
        
        if self._conteo_tipos_relaciones == 0: return
        
        delta_phi = math.pi / (self._conteo_tipos_relaciones)

        for i, tipo in enumerate(self._contador_tipos_relaciones):
            self._posiciones[tipo] = []
            phi = i * delta_phi
            for k in range(self._contador_tipos_relaciones[tipo]):
                n = self._contador_tipos_relaciones[tipo]
                theta = k * (2 * math.pi / n) if n > 0 else 0
                r = rd.random() * 3 + 1.5

                x = r * math.cos(theta) * math.cos(phi)
                y = r * math.sin(theta)
                z = r * math.cos(theta) * math.sin(phi)

                self._posiciones[tipo].append((x, y, z))

    def _proyectar(self, x, y, z, incluir_z_ord=False):
        radianes_acimut = math.radians(self._angulo_acimut)
        radianes_elevacion = math.radians(self._angulo_elevacion)

        x_acimut = x * math.cos(radianes_acimut) - y * math.sin(radianes_acimut)
        y_acimut = x * math.sin(radianes_acimut) + y * math.cos(radianes_acimut)

        x_2d = x_acimut
        y_2d = y_acimut * math.cos(radianes_elevacion) - z * math.sin(radianes_elevacion)
        z_ord = y_acimut * math.sin(radianes_elevacion) + z * math.cos(radianes_elevacion)

        x_2d_escalado = x_2d * self._escala + self._centro[0]
        y_2d_escalado = y_2d * self._escala + self._centro[1]

        proyeccion = (
            (x_2d_escalado, y_2d_escalado)
            if not incluir_z_ord else
            (x_2d_escalado, y_2d_escalado, z_ord)
        )
    
        return proyeccion
    
    def _dibujar_ejes(self):
        limite_eje = max(self._dimensiones) / self._escala
        opacidad = 0.2

        origen = self._proyectar(0, 0, 0)
        eje_x = self._proyectar(limite_eje, 0, 0)
        eje_nx = self._proyectar(-limite_eje, 0, 0)
        eje_y = self._proyectar(0, limite_eje, 0)
        eje_ny = self._proyectar(0, -limite_eje, 0)
        eje_z = self._proyectar(0, 0, limite_eje)
        eje_nz = self._proyectar(0, 0, -limite_eje)

        xc = ft.Colors.with_opacity(opacidad, ft.Colors.RED)
        yc = ft.Colors.with_opacity(opacidad, ft.Colors.GREEN)
        zc = ft.Colors.with_opacity(opacidad, ft.Colors.BLUE)

        ejes = [
            fc.Line(
                *origen,
                *eje_x,
                paint=ft.Paint(color=xc, stroke_width=2, stroke_dash_pattern=[4, 2])
            ),
            fc.Line(
                *origen,
                *eje_nx,
                paint=ft.Paint(color=xc, stroke_width=2, stroke_dash_pattern=[4, 2])
            ),
            fc.Line(
                *origen,
                *eje_y,
                paint=ft.Paint(color=yc, stroke_width=2, stroke_dash_pattern=[4, 2])
            ),
            fc.Line(
                *origen,
                *eje_ny,
                paint=ft.Paint(color=yc, stroke_width=2, stroke_dash_pattern=[4, 2])
            ),
            fc.Line(
                *origen,
                *eje_z,
                paint=ft.Paint(color=zc, stroke_width=2, stroke_dash_pattern=[4, 2])
            ),
            fc.Line(
                *origen,
                *eje_nz,
                paint=ft.Paint(color=zc, stroke_width=2, stroke_dash_pattern=[4, 2])
            )
        ]

        self._canvas.shapes.extend(ejes)

    def dibujar_nodo(self, nodo: Nodo):
        proyeccion = self._proyectar(nodo.x, nodo.y, nodo.z, incluir_z_ord=True)

        representacion = {
            'tipo': 'nodo',
            'z_ord': proyeccion[2] if len(proyeccion) > 2 else 0,
            'representacion': fc.Circle(
                x=proyeccion[0],
                y=proyeccion[1],
                radius=nodo.s,
                paint=ft.Paint(color=nodo.c)
            )
        }
        
        self._instrucciones_representacion.append(representacion)

        self._agregar_colision_nodo(representacion, nodo)

    def _agregar_colision_nodo(self, representacion, nodo):
        colision = {
            'nodo': nodo,
            'representacion': representacion
        }

        tope = representacion['representacion'].y - representacion['representacion'].radius
        bajo = representacion['representacion'].y + representacion['representacion'].radius
        diestra = representacion['representacion'].x + representacion['representacion'].radius
        siniestra = representacion['representacion'].x - representacion['representacion'].radius

        caja_colision = ':'.join([str(punto) for punto in [tope, bajo, diestra, siniestra]])
        self._colisiones[caja_colision] = colision

    def _asignar_posicion_nodo(
        self,
        nodo: Nodo,
        tipo: str,
        indice: int,
    ):
        posicion = self._posiciones[tipo][indice]
        nodo.x = posicion[0]
        nodo.y = posicion[1]
        nodo.z = posicion[2]

    def dibujar_lazo(self, lazo: Lazo, contador_tipos_relaciones):
        nodo = lazo.nodo
        nodo_conectado = lazo.nodo_conectado
        tipo = lazo.i.get('tipo', 'desconocido')
        indice = contador_tipos_relaciones[tipo]
        self._asignar_posicion_nodo(nodo_conectado, tipo, indice)

        proyeccion_nodo = self._proyectar(nodo.x, nodo.y, nodo.z)
        proyeccion_conectado = self._proyectar(nodo_conectado.x, nodo_conectado.y, nodo_conectado.z, incluir_z_ord=True)

        representacion = {
            'tipo': 'lazo',
            'z_ord': proyeccion_conectado[2] if len(proyeccion_conectado) > 2 else 0,
            'representacion': fc.Line(
                x1=proyeccion_nodo[0],
                y1=proyeccion_nodo[1],
                x2=proyeccion_conectado[0],
                y2=proyeccion_conectado[1],
                paint=ft.Paint(color=lazo.c, stroke_width=2)
            )
        }

        self._instrucciones_representacion.append(representacion)

        self.dibujar_nodo(nodo_conectado)

        contador_tipos_relaciones[tipo] += 1

    def _dibujar_red(self):
        self._instrucciones_representacion = []
        self._colisiones = {}
        
        contador_tipos_relaciones = {
            tipo: 0
            for tipo in self._contador_tipos_relaciones.keys()
        }

        self.dibujar_nodo(self._nodo_central)

        for lazo in self._lazos:
            self.dibujar_lazo(lazo, contador_tipos_relaciones)
        
        self._instrucciones_representacion.sort(key=lambda instr: instr['z_ord'], reverse=True)
        
        for instruccion in self._instrucciones_representacion:
            self._canvas.shapes.append(instruccion['representacion'])

    def dibujar(self):
        ahora = time.time() * 1000
        
        if ahora - self._ultimo_dibujo < self._ms_entre_dibujos: return
        
        self._ultimo_dibujo = ahora
        self._canvas.shapes.clear()
        
        self._dibujar_ejes()
        self._dibujar_red()
        self._al_repintar()

    def _calcular_zona_acercamiento(self):
        self._zona_acercamiento = (
            (self._dimensiones[0] // 4, 3 * self._dimensiones[0] // 4),
            (self._dimensiones[1] // 4, 3 * self._dimensiones[1] // 4)
        )

    def _actualizar_dimensiones(self, ancho, alto):
        self._dimensiones = (ancho, alto)
        self._centro = (ancho / 2, alto / 2)
        self._calcular_zona_acercamiento()
        self.dibujar()

    def _al_clic(self, evento: ft.TapEvent):
        if (
            self._zona_acercamiento[0][0] <= evento.local_position.x <= self._zona_acercamiento[0][1] and
            self._zona_acercamiento[1][0] <= evento.local_position.y <= self._zona_acercamiento[1][1]
        ):
            self._escala *= 1.2
        else:
            if evento.local_position.x < self._zona_acercamiento[0][0]:
                self._angulo_acimut -= 15
            elif evento.local_position.x > self._zona_acercamiento[0][1]:
                self._angulo_acimut += 15
            
            if evento.local_position.y < self._zona_acercamiento[1][0]:
                self._angulo_elevacion += 15
            elif evento.local_position.y > self._zona_acercamiento[1][1]:
                self._angulo_elevacion -= 15

        self.dibujar()

    def _al_rodar_mouse(self, evento: ft.ScrollEvent):
        if evento.scroll_delta.y > 0:
            self._escala *= 1.1
        elif evento.scroll_delta.y < 0:
            self._escala *= 0.9

        self.dibujar()

    def _al_apretar_largo(self, _: ft.ControlEventHandler):
        self._escala = self._escala_inicial
        self._angulo_acimut = self._angulo_acimut_inicial
        self._angulo_elevacion = self._angulo_elevacion_inicial
        
        self.dibujar()

    def _al_doble_clic(self, evento: ft.TapEvent):
        x = evento.local_position.x
        y = evento.local_position.y

        for caja_colision, colision in self._colisiones.items():
            tope, bajo, diestra, siniestra = map(float, caja_colision.split(':'))
            if siniestra <= x <= diestra and tope <= y <= bajo:
                nodo = colision['nodo']

                info = nodo.i
                texto_info = info.get('nombre', '') + ' ' + info.get('apellido', '')
                
                if texto_info.strip() == '':
                    texto_info = 'Información no disponible'

                self._bocadillo.content.value = texto_info
                self._bocadillo.x = 10
                self._bocadillo.y = 10
                self._bocadillo.visible = True

                asyncio.create_task(self._ocultar_bocadillo_temporalmente())
                
                break
            else:
                self._bocadillo.visible = False
    
    async def _pre_doble_clic(self, evento: ft.TapEvent):
        await ft.BrowserContextMenu().disable()
    
    def _al_clic_derecho(self, evento: ft.ControlEventHandler):
        self._escala *= 0.8
        self.dibujar()

    async def _pos_clic_derecho(self, evento: ft.ControlEventHandler):
        await ft.BrowserContextMenu().enable()

    async def _ocultar_bocadillo_temporalmente(self):
        await asyncio.sleep(2)
        self._bocadillo.visible = False
        self._al_repintar()

    def _al_actualizar_dimensiones(self, evento: ft.DragUpdateEvent):
        delta_x = evento.local_delta.x
        delta_y = evento.local_delta.y

        self._angulo_acimut += delta_x * 0.5
        self._angulo_elevacion += delta_y * 0.5

        self.dibujar()

    def construir(self):
        if (
            not self._personas
        ):
            return ft.Container(
                ft.Text(
                    "No se encontraron nodos para mostrar.",
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
        
        return ft.Stack(
            controls=[
                ft.GestureDetector(
                    content=self._canvas,
                    on_tap=self._al_clic,
                    on_scroll=self._al_rodar_mouse,
                    on_long_press=self._al_apretar_largo,
                    on_double_tap_down=self._al_doble_clic,
                    on_pan_update=self._al_actualizar_dimensiones,
                    on_secondary_tap=self._al_clic_derecho,
                    on_secondary_tap_down=self._pre_doble_clic,
                    on_secondary_tap_up=self._pos_clic_derecho,
                ),
                self._bocadillo,
            ],
        )