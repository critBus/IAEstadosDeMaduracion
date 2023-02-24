/*
<script src="js/reneJavaScritp/reneJavaScrip.js"></script>


    <script src="js/reneJavaScritp/reneJS_Clases.js"></script>
    <script src="js/reneJavaScritp/reneJS_Repetidores.js"></script>
    <script src="js/reneJavaScritp/reneJS_UtilesParaControles.js"></script>
    <script src="js/reneJavaScritp/reneJS_Filtros.js"></script>
    <script src="js/reneJavaScritp/reneJS_Validacion.js"></script>
    <script src="js/reneJavaScritp/reneJS_UtilesDeLibrerias.js"></script>
    <script src="js/reneJavaScritp/reneJS_Boostrap/reneJS_Bootstrap.js"></script>
    <script src="js/reneJavaScritp/reneJS_Boostrap/reneJS_Bootstrap_Validacion.js"></script>
*/

class ListaSeleccionable{
    constructor(){
        this.KEY_ID_ITEM_LISTA="idItemLista";
        this.bd;//=new BD_RowElement();
        
        this.idLista;

        //this.contenidoOriginalDeLista;


        this.indiceSeleccionado;

        // this.alAgregarComponente;//(fr:FilaRow)=>{}
        // this.alSeleccionar;//(fr:FilaRow)=>{}
        // this.alResetearElVisual;

        this.__alAgregarComponente=new ConjuntoDeEventos();//(fr:FilaRow)=>{}
        this.__alSeleccionar=new ConjuntoDeEventos();//(fr:FilaRow)=>{}
        this.__alDeseleccionar=new ConjuntoDeEventos();//(fr:FilaRow)=>{}
        this.__alResetearElVisual=new ConjuntoDeEventos();

        //this.metodoActualizarRow;
        this.metodoGetListaValues;
        this.idContenedorDeLista;


        this.__setSePuedeRealizarValidacion=true;


        this.filaBDSeleccionada=null;
        this.mngRpLista=null;


    }
    addAlAgregarComponente(metodo){
        //(fr:FilaRow)=>{}
        this.__alAgregarComponente.add(metodo);
    }
    addAlResetearElVisual(metodo){
        this.__alResetearElVisual.add(metodo);
    }
    addAlSeleccionar(metodo){
        this.__alSeleccionar.add(metodo);
    }
    addAlDeseleccionar(metodo){
        this.__alDeseleccionar.add(metodo);
    }


    setSePuedeRealizarValidacion(sePuede){
        this.__setSePuedeRealizarValidacion=sePuede;
    }
    getSePuedeRealizarValidacion(){
        return this.__setSePuedeRealizarValidacion;
    }
    // addAlSeleccionar(metodoAlSeleccionar){//(fr:FilaRow)=>{}
    //     if(this.alSeleccionar!=undefined&&this.alSeleccionar!=null){
    //         const anterior=this.alSeleccionar;
    //         this.alSeleccionar=(fr)=>{
    //             anterior(fr);
    //             metodoAlSeleccionar(fr);
    //         };

    //     }else{
    //         this.alSeleccionar=metodoAlSeleccionar;
    //     }
    // }
    // __guardarContenido(){
    //     this.contenidoOriginalDeLista=getHTML(this.idLista);
    // }

    __getRow(indice){
        return this.bd.getRow(indice);
    }

    __getID_ItemLista(row){
        return row.get(this.KEY_ID_ITEM_LISTA);
    }
    getID_ItemLista(indice){
        return this.__getID_ItemLista(this.__getRow(indice));
    }
    __actualizarBD(){
        //console.log("this.metodoGetListaValues="+this.metodoGetListaValues);
        for (let index = 0; index < this.bd.size(); index++) {
            this.bd.setRow(index,this.metodoGetListaValues(this.__getRow(index)));

            //const filaRow = this.bd.getFila(index);
            //this.metodoActualizarRow(filaRow);

            // let idInputCarpeta=this.__getID_InputCarpeta(row);
            // let idInputClasificacion=this.__getID_InputClasificacion(row);
            // this.bd.setRow([getValue(idInputClasificacion),getValue(idInputCarpeta)]);
        }
    }


    // setLista(lista){
    //     let l=[];
    //     if(lista!=undefined&&lista!=null){
    //         l=lista;
    //     }


    //     for (let index = 0; index < l.length; index++) {
    //         const row = l[index];
    //         this.bd.addRow(row)

