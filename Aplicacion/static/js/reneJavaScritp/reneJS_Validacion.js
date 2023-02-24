class TipoDeValidacion {
    constructor(esValido,mensaje) {
        this.__esValido = esValido;//(t:TipoDeValidacion,v)=>bool v es el contenido o valor
        this.__mensaje=null;//()=>""
        //if(es){}
        this.setMensaje(mensaje);
        this.idElemento;
    }
    getMensaje(){
        if(this.__mensaje!=null&&this.__mensaje!=undefined){
            return this.__mensaje();
        }
        //console.log("zzz this.__mensaje="+this.__mensaje)
        //return this.__mensaje!=null&&this.mensaje!=undefined?this.__mensaje():null;
    }
    // setMetodoGetMensaje(getMensaje){
    //     //getMensaje ()=>""
    //     this.__mensaje=getMensaje;
    //     return this;
    // }
    setMensaje(mensaje){
        if(esFuncion(mensaje)){
           // console.log("!!!!!!!!!!!!fue funcion");
            this.__mensaje=mensaje;
        }else{
            this.__mensaje=()=>mensaje;
        }
        
    }
    esValido(valor){
        return this.__esValido(this,valor);
    }
}



const __MEDIO_LETRAS="(?:\\w|[ÑñáéíóúÁÉÍÓÚÀÈÌÒÙàèìòù])"
const PATRON_CONTIENE_LETRAS = RegExp("(?:\\d*)((?![\\d_])"+__MEDIO_LETRAS+"+(?<![\\d_]))(?:\\d*)");
TipoDeValidacion.NO_NULL =new  TipoDeValidacion((t,v) => v != undefined && v != null
    ,"No puede estar vacío ");
TipoDeValidacion.STR_NO_EMPTY =new  TipoDeValidacion((t,v) => TipoDeValidacion.NO_NULL.esValido(v) && esString(v) && v.trim().length > 0
,"No puede estar vacío ");
TipoDeValidacion.STR_CON_ALFANUMERICOS =new  TipoDeValidacion((t,v) => TipoDeValidacion.STR_NO_EMPTY.esValido(v) && hayMatch(PATRON_CONTIENE_LETRAS, v)
,"Debe de contener letras");
TipoDeValidacion.SOLO_INT_POSITIVO_STR=new  TipoDeValidacion((t,v) => TipoDeValidacion.NO_NULL.esValido(v)&&(esInt(v)?v>=0:esIntPStr(v))
,"Debe ser un numero entero positivo ");
TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR=new  TipoDeValidacion((t,v) => TipoDeValidacion.NO_NULL.esValido(v)&&(esNumero(v)?v>=0:esFloatPStr(v))
,"Debe ser un numero positivo cuyo indicador decimal sea un ‘.’");
// const PATRON_CORREO = RegExp("(\\w+\\.?\\w*[@]\\w+\\.)(com)");

// const PATRON_CORREO = RegExp( /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
const PATRON_CORREO = RegExp("^([a-z0-9_]+(?:(?:[.]?[a-z0-9_])*)[@][a-z0-9_]+\\.)(com)$");
TipoDeValidacion.STR_CORREO =new  TipoDeValidacion((t,v) => TipoDeValidacion.STR_NO_EMPTY.esValido(v) && hayMatch(PATRON_CORREO, v)
,"Correo Incorrecto");

const PATRON_SOLO_LETRAS = RegExp("^(?:(?:[ ]*)(?:(?![\\d_])"+__MEDIO_LETRAS+"(?<![\\d_]))+(?:[ ]*))+$");
TipoDeValidacion.STR_SOLO_LETRAS =new  TipoDeValidacion((t,v) => TipoDeValidacion.STR_NO_EMPTY.esValido(v) && hayMatch(PATRON_SOLO_LETRAS, v)
,"Solo debe de contener letras y espacios ");

const PATRON_SOLO_LETRAS_Y_NUMEROS = RegExp("^(?:(?:[ ]*)(?:(?![_])"+__MEDIO_LETRAS+"(?<![_]))+(?:[ ]*))+$");
TipoDeValidacion.STR_SOLO_LETRAS_Y_NUMEROS =new  TipoDeValidacion((t,v) => TipoDeValidacion.STR_NO_EMPTY.esValido(v) && hayMatch(PATRON_SOLO_LETRAS, v.trim())
,"Solo debe de contener letras, numeros y espacios ");

const PATRON_SOLO_ALFANUMERICOS = RegExp("^(?:(?:[ ]*)"+__MEDIO_LETRAS+"+(?:[ ]*))+$");
TipoDeValidacion.STR_SOLO_ALFANUMERICOS =new  TipoDeValidacion((t,v) => TipoDeValidacion.STR_NO_EMPTY.esValido(v) && hayMatch(PATRON_SOLO_LETRAS, v)
,"Solo debe de contener letras, numeros, espacios y '_'");


