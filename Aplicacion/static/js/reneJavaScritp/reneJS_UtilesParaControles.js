//import reneJavaScript
class ManagerCargaLentaImgBase64{
	constructor(){
		this.__idElementoQueSustituyeLaImagen=null;
		this.__idImagen=null;

		this.mngMangerElementoAOcultar_ElementoQueSustituyeLaImagen=null;
		this.mngMangerElementoAOcultar_Imagen=null;
	}
	setIdElementoQueSustituyeLaImagen(idElementoQueSustituyeLaImagen){
		this.__idElementoQueSustituyeLaImagen=idElementoQueSustituyeLaImagen;
		this.mngMangerElementoAOcultar_ElementoQueSustituyeLaImagen=new MangerElementoAOcultar(idElementoQueSustituyeLaImagen,false);
	}
	setIdImagen(idImagen){
		this.__idImagen=idImagen;
		this.mngMangerElementoAOcultar_Imagen=new MangerElementoAOcultar(idImagen,true);
	}
	verImagen(){
		this.mngMangerElementoAOcultar_ElementoQueSustituyeLaImagen.ocultar();
		this.mngMangerElementoAOcultar_Imagen.desocultar();
	}
	ocultarImagen(){
		this.mngMangerElementoAOcultar_ElementoQueSustituyeLaImagen.desocultar();
		this.mngMangerElementoAOcultar_Imagen.ocultar();
	}
	cargarImgBase64(srcBase64){
		this.ocultarImagen();
		// console.log("this.idImagen="+this.__idImagen);
		// console.log("existe(this.idImagen)="+existe(this.__idImagen));

		setEventosImagen(this.__idImagen
			,()=>{
				console.log("termino de cargar la imagen");
				this.verImagen();
			}
			,()=>{
				console.log("dio error");
				this.ocultarImagen();
			});
		setImgBase64(this.__idImagen,srcBase64);
	}
}
class ManagerContenidoSelecSimple{
	constructor(){
		this.idSelect;
		this.listaParLabelValue;
		this.idPadreSelect;
		this.contenidoHtmlSiEstaVacio;

		this.listaIdADesactivarSiEstaVacio=[];

		// this.accionAlDesactivar=id=>{
		// 	setDisabled(true,[id]);
		// };
		this.accionAlDesactivar=new ConjuntoDeEventos();
		this.accionAlDesactivar.add(id=>{
			setDisabled(true,[id]);
		});
		this.accionAlActivar=new ConjuntoDeEventos();
		this.accionAlActivar.add(id=>{
			setDisabled(false,[id]);
		});

		this.__metodoAlSeleccionar=new ConjuntoDeEventos();
		//this.despuesDeValidar

	}
	addAlSeleccionar(metodo){
		//(value en idSelect)=>{}
		this.__metodoAlSeleccionar.add(metodo);
	}
	addAlDesactivar(metodo){
		this.accionAlDesactivar.add(metodo);
	}
	addAlActivar(metodo){
		this.accionAlActivar.add(metodo);
	}
	setAlDesactivar(metodo){
		this.accionAlDesactivar.setMetodoUnico(metodo);
	}
	setAlActivar(metodo){
		this.accionAlActivar.setMetodoUnico(metodo);
	}
	actualizar(listaParLabelValue){
		if(listaParLabelValue!=null||listaParLabelValue!=undefined){
			this.listaParLabelValue=listaParLabelValue;
		}

		let desactivar=this.listaParLabelValue.length==0;
		if(desactivar){
			//console.log("this.idPadreSelect="+this.idPadreSelect);
			if(this.contenidoHtmlSiEstaVacio!=null||this.contenidoHtmlSiEstaVacio!=undefined){
				setHTML(this.idPadreSelect, this.contenidoHtmlSiEstaVacio);
			}

			//setDisabled(true,this.listaIdADesactivarSiEstaVacio);
			// for (const id of this.listaIdADesactivarSiEstaVacio) {
			// 	this.accionAlDesactivar(id);
			// }

		}else{
			function crearOpcion(valor, label) {
				return '<option value="' + valor + '">' + label + '</option>'
			}

			let contenido = "";
			for (let index = 0; index < this.listaParLabelValue.length; index++) {
				const valor = this.listaParLabelValue[index][1];
				const label = this.listaParLabelValue[index][0];
				contenido += crearOpcion(valor, label);
			}
			setHTML(this.idSelect, contenido);
			const self=this;
			addOnChange(this.idSelect,v=>{
				console.log("algo");
				self.__metodoAlSeleccionar.ejecutar(getValue(self.idSelect));
			});
			self.__metodoAlSeleccionar.ejecutar(getValue(self.idSelect));
		}

		for (const id of this.listaIdADesactivarSiEstaVacio) {
			if(desactivar){
				this.accionAlDesactivar.ejecutar(id);
			}else{
				this.accionAlActivar.ejecutar(id);
			}

		}

	}
	aplicarConfiguracionVisual(){
		//console.log("this.listaParLabelValue.length="+this.listaParLabelValue.length);
		this.actualizar();
	}
}


