from django import template
import re

register = template.Library()



#PATRON_CLASS=re.compile("class=[\"].*[\"]")
PATRON_CLASS=re.compile("(class=[\"](?![\"]).*?[\"])")
PATRON_CLASS_INTERNAS=re.compile("class=[\"]((?![\"]).*?)[\"]")
PATRON_NOMBRE_ETIQUETA=re.compile("[<](\w+)")
class NodeActual(template.Node):
    def __init__(self, salida):
        self.salida = salida

    def render(self, context):
        return str(self.salida)

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

@register.filter(needs_autoescape=True)
def ediTag(value,clasesExtra:str, autoescape=True):#
    nombreEtiqueta=re.findall(PATRON_NOMBRE_ETIQUETA,str(value))[0]
    parametrosExtra = None
    find = re.findall(PATRON_CLASS_INTERNAS, clasesExtra)
    if len(find) > 0:
        # print("0clasesExtra=",clasesExtra)
        # print("re.findall(PATRON_CLASS, clasesExtra)[0]=",re.findall(PATRON_CLASS, clasesExtra)[0])
        temp = clasesExtra.replace(re.findall(PATRON_CLASS, clasesExtra)[0],"")
        clasesExtra=find[0]
        # print("clasesExtra=",clasesExtra)
        # print("temp=", temp)
        # print("temp.strip()=", temp.strip())
        if len(temp.strip())>0:
            parametrosExtra=temp
            # print("parametrosExtra=",parametrosExtra)


    atributoClases=""
    value=str(value)
    find=re.findall(PATRON_CLASS,value)
    if len(find)>0:
        atributoClases=find[0][:-1]+" "+clasesExtra+"\""
        value.replace(find[0],atributoClases)
    else:
        atributoClases="class=\""+clasesExtra+"\""
        #value = value[:-1] + " " + atributoClases + ">"
        value ="<"+nombreEtiqueta+" "+atributoClases+ value[len(nombreEtiqueta)+1:]
    if parametrosExtra is not None and len(str(parametrosExtra))>0:
        # print("value=",value)
        #value=value[:-1]+" "+parametrosExtra+">"
        value = "<"+nombreEtiqueta+" " + parametrosExtra + value[len(nombreEtiqueta)+1:]
        # print("2parametrosExtra=", parametrosExtra)
        # print("2value=", value)
    # return value
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(value)
@register.filter(needs_autoescape=True)
def conHTML(value, autoescape=True):
    return mark_safe(value)
# register.filter('editarEtiqueta2',editarEtiqueta2)
# def editarEtiqueta(parser, token):
#
#     try:
#         # split_contents() knows not to split quoted strings.
#
#         tag_name, value,clasesExtra = token.split_contents()
#         if tag_name=="editarEtiqueta":
#
#             return NodeActual(editarEtiqueta2(value,clasesExtra))
#     except ValueError:
#         msg = '%r tag requires a single argument' % token.split_contents()[0]
#         raise template.TemplateSyntaxError(msg)
#     return NodeActual("vacio")
# register.tag('editarEtiqueta', editarEtiqueta)


def numeroConComa(value):
    return str(value).replace(",",".")
register.filter('numeroConComa', numeroConComa)


def getEn(value,indice):
    return str(value[int(indice)])
register.filter('getEn', getEn)

def getEnDic(value,indice):
    return str(value[indice])
register.filter('getEnDic', getEnDic)

@register.filter(needs_autoescape=True)
def getHtmlEn(value,indice, autoescape=True):
    return mark_safe(str(value[int(indice)]))


@register.filter(needs_autoescape=True)
def quitarSaltos(value, autoescape=True):
    return mark_safe(str(value).replace('\n','<p><br></p>'))
    #return str(value).replace('\n','<br>')
# register.filter('quitarSaltos', quitarSaltos)
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