const PATRON_TIENE_NUMEROS = new RegExp("[0-9]+");
TipoDeValidacion.STR_SEGURIDAD_MINIMA_CONTRASEÑA =new  TipoDeValidacion((t,v) => { 
    if(TipoDeValidacion.STR_NO_EMPTY.esValido(v)&&(v+"").length>7){
        return hayMatch(PATRON_CONTIENE_LETRAS, v)&&hayMatch(PATRON_TIENE_NUMEROS,v);
        // let cantidadDeLetras=0;
        // let cantidadDeNumeros=0;
        // for (let index = 0; index < v.length; index++) {
        //     const element = v[index];
            
        // }
    }
    return false;
    
}
,"Debe de contener letras, numeros, y al menos 8 caracteres");

class TipoDeValidacionMinLength extends TipoDeValidacion{
    constructor(lengthMin,creardorMensaje) {//creador mensaje (v#min)=> mensaje str con v#;
        super((t,v)=>TipoDeValidacion.STR_NO_EMPTY.esValido(v)
        &&(v+"").trim().length>=lengthMin
            ,creardorMensaje(lengthMin));
    }
}
class TipoDeValidacionMaxLength extends TipoDeValidacion{
    constructor(lengthMax,creardorMensaje) {//creador mensaje (v#max)=> mensaje str con v#;
        super((t,v)=>TipoDeValidacion.STR_NO_EMPTY.esValido(v)
        &&(v+"").trim().length<=lengthMax,creardorMensaje(lengthMax));
    }
}

class TipoDeValidacionRangoEnteroPositivo extends TipoDeValidacion{
    constructor( min,max,creardorMensaje) {//creador mensaje (v#min,v#max)=> mensaje str con v#;
        super((t,v)=>TipoDeValidacion.SOLO_INT_POSITIVO_STR.esValido(v)
        &&inT(v)>=min&&inT(v)<=max
        ,creardorMensaje(min,max));
    }
}
class TipoDeValidacionRangoPositivo extends TipoDeValidacion{
    constructor( min,max,creardorMensaje) {//creador mensaje (v#min,v#max)=> mensaje str con v#;
        super((t,v)=>{
            // console.log("v="+v);
            // console.log("min="+min);
            // console.log("max="+max);
            // console.log("inT(v)="+inT(v));
            // console.log("TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR.esValido(v)="+TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR.esValido(v));
            // console.log("inT(v)>=min ="+inT(v)>=min);
            // console.log("inT(v)<=max ="+inT(v)<=max);
            return TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR.esValido(v)
            &&floaT(v)>=min&&floaT(v)<=max;
    }
        ,creardorMensaje(min,max));
    }
}
// TipoDeValidacion.LONGITUD_MIN_5=new TipoDeValidacionMinLength(5,v=>"Debe de tener como mínimo "+v+" caracteres ");
// TipoDeValidacion.LONGITUD_MAX_50=new TipoDeValidacionMaxLength(50,v=>"Debe de tener como máximo "+v+" caracteres ");

