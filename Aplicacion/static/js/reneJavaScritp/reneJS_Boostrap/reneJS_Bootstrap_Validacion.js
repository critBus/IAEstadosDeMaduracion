//import reneJavaScrip.js
//import reneJS_Clases.js
//import reneJS_UtilesParaControles.js
//import rene_Validacion.js
//import rene_Bootstrap.js

class ValidacionConEventos_Boostrap extends ValidacionConEventos{
    constructor(){
        super();

        this.alCrear_ElementoParaValidacion=v=>{
            v.addAlSerInvalido((e,va)=>{
                this.__ocultarMensajeInvalidoSiExiste(e,false);
            });
            // v.alSerInvalido=(e,va)=>{
            //     this.__ocultarMensajeInvalidoSiExiste(e,false);
            // };

            v.addAlSerValido(
                (e,va)=>{
                    this.__ocultarMensajeInvalidoSiExiste(e,true);
                }
            );
            // v.alSerValido=(e,va)=>{
            //     this.__ocultarMensajeInvalidoSiExiste(e,true);
            // };
            return v;
        };
    }
    __getID_MensajeInvalido_DeID(id){
        return id+"_MensajeInvalidoBoostrap";
    }
    __getID_MensajeInvalido(e){
        return this.__getID_MensajeInvalido_DeID(e.id);
       // return e.id+"_MensajeInvalidoBoostrap";
    }
    __existeMensajeInvalido(e){
        return existe(this.__getID_MensajeInvalido(e));
    }
    __ocultarMensajeInvalidoSiExiste(e,ocultar){
        if(this.__existeMensajeInvalido(e)){
            let id=this.__getID_MensajeInvalido(e);
            
            displayNone(id,ocultar);
            let claseInvalida="is-invalid";
            if(ocultar){
                quitarClase(e.id,claseInvalida);
            }else{
                ponerClase(e.id,claseInvalida);
                setHTML(id,e.mensajeInvalido);
            }

        }
    }
}