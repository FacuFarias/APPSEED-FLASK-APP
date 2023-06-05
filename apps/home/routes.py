# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import mysql.connector
import datetime


@blueprint.route('/actualizar', methods=['POST'])
def actualizar():
    # Obtener el valor seleccionado del formulario
    color = request.form['color']
    print(color)

    """# Conexión a la base de datos
    conn = mysql.connector.connect(**db_config)

    # Cursor para ejecutar consultas
    cursor = conn.cursor()

    # Consulta para actualizar las filas en la base de datos
    sql = "UPDATE nombre_de_tu_tabla SET columna_color = %s"

    # Ejecutar la consulta con el valor seleccionado
    cursor.execute(sql, (color,))

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()"""

    return jsonify({'message': 'Filas actualizadas correctamente'})

@blueprint.route('/index')
@login_required
def index():
    connection =mysql.connector.connect(
        host = "localhost",
        user = "test",
        password = "",
        database = "db_stockvision"
    )
    cursor = connection.cursor()
    fecha=datetime.datetime(2022, 1, 1, 0, 0)
    query="SELECT t.Transaccion, t.Fecha, t.ProductID, p.precio, p.ProductName AS Producto, v.Nombre AS Vendedor \
            FROM ventas AS t INNER JOIN vendedores AS v ON t.VendedorID = v.VendedorID INNER JOIN productos AS p ON t.ProductID = p.ProductID \
                WHERE t.Fecha = %s LIMIT 10"
    cursor.execute(query,(fecha,))

    myresult = cursor.fetchall()
    #Convertir los datos a diccionarios
    insertObject=[]
    columnNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columnNames,record)))
    
    #print(insertObject)
    #--------------------SUMA DE DATOS DIARIOS, MENSUALES Y ANUALES----------------------------
    # Ejecutar la consulta para obtener la suma de la columna "precio"
    query="SELECT SUM(p.precio) \
            FROM ventas AS t INNER JOIN productos AS p ON t.ProductID = p.ProductID \
                WHERE t.Fecha = %s"
    cursor.execute(query,(fecha,))
    result = cursor.fetchone()
    suma_dia = result[0]

    # Ejecutar la consulta para obtener la suma del mes

    query="SELECT SUM(p.precio) \
            FROM ventas AS t INNER JOIN productos AS p ON t.ProductID = p.ProductID \
                WHERE MONTH(t.Fecha) = %s"
    cursor.execute(query,(fecha.month,))
    result = cursor.fetchone()
    suma_mes = result[0]
    #print(suma_mes)

    query="SELECT SUM(p.precio) \
            FROM ventas AS t INNER JOIN productos AS p ON t.ProductID = p.ProductID \
                WHERE YEAR(t.Fecha) = %s"
    cursor.execute(query,(fecha.year,))
    result = cursor.fetchone()
    suma_ano = result[0]
    #----------------------------------------------------------------------------------------


    #-------------------RELLENAR LISTA DE COLORES--------------------------------------------#

    query="SELECT ColorName FROM colores"
    cursor.execute(query)
    result = cursor.fetchall()

    colores=[]
    for color in result:
        colores.append(color[0])
    #print(type(result))
    #print(colores)


    #-----------------RELLENAR LISTA DE GENEROS-----------------------#

    query="SELECT Genero FROM genero"
    cursor.execute(query)
    result = cursor.fetchall()

    generos=[]
    for genero in result:
        generos.append(genero[0])


    #-----------------RELLENAR LISTA DE MARCAS-----------------------#

    query="SELECT Marca FROM marcas"
    cursor.execute(query)
    result = cursor.fetchall()

    marcas=[]
    for marca in result:
        marcas.append(marca[0])

    #-----------------RELLENAR LA TABLA DE PRODUCTOS-------------------#

    query="SELECT p.ProductName,m.Marca,g.Genero,c.ColorName \
        FROM productos as p INNER JOIN marcas as m ON p.MarcaID = m.MarcaID \
            INNER JOIN genero as g ON p.GeneroID = g.GeneroID \
            INNER JOIN colores as c ON p.ColorID = c.ColorID"
    cursor.execute(query)
    result = cursor.fetchall()

    productos=[]
    columnNames = [column[0] for column in cursor.description]

    for record in result:
        productos.append(dict(zip(columnNames,record)))
    #print(result)
    print(len(productos))
    cursor.close()
    connection.close()  

    return render_template('home/index.html', segment='index', data=insertObject,ventas=[suma_dia,suma_mes,suma_ano],colores=colores,generos=generos,marcas=marcas,productos=productos)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