    //     }
    //     this.actualizarVisual_APartirDeBD();
    // }
    actualizarVisual_APartirDeBD(){
        //console.log("va a ver si no era undefinained");
        // if(this.alResetearElVisual!=undefined&&this.alResetearElVisual!=null){
        //     //console.log("intenta resetear el visual");
        //     this.alResetearElVisual();
        // }
        this.__alResetearElVisual.ejecutar();
        //this.bd.mirarBD("a3:");
        //console.log("reseteo el visual");
        // console.log("this.bd="+this.bd);
        // console.log("this.bd.llaves="+this.bd.llaves);
        // console.log("this.bd.llaves.length="+this.bd.llaves.length );
        //repetidor(this.idLista,this.bd,this.contenidoOriginalDeLista);
        this.mngRpLista.repetir();
        //this.bd.mirarBD("a4:");
        for (let index = 0; index < this.bd.size(); index++) {
            //const row = this.__getRow(index);
            const fila=this.bd.getFila(index);
            const row =fila.map;
            this.__addOnClickItemLista(row,index);

            // if(this.alAgregarComponente!=undefined&&this.alAgregarComponente!=null){
            //     this.alAgregarComponente(fila);
            // }
            this.__alAgregarComponente.ejecutar(fila);
        }
        //console.log("termino de actualizar");
    }
    haySeleccionado(){
        return this.indiceSeleccionado!=undefined&&this.indiceSeleccionado!=null;
    }


    __setSelected(indice,idItemListaParametro){
        let idItemLista=idItemListaParametro;
        if(idItemListaParametro==undefined||idItemListaParametro==null){
            idItemLista=this.getID_ItemLista(indice);
        }



        const CLASE_SELECTED="active";
        this.indiceSeleccionado=indice;

        ponerClase(idItemLista,CLASE_SELECTED);
        for (let index = 0; index < this.bd.size(); index++) {
            const row = this.__getRow(index);
            let idItemListaActual=this.__getID_ItemLista(row);
            if(indice!==index){
                quitarClase(idItemListaActual,CLASE_SELECTED);
            }
        }
        // if(this.alSeleccionar!=undefined&&this.alSeleccionar!=null){
        //     this.filaBDSeleccionada=this.bd.getFila(indice);
        //     this.alSeleccionar(this.filaBDSeleccionada);

        // }
        this.filaBDSeleccionada=this.bd.getFila(indice);
        this.__alSeleccionar.ejecutar(this.filaBDSeleccionada);

    }


    __setDeselected(indice,idItemListaParametro){
        let idItemLista=idItemListaParametro;
        if(idItemListaParametro==undefined||idItemListaParametro==null){
            idItemLista=this.getID_ItemLista(indice);
        }



        const CLASE_SELECTED="active";

        this.indiceSeleccionado=null;




        quitarClase(idItemLista,CLASE_SELECTED);


        //if(!this.__alDeseleccionar.isEmpty()){
            this.filaBDSeleccionada=this.bd.getFila(indice);
            this.__alDeseleccionar.ejecutar(this.filaBDSeleccionada);
            //this.alSeleccionar(this.filaBDSeleccionada);

        //}


    }

    __addOnClickItemLista(row,indice){//
        const self=this;
        const idItemLista=this.__getID_ItemLista(row);
        addOnClick(idItemLista,v=>{
            self.__setSelected(indice,idItemLista);

        });
    }

    deseleccionarTodo(){
        if(this.haySeleccionado()){
            this.__setDeselected(this.indiceSeleccionado);
        }


        this.indicesSeleccionados=[];
        this.indicesSeleccionado=null;
    }
    aplicarConfiguracion(){
        //this.__guardarContenido();
        //this.setLista(lista);
        if(this.mngRpLista==null||this.mngRpLista==undefined){
            this.mngRpLista=new ManagerRepetidor(this.idLista,this.bd);
        }

        this.actualizarVisual_APartirDeBD();


        const self=this;




    }
    actualizarUsandoLaBD(usarLaBD){
        //usarLaBD bd=>{}
        //console.log("va a intentar actualizar la bd");
        this.__actualizarBD();
        this.bd.mirarBD("a1:");
        //console.log("la actualizo");
        this.setSePuedeRealizarValidacion(false);
        usarLaBD(this.bd);
        this.setSePuedeRealizarValidacion(true);
        this.bd.mirarBD("a2:");
        //console.log("la uso");
        this.actualizarVisual_APartirDeBD();
    }

