from os.path import join
import os
from jinja2 import Template
import subprocess
import jinja2
import xlrd
from slugify import slugify

loc = "casos_de_uso_fomix.xlsx"

wb = xlrd.open_workbook(loc)
casos_uso = []

for shidx in range(1, wb.nsheets):
    sheet = wb.sheet_by_index(shidx)
    nombre = sheet.cell_value(0, 1)
    label = slugify(nombre).replace("-","_")
    id = int(sheet.cell_value(1, 1))
    actores = sheet.cell_value(4, 1).splitlines()
    descripcion = sheet.cell_value(7, 1)
    precondiciones = sheet.cell_value(10, 1)
    pre_proceso = precondiciones.split("Del proceso")[1].split("Del sistema")[0].strip()
    pre_sistema = precondiciones.split("Del sistema")[1].strip()
    flujo_lines = sheet.cell_value(13, 1).splitlines()
    flujos_alternos =  sheet.cell_value(16, 1).splitlines()
    flujos_excepcion = sheet.cell_value(19, 1).splitlines()
    post_condiciones = sheet.cell_value(22, 1)

    casos_uso.append({"nombre": nombre,
                      "label": label,
                      "id": id,
                      "actores": actores,
                      "descripcion": descripcion,
                      "pre_proceso": pre_proceso,
                      "pre_sistema": pre_sistema,
                      "flujo_lines": flujo_lines,
                      "flujos_alternos": flujos_alternos,
                      "flujos_excepcion": flujos_excepcion,
                      "post_condiciones": post_condiciones
                      })

print(casos_uso)


def getTemplate(tpl_path):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename)

script_path = os.path.dirname(os.path.abspath( __file__ ))
tex_path = os.path.join(script_path,"EspReque_py.tex")
template = getTemplate(os.path.join(script_path,"EspReque.jinja"))
with open (tex_path, "w") as miFile:
    output = template.render(casos_uso=casos_uso)
    miFile.write(output)
