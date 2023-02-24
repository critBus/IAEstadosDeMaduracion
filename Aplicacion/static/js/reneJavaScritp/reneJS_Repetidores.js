//import reneJavaScript

class ManagerRepetidor{
	constructor(id,lista){
		this.plantilla=getHTML(id);

		this.id=id;
		this.lista=lista;
	}
	repetir(){
		repetidor(this.id,this.lista,this.plantilla);
	}
}




function repetirHTML(id, cantidad, contenidoHtml) {
	if (contenidoHtml == null) { contenidoHtml = getHTML(id) }
	contenido = "";
	for (let i = 0; i < cantidad; i++) {
		contenido += contenidoHtml
	}
	setHTML(id, contenido)
}
function crearElementoDesdeLista(idOrNode, lista, indice) {
	linea=getHtmlEl(idOrNode);
	return crearElementoDesdeLista_htmlStr(linea,lista, indice);
	
}
function crearElementoDesdeLista_htmlStr(HtmlStr, lista, indice) {
	contenidoHtml = "";
	function recorrerRow(indice,iteradorDePares){
		lineaMomentanea = HtmlStr;
		for (const entrada of iteradorDePares) {
			// console.log("entrada[0]="+entrada[0]+" entrada[1]="+entrada[1]);
			let valor=entrada[1];
			if ( valor instanceof ValorBD ){
				// console.log("0 valor="+valor.valor)
				valor=valor.toString();
				// console.log("0 str="+valor);
			}else{
				valor=(valor+"")
			}
			lineaMomentanea = lineaMomentanea.replaceAll("{" + entrada[0] + "}", valor);
		}
		lineaMomentanea = lineaMomentanea.replaceAll("{indice}", (indice + 1) + "");
		lineaMomentanea = lineaMomentanea.replaceAll("{iteracion}", (indice) + "");
		contenidoHtml += "\n" + lineaMomentanea;
	}


	if(lista instanceof BD_RowElement){
		recorrerRow(indice,lista.getRow(indice));
	}else{
		recorrerRow(lista[indice]);
	}
	return toEl(contenidoHtml);

}

function ponerElementoDeLista(id, lista, indice, linea=null) {
	contenidoHtml = "";
	if (linea == null||linea == undefined || linea === "") {

		linea = document.getElementById(id).innerHTML;

	}

	function recorrerRow(indice,iteradorDePares){
		lineaMomentanea = linea;
		for (const entrada of iteradorDePares) {
			// console.log("entrada[0]="+entrada[0]+" entrada[1]="+entrada[1]);
			let valor=entrada[1];
			if ( valor instanceof ValorBD ){
				// console.log("0 valor="+valor.valor)
				valor=valor.toString();
				// console.log("0 str="+valor);
			}else{
				valor=(valor+"")
			}
			lineaMomentanea = lineaMomentanea.replaceAll("{" + entrada[0] + "}", valor);
		}
		lineaMomentanea = lineaMomentanea.replaceAll("{indice}", (indice + 1) + "");
		lineaMomentanea = lineaMomentanea.replaceAll("{iteracion}", (indice) + "");
		contenidoHtml += "\n" + lineaMomentanea;
	}


	if(lista instanceof BD_RowElement){
		recorrerRow(indice,lista.getRow(indice));
	}else{
		recorrerRow(lista[indice]);
	}
	//var element = lista[indice];
	// lineaMomentanea = linea;
	// for (var j = 0; j < element.length; j++) {
	// 	var parAtributo = element[j];
	// 	lineaMomentanea = lineaMomentanea.replace("{" + parAtributo[0] + "}", parAtributo[1])
	// }
	// lineaMomentanea = lineaMomentanea.replace("{indice}", (indice + 1) + "")

	document.getElementById(id).innerHTML = lineaMomentanea;

}



