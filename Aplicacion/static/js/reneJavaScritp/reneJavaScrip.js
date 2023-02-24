

function remove(lista,indice){
	return lista.splice(indice,1);
}
function removeO(lista,objetoEnlista){
	if(lista.includes(objetoEnlista)){
		return remove(lista,lista.indexOf(objetoEnlista));
	}
	return null;
}


function getHijosEl(id) {
	let el=getEl(id);
	let hijos=[];
	let hijoActual=el.firstElementChild;
	while(hijoActual!=null){
		hijos.push(hijoActual);
		hijoActual=hijoActual.nextElementSibling;
	}
	return hijos;
}

function toInt(a) {
	return Number.parseInt(a);
}
function len(a) {
	return a.length;
}
function getDate_IncrementarDias(date,cantidadDeDias){
	return new Date(date.getTime()+60*60*24*1000*cantidadDeDias); 
}
function getCantidadDeSegundosTotales(date){
	if(date!=null&&date!=undefined&&esDate(date)){
		return date.getTime();
	}
	return -1;
}

function newDate(y, m, d,h,min,s) {
	//m 1-12 d 1-31
	if(h!=null&&h!=undefined){
		if(s!=null&&s!=undefined){
			return new Date(Date.UTC(y, m - 1, d - 1,h,min,s))
		}
		return new Date(Date.UTC(y, m - 1, d - 1,h,min))
	}
	return new Date(Date.UTC(y, m - 1, d - 1))
}


function toEl(strHtml) {
	return new DOMParser().parseFromString(strHtml, 'text/html').body;
}
function getHtmlEl(id) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	return el.outerHTML;
}
function getHTML(id, contenidoHtml) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	return el.innerHTML;
	// return document.getElementById(id).innerHTML;
}
function clearEl(id) {
	// for (const el of getEl(id).childNodes) {
	// 	el.remove();
	// }
	lis = getEl(id).childNodes;
	while (lis.length != 0) {
		lis[0].remove();
	}
}
function getLastEl(idPadre) {
	return getEl(idPadre).lastElementChild;
}

function getFirsEl(idPadre) {
	return getEl(idPadre).firstElementChild;
}

function addAntesDe(idExistenteSiguiente, elementoNuevoAnterior) {
	let elSiguiente = getEl(idExistenteSiguiente);
	elSiguiente.parentNode.insertBefore(elementoNuevoAnterior, elSiguiente);

	//getEl(idPadre).insertBefore(elementoNuevoAnterior,getEl(idExistenteSiguiente));
}

function removeEl(id) {
	getEl(id).remove();
}

function addEl(id, newNodeElement) {
	getEl(id).appendChild(newNodeElement);
}

function getCopyEl(id, copiarTodosLosElementosInternos = true) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	return el.cloneNode(copiarTodosLosElementosInternos);
}


function setEventosImagen(idImagen, metodoOnLoad, metodoOnError) {
	let el = getEl(idImagen);
	el.onload = function () {
		metodoOnLoad();
	};
	el.onerror = function () {
		metodoOnError();
	}
}

function setImgBase64(idImg, strBase64) {
	getEl(idImg).src = "data:image/png;base64," + strBase64;
}


function esFuncion(a) {
	return a instanceof Function;
}


function moverScrollAlfinal(id) {
	let e = getEl(id);
	e.scrollTop = e.scrollHeight;

}

function existe(id) {
	return getEl(id) != null;
}

const PATRON_SOLO_FLOAT_POSITIVO = new RegExp("^[0-9]+(?:(?:[.](?:[0-9]+))?)$");
function esFloatPStr(a) {
	return hayMatch(PATRON_SOLO_FLOAT_POSITIVO, a);
}
const PATRON_SOLO_INT_POSITIVO = new RegExp("^[0-9]+$");
function esIntPStr(a) {
	return hayMatch(PATRON_SOLO_INT_POSITIVO, a);
}
function inT(a) {
	// console.log("typeof(a)="+typeof(a));
	// console.log("a="+a);
	// console.log("Number.parseInt(a)="+Number.parseInt(a));
	return Number.parseInt(a);
}
function floaT(a) {
	return Number.parseFloat(a);
}