class CondicionDeValidacion {
    constructor(seCumple) {
        this.seCumple = seCumple;//()=>bool
    }
}
class RespuestaValidacionDeServidor{
    constructor(valor,mensaje){
        this.valor=valor;
        this.__mensaje=null;
        this.setMensaje(mensaje);
        this.esValido=false;
    }
    getMensaje(){
        return this.__mensaje;
    }
    setMensaje(mensaje){
        this.__mensaje=mensaje;
    }
}
class ElementoParaValidacion {
    constructor(id,condicionDeValidacion) {
        let cev=condicionDeValidacion;
        if(condicionDeValidacion==undefined||condicionDeValidacion==null){
            cev=new CondicionDeValidacion(v=>true);
        }else if(esFuncion(condicionDeValidacion)){
            cev=new CondicionDeValidacion(condicionDeValidacion);
        }
        this.id=id;
        this.condicionDeValidacion=cev;
        this.listaTiposDeValidacion = [];
        this.metodoGetValorAEvaluar = v => getValue(v.id);//aqui se busca la manera de obtener el valor del elemento , v es this, 

        this.mensajeInvalido;

        this.alSerInvalido=new ConjuntoDeEventos();//(e:ElementoParaValidacion,v:valorActual)=>{}
        this.alSerValido=new ConjuntoDeEventos();//(e:ElementoParaValidacion,v:valorActual)=>{}
        this.respuestaValidacionDeServidor=null;
    }
    setRespuestaValidacionDelServidor(valor,mensaje){
        this.respuestaValidacionDeServidor=new RespuestaValidacionDeServidor(valor,mensaje);
        return this;
    }
    getValorInterno() {
        //console.log("v="+this.metodoGetValorAEvaluar(this));
        //console.log("ty v="+typeof(this.metodoGetValorAEvaluar(this)) );
        // console.log("--------------------------------------");
        // let b=this.metodoGetValorAEvaluar(this) instanceof ListaSeleccionable_MenuAgregarEliminarArribaAbajo;
        // console.log("ES LISTA v="+b);
        // console.log("++++++++++++++++++++++++++++++++++++++");
        return this.metodoGetValorAEvaluar(this);
    }
    __alSerInvalido(valorActual){
        this.alSerInvalido.ejecutar(this,valorActual);
        // if(this.alSerInvalido!=undefined&&this.alSerInvalido!=null){
        //     this.alSerInvalido(this,valorActual);
        // }
    }
    __alSerValido(valorActual){
        this.alSerValido.ejecutar(this,valorActual);
       // console.log("se llama al ser valido");
        // if(this.alSerValido!=undefined&&this.alSerValido!=null){
        //     this.alSerValido(this,valorActual);
        // }
    }
    addAlSerValido(metodoAlSerValido){//(e:ElementoParaValidacion,v:valorActual)=>{}
        this.alSerValido.add(metodoAlSerValido);
        // if(this.alSerValido!=undefined&&this.alSerValido!=null){
        //     const anterior=this.alSerValido;
        //     this.alSerValido=(e,v)=>{
        //         anterior(e,v);
        //         metodoAlSerValido(e,v);
        //     };

        // }else{
        //     this.alSerValido=metodoAlSerValido;
        // }
        return this;
    }
    addAlSerInvalido(metodoAlSerInvalido){//(e:ElementoParaValidacion,v:valorActual)=>{}
        this.alSerInvalido.add(metodoAlSerInvalido);
        // if(this.alSerInvalido!=undefined&&this.alSerInvalido!=null){
        //     const anterior=this.alSerInvalido;
        //     this.alSerInvalido=(e,v)=>{
        //         anterior(e,v);
        //         metodoAlSerInvalido(e,v);
        //     };

        // }else{
        //     this.alSerInvalido=metodoAlSerInvalido;
        // }
        return this;
    }
    esValido() {
        let lv = this.listaTiposDeValidacion;
        let valorActual=this.getValorInterno();
        for (let index = 0; index < lv.length; index++) {
            const tipoDeValidacion = lv[index];
            // console.log("valorActual="+valorActual);
            // console.log("ty valorActual="+typeof(valorActual) );
            // console.log(">>>>>>>>> va comprobar");
            // let ss=valorActual instanceof ListaSeleccionable_MenuAgregarEliminarArribaAbajo;
            // console.log("!!ES lista valorActual="+ss);
            if (!tipoDeValidacion.esValido(valorActual)) {
                this.mensajeInvalido=tipoDeValidacion.getMensaje();
                this.__alSerInvalido(valorActual);
               // console.log("primer invalido");
                return false;
            }
        }
        if(this.respuestaValidacionDeServidor!=undefined&&this.respuestaValidacionDeServidor!=null){
            if(esString(valorActual)){
                valorActual=valorActual.trim();
            }
            if((!this.respuestaValidacionDeServidor.esValido)&&this.respuestaValidacionDeServidor.valor==valorActual){
                this.mensajeInvalido=this.respuestaValidacionDeServidor.getMensaje();
                this.__alSerInvalido(valorActual);
               // console.log("segundo invalido");
                return false;
            }
        }
        this.__alSerValido(valorActual);
        // if(this.alSerValido!=undefined&&this.alSerValido!=null){
        //     this.alSerValido(this,valorActual);
        // }
        return true;
    }
    addTipoDeValidacion(tipo){
        tipo.idElemento=this.id;
        this.listaTiposDeValidacion.push(tipo);
        return this;
    }
    setMaxCar(max){
        this.addTipoDeValidacion(new TipoDeValidacionMaxLength(max,v=>"Debe de tener como máximo "+v+" caracteres "));
        return this;
    }
    setMinCar(min){
        this.addTipoDeValidacion(new TipoDeValidacionMinLength(min,v=>"Debe de tener como mínimo "+v+" caracteres "));
        return this;
    }
    setDependeDeCB(idCB){
        this.condicionDeValidacion=new CondicionDeValidacion(()=>{
            // console.log("idCB="+idCB);
            // console.log("estaSeleccionado(idCB)="+estaSeleccionado(idCB));
            return estaSeleccionado(idCB);});
        return this;
    }
    setDependeDeCB_Not(idCB){
        this.condicionDeValidacion=new CondicionDeValidacion(()=>!estaSeleccionado(idCB));
        return this;
    }


    verAlSerInvalido(idElemento){
        const self=this;
        this.addAlSerInvalido((e,v)=>{
            setHTML(idElemento,self.mensajeInvalido);
            displayNone(idElemento,false);
        });
        this.addAlSerValido((e,v)=>displayNone(idElemento,true));

        return this;
    }

}