    // this.__actualizarBD();
    //         self.bd.addRowEmpty();
    //         self.actualizarVisual_APartirDeBD();
}



class ElementoParaValidacion_ListaSeleccionable_MenuAgregarEliminarArribaAbajo extends ElementoParaValidacion{
    constructor(lista){
        super(lista.idLista);
        this.lista=lista;
        this.metodoGetValorAEvaluar=v=>{
            // console.log("retorna lista? "+(v.lista instanceof ListaSeleccionable_MenuAgregarEliminarArribaAbajo));
            // console.log("retorna a "+v.lista);
            return v.lista;
        };
    }
    
}
class ElementoDisparadorDeValidacion_ListaSeleccionable_MenuAgregarEliminarArribaAbajo extends ElementoDisparadorDeValidacion{
    constructor(lista){
        super();
        this.lista=lista;
        this.metodoAplicarDisparador=(e,v)=>{
            e.lista.bd.addAlVariarSize(bd=>{
                if(e.lista.getSePuedeRealizarValidacion()){
                    v.comprovarValidacionYDesactivar();
                }
                
            });
        };
    }
}

class ListaSeleccionable_MenuAgregarEliminarArribaAbajo extends ListaSeleccionable{
    constructor(){
        super();
        
        
        this.idB_Agregar;
        this.idB_Eliminar;
        this.idB_Arriba;
        this.idB_Abajo;


        this.__minimoDeFilas;
        this.__maximoDeFilas;

        this.__sePusoEvento_MinimoDefilas=false;
        this.__sePusoEvento_MaximoDefilas=false;
        // this.__alVariarSize_minimo_anterior;
        // this.__alVariarSize_maximo_anterior;
        
    }
    __setMinimoDeFilas_evento(){
        const self=this;
        //if(){}
        this.bd.addAlVariarSize(v=>{
            setDisabled(self.bd.size()<=self.__minimoDeFilas,[self.idB_Eliminar])
            
        });
    }
    setMinimoDeFilas(cantidad){
        this.__minimoDeFilas=cantidad;
        if(!this.__sePusoEvento_MinimoDefilas){
            this.__setMinimoDeFilas_evento();
            this.__sePusoEvento_MinimoDefilas=true;
        }
        return this;
    }
    __setMaximoDeFilas_evento(){
        const self=this;
        this.bd.addAlVariarSize(v=>{
            setDisabled(self.bd.size()>=self.__maximoDeFilas,[self.idB_Agregar])
            
        });
    }
    setMaximoDeFilas(cantidad){
        this.__maximoDeFilas=cantidad;
        if(!this.__sePusoEvento_MaximoDefilas){
            this.__setMaximoDeFilas_evento();
            this.__sePusoEvento_MaximoDefilas=true;
        }
        return this;
    }
    hayMinimoDeFilas(){
        return this.__minimoDeFilas!=undefined&&this.__minimoDeFilas!=null;
    }

    aplicarConfiguracion(){
        if(this.hayMinimoDeFilas()&&this.bd.size()<this.__minimoDeFilas){
            for (let index = this.bd.size(); index < this.__minimoDeFilas; index++) {
                this.bd.addRowEmpty();
            }
        }
        super.aplicarConfiguracion();
       
        

        const self=this;

        

        addOnClick(this.idB_Agregar,v=>{
            this.__actualizarBD();
            self.bd.addRowEmpty();
            self.actualizarVisual_APartirDeBD();

            
            self.__setSelected(self.bd.getLastIndex());
            moverScrollAlfinal(this.idContenedorDeLista);
        });
        addOnClick(this.idB_Eliminar,v=>{
            if(!self.bd.isEmpty()){
                this.__actualizarBD();
                let seleccionadoAnterior=self.indiceSeleccionado;
                let habiaSeleccionado=self.haySeleccionado();
                if(habiaSeleccionado){
                    self.bd.remove(self.indiceSeleccionado);
                    
                }else{
                    self.bd.removeLast();
                    
                }
                
                self.actualizarVisual_APartirDeBD();
                if(habiaSeleccionado){
                    if(seleccionadoAnterior>0){
                        self.__setSelected(seleccionadoAnterior-1);
                    }else{
                        if(self.bd.size()>0){
                            self.__setSelected(seleccionadoAnterior);
                        }else{
                            self.indiceSeleccionado=null;
                        }
                    }
                }
            }
            

        });
        addOnClick(this.idB_Arriba,v=>{
            if((!self.bd.isEmpty())&&self.bd.size()>1&&self.haySeleccionado()&&self.indiceSeleccionado>0){
                this.__actualizarBD();
                let indiceNuevo=self.indiceSeleccionado-1;
                self.bd.swap(self.indiceSeleccionado,indiceNuevo);
                self.actualizarVisual_APartirDeBD();
                self.__setSelected(indiceNuevo);

            }
            
            
        });

        addOnClick(this.idB_Abajo,v=>{
            if((!self.bd.isEmpty())&&self.bd.size()>1&&self.haySeleccionado()&&self.indiceSeleccionado<self.bd.getLastIndex()){
                this.__actualizarBD();
                let indiceNuevo=self.indiceSeleccionado+1;
                self.bd.swap(self.indiceSeleccionado,indiceNuevo);
                self.actualizarVisual_APartirDeBD();
                self.__setSelected(indiceNuevo);

            }
            
            
        });


    }