function hayMatch(patronRe, texto) { return patronRe instanceof RegExp ? patronRe.test(texto) : texto.match(patronRe) != null; }

function setStyleWidth(id, w) {
	getEl(id).style.width = w;
}

function getCopia(v) {
	if (v instanceof Map) {
		return new Map(v);
	}
	if (v instanceof Array) {
		l = [];
		for (const e of v) {
			l.push(e);
		}
		return l;
	}
}
function esLista(a) {
	return a instanceof Array;
}

function setText(id, text) {
	let v;
	if (esString(id)) {
		v = document.getElementById(id);
	} else {

		v = id;
	}

	while (contains(text, '<br><br>')) {
		text = text.replace('<br><br>', '<br>');
	}
	while (contains(text, '\n\n')) {
		text = text.replace('\n\n', '\n');
	}
	if (text.startsWith('\n')) {
		text = text.substring(1);
	}
	//console.log(text)
	v.innerText = text;
}

function displayNone(id, ocultar = true) {
	if (ocultar == undefined) { ocultar = true; }
	if (ocultar) {
		//getEl(id).style.display = "none";
		getEl(id).style.setProperty("display","none","important");
	} else {
		getEl(id).style.display = "";
	}
}
function setClase(id, clase) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	el.className = clase;
}
// function newDate(y, m, d) {
// 	//m 1-12 d 1-31
// 	return new Date(Date.UTC(y, m - 1, d - 1))
// }
function compareTo(a, b) {
	//console.log("c a="+a+" b="+b);
	//console.log("c ta="+typeof(a)+" b="+typeof(b));
	if (esNumero(a) && esNumero(b)) {
		//console.log("son numero");
		return (a == b) ? 0 : (a < b ? 1 : -1)
	}
	if (esString(a) && esString(b)) {
		return a.localeCompare(b);
	}

	if (esDate(a) && esDate(b)) {
		//console.log("son date");
		return compareTo(a.getTime(), b.getTime());
	}
	//console.log("son nada");
	return 0;
}

function esInt(a) {
	return Number.isInteger(a);
}
function esNumero(a) {
	return Number.isFinite(a) || typeof (a) === 'number';
}
function esString(a) {
	return typeof (a) == "string" || a instanceof String;
}
function esDate(a) {
	return a instanceof Date;
}

function getListaKeys(map) {
	if (v instanceof Map) {
		l = [];
		for (const key of v.keys()) {
			l.push(key);
		}
		return l;
	}
}

function simularClick(id) {
	getEl(id).click();
}

function togleCB(idCB) {
	setSelectecCB(idCB, !estaSeleccionado(idCB));
}
function setSelectedCB(idCB, seleccionar) {
	getEl(idCB).checked = seleccionar;
}


function setDisabled(desactivar, listaIdsADesactivar) {
	var atributoDisabled = "disabled";
	for (let i = 0; i < listaIdsADesactivar.length; i++) {
		const idActual = listaIdsADesactivar[i];
		if (desactivar) {
			//console.log("idActual="+idActual);
			setAtr(idActual, atributoDisabled, "true");

		} else {
			if (containsAtr(idActual, atributoDisabled)) {
				removeAtr(idActual, atributoDisabled);
			}
		}
	}
}

function addOnInput(id, metodoUtilizarE) {
	getEl(id).addEventListener("input", metodoUtilizarE)
}


function quitarClase(id, clase) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	el.className = el.className.replace(clase, "");
}
function ponerClase(id, clase) {
	//console.log("id="+id);
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	//console.log(e.className.contains);
	//if(!e.className.includes(clase)){
	if (!contieneClase(id, clase)) {
		el.className = el.className + " " + clase;
	}
}
function contieneClase(id, clase) {
	//console.log("id="+id);
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}

	//console.log(e.className.contains);
	return el.className.includes(clase);
}

