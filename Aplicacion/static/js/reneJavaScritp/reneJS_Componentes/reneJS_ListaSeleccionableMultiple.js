
class ListaSeleccionableMultiple{
    constructor(){
        this.KEY_ID_ITEM_LISTA="idItemLista";
        this.bd;//=new BD_RowElement();

        this.idLista;

        //this.contenidoOriginalDeLista;


        this.indiceSeleccionado;

        this.__alAgregarComponente=new ConjuntoDeEventos();//(fr:FilaRow)=>{}
        this.__alSeleccionar=new ConjuntoDeEventos();;//(fr:FilaRow)=>{}
        this.__alDeseleccionar=new ConjuntoDeEventos();;//(fr:FilaRow)=>{}
        this.__alResetearElVisual=new ConjuntoDeEventos();

        //this.metodoGetListaValues;
        //this.idContenedorDeLista;


        //this.__setSePuedeRealizarValidacion=true;


        this.filaBDSeleccionada=null;


        this.indicesSeleccionados=[];
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

    deseleccionarTodo(){
        while(this.indicesSeleccionados.length>0){
            this.__setDeselected(this.indicesSeleccionados[0]);
        }
        // for (let index = 0; index < this.indicesSeleccionados.length; index++) {
        //     const indice = this.indicesSeleccionados[index];
        //     this.__setDeselected(indice);
        // }
        this.indicesSeleccionados=[];
        this.indicesSeleccionado=null;
    }


    actualizarVisual_APartirDeBD(){


        //console.log("va a ver si no era undefinained");
        //if(!this.__alResetearElVisual.isEmpty()){
            //console.log("intenta resetear el visual");
            this.__alResetearElVisual.ejecutar();
        //}
       this.mngRpLista.repetir();
        //repetidor(this.idLista,this.bd,this.contenidoOriginalDeLista);
        //this.bd.mirarBD("a4:");
        for (let index = 0; index < this.bd.size(); index++) {
            const fila=this.bd.getFila(index);
            const row =fila.map;
            this.__addOnClickItemLista(row,index);

            //if(!this.__alAgregarComponente.isEmpty()){
                this.__alAgregarComponente.ejecutar(fila);

            //}
        }




        //console.log("termino de actualizar");
    }
    haySeleccionado(){
        //return this.indiceSeleccionado!=undefined&&this.indiceSeleccionado!=null;
        return this.indicesSeleccionados.length>0;
    }


    __setSelected(indice,idItemListaParametro){
        let idItemLista=idItemListaParametro;
        if(idItemListaParametro==undefined||idItemListaParametro==null){
            idItemLista=this.getID_ItemLista(indice);
        }



        const CLASE_SELECTED="active";
        this.indiceSeleccionado=indice;
        this.indicesSeleccionados.push(indice);

        ponerClase(idItemLista,CLASE_SELECTED);

        // for (let index = 0; index < this.bd.size(); index++) {
        //     const row = this.__getRow(index);
        //     let idItemListaActual=this.__getID_ItemLista(row);
        //     if(indice!==index){
        //         quitarClase(idItemListaActual,CLASE_SELECTED);
        //     }
        // }

        //if(!this.__alSeleccionar.isEmpty()){
            this.filaBDSeleccionada=this.bd.getFila(indice);
            this.__alSeleccionar.ejecutar(this.filaBDSeleccionada);
            //this.alSeleccionar(this.filaBDSeleccionada);

       // }


    }
    remove(indice){
        this.indicesSeleccionados=[...this.indicesSeleccionados].sort();

        if(this.indicesSeleccionados.includes(indice)){
            this.__setDeselected(indice);

        }
        for (let i = 0; i < this.indicesSeleccionados.length; i++) {
            if(this.indicesSeleccionados[i]<=indice){
                this.indicesSeleccionados[i]=this.indicesSeleccionados[i]-1;
            }

        }
        this.bd.remove(indice);
    }
    removeLosSeleccionados(){
        let aEliminar=[...this.indicesSeleccionados];
        for (let i = 0; i < aEliminar.length; i++) {
            this.__setDeselected(aEliminar[i]);
        }
        bd.remove(aEliminar);
    }
    clear(){
        this.indicesSeleccionados=[];
        this.indiceSeleccionado=null;
        this.bd.clear()
        this.actualizarVisual_APartirDeBD()
    }

    __setDeselected(indice,idItemListaParametro){
        let idItemLista=idItemListaParametro;
        if(idItemListaParametro==undefined||idItemListaParametro==null){
            idItemLista=this.getID_ItemLista(indice);
        }



        const CLASE_SELECTED="active";
        removeO(this.indicesSeleccionados,indice);
        if(indice==this.indiceSeleccionado){
            this.indiceSeleccionado=null;
            if(this.indicesSeleccionados.length>0){
                this.indiceSeleccionado=this.indicesSeleccionados[0];
            }
        }




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
            if(self.indicesSeleccionados.includes(indice)){
                self.__setDeselected(indice,idItemLista);
            }else{
                self.__setSelected(indice,idItemLista);
            }


        });
    }

    // setSePuedeRealizarValidacion(sePuede){
    //     this.__setSePuedeRealizarValidacion=sePuede;
    // }
    // getSePuedeRealizarValidacion(){
    //     return this.__setSePuedeRealizarValidacion;
    // }
    // actualizarUsandoLaBD(usarLaBD){
    //     //console.log("va a intentar actualizar la bd");
    //     this.__actualizarBD();
    //     this.bd.mirarBD("a1:");
    //     //console.log("la actualizo");
    //     this.setSePuedeRealizarValidacion(false);
    //     usarLaBD(this.bd);
    //     this.setSePuedeRealizarValidacion(true);
    //     this.bd.mirarBD("a2:");
    //     //console.log("la uso");
    //     this.actualizarVisual_APartirDeBD();
    // }
    // __actualizarBD(){
    //     //console.log("this.metodoGetListaValues="+this.metodoGetListaValues);
    //     for (let index = 0; index < this.bd.size(); index++) {
    //         this.bd.setRow(index,this.metodoGetListaValues(this.__getRow(index)));

    //         //const filaRow = this.bd.getFila(index);
    //         //this.metodoActualizarRow(filaRow);

    //         // let idInputCarpeta=this.__getID_InputCarpeta(row);
    //         // let idInputClasificacion=this.__getID_InputClasificacion(row);
    //         // this.bd.setRow([getValue(idInputClasificacion),getValue(idInputCarpeta)]);
    //     }
    // }


    aplicarConfiguracion(){
        //this.__guardarContenido();
        this.mngRpLista=new ManagerRepetidor(this.idLista,this.bd);;

        this.actualizarVisual_APartirDeBD();


        const self=this;




    }



}