class ElementoParaValidacion_File extends ElementoParaValidacion{
    constructor(){
        super();
        this.metodoGetValorAEvaluar = v => getEl(v.id).files;//.length>0
    }
}

ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO =new  TipoDeValidacion((t,v) => {
    //console.log("va a comprobar el input");
    //console.log("v.length>0="+v.length>0);
    return v.length>0;
}
,"Debe de seleccionar algún archivo");
ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO_NO_EMPTY =new  TipoDeValidacion((t,v) =>{
    //console.log("notEmpty_ArchivoEnInput(t.idElemento)="+notEmpty_ArchivoEnInput(t.idElemento));
    return notEmpty_ArchivoEnInput(t.idElemento);
}
,"El archivo no debe estar vacio");
ElementoParaValidacion_File.VALIDACION_ALMENOS_TIPO_IMAGEN =new  TipoDeValidacion((t,v) => {
    //console.log("esImagen(getExtencionArchivoEnInput(t.idElemento))="+esImagen(getExtencionArchivoEnInput(t.idElemento)));
    return esImagen(getExtencionArchivoEnInput(t.idElemento));
}
,"Debe de seleccionar algun archivo de tipo imagen");
ElementoParaValidacion_File.VALIDACION_ALMENOS_TIPO_IMAGEN_JPG_PNG =new  TipoDeValidacion(
    (t,v) => {
        //console.log("esImagen_InputFile_JPG_PNG(t.idElemento)="+esImagen_InputFile_JPG_PNG(t.idElemento));
       return  esImagen_InputFile_JPG_PNG(t.idElemento);
    }
,"Debe de seleccionar algun archivo de tipo imagen .jpg .png");

ElementoParaValidacion_File.VALIDACION_ES_ZIP=new  TipoDeValidacion(
    (t,v) => {
       return  esZipEnInput(t.idElemento);
    }
,"Debe de seleccionar algun archivo comprimido en formato .zip");

class TipoDeValidacionArchivoMenorQueCantidadDeMGBs extends TipoDeValidacion{
    constructor( max) {//creador mensaje (v#max)=> mensaje str con v#;
        super((t,v)=>elArchivoEnInputFileEsMenorQueMGBs(t.idElemento,max)
        ,"El archivo debe de tener un tamaño inferior a los "+max+" megas");

    }
}

class Validacion {
    constructor() {
        this.condicionDeValidacion=new CondicionDeValidacion(v=>true);
        this.mapCondicionDeValidacion_Y_ListaDeElementos = new Map();
        
        this.listaElementoParaValidacion=[];
        
        this.mapListaDeElementosParaValidacionTemporales=new Map();

        this.alCrear_ElementoParaValidacion=null;//(v:ElementoParaValidacion)=>ElementoParaValidacion
    }
    esValido() {
        this.__actualizar_MapCondicionDeValidacion_Y_ListaDeElementos();
        // console.log("---------------------------------");
        let respuestaEsValido=true;
        for (let row of this.mapCondicionDeValidacion_Y_ListaDeElementos) {
            let condicionDeEvaluacion = row[0];
            let listaElementosParaValidacion=row[1]

            if(condicionDeEvaluacion.seCumple()){
                for (let index = 0; index < listaElementosParaValidacion.length; index++) {
                    const elementoParaValidacion = listaElementosParaValidacion[index];
                    let id=elementoParaValidacion.id;
                    if(id=="idInputConfirmarContraseña"){
                        console.log("aqui");
                    }
                    if (!elementoParaValidacion.esValido()) {
                        //return false;
                        // console.log("elementoParaValidacion.id="+elementoParaValidacion.id);
                        respuestaEsValido=false;// no lo detengo aqui por hay que mandar a validar cada elemento para que de cada uno se obtenga el mensaje y puede que este se muestre, recordar que cada elemento es un campo visual
                    }
                }
            }
            
            
            
        }
        return respuestaEsValido;
    }
    __enElMomentoDeAgregarElemento(elemento,condicionDeEvaluacionParametro){
        let e=elemento;
        if(this.alCrear_ElementoParaValidacion!=undefined&&this.alCrear_ElementoParaValidacion!=null){
            e=this.alCrear_ElementoParaValidacion(e);
        }
        if(condicionDeEvaluacionParametro!=undefined&&condicionDeEvaluacionParametro!=null){
            e.condicionDeValidacion=condicionDeEvaluacionParametro;
        }
    }
    addElemento(elemento,condicionDeEvaluacionParametro){
        this.__enElMomentoDeAgregarElemento(elemento,condicionDeEvaluacionParametro);
        this.listaElementoParaValidacion.push(elemento);
        
    }
    addElementoTemporal(key,elemento,condicionDeEvaluacionParametro){
        this.__enElMomentoDeAgregarElemento(elemento,condicionDeEvaluacionParametro);
        if(!this.mapListaDeElementosParaValidacionTemporales.has(key)){
            this.mapListaDeElementosParaValidacionTemporales.set(key,[]);
        }
        this.mapListaDeElementosParaValidacionTemporales.get(key).push(elemento);

    }
    clearTemporal(key){
        this.mapListaDeElementosParaValidacionTemporales.set(key,[]);
    }
    __agregarElementoParaValidacionAl_MapCondicionDeValidacion_Y_ListaDeElementos(e){
        let condicionDeEvaluacion=e.condicionDeValidacion;
        let m=this.mapCondicionDeValidacion_Y_ListaDeElementos;
        if(m.has(condicionDeEvaluacion)){
            m.get(condicionDeEvaluacion).push(e);
        }else{
            m.set(condicionDeEvaluacion,[e]);
        }
    }
    __actualizar_MapCondicionDeValidacion_Y_ListaDeElementos(){
        this.mapCondicionDeValidacion_Y_ListaDeElementos = new Map();
        for (let index = 0; index < this.listaElementoParaValidacion.length; index++) {
            let e = this.listaElementoParaValidacion[index];
            this.__agregarElementoParaValidacionAl_MapCondicionDeValidacion_Y_ListaDeElementos(e);
            
        }
        for (let entrada of this.mapListaDeElementosParaValidacionTemporales) {
            let lista=entrada[1];
            for (let index = 0; index < lista.length; index++) {
                let e=lista[index];
                this.__agregarElementoParaValidacionAl_MapCondicionDeValidacion_Y_ListaDeElementos(e);
            }
            
        }
    }