function repetidor(id, lista, linea) {
	contenidoHtml = "";

	if (linea == undefined || linea === "") {

		linea = document.getElementById(id).innerHTML;

	}
	//console.log(linea)
	// datosDeSalida={contenidoHtml:""};
	function recorrerRow(indice,iteradorDePares){
		lineaMomentanea = linea;
		for (const entrada of iteradorDePares) {
			// console.log("entrada[0]="+entrada[0]+" entrada[1]="+entrada[1]);
			let valor=entrada[1];
			if ( valor instanceof ValorBD ){
				// console.log("0 valor="+valor.valor)
				valor=valor.toString();
				// console.log("0 str="+valor);
			}else{
				valor=(valor+"")
			}
			lineaMomentanea = lineaMomentanea.replaceAll("{" + entrada[0] + "}", valor)
		}
		lineaMomentanea = lineaMomentanea.replaceAll("{indice}", (indice + 1) + "");
		lineaMomentanea = lineaMomentanea.replaceAll("{iteracion}", (indice) + "")
		contenidoHtml += "\n" + lineaMomentanea;
	}
	if(lista instanceof BD_RowElement){
		for (let i = 0; i < lista.listaDeMapBD.length; i++) {
			//console.log("i="+i);
			//console.log(lista.getRow(i));
			recorrerRow(i,lista.getRow(i));
		}
		//lista=lista.listaDeMapBD;
	}else{
		for (var i = 0; i < lista.length; i++) {
			recorrerRow(i,lista[i]);
		}
	}
	// for (const row of lista.listaDeMapBD) {
	// 	lineaMomentanea = linea;
	// 	for (const entrada of row) {
	// 		lineaMomentanea = lineaMomentanea.replaceAll("{" + entrada[0] + "}", entrada[1])
	// 	}
	// 	lineaMomentanea = lineaMomentanea.replaceAll("{indice}", (i + 1) + "")
	// 	contenidoHtml += "\n" + lineaMomentanea;
	// }
	// for (var i = 0; i < lista.length; i++) {
	// 	var element = lista[i];
	// 	lineaMomentanea = linea;
	// 	for (var j = 0; j < element.length; j++) {
	// 		var parAtributo = element[j];
	// 		//if(parAtributo[0]==="asd"){console.log("va a aplastarlo")}
	// 		lineaMomentanea = lineaMomentanea.replaceAll("{" + parAtributo[0] + "}", parAtributo[1])
	// 	}
	// 	lineaMomentanea = lineaMomentanea.replaceAll("{indice}", (i + 1) + "")
	// 	contenidoHtml += "\n" + lineaMomentanea;
	// }

	document.getElementById(id).innerHTML = contenidoHtml;


}



function ponerElementoDeLista(id, lista, indice, linea) {
	contenidoHtml = ""
	if (linea == undefined || linea === "") {

		linea = document.getElementById(id).innerHTML

	}
	var element = lista[indice];
	lineaMomentanea = linea;
	for (var j = 0; j < element.length; j++) {
		var parAtributo = element[j];
		lineaMomentanea = lineaMomentanea.replace("{" + parAtributo[0] + "}", parAtributo[1])
	}
	lineaMomentanea = lineaMomentanea.replace("{indice}", (indice + 1) + "")
	contenidoHtml += "\n" + lineaMomentanea;


	document.getElementById(id).innerHTML = contenidoHtml;


}


function ponerElemntosDeLista(id, lista, llave) {
	linea = document.getElementById(id).innerHTML;


	lineaMomentanea = "";
	for (var j = 0; j < lista.length; j++) {

		lineaMomentanea += linea.replace("{" + llave + "}", lista[j])
	}




	document.getElementById(id).innerHTML = lineaMomentanea;

}


function ponerElemntosDeListaGeneral(id, lista, indice, llave) {
	listaMomentanea = getItem(lista, indice, llave);
	ponerElemntosDeLista(id, listaMomentanea, llave);

}

function ponerElemntosDeListaTodos(id, lista, indice, llaves) {
	for (var j = 0; j < llaves.length; j += 2) {
		ponerElemntosDeListaGeneral(llaves[j], lista, indice, llaves[j + 1]);
	}
	ponerElementoDeLista(id, lista, indice);

}




class ArgumentosParaActualizadorDeListaYValidacion {
	constructor() {
		this.idIndependiente = null;
		this.idDependiente = null;
		this.listaDatosDependientes = null;
		this.idPadreIndependiente = null;
		this.idPadreDependiente = null;
		this.contenidoVacioIndependiente = null;
		this.contenidoVacioDependiente = null;
		this.idBotonADesactivar = null
	}

}

