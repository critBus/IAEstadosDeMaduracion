
class DatosDelDataset{
    constructor(){
        this.id=null;
        this.nombre=null;
        this.descripcion=null;
        this.tipoDeFruto=null;
        this.nombreCientificoFruto=null;
        this.variedadFruto=null;
        this.usuario=null;
        this.creacion=null;
        this.cantidadDeImagenes=null;
        this.cantidadDeClasificaciones=null;
        this.listaPar_Clasificicacion_CantidadDeImagenes=[];
        this.lista_Clasificaciones=[];
        
        this.matriz_clasificacion_detalles=[];

    }
}

const mngDlgError2=new ManagerDlg_AceptarCancelar_Bootstrap("idDlgError2");
mngDlgError2.idContenido="idContenido_DlgError2";
mngDlgError2.idTitulo="idTitulo_idDlgError2";
mngDlgError2.setIdBotonAceptar("idBotonAceptar_DlgError2");

function showDlgError2(){
    mngDlgError2.showDlg("Advertencia "
    ,"Le informamos de la perdida de conexión con el servidor"
    ,"Aceptar",()=>{
        submit("idFormRecargarPaginaDatallesDataset");
        });
}

class MngDatosDeDataset{
    constructor(){
        this.bdDetalles=new BD_RowElement();
        this.bdDetalles.llaves=["NombreDato","Valor"];
        this.idContenendorDeParesdeDetalles="idContenendorDeParesdeDetalles";

        this.mngRepetidor=new ManagerRepetidor(this.idContenendorDeParesdeDetalles,this.bdDetalles);
    }
    actualizar(datosDelDataset){
        this.bdDetalles.clear();
        this.bdDetalles.addRow([
            "Nombre",datosDelDataset.nombre
        ]);
        this.bdDetalles.addRow([
            "Tipo De Fruto",datosDelDataset.tipoDeFruto
        ]);
        this.bdDetalles.addRow([
            "Usuario",datosDelDataset.usuario
        ]);
        this.bdDetalles.addRow([
            "Creación",datosDelDataset.creacion
        ]);
        this.bdDetalles.addRow([
            "Imagenes",datosDelDataset.cantidadDeImagenes
        ]);
        this.bdDetalles.addRow([
            "Clasificaciones",datosDelDataset.cantidadDeClasificaciones
        ]);
        this.mngRepetidor.repetir();
        //repetidor(this.idContenendorDeParesdeDetalles,this.bdDetalles);
    }
}


//()

class MngCarrusel{
    constructor(){
        this.KEY_ID_IMG_CARRUSEL="KEY_ID_IMG_CARRUSEL_";
        this.KEY_ID_SPINNER_CARRUSEL="KEY_ID_SPINNER_CARRUSEL_";
        this.bdImagenesClasificaciones=new BD_RowElement();
        this.bdImagenesClasificaciones.llaves=["Clasificacion","CantidadDeImagenes"];
        this.bdImagenesClasificaciones.listaDeNombresIds=[this.KEY_ID_IMG_CARRUSEL,this.KEY_ID_SPINNER_CARRUSEL];

        this.idListaItemsDataset="idListaItemsDataset";
        this.idContenidoDelCarrusel="idContenidoDelCarrusel";

        this.urlAjaxGetImagen=null;

        this.mngRepetidor_itemsDataset=new ManagerRepetidor(this.idListaItemsDataset,this.bdImagenesClasificaciones);
        this.mngRepetidor_Carrusel=new ManagerRepetidor(this.idContenidoDelCarrusel,this.bdImagenesClasificaciones);

    }
    actualizar(listaPar_Clasificacion_CantidadDeImagenes){
        this.bdImagenesClasificaciones.clear();
        for (const row of listaPar_Clasificacion_CantidadDeImagenes) {
            this.bdImagenesClasificaciones.addRow(row);
        }
        this.mngRepetidor_itemsDataset.repetir();
        this.mngRepetidor_Carrusel.repetir();
        // repetidor(this.idListaItemsDataset,this.bdImagenesClasificaciones);
        // repetidor(this.idContenidoDelCarrusel,this.bdImagenesClasificaciones);

        let classActive="active";
        ponerClase(getFirsEl(this.idListaItemsDataset),classActive);
        ponerClase(getFirsEl(this.idContenidoDelCarrusel),classActive);


        for (let index = 0; index < this.bdImagenesClasificaciones.size(); index++) {
            let fila = this.bdImagenesClasificaciones.getFila(index);
            let map = fila.map;
            let mgImg64=new ManagerCargaLentaImgBase64();
            mgImg64.setIdElementoQueSustituyeLaImagen(map.get(this.KEY_ID_SPINNER_CARRUSEL));
            mgImg64.setIdImagen(map.get(this.KEY_ID_IMG_CARRUSEL));
            mgImg64.ocultarImagen();

            const indiceDeEstaImagen=index;
            ejecutarAjax("/"+this.urlAjaxGetImagen+"/",{
                    "idDataset":mngDts.datosDelDataset.id
                 ,"indiceDeImagen":indiceDeEstaImagen
                 },r=>{
                if(r.existeDataset){
                    mgImg64.cargarImgBase64(r.imgBase64);
                    //mgb.cargarImgBase64(r.imgBase64);

                }else{
                    console.log("no existe dataset");
                    //noMostrarImg()
                }

            }
            ,r=>{
                console.log("error al pedir la imagen del dataset");
                 //noMostrarImg()
                });

            //ajax
            //mgImg64.cargarImgBase64(str64);
        }

    }
}