class ParIdRadioYListaIdsElementos{
	constructor(idRadio,listaIdsADesactivar){
		this.idRadio=idRadio;
		this.listaIdsADesactivar=listaIdsADesactivar;
	}
}
function desactivarNotRadios(lista_ParIdRadioYListaIdsElementos){
	for (let i = 0; i < lista_ParIdRadioYListaIdsElementos.length; i++) {
		const pr = lista_ParIdRadioYListaIdsElementos[i];
		addOnChange(pr.idRadio,()=>{
			//console.log("aqui!!");
			for (let j = 0; j < lista_ParIdRadioYListaIdsElementos.length; j++) {
				const pr2 = lista_ParIdRadioYListaIdsElementos[j];
				//console.log(pr2.idRadio+" sel="+estaSeleccionado(pr2.idRadio));
				setDisabled(!estaSeleccionado(pr2.idRadio),pr2.listaIdsADesactivar);
			}
			
		});
		
	}
}

function addOnClick_StopProp(id, metodoUtilizarE) {
	getEl(id).addEventListener("click",e=>{ 
		if(metodoUtilizarE!=undefined){metodoUtilizarE(e);}
		
		//console.log("se llama al padre");
		e.stopPropagation();
		//e.preventDefault();
		})
}
function addOnClickTogleSelectedCB_StopProp(idCB,listaIdsConOnClick){
	for (let i = 0; i < listaIdsConOnClick.length; i++) {
		const idActual = listaIdsConOnClick[i];
		//addOnClick_StopProp(idActual,()=>togleCB(idCB));
		addOnClick_StopProp(idActual,()=>simularClick(idCB));
	}
	addOnClick_StopProp(idCB);
	// getEl(idCB).onclick=e=>{
	// 	//console.log("se llama aqui");
	// 	e.stopPropagation();
	// 	//e.preventDefault();
	// };
}

function desactivarNotCheckBox(idCB,listaIdsADesactivar){
	// addOnInput(idCB,()=>{
	// 	console.log("evento input");
	// });
	addOnChange(idCB,()=>{
		//console.log("esta seleccionado=",estaSeleccionado(idCB));
		//console.log("se llamo esto");
		setDisabled(!estaSeleccionado(idCB),listaIdsADesactivar);
	});
}
function setValorDeSliderOnInput(idSlider,idObjetivo,metodoCreadorStr){
	if(metodoCreadorStr== undefined){
		//metodoCreadorStr=function(valorDeslider){return valorDeslider+"";};
		metodoCreadorStr=valorDeslider=>valorDeslider+"";
	}
	addOnInput(idSlider,()=>setHTML(idObjetivo,metodoCreadorStr(getValue(idSlider))));
	//addOnChange(idSlider,function(){setHTML(idObjetivo,metodoCreadorStr(getValue(idSlider)))});
}
function ponerClaseAlSeleccionar(listaDeIdsElementosInternos,claseATurnear,alHacerClick){
	for (let i = 0; i < listaDeIdsElementosInternos.length; i++) {
		var id=listaDeIdsElementosInternos[i];
		const paraInternos=[id,i]
		function seleccionarElementoDeNavegacionAlHacerClickEnEl(){
			var idInterno=paraInternos[0];
			var indiceInterno=paraInternos[1];
			
			for (let j = 0; j < listaDeIdsElementosInternos.length; j++) {
				var idActual=listaDeIdsElementosInternos[j];
				if(indiceInterno!=j&&contieneClase(idActual,claseATurnear)){
					quitarClase(idActual,claseATurnear);
					break;
				}
			}
			ponerClase(idInterno,claseATurnear);
		}
		addOnClick(id,seleccionarElementoDeNavegacionAlHacerClickEnEl);
		function alHacerClickInterno(){
			//var idInterno=paraInternos[0];
			var indiceInterno=paraInternos[1];
			alHacerClick(indiceInterno);
		}
		addOnClick(id,alHacerClickInterno);
	}
}