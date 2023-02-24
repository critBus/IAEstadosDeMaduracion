from django import template

register = template.Library()
#
# """
# <input type="file" name="imagen" accept="image/*" required="" id="id_imagen">
# class=[\"].*[\"]
# """
# import re
# PATRON_CLASS=re.compile("class=[\"].*[\"]")
# class NodeActual(template.Node):
#     def __init__(self, salida):
#         self.salida = salida
#
#     def render(self, context):
#         return str(self.salida)
#
# from django.utils.html import conditional_escape
# from django.utils.safestring import mark_safe
#
# @register.filter(needs_autoescape=True)
# def editarEtiqueta2(value,clasesExtra,parametrosExtra=None, autoescape=True):#
#     atributoClases=""
#     value=str(value)
#     find=re.findall(PATRON_CLASS,value)
#     if len(find)>0:
#         atributoClases=find[0][:-1]+" "+clasesExtra+"\""
#         value.replace(find[0],atributoClases)
#     else:
#         atributoClases="class=\""+clasesExtra+"\""
#         value = value[:-1] + " " + atributoClases + ">"
#     if len(parametrosExtra) is not None and len(str(parametrosExtra))>0:
#         value=value[:-1]+" "+parametrosExtra+">"
#     # return value
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     return mark_safe(value)
#
# # register.filter('editarEtiqueta2',editarEtiqueta2)
# # def editarEtiqueta(parser, token):
# #
# #     try:
# #         # split_contents() knows not to split quoted strings.
# #
# #         tag_name, value,clasesExtra = token.split_contents()
# #         if tag_name=="editarEtiqueta":
# #
# #             return NodeActual(editarEtiqueta2(value,clasesExtra))
# #     except ValueError:
# #         msg = '%r tag requires a single argument' % token.split_contents()[0]
# #         raise template.TemplateSyntaxError(msg)
# #     return NodeActual("vacio")
# # register.tag('editarEtiqueta', editarEtiqueta)
#
#
#
#
#
# def cuta(value, arg):
#     "Removes all values of arg from the given string"
#     return value.replace(arg, '')
#
#
# register.filter('cuta', cuta)
#
#
#
# def etiquetaUno(parser, token):
#
#     try:
#         # split_contents() knows not to split quoted strings.
#         tag_name, arg1 = token.split_contents()
#         if tag_name=="etiquetaA":
#
#             return NodeActual(str(arg1)+" asd")
#     except ValueError:
#         msg = '%r tag requires a single argument' % token.split_contents()[0]
#         raise template.TemplateSyntaxError(msg)
#     return NodeActual("vacio")
#
# register.tag('etiquetaA', etiquetaUno)
#
#
# def do_current_time3(parser, token):
#     try:
#         # split_contents() knows not to split quoted strings.
#         tag_name, asd = token.split_contents()
#         if tag_name == "current_time2":
#             return NodeActual(str(asd) + " asd4")
#     except ValueError:
#         msg = '%r tag requires a single argument' % token.split_contents()[0]
#         raise template.TemplateSyntaxError(msg)
#     return NodeActual(asd+" asd")
# register.tag('current_time2', do_current_time3)