class MngImagenes{
    constructor(){
        this.bd=new BD_RowElement();
        this.bd.llaves=["NombreImagen","IndiceImagen"];
        this.idCuerpoTablaImagenes="idBodyTableImagenes";
        this.pagV=new PaginacionVisual_Bootstrap();
        this.pagV.idListaPaginacion="idListaPaginacion";
        this.pagV.idNodoSeleccionadoPlantilla="idPaginacionSeleccionado";
        this.pagV.idNodoNoSeleccionadoPlantilla="idPaginacionNoSeleccionado";

        this.idSelectImgProcesadas="idSelectImgProcesadas";
        this.idSelectClasificacion="idSelectClasificacion";

        this.idCargandoPaginacion="idCargandoPaginacion";
        this.idPaginacionImg="idPaginacionImg";
        this.idCargandoTablaImagenes="idCargandoTablaImagenes";

        this.idCargandoImagenDlg="idCargandoImagenDlg";
        this.idImgSeleccionada="idImgSeleccionada";

        this.mgImg64=new ManagerCargaLentaImgBase64();
        this.mgImg64.setIdElementoQueSustituyeLaImagen(this.idCargandoImagenDlg);
        this.mgImg64.setIdImagen(this.idImgSeleccionada);

        this.idDlgImagenSeleccionada="idDlgImagenSelecciondada";
        this.bdClasificaciones=new BD_RowElement();
        this.bdClasificaciones.llaves=["Clasificacion"];

        this.urlAjaxMetodoGetListaDeImagenes=null;
        this.datosDelDataset=null;

        this.urlAjaxMetodoGetImagen=null;

        this.mngRepetidor_Clasificaciones=new ManagerRepetidor(this.idSelectClasificacion,this.bdClasificaciones);
        this.mngRepetidor_TablaImagenes=new ManagerRepetidor(this.idCuerpoTablaImagenes,this.bd);
    }
    actualizarClasificaciones(listaClasificaciones){
        this.bdClasificaciones.clear();
        for (const cla of listaClasificaciones) {
            this.bdClasificaciones.addRow([cla]);
        }
        //repetidor(this.idSelectClasificacion,this.bdClasificaciones);
        this.mngRepetidor_Clasificaciones.repetir();
        setAtr(getFirsEl(this.idSelectClasificacion),"selected","true")
    }
    mostrarImagenSeleccionada(str64){
        this.mgImg64.cargarImgBase64(str64);
        // showDlgBostrap(this.idDlgImagenSeleccionada);
    }
    estaSeleccionadaImagenesProcesadas(){
        return getValue(this.idSelectImgProcesadas)=="Procesadas";
    }

