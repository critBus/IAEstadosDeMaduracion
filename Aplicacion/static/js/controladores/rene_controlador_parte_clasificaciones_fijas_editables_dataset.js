class ManagerClasesClasificicacionesFijosEditables {
    constructor(v) {
        this.V =v;

        this.metodo_CondicionComprobarCoicidenciaDeClases=()=>true;

        this.idCkEditor2="editor2"
        this.idLista = "idLista_2ColTextInput";

        this.idB_Agregar_L = "idB_ListaClases_Agregar";
        this.idB_Eliminar_L = "idB_ListaClases_Eliminar";
        this.idB_Arriba_L = "idB_ListaClases_Arriba";
        this.idB_Abajo_L = "idB_ListaClases_Abajo";
        this.idContenedorDeLista_L = "idContenedorDeLista";

        this.idB_Detalles_L = "idB_ListaClases_DetallesClase";
        this.idTextAreaDlg_Detalles_L = "idClasificacion_idDlgDetalles";
        this.idBAceptar_idDlgDetalles_L = "idBAceptar_idDlgDetalles";
        this.idDlgDetalles_L = "idDlgDetalles";



        this.idAlertaClasificaciones_MSL = "idAlerta_Listaclasificaciones";
        this.idConendorDebordeDeListaClasificaciones_MSL = "idContendorDeBordeDeListaclasificaciones";
        this.idBotonReiniciarClases_MSL = "idB_ListaClases_ReiniciarClases";







    }

    aplicarConfiguracion(){
        if(this.V==null||this.V==undefined){
            this.V = new ValidacionConEventos_Boostrap();
        }

        class EstadoDeEstaPagina {
            constructor() {


                //this.nombreCarpetasDeclasificacion = [];
                this.matris_Clasificacion_Carpeta_Descripcion=[];

            }

        }
        this.estado = new EstadoDeEstaPagina()

        this.KEY_CLASIFICACION = "Clasificacion";
        this.KEY_CARPETA = "Carpeta";
        this.KEY_ID_INPUT_CLASIFICACION = "IdInputClasificacion";
        this.KEY_ID_INPUT_CARPETA = "IdInputCarpeta";
        this.KEY_ID_ITEM_LISTA = "idItemLista";
        this.KEY_DETALLES = "detalles";

        const parent = this;


        CKEDITOR.replace(this.idCkEditor2);
        class ListaClasificacionesCarpeta extends ListaSeleccionable_MenuAgregarEliminarArribaAbajo {
            constructor() {
                super();
                this.idB_Detalles = parent.idB_Detalles_L;
                this.idTextAreaDlg_Detalles = parent.idTextAreaDlg_Detalles_L;
                this.idBAceptar_idDlgDetalles = parent.idBAceptar_idDlgDetalles_L;
                this.idDlgDetalles = parent.idDlgDetalles_L;

            }
            __getMapActual() {
                let habiaSeleccionado = this.haySeleccionado();
                let filaMap = null;
                if (habiaSeleccionado) {
                    filaMap = this.bd.getFila(this.indiceSeleccionado);//this.filaBDSeleccionada;
                } else {
                    filaMap = this.bd.getFila(0)
                }
                return filaMap.map;

            }
            getDetallesActuales() {
                let filaMap=this.__getMapActual();
                return filaMap.get(parent.KEY_DETALLES);
            }
            getDetallesEn(indice) {
                let filaMap = this.bd.getFila(indice);
                return filaMap.map.get(parent.KEY_DETALLES);
            }
            setDetalesActuales(detalles) {
                let indice = 0;
                if (this.haySeleccionado()) {
                    indice = this.indiceSeleccionado;
                }
                this.bd.set(indice, parent.KEY_DETALLES, detalles);

            }
            aplicarConfiguracion() {
                super.aplicarConfiguracion();
                const self = this;
                this.bd.addAlVariarSize(v => {
                    setDisabled(self.bd.isEmpty(), [this.idB_Detalles])

                });
                addOnClick(this.idB_Detalles, v => {
                    if (self.bd.isEmpty()) {
                        //console.log("canselado por return1 ");
                        return;
                    }
                    //self.bd.mirarBD("a2");
                    let detallesActuales=self.getDetallesActuales();
                    //console.log("detallesActuales="+detallesActuales);
                    CKEDITOR.instances.editor2.setData(detallesActuales);
                    showDlgBostrap(self.idDlgDetalles);
                    //let contenidoDetalles="";

                });
                addOnClick(this.idBAceptar_idDlgDetalles, v => {
                    if (self.bd.isEmpty()) {
                        console.log("canselado por return2 ");
                        return;
                    }
                    let detallesRecopilados = CKEDITOR.instances.editor2.getData();
                    //console.log("detallesRecopilados=" + detallesRecopilados);
                    self.setDetalesActuales(detallesRecopilados);

                    //self.bd.mirarBD("a1");

                });


            }
        }


        this.bd = new BD_RowElement();
        this.bd.llaves = [parent.KEY_CLASIFICACION, parent.KEY_CARPETA, parent.KEY_DETALLES];
        this.bd.listaDeNombresIds = [parent.KEY_ID_INPUT_CLASIFICACION, parent.KEY_ID_INPUT_CARPETA, parent.KEY_ID_ITEM_LISTA];

        this.bd.addAlVerBD(mbd => {
            for (let index = 0; index < parent.bd.size(); index++) {
                let fila = parent.bd.getFila(index);
                let map = fila.map;
                console.log("i=" + index);
                for (const m of map) {
                    console.log(m);
                }
            }
        });


        this.L = new ListaClasificacionesCarpeta();


        this.L.metodoGetListaValues = map => {
            let clasificacion = "";
            let carpeta = "";
            let idClasificacion = map.get(parent.KEY_ID_INPUT_CLASIFICACION);
            let idCarpeta = map.get(parent.KEY_ID_INPUT_CARPETA);
            if (existe(idClasificacion) && existe(idCarpeta)) {
                clasificacion = getValue(idClasificacion);
                carpeta = getValue(idCarpeta);
            }
            let detalles = map.get(parent.KEY_DETALLES);
            return [clasificacion, carpeta, detalles];
            //return [getValue(map.get(KEY_ID_INPUT_CLASIFICACION)), getValue(map.get(KEY_ID_INPUT_CARPETA))];
        };



        this.L.KEY_ID_ITEM_LISTA = parent.KEY_ID_ITEM_LISTA;
        this.L.bd = parent.bd;

        this.L.idLista = this.idLista;

        this.L.idB_Agregar = this.idB_Agregar_L;
        this.L.idB_Eliminar = this.idB_Eliminar_L;
        this.L.idB_Arriba =  this.idB_Arriba_L;
        this.L.idB_Abajo = this.idB_Abajo_L;
        this.L.idContenedorDeLista = this.idContenedorDeLista_L;
        this.L.setMinimoDeFilas(2);

        this.V.addAntesDeRealizarValidacion(v => {
            parent.L.__actualizarBD();
        });



        this.KEY_LISTA_TEMPORAL = "KEY_LISTA_TEMPORAL";
        this.L.alResetearElVisual = () => {
            //V.__getUltimaValidacion().mapListaDeElementosParaValidacionTemporales.set(KEY_LISTA_TEMPORAL,[]);
            parent.V.clearTemporal(parent.KEY_LISTA_TEMPORAL);
            // V.comprovarValidacionYDesactivar();
        };

        this.L.alAgregarComponente = (fr) => {

            const indice = fr.indice;
            const mapExterno = fr.map;
            //let elemento=null;

            let getTipoDeValidacion = (k, kc, m) => {
                let comprobacion = (t, v, k, kc) => {
                    //console.log("----------------------------------");
                    let id = t.idElemento;
                    let contenido = getValue(id);
                    //let lista=V.__getUltimaValidacion().mapListaDeElementosParaValidacionTemporales.get(KEY_LISTA_TEMPORAL);
                    for (let index = 0; index < parent.bd.size(); index++) {
                        let fila = parent.bd.getFila(index);
                        let map = fila.map;
                        let idActual = map.get(k);

                        let contenidoActual = map.get(kc);

                        if (id != idActual && contenido === contenidoActual) {//getValue(idActual)
                            //console.log("idActual="+idActual);
                            //console.log("getValue(idActual)="+getValue(idActual));
                            return false;
                        }
                    }
                    return true;
                };
                return new TipoDeValidacion((t, v) => comprobacion(t, v, k, kc), m);
            };//
            let tcarpeta = getTipoDeValidacion(parent.KEY_ID_INPUT_CARPETA, parent.KEY_CARPETA, "No puede existir carpetas con el mismo nombre");
            let tclasificacion = getTipoDeValidacion(parent.KEY_ID_INPUT_CLASIFICACION, parent.KEY_CLASIFICACION, "No puede existir Clasificaciones iguales ");


            let comprobacion = (t, v) => {
                //if (estado.faseDatasetDescomprimido) {
                if (parent.metodo_CondicionComprobarCoicidenciaDeClases()) {

                let id = t.idElemento;
                let contenido = getValue(id);
                for (let i = 0; i < parent.estado.matris_Clasificacion_Carpeta_Descripcion.length; i++) {
                    let carpeta = parent.estado.matris_Clasificacion_Carpeta_Descripcion[i][1];
                    if (carpeta === contenido) {
                        return true;
                    }
                }
                return false;

                }

                return true;
            };
            let tCarpeta_NombresCarpetas = new TipoDeValidacion(comprobacion, "Tienen que coincidir con los nombres reales de las carpetas del Dataset ");


            // console.log("mapExterno.get(KEY_CARPETA)=" + mapExterno.get(KEY_CARPETA));
            // console.log("mapExterno.get(KEY_ID_INPUT_CARPETA)=" + mapExterno.get(KEY_ID_INPUT_CARPETA));
            setValue(mapExterno.get(parent.KEY_ID_INPUT_CLASIFICACION), mapExterno.get(parent.KEY_CLASIFICACION));
            setValue(mapExterno.get(parent.KEY_ID_INPUT_CARPETA), mapExterno.get(parent.KEY_CARPETA));



            parent.V.add_Temporal_Text_NO_EMPTY(parent.KEY_LISTA_TEMPORAL, mapExterno.get(parent.KEY_ID_INPUT_CLASIFICACION)).addTipoDeValidacion(tclasificacion);//.addAlSerInvalido(alSerInvalido);
            parent.V.add_Temporal_Text_NO_EMPTY(parent.KEY_LISTA_TEMPORAL, mapExterno.get(parent.KEY_ID_INPUT_CARPETA)).addTipoDeValidacion(tcarpeta).addTipoDeValidacion(tCarpeta_NombresCarpetas);//.addAlSerInvalido(alSerInvalido);
            parent.V.comprovarValidacionYDesactivar();
            // V.__getUltimaValidacion().add_Temporal_Text_NO_EMPTY(KEY_LISTA_TEMPORAL,map.get(KEY_ID_INPUT_CLASIFICACION)).addTipoDeEvaluacion(tclasificacion);
            // V.__getUltimaValidacion().add_Temporal_Text_NO_EMPTY(KEY_LISTA_TEMPORAL,map.get(KEY_ID_INPUT_CARPETA)).addTipoDeEvaluacion(tcarpeta);
            //V.__getUltimaValidacion().mapListaDeElementosParaValidacionTemporales.get(KEY_LISTA_TEMPORAL).push(elemento);

        };


        this.L.addAlSeleccionar((fr) => {
            const indice = fr.indice;
            const map = fr.map;

            // console.log("----------------------------------");
            let claseTextoAmarillo = "text-warning";
            let idTextoNoValidoClasificacion = parent.V.__getID_MensajeInvalido_DeID(map.get(parent.KEY_ID_INPUT_CLASIFICACION));
            let idTextoNoValidoCarpeta = parent.V.__getID_MensajeInvalido_DeID(map.get(parent.KEY_ID_INPUT_CARPETA));
            ponerClase(idTextoNoValidoClasificacion, claseTextoAmarillo);
            ponerClase(idTextoNoValidoCarpeta, claseTextoAmarillo);

            for (let index = 0; index < parent.bd.size(); index++) {
                let fila = parent.bd.getFila(index);
                let mapActual = fila.map;


                if (indice != index) {

                    quitarClase(parent.V.__getID_MensajeInvalido_DeID(mapActual.get(parent.KEY_ID_INPUT_CLASIFICACION)), claseTextoAmarillo);
                    quitarClase(parent.V.__getID_MensajeInvalido_DeID(mapActual.get(parent.KEY_ID_INPUT_CARPETA)), claseTextoAmarillo);
                }
            }

        });
        this.L.aplicarConfiguracion();


        class ManagerValidacionSizeLista {
            constructor() {
                this.lista = parent.L;
                this.validacionConEneventos = parent.V;

                this.idAlertaClasificaciones = parent.idAlertaClasificaciones_MSL;
                this.idConendorDebordeDeListaClasificaciones = parent.idConendorDebordeDeListaClasificaciones_MSL;

                this.condicionSiEvaluarElSize = () => false;

                this.sizeQueTieneQueTener = 4;

                this.creadorDeMensaje = sz => "la lista tiene que tener " + sz + " elementos";

                this.claseColorBordeValido = "border-secondary";
                this.claseColorBordeInvalido = "border-danger";



                this.idBotonReiniciarClases = parent.idBotonReiniciarClases_MSL;

                this.mngDesactivarBotonReiniciarClases = new MangerElementoADesactivar(this.idBotonReiniciarClases, true);

                this.listaNombresDeCarpetas = null;

            }

            desactivarBotonReiniciarClases() {
                this.mngDesactivarBotonReiniciarClases.desactivar();
                //setDisabled(true,[this.idBotonReiniciarClases])
            }

            activarBotonReiniciarClases() {
                this.mngDesactivarBotonReiniciarClases.activar();
                //setDisabled(false,[this.idBotonReiniciarClases])
            }

            setEvaluarElSize(evaluar, size) {
                this.sizeQueTieneQueTener = size;
                this.condicionSiEvaluarElSize = () => evaluar;
            }

            aplicarConfiguracion() {
                const self = this;

                addOnClick(this.idBotonReiniciarClases, v => {
                    if (parent.estado.matris_Clasificacion_Carpeta_Descripcion != null) {
                        this.lista.actualizarUsandoLaBD(bd2 => {
                            bd2.clear();
                            for (const elementos of parent.estado.matris_Clasificacion_Carpeta_Descripcion) {
                                // console.log("agrega a " + nombreCarpeta);
                                bd2.addRow(elementos);
                            }


                        });
                    }
                });

                const mngAlertaListaErronea = new MangerElementoAOcultar(this.idAlertaClasificaciones, true);

                const elementoParaValidacionDeLista = parent.L.newElementoParaValidacion();
                const t = new TipoDeValidacion((t, z) => {
                    if (self.condicionSiEvaluarElSize()) {
                        // let b=z instanceof ListaSeleccionable_MenuAgregarEliminarArribaAbajo;
                        // console.log("ess lista="+b);
                        // console.log("lista="+z);
                        // console.log("typeof(lista)="+typeof(z));
                        // console.log("lista.bd="+z.bd);
                        // console.log("typeof(lista.bd)="+typeof(z.bd));
                        let a = z.bd.size();
                        //console.log("z.bd.size()="+a);
                        let b = self.sizeQueTieneQueTener;
                        //console.log("self.sizeQueTieneQueTener="+b);
                        let c = a == b;
                        //console.log("c="+c);
                        return c;
                        //return z.bd.size() == self.sizeQueTieneQueTener;
                    }
                    return true;
                }, () => {
                    // console.log("mensaje="+self.creadorDeMensaje(self.sizeQueTieneQueTener));
                    return self.creadorDeMensaje(self.sizeQueTieneQueTener);
                });
                //console.log("mensaje 2="+t.getMensaje());
                elementoParaValidacionDeLista.addTipoDeValidacion(t);
                elementoParaValidacionDeLista.addAlSerInvalido((e, lista) => {
                    // console.log("invalido %%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
                    setHTML(self.idAlertaClasificaciones, e.mensajeInvalido);
                    mngAlertaListaErronea.desocultar();
                    quitarClase(self.idConendorDebordeDeListaClasificaciones, self.claseColorBordeValido);
                    ponerClase(self.idConendorDebordeDeListaClasificaciones, self.claseColorBordeInvalido);
                });
                elementoParaValidacionDeLista.addAlSerValido((e, lista) => {
                    // console.log("al ser valido !!!!!!!!!!!!!!!!!!!!");
                    mngAlertaListaErronea.ocultar();
                    quitarClase(self.idConendorDebordeDeListaClasificaciones, self.claseColorBordeInvalido);
                    ponerClase(self.idConendorDebordeDeListaClasificaciones, self.claseColorBordeValido);

                });
                //elementoParaValidacionDeLista.alSerInvalido =
                // elementoParaValidacionDeLista.alSerValido =
                parent.L.setValidacion(self.validacionConEneventos, [elementoParaValidacionDeLista]);
                return this;
            }


            setValoresA() {
                const listaDeValoresNuevos = this.listaNombresDeCarpetas;
                parent.L.setMaximoDeFilas(listaDeValoresNuevos.length);
                const sizeNuevo = listaDeValoresNuevos.length;
                this.lista.actualizarUsandoLaBD(bd2 => {
                    // for (let index = 0; index < bd.size(); index++) {
                    //     const fr = bd.getFila(index);
                    //     let map = fr.map;
                    //     console.log("map.get(KEY_CLASIFICACION)=" + map.get(KEY_CLASIFICACION));
                    //     console.log("map.get(KEY_CARPETA)=" + map.get(KEY_CARPETA));
                    //     console.log("map.get(KEY_ID_INPUT_CLASIFICACION)=" + getValue(map.get(KEY_ID_INPUT_CLASIFICACION)));
                    //     console.log("map.get(KEY_ID_INPUT_CARPETA)=" + getValue(map.get(KEY_ID_INPUT_CARPETA)));
                    // }

                    let sizeActual = bd2.size();
                    let i = 0;
                    while (i < sizeActual) {
                        const m=parent.estado.matris_Clasificacion_Carpeta_Descripcion[i];
                        //console.log("i="+i);
                        const fr = bd2.getFila(i);
                        let map = fr.map;
                        //let idCarpeta = map.get(KEY_ID_INPUT_CARPETA);

                        let incremetarI = true;
                        //console.log("entro en i="+i);
                        if (i >= listaDeValoresNuevos.length) {
                            //console.log("p0 i="+i);
                            bd2.remove(i);
                            //console.log("p1 i="+i);
                            --sizeActual;
                            incremetarI = false;
                        } else {
                            let nombreCarpeta = map.get(parent.KEY_CARPETA).trim();

                            if (nombreCarpeta.length == 0) {
                                //console.log("p2 i="+i);
                                //setValue(idCarpeta,valorCarpetaEnEstaPosicion);
                                //bd.setRow(i, [map.get(parent.KEY_CLASIFICACION), listaDeValoresNuevos[i]]);
                                bd2.setRow(i, [m[0]
                                    ,m[1]
                                    ,m[2]
                                ]);
                                //console.log("p3 i="+i);
                            } else {
                                let loEncontro = false;
                                for (const valorCarpetaEnEstaPosicion of listaDeValoresNuevos) {

                                    if (nombreCarpeta === valorCarpetaEnEstaPosicion) {
                                        loEncontro = true;
                                        break;
                                    }

                                }

                                if (!loEncontro) {
                                    //console.log("p4 i="+i);
                                    bd2.remove(i);
                                    //console.log("p5 i="+i);
                                    --sizeActual;
                                    incremetarI = false;
                                }


                            }


                            //let valorCarpetaEnEstaPosicion = listaDeValoresNuevos[i];


                        }

                        if (incremetarI) {
                            i++;
                        }

                    }
                    //console.log("p6 i="+i);
                    if (sizeActual < listaDeValoresNuevos.length) {
                        i = sizeActual;
                        while (i < listaDeValoresNuevos.length) {
                            //console.log("j=" + i);



                            //let indiceParaAgregar=i;
                            //console.log("p7 j="+i);
                            for (const elementos of parent.estado.matris_Clasificacion_Carpeta_Descripcion) {
                                const nombreCarpeta=elementos[1];
                                let saltar = false;
                                //console.log("p8 j="+i);
                                for (let index = 0; index < bd2.size(); index++) {
                                    const fr = bd2.getFila(index);
                                    let map = fr.map;
                                    //let idCarpeta = map.get(KEY_ID_INPUT_CARPETA);
                                    //console.log("p9 j="+i);
                                    //console.log(map);
                                    let nombreCarpeta_ValorEnInput = map.get(parent.KEY_CARPETA).trim();//getValue(idCarpeta).trim();
                                    //console.log("p10 j="+i);
                                    if (nombreCarpeta_ValorEnInput === nombreCarpeta) {
                                        saltar = true;
                                        break;
                                    }

                                }
                                if (saltar) {
                                    continue;
                                }
                                //console.log("p11 j="+i);
                                //console.log("nombreCarpeta="+nombreCarpeta);
                                bd2.addRow([elementos[0], nombreCarpeta,elementos[2]]);
                                //console.log("p12 j="+i);
                                break;
                            }
                            i++;
                            //---------------------------
                        }
                    }

                    // console.log("por aqui !!!!!!!!");
                });
                parent.V.comprovarValidacionYDesactivar();
                this.activarBotonReiniciarClases();
            }
        }



        this.mngVSizL = new ManagerValidacionSizeLista().aplicarConfiguracion();


        //const ID_ALERTA_LISTA_CLASIFICACIONES="idAlerta_Listaclasificaciones";
        //const



        //parent.V.addBotonADesactivar("idBotonAgregar");
        parent.V.comprovarValidacionYDesactivar();
    }
    actualizar(matris_Clasificacion_Carpeta_Descripcion){
        this.estado.matris_Clasificacion_Carpeta_Descripcion=matris_Clasificacion_Carpeta_Descripcion;
        this.mngVSizL.listaNombresDeCarpetas = [];
        for (const elementos of matris_Clasificacion_Carpeta_Descripcion) {
            this.mngVSizL.listaNombresDeCarpetas.push(elementos[1]);
        }

        this.mngVSizL.setEvaluarElSize(true, this.estado.matris_Clasificacion_Carpeta_Descripcion.length)
        this.mngVSizL.setValoresA();
    }


}