    add_Temporal_Text_NO_EMPTY(key,id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_NO_EMPTY);
        this.addElementoTemporal(key,e);
        return e;
    }

    
    addText_CON_ALFANUMERICOS(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_CON_ALFANUMERICOS);
        this.addElemento(e);
        return e;
    }
    addText_NO_EMPTY(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_NO_EMPTY);
        this.addElemento(e);
        return e;
    }

    addText_NO_EMPTY_CondicionCB(id,idCB){
        const ID_CB=idCB;
        let e=this.addText_NO_EMPTY(id,new CondicionDeValidacion(()=>estaSeleccionado(ID_CB)));
        return e;
    }
    add_EnteroPositivo(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.SOLO_INT_POSITIVO_STR);
        this.addElemento(e);
        return e;
    }
    addRange_EnteroPositivo(id,min,max,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.SOLO_INT_POSITIVO_STR);
        e.addTipoDeValidacion(new TipoDeValidacionRangoEnteroPositivo(min,max
            ,v=>"El numero debe de estar en el rango de "+min+" a "+max+" y debe ser un numero entero positivo "));
        this.addElemento(e);
        return e;
    }
    add_Positivo(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR);
        this.addElemento(e);
        return e;
    }
    addRange_Positivo(id,min,max,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.SOLO_FLOAT_POSITIVO_STR);
        e.addTipoDeValidacion(new TipoDeValidacionRangoPositivo(min,max
            ,v=>"El numero debe de estar en el rango de "+min+" a "+max+" y debe ser un numero positivo cuyo indicador decimal sea un ‘.’"));
        this.addElemento(e);
        return e;
    }


    addText_CORREO(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_CORREO);
        this.addElemento(e);
        return e;
    }

    addText_SOLO_LETRAS(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_SOLO_LETRAS);
        this.addElemento(e);
        return e;
    }
    addText_SOLO_LETRAS_Y_NUMEROS(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_SOLO_LETRAS_Y_NUMEROS);
        this.addElemento(e);
        return e;
    }
    addText_SOLO_ALFANUMERICOS(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_SOLO_ALFANUMERICOS);
        this.addElemento(e);
        return e;
    }

    addTexts_Contraseña(id,idConfirmacion,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(TipoDeValidacion.STR_SEGURIDAD_MINIMA_CONTRASEÑA);
        this.addElemento(e);

        let e2=new ElementoParaValidacion(idConfirmacion,condicionDeEvaluacion);
        e2.addTipoDeValidacion(new TipoDeValidacion((t,v)=>{
            // console.log("id="+id);
            // console.log("v="+v);
            // console.log("ty v="+typeof(v));
            // console.log("getValue(id)="+getValue(id));
            // console.log("v==getValue(id) ="+(v==getValue(id)));
            return v==getValue(id);
        },
            "Tiene que coincidir con la contraseña"
        ));
        this.addElemento(e2);
        return [e,e2];
    }

     addInputFileImagen(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO_NO_EMPTY);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_TIPO_IMAGEN);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_TIPO_IMAGEN_JPG_PNG);
        e.addTipoDeValidacion(new TipoDeValidacionArchivoMenorQueCantidadDeMGBs(10));
        this.addElemento(e);
        return e;
    }

    addInputFile_Zip(id,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ALMENOS_UN_ARCHIVO_NO_EMPTY);
        e.addTipoDeValidacion(ElementoParaValidacion_File.VALIDACION_ES_ZIP);

        this.addElemento(e);
        return e;
    }


     addSelect_TipoValuePositivo(id,mensaje,condicionDeEvaluacion){
        let e=new ElementoParaValidacion(id,condicionDeEvaluacion);
        e.addTipoDeValidacion(new TipoDeValidacion((t,v)=>{
            //console.log("v="+v);
            return v!=null&&v>0;
        },mensaje));
        this.addElemento(e);
        return e;
    }
    //__actualizarMap(){}
}
class ElementoADesactivar{
    constructor(){
        this.id;
        this.desactivado=false;
        this.metodoDesactivar=v=>{
            //console.log("v.desactivado="+v.desactivado);
            if(!v.desactivado){
                //console.log("id="+v.id);
                setDisabled(true,[v.id]);
            }
        };
        this.metodoActivar=v=>{
            if(v.desactivado){
                setDisabled(false,[v.id]);
            }
        };
    }
    activar(){
        
        this.metodoActivar(this);
        this.desactivado=false;
    }
    desactivar(){
        
        this.metodoDesactivar(this);
        this.desactivado=true;
    }
}
class ElementoDisparadorDeValidacion{
    constructor(){
        this.id;
        this.metodoAplicarDisparador;//(e:this , v:ValidacionConEventos)=>{} la idea es en el { usar v en el onclick o en el onTextChange} 
        this.validacionConEventos;
    }
    aplicarDisparador(){
        this.metodoAplicarDisparador(this,this.validacionConEventos);
    }
}