    newElementoParaValidacion(){
        return new ElementoParaValidacion_ListaSeleccionable_MenuAgregarEliminarArribaAbajo(this);
    }

    setValidacion(validacionConEventos,listaElementosParaValidacion){//matrisPar_MetodoValidarLista_Y_mensaje
        for (let index = 0; index < listaElementosParaValidacion.length; index++) {
            const e = listaElementosParaValidacion[index];
            validacionConEventos.agregarElemento(e);
        }
        // for (const e of listaElementosParaValidacion) {
        //     validacionConEventos.agregarElemento(e);
        // }
        validacionConEventos.agregarDisparador(new ElementoDisparadorDeValidacion_ListaSeleccionable_MenuAgregarEliminarArribaAbajo(this));
        return this;
    }


}



// class TipoDeValidacion_ListaSeleccionable_MenuAgregarEliminarArribaAbajo extends TipoDeValidacion{
    
// }




// class Lista2ColTextInput{
//     constructor(){
//         this.KEY_CLASIFICACION="Clasificacion";
//         this.KEY_CARPETA="Carpeta";
//         this.KEY_ID_INPUT_CLASIFICACION="IdInputClasificacion";
//         this.KEY_ID_INPUT_CARPETA="IdInputCarpeta";
//         this.KEY_ID_ITEM_LISTA="idItemLista";
//         this.bd=new BD_RowElement();
//         bd.llaves=[this.KEY_CLASIFICACION,this.KEY_CARPETA];
//         bd.listaDeNombresIds=[this.KEY_ID_INPUT_CLASIFICACION,this.KEY_ID_INPUT_CARPETA,this.KEY_ID_ITEM_LISTA];

//         this.idLista;

//         this.contenidoOriginalDeLista;
        
//         this.idB_Agregar;
//         this.idB_Eliminar;
//         this.idB_Arriba;
//         this.idB_Abajo;

//         this.indiceSeleccionado;

//         this.alAgregarComponente;
//     }
//     __guardarContenido(){
//         this.contenidoOriginalDeLista=getHTML(this.idLista);
//     }
    // __actualizarBD(){
    //     for (let index = 0; index < this.bd.size(); index++) {
    //         const row = this.__getRow(index);
    //         let idInputCarpeta=this.__getID_InputCarpeta(row);
    //         let idInputClasificacion=this.__getID_InputClasificacion(row);
    //         this.bd.setRow([getValue(idInputClasificacion),getValue(idInputCarpeta)]);
    //     }
    // }
//     __getListaContenido(){
//         let l=[];
//         for (let index = 0; index < this.bd.size(); index++) {
//             const row = this.__getRow(index);
//             let idInputCarpeta=this.__getID_InputCarpeta(row);
//             let idInputClasificacion=this.__getID_InputClasificacion(row);
//             l.push([getValue(idInputClasificacion),getValue(idInputCarpeta)]);
//         }
//         return l;
//     }
//     __getRow(indice){
//         return this.bd.getRow(indice);
//     }
//     __getID_InputCarpeta(row){
//         return row.get(this.KEY_ID_INPUT_CARPETA);
//     }
//     __getID_InputClasificacion(row){
//         return row.get(this.KEY_ID_INPUT_CLASIFICACION);
//     }
//     __getID_ItemLista(row){
//         return row.get(this.KEY_ID_ITEM_LISTA);
//     }
//     getID_ItemLista(indice){
//         return this.__getID_ItemLista(this.__getRow(indice));
//     }
//     getID_InputCarpeta(indice){
//         return this.__getID_InputCarpeta(this.__getRow(indice));
//     }
//     getID_InputClasificacion(indice){
//         return this.__getID_InputClasificacion(this.__getRow(indice));
//     }