function addOnClick(id, metodoUtilizarE) {
	getEl(id).addEventListener("click", metodoUtilizarE)
}


function setOnlyOnHover(id, metodoOnMouseEnter, metodoOnMouseExit) {
	addOnMouseEnter(id, metodoOnMouseEnter)
	addOnMouseLeave(id, metodoOnMouseExit)
}

function addOnMouseEnter(id, metodoUtilizarE) {
	getEl(id).addEventListener("mouseenter", metodoUtilizarE)
}
function addOnMouseLeave(id, metodoUtilizarE) {
	getEl(id).addEventListener("mouseleave", metodoUtilizarE)
}

function submit(id) {
	getEl(id).submit()
}

function estaSeleccionado(id) {
	return getEl(id).checked;
	//checked
}


function getValueCheckedRBs() {
	lista = arguments
	for (let i = 1; i < lista.length; i++) {
		const element = lista[i];
		if (a.checked) {
			return a.value;
		}
	}
	return null;
}
function or(a) {
	lista = arguments
	for (let i = 1; i < lista.length; i++) {
		const element = lista[i];
		if (a === element) {
			return true;
		}
	}
	return false;
}



function contains(a, b) {
	return a.length > 0 && a.includes(b);
}
// function contains(a, sub) {
// 	return a.indexOf(sub) != -1
// }
function setAtr(id, atributo, valor) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	el.setAttribute(atributo, valor)
}
function removeAtr(id, atributo) {
	if (containsAtr(id, atributo)) {
		//document.getElementById(id).removeAttribute(atributo)
		let el = null;
		if (esString(id)) {
			el = getEl(id);
		} else {
			el = id;
		}
		el.attributes.removeNamedItem(atributo)
	}
}
function containsAtr(id, atributo) {
	let el = null;
	if (esString(id)) {
		el = getEl(id);
	} else {
		el = id;
	}
	//return document.getElementById(id).attributes.contains(atributo)
	return el.attributes.getNamedItem(atributo)
}

function setHTML(id, contenidoHtml) {
	document.getElementById(id).innerHTML = contenidoHtml;
}


function getEl(id) {
	return document.getElementById(id)
}
function getValue(id) {
	return document.getElementById(id).value
}
function setValue(id, valor) {
	document.getElementById(id).value = valor
}

function addOnChange(id, metodoUtilizarE) {
	getEl(id).addEventListener("change", metodoUtilizarE)
	//getEl("e1").onchange=function(e){alert(getValue("e1"))}
	//getEl("e1").addEventListener("change",function(e){alert("a")})
}

function addOnKeyUp(id, metodoUtilizarE) {
	getEl(id).addEventListener("keyup", metodoUtilizarE)
	//getEl("e1").onchange=function(e){alert(getValue("e1"))}
	//getEl("e1").addEventListener("change",function(e){alert("a")})
}




function irA(file) {
	location.href = file
}






function volverCodigoInternoATexto_Clase(clase) {
	elments = document.getElementsByClassName(clase);
	for (var i = elments.length - 1; i >= 0; i--) {
		v = elments[i];
		setText(v, v.innerHTML);
	}
}
function volverCodigoInternoATexto(id) {
	setText(id, document.getElementById(id).innerHTML);
}



function put(llave, valor) {
	localStorage.setItem(llave, valor);
}

function get(llave) {
	return localStorage.getItem(llave);
}

var LLAVE_INDICE = "LLAVE_INDICE";


function irA(direccion) {
	location.href = direccion;
}

function getItem(lista, indice, llave) {
	var element = lista[indice];

	for (var j = 0; j < element.length; j++) {
		var parAtributo = element[j];
		if (llave === parAtributo[0]) {
			return parAtributo[1];
		}


	}

}