class ElementoDisparadorDeValidacionText extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{
            addOnKeyUp(e.id,()=>{
                //console.log("se llama al escribir");
                v.comprovarValidacionYDesactivar();
            });
            addOnChange(e.id,()=>{
                //console.log("se llama al escribir2");
                v.comprovarValidacionYDesactivar();
            });
        }
    }
}
class ElementoDisparadorDeValidacionBoton extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{
            addOnClick(e.id,()=>{
                v.comprovarValidacionYDesactivar();
            });
            
        }
    }
}
class ElementoDisparadorDeValidacionCB extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{
            addOnClick(e.id,()=>{
                v.comprovarValidacionYDesactivar();
            });
            addOnChange(e.id,()=>{
                v.comprovarValidacionYDesactivar();
            });
            
        }
    }
}

class ElementoDisparadorNumerico extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{
            addOnKeyUp(e.id,()=>{
                //console.log("se llama al escribir");
                v.comprovarValidacionYDesactivar();
            });
            addOnChange(e.id,()=>{
                //console.log("se llama al escribir2");
                v.comprovarValidacionYDesactivar();
            });
        }
    }
}

class ElementoDisparadorSelect extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{

            addOnChange(e.id,()=>{
                // console.log("se llama al escribir2");
                v.comprovarValidacionYDesactivar();
            });
        }
    }
}

class ElementoDisparadorDeValidacionInputFile extends ElementoDisparadorDeValidacion{
    constructor(){
        super();
        this.metodoAplicarDisparador=(e,v)=>{
            addOnChange(e.id,()=>{
                //console.log("se llama al escribir2");
                v.comprovarValidacionYDesactivar();
            });
        }
    }
}


class ValidacionConEventos{
    constructor(){
        this.listaDeValidaciones=[];
        this.listaElementosADesactivar=[];
        this.listaElementosDisparadoresDeValidacion=[];

        this.mapListaDeElementosDisparadoresDeValidacionTemporales=new Map();


        this.aplicarConfiguracionAutomatica=true;

        this._ultimos_ElementoParaValidacion_Agregados=[];
        this._ultimo_ElementoParaValidacion_Agregado=null;

        this.alCrear_ElementoParaValidacion=null;//(v:ElementoParaValidacion)=>ElementoParaValidacion

        this.__antesDeRealizarValidacion=new ConjuntoDeEventos();
    }
    addAntesDeRealizarValidacion(metodo){
        //metodo (v:ValidacionConEventos)=>{}
        this.__antesDeRealizarValidacion.add(metodo);
    }
    

    esValido(){
        let respuestaEsValido=true;
        for (let index = 0; index < this.listaDeValidaciones.length; index++) {
            const validacion = this.listaDeValidaciones[index];
            // console.log("validacion.condicionDeValidacion="+validacion.condicionDeValidacion);
            // console.log("typeof(validacion.condicionDeValidacion)="+typeof(validacion.condicionDeValidacion));
            if(validacion.condicionDeValidacion.seCumple()&&(!validacion.esValido())){
                //return false;
                respuestaEsValido=false;// no lo detengo aqui por hay que mandar a validar cada elemento para que de cada uno se obtenga el mensaje y puede que este se muestre, recordar que cada elemento es un campo visual
            }
        }
        return respuestaEsValido;
    }
    comprovarValidacionYDesactivar(){
        this.__antesDeRealizarValidacion.ejecutar(this);

        let valido=this.esValido();
        //console.log("valido="+valido);
        for (let index = 0; index < this.listaElementosADesactivar.length; index++) {
            const elementoADesactivar = this.listaElementosADesactivar[index];
            if(valido){
                elementoADesactivar.activar();
            }else{
                elementoADesactivar.desactivar();
            }
        }
    }
    aplicarConfiguracion(){
        if(!this.aplicarConfiguracionAutomatica){
            for (let index = 0; index < this.listaElementosDisparadoresDeValidacion.length; index++) {
                const elementoDisparadorDeValidacion = this.listaElementosDisparadoresDeValidacion[index];
                elementoDisparadorDeValidacion.aplicarDisparador();
            }
        }
        
    }


    addValidacion(v){
        this.listaDeValidaciones.push(v);
    }

