class Procesador:

    """
    Procesador realiza un procesado de los resultados obtenidos en la solicitud, retornándolos en un formato amigable para ser analizados.
    Sin atributos

    """

    # def _procesar_item(self, resultados: dict) -> list:
    #     resultados_limpios = []
    #     for i in resultados:
    #         item = {}
    #         item['titulo'] = i['title']
    #         item['precio'] = i['price']
    #         item['provincia'] = i['location']['state']['name']
    #         item['']
    #         print(i['title'])
    #         break

    def _procesar_inmuebles(self, resultados:dict) -> list:
            atributos_inmuebles = [
                ('HAS_AIR_CONDITIONING', 'aire_acondicionado'),
                ('HAS_TELEPHONE_LINE', 'linea_telefonica'),
                ('BEDROOMS', 'dormitorios'),
                ('COVERED_AREA', 'metros_cubiertos'),
                ('FULL_BATHROOMS', 'banios'),
                ('ROOMS', 'ambientes'),
                ('TOTAL_AREA', 'metros_totales'),
                ('OPERATION', 'operacion'),
                ('PROPERTY_TYPE', 'tipo_propiedad'),
                ('ITEM_CONDITION', 'condicion'),
                ('WITH_VIRTUAL_TOUR', 'virtual_tour')
            ]
            
            inmuebles = []

            for i in range(len(resultados)):
                inmueble = {
                    'titulo': resultados[i]['title'],
                    'precio': resultados[i]['price'],
                    'provincia': resultados[i]['location']['state']['name'],
                    'idprovincia': resultados[i]['location']['state']['id'],
                    'localidad': resultados[i]['location']['city']['name'],
                    'idlocalidad': resultados[i]['location']['city']['id'],
                    'direccion': resultados[i]['location']['address_line'],
                    'latitud': resultados[i]['location']['latitude'],
                    'longitud': resultados[i]['location']['longitude'],
                    'fecha_finalizacion': resultados[i]['stop_time']
                }
                for j in range(len(resultados[i]['attributes'])):
                    atributo_inmuebles = resultados[i]['attributes'][j]['id']
                    for atributo_resp, atributo_clase in atributos_inmuebles:
                        if atributo_resp == atributo_inmuebles:
                            if atributo_resp == 'TOTAL_AREA' or atributo_resp == 'COVERED_AREA':
                                inmueble[atributo_clase] = resultados[i]['attributes'][j]['value_struct']['number']
                            else:
                                try:
                                    inmueble[atributo_clase] = resultados[i]['attributes'][j]['values'][0]['name']
                                except:
                                        inmueble[atributo_clase] = resultados[i]['attributes'][j]['value_struct']['number']

                inmuebles.append(inmueble)
            
            return inmuebles