    __actualizarListaDeImagenes(idDelDataset,indiceDeLasImagenes
                                ,seEncuentraSeleccionadaImagenesProcesadas
    ,clasificacion){
        mngImg.ponerCargando()
        ejecutarAjax("/"+this.urlAjaxMetodoGetListaDeImagenes+"/",{
                    "idDelDataset":idDelDataset
                 ,"indiceDeLasImagenes":indiceDeLasImagenes
            ,"seEncuentraSeleccionadaImagenesProcesadas":seEncuentraSeleccionadaImagenesProcesadas
            ,"clasificacion":clasificacion
                 },r=>{
            console.log("r.existeDataset="+r.existeDataset);
                if(r.existeDataset){
                    let li=[];
                    console.log("r.primerIndiceDeImagen="+r.primerIndiceDeImagen);
                    console.log("r.dicDeImagenes="+r.dicDeImagenes);
                    console.log("r.listaDeIndices="+r.listaDeIndices);
                    let primerIndiceDeImagen=Number.parseInt(r.primerIndiceDeImagen);
                    for (let i = 0; i < r.cantidadDeImg; i++) {
                        li.push([r.dicDeImagenes[primerIndiceDeImagen+i],primerIndiceDeImagen+i]);
                    }
                    let p=new Paginacion(r.listaDeIndices,r.iActual);
                    mngImg.actualizar(p,li);
                    mngImg.quitarCargando();
                    //mgb.cargarImgBase64(r.imgBase64);

                }else{
                    showDlgError2();
                }

            }
            ,r=>{
                 showDlgError2();
                });
    }

    aplicarConfiguracion(){
        const self=this;
        this.pagV.addOnClickNoSeleccionado((id,indice)=>{
            let seEncuentraSeleccionadaImagenesProcesadas=self.estaSeleccionadaImagenesProcesadas();
            let clasificacion=getValue(self.idSelectClasificacion);
            self.__actualizarListaDeImagenes(
                self.datosDelDataset.id
                ,indice
                ,seEncuentraSeleccionadaImagenesProcesadas
                ,clasificacion

            );
            // console.log("id="+id);
            // console.log("indice="+indice);
            // console.log("seEncuntraSeleccionadaImagenesProcesadas="+seEncuntraSeleccionadaImagenesProcesadas);
            // console.log("clasificacion="+clasificacion);
        });
        addOnChange(self.idSelectClasificacion,v=>{
            let seEncuentraSeleccionadaImagenesProcesadas=self.estaSeleccionadaImagenesProcesadas();
            let clasificacion=getValue(self.idSelectClasificacion);
            //let indiceSeleccionado=self.pagV.paginacion.getIndiceSeleccionado();

            self.__actualizarListaDeImagenes(
                self.datosDelDataset.id
                ,1//indiceSeleccionado
                ,seEncuentraSeleccionadaImagenesProcesadas
                ,clasificacion

            );
            //---------------------------
            // console.log("------------------------------------");
            // console.log("indice="+indiceSeleccionado);
            // console.log("seEncuntraSeleccionadaImagenesProcesadas="+seEncuntraSeleccionadaImagenesProcesadas);
            // console.log("clasificacion="+clasificacion);
        });
        this.pagV.aplicarConfiguracion();
    }
    actualizarListaDeImagenes(){
        const self=this;
        let seEncuentraSeleccionadaImagenesProcesadas=self.estaSeleccionadaImagenesProcesadas();
        let clasificacion=getValue(self.idSelectClasificacion);
        let indiceSeleccionado=self.pagV.paginacion.getIndiceSeleccionado();
        self.__actualizarListaDeImagenes(
                self.datosDelDataset.id
                ,indiceSeleccionado
                ,seEncuentraSeleccionadaImagenesProcesadas
                ,clasificacion

            );
    }
    ponerCargando(){
        displayNone( this.idCargandoPaginacion,false);
        displayNone( this.idCargandoTablaImagenes,false);
        displayNone( this.idPaginacionImg,true);
        displayNone( this.idCuerpoTablaImagenes,true);
    }
    quitarCargando(){
        displayNone( this.idCargandoPaginacion,true);
        displayNone( this.idCargandoTablaImagenes,true);
        displayNone( this.idPaginacionImg,false);
        displayNone( this.idCuerpoTablaImagenes,false);
    }
    actualizar(paginacion,listaPar_Nombre_Indice){
        this.pagV.actualizar(paginacion);
        this.bd.clear();
        for (const row of listaPar_Nombre_Indice) {
            this.bd.addRow(row);
            // let NombreImagen=row[0];
            // let IndiceImagen=row[1];

        }
        //repetidor(this.idCuerpoTablaImagenes,this.bd);
        this.mngRepetidor_TablaImagenes.repetir();
        this.quitarCargando();
    }

}

const mngDts=new MngDatosDeDataset();
const mngCarr=new MngCarrusel();

const mngImg=new MngImagenes();
mngImg.aplicarConfiguracion();