    addDisparador(e){
        this.listaElementosDisparadoresDeValidacion.push(e);
        if(this.aplicarConfiguracionAutomatica){
            e.aplicarDisparador();
        }
    }
    addDisparadorTemporal(key,e){
        if(!this.mapListaDeElementosDisparadoresDeValidacionTemporales.has(key)){
            this.mapListaDeElementosDisparadoresDeValidacionTemporales.set(key,[]);
        }
        this.mapListaDeElementosDisparadoresDeValidacionTemporales.get(key).push(e);

        if(this.aplicarConfiguracionAutomatica){
            e.aplicarDisparador();
        }
    }
    clearTemporal(key){
        this.mapListaDeElementosDisparadoresDeValidacionTemporales.set(key,[]);
        for (let index = 0; index < this.listaDeValidaciones.length; index++) {
            const validacion = this.listaDeValidaciones[index];
            validacion.clearTemporal(key);
        }
    }

    addElementoADesactivar(e){
        this.listaElementosADesactivar.push(e);
    }
    __addElementoADesactivar(id,crearElemento){
        let e=crearElemento();
        e.id=id;
        this.addElementoADesactivar(e);
        return e;
    }
    __alAddDisparador(id,crearDisparador){
        let e=crearDisparador();
        e.id=id;
        e.validacionConEventos=this;
        return e;
    }
    __addDisparador(id,crearDisparador){
        let e=this.__alAddDisparador(id,crearDisparador);
        this.addDisparador(e);
        return e;
    }
    __addDisparadorTemporal(key,id,crearDisparador){
        let e=this.__alAddDisparador(id,crearDisparador);
        this.addDisparadorTemporal(key,e);
        return e;
    }
    __getUltimaValidacion(){
        if(this.listaDeValidaciones.length==0){
            let v=new Validacion();
            if(this.alCrear_ElementoParaValidacion!=undefined&&this.alCrear_ElementoParaValidacion!=null){
                v.alCrear_ElementoParaValidacion=this.alCrear_ElementoParaValidacion;
            }
            this.addValidacion(v);
        }
        return this.listaDeValidaciones[this.listaDeValidaciones.length-1];
    }
    __alAddElemento_V_D(usarUltimaValidacion){//id,
        //usarUltimaValidacion (v:Validacion)=>{} 
        //crearDisparador ()=>ElementoDisparadorDeValidacion 
        let v=this.__getUltimaValidacion();
        let e=usarUltimaValidacion(v);
        if(esLista(e)){
            this._ultimos_ElementoParaValidacion_Agregados=e;
        }else{
            this._ultimo_ElementoParaValidacion_Agregado=e;
        }
        
        return e;
    }

    agregarElemento(elemento){
        return this.__alAddElemento_V_D(v=>v.addElemento(elemento));
    }
    agregarDisparador(disparador){
        return this.__addDisparador(disparador.id,()=>disparador);
    }
    __AddElemento_V_D(id,usarUltimaValidacion,crearDisparador){
        let e=this.__alAddElemento_V_D(usarUltimaValidacion);//id,
        if(esLista(id)){
            for (const idActual of id) {
                this.__addDisparador(idActual,crearDisparador);
            }
        }else{
            this.__addDisparador(id,crearDisparador);
            
        }
        return e;
    }
    __AddElementoTemporal_V_D(key,id,usarUltimaValidacion,crearDisparador){
        let e=this.__alAddElemento_V_D(usarUltimaValidacion);//id,
        this.__addDisparadorTemporal(key,id,crearDisparador);
        return e;
    }
    
    __AddElemento_V_D_Text(id,usarUltimaValidacion){
        //let usarUltimaValidacion=v=>v.addText_CON_ALFANUMERICOS(id,condicionDeEvaluacion);
        //let crearDisparador=()=>new ElementoDisparadorDeValidacionText();
        return this.__AddElemento_V_D(id,usarUltimaValidacion,()=>new ElementoDisparadorDeValidacionText());
    }

    __AddElementoTemporal_V_D_Text(key,id,usarUltimaValidacion){
        return this.__AddElementoTemporal_V_D(key,id,usarUltimaValidacion,()=>new ElementoDisparadorDeValidacionText());
    }

    
    __aplicarAUltimos_ElementoParaValidacion_Agregados(accion){//tipo v=>{usar v} v es el elemento actual
        if(this._ultimo_ElementoParaValidacion_Agregado==null){
            this._ultimos_ElementoParaValidacion_Agregados.forEach(accion);
        }else{
            accion(this._ultimo_ElementoParaValidacion_Agregado);
        }
        
        return this;
    }
    setMaxCar(max){
        return this.__aplicarAUltimos_ElementoParaValidacion_Agregados(v=>v.setMaxCar(max));
    }
    setMinCar(min){
        return this.__aplicarAUltimos_ElementoParaValidacion_Agregados(v=>v.setMinCar(max));
    }
    setDependeDeCB(idCB){
        this.addDisparadorCB(idCB);
        return this.__aplicarAUltimos_ElementoParaValidacion_Agregados(v=>v.setDependeDeCB(idCB));
        
    }
    setDependeDeCB_Not(idCB){
        this.addDisparadorCB(idCB);
        return this.__aplicarAUltimos_ElementoParaValidacion_Agregados(v=>v.setDependeDeCB_Not(idCB));
    }

