//import reneJavaScrip
//import reneJS_Clases
//import reneJS_Paginacion
class PaginacionVisual {
    constructor() {
        this.idListaPaginacion = null;
        this.idNodoSeleccionadoPlantilla = null;
        this.idNodoNoSeleccionadoPlantilla = null;
        //los id de arriba son los que se necesitan


        this.idAnterior = null;
        this.idSiguiente = null;

        this.KEY_INDICE = "KEY_INDICE";
        this.KEY_ID = "KEY_ID_";
        this.bd = new BD_RowElement();
        this.bd.llaves = [this.KEY_INDICE];
        this.bd.listaDeNombresIds = [this.KEY_ID];

        this.paginacion = null;
        this.nodoSiguiente = null;
        this.nodoAnterior = null;

        this.nodoSiguientePlantilla = null;
        this.nodoAnteriorPlantilla  = null;

        this.nodoSeleccionado = null;
        this.nodoNoSeleccionado = null;

        // this.mngDesactivarAnterior=null;
        // this.mngDesactivarSiguiente=null;

        this.eventosOnClickNoSeleccionado = new ConjuntoDeEventos();

        this.eventosAlDesactivarAnteriorOSiguiente = new ConjuntoDeEventos();
    }
    addOnClickNoSeleccionado(metodo) {
        //metodo  (id,indice)->{}
        this.eventosOnClickNoSeleccionado.add(metodo);
    }
    addAlDesactivarAnteriorOSiguiente(metodo) {
        //metodo (id)=>{} 
        this.eventosAlDesactivarAnteriorOSiguiente.add(metodo);
    }
    __getNombreID_elemntoPaginacion(i) {
        return this.idListaPaginacion + "_paginacion_" + i;
    }
    actualizar(paginacion) {
        const self = this;
        this.paginacion = paginacion;
        this.bd.clear();
        for (let index = 0; index < this.paginacion.listaDeIndices.length; index++) {
            const indiceActual = this.paginacion.listaDeIndices[index];
            this.bd.addRow([indiceActual]);
        }

        this.nodoSiguiente = getCopyEl(this.nodoSiguientePlantilla);
        this.nodoAnterior = getCopyEl(this.nodoAnteriorPlantilla);



        clearEl(this.idListaPaginacion);
        addEl(this.idListaPaginacion, this.nodoAnterior);
        for (let index = 0; index < this.bd.size(); index++) {
            let fila = this.bd.getFila(index);
            let map = fila.map;
            let node = null;
            let esElSeleccionado = this.paginacion.iSeleccionado == index
            if (esElSeleccionado) {
                node = this.nodoSeleccionado;
            } else {
                node = this.nodoNoSeleccionado;
            }
            node = getCopyEl(node);
            const idDeEsteNodo = this.__getNombreID_elemntoPaginacion(index);
            node.id = idDeEsteNodo;
            node = crearElementoDesdeLista(node, this.bd, index)
            addEl(this.idListaPaginacion, node);
            if (!esElSeleccionado) {
                const indiceActual = this.paginacion.getIndice(index);
                addOnClick(idDeEsteNodo, v => {
                    self.eventosOnClickNoSeleccionado.ejecutar(idDeEsteNodo, indiceActual);
                })
            }
        }

        addEl(this.idListaPaginacion, this.nodoSiguiente);

        let haySiguiente = this.paginacion.haySiguiente();
        setDisabled(!haySiguiente, [this.idSiguiente]);

        if (haySiguiente) {
            addOnClick(this.idSiguiente, v => {
                self.eventosOnClickNoSeleccionado.ejecutar(this.idSiguiente, this.paginacion.getIndiceSiguiente());
            })
        } else {
            this.eventosAlDesactivarAnteriorOSiguiente.ejecutar(this.idSiguiente);
        }

        let hayAnterior = this.paginacion.hayAnterior();
        setDisabled(!hayAnterior, [this.idAnterior]);

        if (hayAnterior) {
            addOnClick(this.idAnterior, v => {
                self.eventosOnClickNoSeleccionado.ejecutar(this.idAnterior, this.paginacion.getIndiceAnterior());
            })
        } else {
            this.eventosAlDesactivarAnteriorOSiguiente.ejecutar(this.idAnterior);
        }

    }

    aplicarConfiguracion() {

        //const nodoFirst=getCopyEl(this.idSiguiente);
        this.nodoSiguiente = getLastEl(this.idListaPaginacion);
        this.nodoSiguientePlantilla=getCopyEl(this.nodoSiguiente);
        // console.log("nodoSiguiente="+nodoSiguiente);
        // console.log("ty nodoSiguiente="+typeof(nodoSiguiente));
        this.idSiguiente = this.nodoSiguiente.id;

        this.nodoAnterior = getFirsEl(this.idListaPaginacion);
        this.nodoAnteriorPlantilla=getCopyEl(this.nodoAnterior);

        this.idAnterior = this.nodoAnterior.id;

        // this.mngDesactivarAnterior=new MangerElementoADesactivar(this.idAnterior);
        // this.mngDesactivarSiguiente=new MangerElementoADesactivar(this.idSiguiente);

        this.nodoSeleccionado = getCopyEl(this.idNodoSeleccionadoPlantilla);
        this.nodoNoSeleccionado = getCopyEl(this.idNodoNoSeleccionadoPlantilla);

        //this.actualizar(paginacion);
    }
}


class PaginacionVisualIndependiente extends PaginacionVisual{
    constructor(){
        super();
        this.gestorDePaginacion=null; 
    }
    aplicarConfiguracion() {
        const self=this;
        super.aplicarConfiguracion();
        this.addOnClickNoSeleccionado(
            (id,indice)=>{
                self.gestorDePaginacion.actualizar(indice);
                let p=self.gestorDePaginacion.getPaginacion();
                self.actualizar(p);
            }
        );
    }
}
////el nodo no ha sido añadido plq que no se debe buscar por getEl(id)