function alApretarEnVerImagen(indiceDeLaImagen){
    let seEncuntraSeleccionadaImagenesProcesadas=mngImg.estaSeleccionadaImagenesProcesadas();
    let clasificacion=getValue(mngImg.idSelectClasificacion);
    //let indiceSeleccionado=mngImg.pagV.paginacion.getIndiceSeleccionado();

    let indiceDeLaImagenAMostrar=indiceDeLaImagen;
    mngImg.mgImg64.ocultarImagen();
    // console.log("mngImg="+mngImg);
    // console.log("mngImg.datosDelDataset="+mngImg.datosDelDataset);
    // console.log("mngImg.datosDelDataset.id="+mngImg.datosDelDataset.id);
    //console.log("this.urlAjaxMetodoGetListaDeImagenes="+mngImg.urlAjaxMetodoGetListaDeImagenes);
    //ajax
    ejecutarAjax("/"+mngImg.urlAjaxMetodoGetImagen+"/",{
                    "idDelDataset":mngImg.datosDelDataset.id
                 ,"indiceDeImagen":indiceDeLaImagenAMostrar
            ,"seEncuentraSeleccionadaImagenesProcesadas":seEncuntraSeleccionadaImagenesProcesadas
            ,"clasificacion":clasificacion
                 },r=>{
                if(r.existeDataset){
                    mngImg.mostrarImagenSeleccionada(r.imgBase64);
                }else{
                    showDlgError2();
                }

            }
            ,r=>{
                showDlgError2();
                });

    //mng.mostrarImagenSeleccionada(str);

    showDlgBostrap(mngImg.idDlgImagenSeleccionada);
}


class ManagerDetallesClasificacionesDataset{
    constructor(){
        this.idHeaders_DetallesClasificaciones="idHeaders_DetallesClasificaciones";
        this.idContenido_DetallesClasificaciones="idContenido_DetallesClasificaciones";
        
    }
    aplicarConfiguracion(){
        let parent=this;

        this.KEY_CLASIFICACION="clasificacion";
        this.KEY_DETALLES="detalles";

        this.bd = new BD_RowElement();
        this.bd.llaves = [parent.KEY_CLASIFICACION, parent.KEY_DETALLES];
        

        this.mngRpHeaders=new ManagerRepetidor(this.idHeaders_DetallesClasificaciones,this.bd);
        this.mngRpContenidos=new ManagerRepetidor(this.idContenido_DetallesClasificaciones,this.bd);

    }
    actualizar(matriz_Clasificacion_Detalles){
        this.bd.clear();
        for (const row of matriz_Clasificacion_Detalles) {
            let clasificacion=row[0];
            let detalles=row[1];
            this.bd.addRow([clasificacion,detalles]);
        }
        this.mngRpHeaders.repetir();
        this.mngRpContenidos.repetir();

        if(matriz_Clasificacion_Detalles.length>0){
            ponerClase(getFirsEl(this.idHeaders_DetallesClasificaciones),"active");
        let content1=getFirsEl(this.idContenido_DetallesClasificaciones);
        ponerClase(content1,"show");
        ponerClase(content1,"active");
        }


    }
}


const mngDtaCla=new ManagerDetallesClasificacionesDataset();
mngDtaCla.idHeaders_DetallesClasificaciones="idHeaders_DetallesClasificaciones";
mngDtaCla.idContenido_DetallesClasificaciones="idContenido_DetallesClasificaciones";
mngDtaCla.aplicarConfiguracion();


function actualizarDatosDeImg(datosDeDatasetActual
                              ,urlAjaxGetImagenes
                              ,urlAjaxImagen900_600
                              ,urlAjaxMetodoGetImagen
){
    setHTML("idContenidoDescripcion",datosDeDatasetActual.descripcion);

mngImg.urlAjaxMetodoGetListaDeImagenes= urlAjaxGetImagenes;
mngImg.datosDelDataset=datosDeDatasetActual;
mngDts.datosDelDataset=datosDeDatasetActual;
mngCarr.urlAjaxGetImagen=urlAjaxImagen900_600;
mngImg.urlAjaxMetodoGetImagen=urlAjaxMetodoGetImagen;
mngDts.actualizar(datosDeDatasetActual);
mngCarr.actualizar(datosDeDatasetActual.listaPar_Clasificicacion_CantidadDeImagenes);
mngImg.actualizarClasificaciones(datosDeDatasetActual.lista_Clasificaciones);


mngDtaCla.actualizar(datosDeDatasetActual.matriz_clasificacion_detalles);

// mngImg.actualizarListaDeImagenes();



}