    addBotonesDisparadores(listaIds){
        
        for (let index = 0; index < listaIds.length; index++) {
            const id = listaIds[index];
            this.__addDisparador(id,()=>new ElementoDisparadorDeValidacionBoton());
        }
        return this;
    }
    addDisparadorCB(id){
        this.__addDisparador(id,()=>new ElementoDisparadorDeValidacionCB());
    }
    addCBDisparadores(listaIds){
        for (let index = 0; index < listaIds.length; index++) {
            const id = listaIds[index];
            this.addDisparadorCB(id);
        }
        return this;
    }

    addBotonADesactivar(id){
        this.__addElementoADesactivar(id,()=>new ElementoADesactivar());
    }

    __addElementoNumerico(id,usarUltimaValidacion){
        return this.__AddElemento_V_D(id,usarUltimaValidacion
        ,()=>new ElementoDisparadorNumerico());
    }

    add_Temporal_Text_NO_EMPTY(key,id,condicionDeEvaluacion){
        let e=this.__AddElementoTemporal_V_D_Text(key,id,v=>v.add_Temporal_Text_NO_EMPTY(key,id,condicionDeEvaluacion));
        return e;
        
    }

    addText_CON_ALFANUMERICOS(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_CON_ALFANUMERICOS(id,condicionDeEvaluacion));
        return e;
    }
    addTexts_CON_ALFANUMERICOS(listaIds){
        this._ultimos_ElementoParaValidacion_Agregados=[];
        for (let index = 0; index < listaIds.length; index++) {
            const id = listaIds[index];
            let e=this.addText_CON_ALFANUMERICOS(id);
            this._ultimos_ElementoParaValidacion_Agregados.push(e);
        }
        this._ultimo_ElementoParaValidacion_Agregado=null;
        return e;
    }
    addText_NO_EMPTY(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_NO_EMPTY(id,condicionDeEvaluacion));
        return e;
    }


    addText_CORREO(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_CORREO(id,condicionDeEvaluacion));
        return e;
    }
    addText_SOLO_LETRAS(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_SOLO_LETRAS(id,condicionDeEvaluacion));
        return e;
    }
    addText_SOLO_LETRAS_Y_NUMEROS(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_SOLO_LETRAS_Y_NUMEROS(id,condicionDeEvaluacion));
        return e;
    }
    addText_SOLO_ALFANUMERICOS(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text(id,v=>v.addText_SOLO_ALFANUMERICOS(id,condicionDeEvaluacion));
        return e;
    }
    addTexts_Contraseña(id,idConfirmacion,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D_Text([id,idConfirmacion],v=>v.addTexts_Contraseña(id,idConfirmacion,condicionDeEvaluacion));
        return this;
    }

    //addText_SOLO_ALFANUMERICOS
    //addText_SOLO_LETRAS_Y_NUMEROS
    //addText_SOLO_LETRAS
    //addTexts_Contraseña(id,idConfirmacion,condicionDeEvaluacion){
    

    // addText_NO_EMPTY_CondicionCB(id,idCB){
    //     this.addDisparadorCB(idCB);
    //     let e=this.__AddElemento_V_D_Text(id,v=>v.addText_NO_EMPTY_CondicionCB(id,idCB));
    //     return e;
    // }

    

    add_EnteroPositivo(id,condicionDeEvaluacion){
        let e=this.__addElementoNumerico(id,v=>v.add_EnteroPositivo(id,condicionDeEvaluacion));
        return e;
        
    }
    addRange_EnteroPositivo(id,min,max,condicionDeEvaluacion){
        let e=this.__addElementoNumerico(id,v=>v.addRange_EnteroPositivo(id,min,max,condicionDeEvaluacion));
        return e;
        
    }
    add_Positivo(id,condicionDeEvaluacion){
        let e=this.__addElementoNumerico(id,v=>v.add_Positivo(id,condicionDeEvaluacion));
        return e;
    }
    addRange_Positivo(id,min,max,condicionDeEvaluacion){
        let e=this.__addElementoNumerico(id,v=>v.addRange_Positivo(id,min,max,condicionDeEvaluacion));
        return e;
    }

    addSelect_TipoValuePositivo(id,mensaje,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D(id,v=>v.addSelect_TipoValuePositivo(id,mensaje,condicionDeEvaluacion)
            ,()=>new ElementoDisparadorSelect());


        return e;
    }


    addInputFileImagen(id,condicionDeEvaluacion){

        let e=this.__AddElemento_V_D(id
            ,v=>v.addInputFileImagen(id,condicionDeEvaluacion)
            ,()=>new ElementoDisparadorDeValidacionInputFile()
            );


        return e;
    }

    addInputFile_Zip(id,condicionDeEvaluacion){
        let e=this.__AddElemento_V_D(id
            ,v=>v.addInputFile_Zip(id,condicionDeEvaluacion)
            ,()=>new ElementoDisparadorDeValidacionInputFile()
            );


        return e;
    }
    
}