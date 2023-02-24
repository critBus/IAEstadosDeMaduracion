function getHTML_AlertaSimple(mensaje){
                return '<div class="alert alert-danger btn-block" role="alert">'+mensaje+'</div>'
            }
function setHTML_Error(id,mensaje){
    setHTML(id,getHTML_AlertaSimple(mensaje))
}