function setActualizadorDeListaYValidacion(argumentosParaActualizadorDeListaYValidacion) {
	idIndependiente = argumentosParaActualizadorDeListaYValidacion.idIndependiente
	idDependiente = argumentosParaActualizadorDeListaYValidacion.idDependiente
	listaDatosDependientes = argumentosParaActualizadorDeListaYValidacion.listaDatosDependientes

	idPadreIndependiente = argumentosParaActualizadorDeListaYValidacion.idPadreIndependiente;
	idPadreDependiente = argumentosParaActualizadorDeListaYValidacion.idPadreDependiente;
	contenidoVacioIndependiente = argumentosParaActualizadorDeListaYValidacion.contenidoVacioIndependiente;
	contenidoVacioDependiente = argumentosParaActualizadorDeListaYValidacion.contenidoVacioDependiente;
	idBotonADesactivar = argumentosParaActualizadorDeListaYValidacion.idBotonADesactivar
	//asumo que el value de idIndependiente es un #i 0-...
	//listaDatosDependientes [ [i,[opcionesParaDependiente]] , [i2,[opcionesParaDependiente]] , ... ]

	contenidoPadreIndependiente = null
	contenidoPadreDependiente = null
	estaDesactivado = false

	function guardarContenidoPadreIndependiente() {
		contenidoPadreIndependiente = getHTML(idPadreIndependiente)
	}
	function guardarContenidoPadreDependiente() {
		contenidoPadreDependiente = getHTML(idPadreDependiente)
	}
	function cargarContenidoPadreDependiente() {
		setHTML(idPadreDependiente, contenidoPadreDependiente)
	}

	function desactivar() {
		setAtr(idBotonADesactivar, "disabled", "")
		estaDesactivado = true
	}
	function activar() {
		removeAtr(idBotonADesactivar, "disabled")
		estaDesactivado = false
	}

	if (listaDatosDependientes.length == 0) {
		guardarContenidoPadreIndependiente()
		setHTML(idPadreIndependiente, contenidoVacioIndependiente)
		guardarContenidoPadreDependiente()
		setHTML(idPadreDependiente, contenidoVacioDependiente)
		desactivar()
	} else {
		function crearOpcion(indice, contenido) {
			return '<option value="' + indice + '">' + contenido + '</option>'
		}


		contenido = ""
		for (let index = 0; index < listaDatosDependientes.length; index++) {
			const element = listaDatosDependientes[index][0];
			contenido += crearOpcion(index, element)
		}
		setHTML(idIndependiente, contenido)

		function actualizar(e) {
			indice = getValue(idIndependiente)
			listaActual = listaDatosDependientes[indice][1]
			if (listaActual.length == 0) {
				guardarContenidoPadreDependiente()
				setHTML(idPadreDependiente, contenidoVacioDependiente)
				desactivar()
			} else {
				contenido = ""
				for (let index = 0; index < listaActual.length; index++) {
					const element = listaActual[index];
					contenido += crearOpcion(index, element)
				}
				if (estaDesactivado) {
					cargarContenidoPadreDependiente()
				}
				setHTML(idDependiente, contenido)
				activar()
			}


		}

		addOnChange(idIndependiente, actualizar)
		actualizar("")

	}






}



function setActualizadorDeLista(idIndependiente, idDependiente, listaDatosDependientes) {
	//asumo que el value de idIndependiente es un #i 0-...
	//listaDatosDependientes [ [i,[opcionesParaDependiente]] , [i2,[opcionesParaDependiente]] , ... ]

	function crearOpcion(indice, contenido) {
		return '<option value="' + indice + '">' + contenido + '</option>'
	}

	contenido = ""
	for (let index = 0; index < listaDatosDependientes.length; index++) {
		const element = listaDatosDependientes[index][0];
		contenido += crearOpcion(index, element)
	}
	setHTML(idIndependiente, contenido)

	function actualizar(e) {
		indice = getValue(idIndependiente)
		listaActual = listaDatosDependientes[indice][1]
		contenido = ""
		for (let index = 0; index < listaActual.length; index++) {
			const element = listaActual[index];
			contenido += crearOpcion(index, element)
		}
		setHTML(idDependiente, contenido)

	}

	addOnChange(idIndependiente, actualizar)
	actualizar("")



}




// function repetidor(id, lista, linea) {
// 	contenidoHtml = ""
// 	for (var i = 0; i < lista.length; i++) {
// 		var element = lista[i];
// 		lineaMomentanea = linea;
// 		for (var j = 0; j < element.length; j++) {
// 			var parAtributo = element[j];
// 			lineaMomentanea = lineaMomentanea.replace("{" + parAtributo[0] + "}", parAtributo[1])
// 		}
// 		lineaMomentanea = lineaMomentanea.replace("{indice}", (i + 1) + "")
// 		contenidoHtml += "\n" + lineaMomentanea;
// 	}

// 	document.getElementById(id).innerHTML = contenidoHtml;


// }
// setIdIndependiente(v){
	// 	this.idIndependiente=v;
	// }
	// setIdDependiente(v){
	// 	this.idDependiente=v;
	// }
	// setListaDatosDependientes(v){
	// 	this.ListaDatosDependientes=v;
	// }

	// setIdPadreIndependiente(v){
	// 	this.idPadreIndependiente=v;
	// }
	// setIdPadreDependiente(v){
	// 	this.idPadreDependiente=v;
	// }
	// setContenidoVacioIndependiente(v){
	// 	this.contenidoVacioIndependiente=v;
	// }
	// setContenidoVacioDependiente(v){
	// 	this.contenidoVacioDependiente=v;
	// }

	// setIdBotonADesactivar(v){
	// 	this.idBotonADesactivar=v;
	// }


	// function ponerElementoDeLista(id, lista, indice, linea) {

	// 	var element = lista[indice];
	// 	lineaMomentanea = linea;
	// 	for (var j = 0; j < element.length; j++) {
	// 		var parAtributo = element[j];
	// 		lineaMomentanea = lineaMomentanea.replace("{" + parAtributo[0] + "}", parAtributo[1])
	// 	}
	// 	lineaMomentanea = lineaMomentanea.replace("{indice}", (indice + 1) + "")
	
	// 	document.getElementById(id).innerHTML = lineaMomentanea;
	
	// }