//     setLista(lista){
//         let l=[];
//         if(lista!=undefined&&lista!=null){
//             l=lista;
//         }

        
//         for (let index = 0; index < l.length; index++) {
//             const row = l[index];
//             this.bd.addRow(row)
//             // let contenidoClasificacion=row[0];
//             // let contenidoCarpeta=row[1];
//         }
//         this.actualizarVisual_APartirDeBD();
//     }
//     actualizarVisual_APartirDeBD(){
//         repetidor(this.idLista,this.bd,this.contenidoOriginalDeLista);
//         for (let index = 0; index < this.bd.size(); index++) {
//             const row = this.__getRow(index);
//             this.__addOnClickItemLista(row,index);
//         }
//     }
//     haySeleccionado(){
//         return this.indiceSeleccionado!=undefined&&this.indiceSeleccionado!=null;
//     }
    

//     __setSelected(indice){

//         const CLASE_SELECTED="active";
//         self.indiceSeleccionado=indice;
//         ponerClase(idItemLista,CLASE_SELECTED);
//         for (let index = 0; index < self.bd.size(); index++) {
//             const row = self.__getRow(index);
//             let idItemListaActual=this.__getID_ItemLista(row);
//             //if(idItemLista!==idItemListaActual){
//             if(indice!==index){
//                 quitarClase(idItemListaActual,CLASE_SELECTED);
//             }
//         }
//     }

//     __addOnClickItemLista(row,indice){
//         const self=this;
//         const idItemLista=this.__getID_ItemLista(row);
//         addOnClick(idItemLista,v=>{
//             self.__setSelected(indice);

//         });
//     }
    

//     aplicarConfiguracion(lista){
//         this.__guardarContenido();
//         this.setLista(lista);

//         const self=this;

        

//         addOnClick(this.idB_Agregar,v=>{
//             // let lista=self.__getListaContenido();
//             // lista.push(["",""]);

//             //self.setLista(lista);
//             self.bd.addRow(["",""]);
//             self.actualizarVisual_APartirDeBD();

//             // let index=self.bd.getLastIndex();
//             // let row=self.bd.getRow(index);
//             // self.__addOnClickItemLista(row,index);

//             self.__setSelected(self.bd.getLastIndex());
//         });
//         addOnClick(this.idB_Eliminar,v=>{
//             if(!self.bd.isEmpty()){
//                 //let lista=self.__getListaContenido();
//                 let seleccionadoAnterior=self.indiceSeleccionado;
//                 let habiaSeleccionado=self.haySeleccionado();
//                 if(habiaSeleccionado){
//                     self.bd.remove(self.indiceSeleccionado);
//                     // lista.splice(self.indiceSeleccionado,1);
//                 }else{
//                     self.bd.removeLast();
//                     // lista.pop();
//                 }
//                 //self.setLista(lista);
//                 self.actualizarVisual_APartirDeBD();
//                 if(habiaSeleccionado){
//                     if(seleccionadoAnterior>0){
//                         self.__setSelected(seleccionadoAnterior-1);
//                     }else{
//                         if(self.bd.size()>0){
//                             self.__setSelected(seleccionadoAnterior);
//                         }else{
//                             self.indiceSeleccionado=null;
//                         }
//                     }
//                 }
//             }
            

//         });
//         addOnClick(this.idB_Arriba,v=>{
//             if((!self.bd.isEmpty())&&self.bd.size()>1&&self.haySeleccionado()&&self.indiceSeleccionado>0){
//                 let indiceNuevo=self.indiceSeleccionado-1;
//                 self.bd.swap(self.indiceSeleccionado,indiceNuevo);
//                 self.actualizarVisual_APartirDeBD();
//                 self.__setSelected(indiceNuevo);

//             }
            
            
//         });

//         addOnClick(this.idB_Abajo,v=>{
//             if((!self.bd.isEmpty())&&self.bd.size()>1&&self.haySeleccionado()&&self.indiceSeleccionado<self.bd.getLastIndex()){
//                 let indiceNuevo=self.indiceSeleccionado+1;
//                 self.bd.swap(self.indiceSeleccionado,indiceNuevo);
//                 self.actualizarVisual_APartirDeBD();
//                 self.__setSelected(indiceNuevo);

//             }
            
            
//         });


//     }
// }