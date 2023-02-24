//import reneJavaScript
//import reneJS_Clases

class Ordenador_BD {
	constructor(bd) {
		//this.idText;
		this.bd_rowElement = bd;
		//this.ordenAsendente=true;
		this.keyPorElQueOrdenar;
	}
	ordenar(asendente) {
		const thisA = this;
		this.bd_rowElement.listaDeMapBD.sort((a, b) => {
			let datoA = a.get(thisA.keyPorElQueOrdenar);
			if (datoA instanceof ValorBD) {
				datoA = datoA.valor;
			}
			let datoB = b.get(thisA.keyPorElQueOrdenar);
			if (datoB instanceof ValorBD) {
				datoB = datoB.valor;
			}
			let resultado = compareTo(datoA, datoB);
			//console.log("k="+thisA.keyPorElQueOrdenar+" a="+datoA+" b="+datoB+" r="+resultado);
			if (!asendente) {
				resultado *= -1;
				//console.log("se invertio r="+resultado);
			}

			return resultado;
		})

	}
}

class OrdenadorRB_BD extends Ordenador_BD {
	constructor(bd) {
		super(bd);
		this.llaves = this.bd_rowElement.llaves;
		this.mapKeysYIdsRb = new Map();
		this.ordenarAsendente = true;
		this.idBToggleOrdenamiento;
		this.accionDespuesDeOrdenar = () => { };
		//this.__metodoDeBToggleOrdenamiento
		//const ordenarAnterior=this.ordenar;
		//this.ordenar=()=>{}

	}
	setIdsCb(listaIdsRb) {
		for (let i = 0; i < this.llaves.length; i++) {
			const key = this.llaves[i];
			this.mapKeysYIdsRb.set(key, listaIdsRb[i])
		}
		// if(esLista(listaIdsRb)&&listaIdsRb.length>0){
		// 	if(esLista(listaIdsRb[0])){
		// 		for (const entrada of listaIdsCb) {

		// 		}
		// 	}else{

		// 	}



		// }


	}
	decidirKeyAOrdenar() {
		for (const entrada of this.mapKeysYIdsRb) {
			let idRB = entrada[1];
			let key = entrada[0];
			//console.log("estaSeleccionado(idRB)="+estaSeleccionado(idRB)+" idRB="+idRB+" key="+key);
			if (estaSeleccionado(idRB)) {
				this.keyPorElQueOrdenar = key;
				break;
			}
		}
		//console.log("decidir k="+this.keyPorElQueOrdenar);
	}
	toggleOrden() {
		this.ordenarAsendente = !this.ordenarAsendente;
	}
	aplicarOrden() {
		//console.log("llamo a plicar orden");
		this.decidirKeyAOrdenar();
		this.ordenar(this.ordenarAsendente);
		this.accionDespuesDeOrdenar();
	}



	aplicarConfiguracionToggle() {
		const thisORd = this;

		addOnClick(this.idBToggleOrdenamiento, (e) => {
			//console.log("se llama a togle");
			//console.log("5todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
			thisORd.toggleOrden();
			//console.log("5todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
			thisORd.aplicarOrden();
			//console.log("5todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
		});
		for (const entrada of this.mapKeysYIdsRb) {
			let idRB = entrada[1];
			let key = entrada[0];
			//console.log("idRB="+idRB+" key="+key);
			addOnClick(idRB, (e) => {
				//console.log("6todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
				thisORd.aplicarOrden();
				//console.log("6todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
			})
		}
		//console.log("this.mapKeysYIdsRb.values()="+this.mapKeysYIdsRb.values());
		//simularClick();
		//simularClick(this.mapKeysYIdsRb.values().next().value);
	}


}

class OrdenadorRB_Visual_BD extends OrdenadorRB_BD {
	constructor(bd) {
		super(bd);
		this.mapIdsRByIcono;
		this.idIconoOrdenSeleccionado;
		this.idIconoDireccionDeOrden;
		this.iconoOrdenAscendente;
		this.iconoOrdenDescendente;

	}
	setMapIdsRByIcono(mapIdsRByIcono) {
		this.mapIdsRByIcono = mapIdsRByIcono;
		let lista = [];
		for (const id of this.mapIdsRByIcono.keys()) {
			lista.push(id);
		}
		this.setIdsCb(lista);
	}
	aplicarConfiguracionVisual(indiceSeleccionadoDefault) {
		// console.log("3todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
		for (const entrada of this.mapIdsRByIcono) {
			const id = entrada[0];
			const icono = entrada[1];
			const thisIdIconoOrdenSeleccionado = this.idIconoOrdenSeleccionado;
			addOnClick(id, e => {
				setClase(thisIdIconoOrdenSeleccionado, icono);
			});
		}
		const idIconoDireccionDeOrden = this.idIconoDireccionDeOrden;
		const iconoOrdenAscendente = this.iconoOrdenAscendente;
		const iconoOrdenDescendente = this.iconoOrdenDescendente;
		const thisA = this;
		// console.log("3todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
		let ponerIconoCorrecto = e => {
			//console.log("thisA.ordenarAsendente="+thisA.ordenarAsendente);
			setClase(idIconoDireccionDeOrden, (thisA.ordenarAsendente ? iconoOrdenAscendente : iconoOrdenDescendente));
		};//contieneClase(idIconoDireccionDeOrden,iconoOrdenAscendente)
		addOnClick(this.idBToggleOrdenamiento, ponerIconoCorrecto);
		ponerIconoCorrecto();
		//console.log("va a simular el click");
		// console.log("3todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
		// for (const row of this.mapKeysYIdsRb.values()) {

		// }
		if (indiceSeleccionadoDefault != null && indiceSeleccionadoDefault != undefined) {
			let idParaClickDefault = Array.from(this.mapKeysYIdsRb.values())[indiceSeleccionadoDefault];
			//console.log("row="+row);
			//let idParaClickDefault=row[0];
			// console.log("idParaClickDefault="+idParaClickDefault);
			// console.log("existe idParaClickDefault="+existe(idParaClickDefault));
			simularClick(idParaClickDefault);
		}
		// console.log("4todo seleccionado="+estaSeleccionado("idCBFiltroTodos"));
		// let v=this.mapKeysYIdsRb.values();
		// v.
		// console.log(v);
		// console.log(typeof(v));

		// v.forEach(v2 => {
		// 	console.log(v2);
		// });

		// let z=v.next();
		// console.log(z);
		// z=v.next();
		// console.log(z);
		// z=v.next();
		// console.log(z);

		// simularClick(z.value);
	}
}

class FiltroText_v2 {
	constructor(bd) {
		this.idText;
		//this.listaDeRowDeDatos=[];
		this.bd_rowElement = bd;//new BD_RowElement();
		//this.metodoGetListaDeKeysAComparar;
		this.predicateCompararEstaLLave;//keystr=>bool
		this.listaIdsGenericosAOcultar=[];

		this.indicesVisibles=[];
		const self=this;

		//this.__keyID_elementoAOcultar;// o seleccionar 
		this.predicateDeComparacion = (vtextoDeEntrada, vstr) => {
			vtextoDeEntrada = vtextoDeEntrada.trim().toLowerCase() + "";
			vstr = vstr.trim().toLowerCase() + "";
			// let b="asd".contains("w");
			// let c="qwe".indexOf
			//let ocultar=(vtextoDeEntrada+"").contains((vstr+""));
			let ocultar = contains((vstr + ""), (vtextoDeEntrada + ""));
			//console.log("vtextoDeEntrada="+vtextoDeEntrada+" vstr="+vstr+" ocultar="+ocultar);
			//console.log();

			return ocultar;
		};
		this.__metodoAplicarFiltro = textoActual => {
			self.indicesVisibles=[];
			//console.log("pasa por el filtro");
			//let textoActual=e.target.value;
			let bd = self.bd_rowElement;
			for (let i = 0; i < bd.size(); i++) {
				const row = bd.listaDeMapBD[i];
				let ocultarElemento = true;
				if(textoActual.trim().length == 0){
					ocultarElemento = false;
				}else{
					for (const entryMap of row) {
						let key = entryMap[0]
						let valor = entryMap[1]
						if (valor instanceof ValorBD) {
							//console.log("valor="+valor.valor)
							valor = valor.toString();
							//console.log("str="+valor);
						} else {
							valor = (valor + "")
						}
						if (self.predicateCompararEstaLLave(key)) {
							if (self.predicateDeComparacion(textoActual, valor) ) {//|| textoActual.trim().length == 0
								ocultarElemento = false;
								break;
							}
						}
					}
				}

				

				//let mapIdsCh = bd.getMapIds(i);
				// for (const entrada of mapIdsCh) {
				// 	console.log("entrada[1]="+entrada[1]);
				// 	displayNone(entrada[1], ocultarElemento);
				// }

				let mapIdsCh = self.listaIdsGenericosAOcultar;
				let map=bd.getFila(i).map;
				for (const entrada of mapIdsCh) {
					// console.log("entrada[1]="+entrada[1]);
					displayNone(map.get(entrada), ocultarElemento);
				}
				if(!ocultarElemento){
					self.indicesVisibles.push(i);
				}


			}


		};
	this._alTerminarDeFiltrar=new ConjuntoDeEventos();

	}
	addAlTerminarDeFiltrar(metodo){
		this._alTerminarDeFiltrar.add(metodo);
	}
	setIdBaseElemtosAOcultar(idBase) {//la ideea es que en la realidad los ide de los elemntos sean = idBase+i
		//this.__keyID_elementoAOcultar = idBase;
		this.listaIdsGenericosAOcultar.push(idBase);
		let lista=this.bd_rowElement.listaDeNombresIds;
		if(!contains(lista,idBase)){
			lista.push(idBase);
		}
		
	}
	filtrar() {
		this.__metodoAplicarFiltro(getValue(this.idText));
		this._alTerminarDeFiltrar.ejecutar();
	}
	setFiltroText() {//No llamar hasta tener todo listo
		//const idTexo=this.idText;
		addOnKeyUp(this.idText, e => this.filtrar());
		//addOnKeyUp(this.idText,e=>this.__metodoAplicarFiltro(e.target.value));
	}
}
class FiltroText_CByTodos_v2 extends FiltroText_v2 {
	constructor(bd) {
		super(bd);
		this.llaves = this.bd_rowElement.llaves;
		this.mapKeysYIdsCb = new Map();
		this.IdCB_Todo;
		const self=this;
		this.predicateCompararEstaLLave = keystr => {

			// console.log("this.IdCB_Todo="+this.IdCB_Todo);
			// console.log("existe="+existe(this.IdCB_Todo));
			// console.log(getEl(this.IdCB_Todo));
			if (self.mapKeysYIdsCb.has(keystr)) {
				console.log("-------------------------------------------------");
				console.log("keystr=" + keystr);
			// 	console.log("this.mapKeysYIdsCb.get(keystr)=" + this.mapKeysYIdsCb.get(keystr));
			// 	console.log("existe=" + existe(this.mapKeysYIdsCb.get(keystr)));
			// 	console.log(getEl(this.mapKeysYIdsCb.get(keystr)));
			}


			return self.mapKeysYIdsCb.has(keystr)
			 && (
				 estaSeleccionado(self.IdCB_Todo) || estaSeleccionado(self.mapKeysYIdsCb.get(keystr))
				 );
		};
	}
	// setKeysYIdsCb(listaParKeysYIdsCb){
	// 	//[ [key,idChb],[...] ]
	// 	this.mapKeysYIdsCb=new Map(listaParKeysYIdsCb);
	// 	// this.bd_rowElement.llaves=getListaKeys(this.mapKeysYIdsCb);
	// }
	setIdsCb(listaIdsCb) {
		for (let i = 0; i < this.llaves.length; i++) {
			const key = this.llaves[i];
			this.mapKeysYIdsCb.set(key, listaIdsCb[i])
		}

	}
	// addRow(listaDeDatos){//,idElementoADecidirSiOcultar
	// 	//una fila de la lista de datos

	// 	// mapRowDeDatos=new Map();
	// 	// for (let i = 0; i < listaDeDatos.length; i++) {
	// 	// 	const valor = listaDeDatos[i];
	// 	// 	let key=this.mapKeysYIdsCb.keys()[i];
	// 	// 	mapRowDeDatos.set(key,valor);

	// 	// }
	// 	// rw=new RowDeDatos_FiltroText_v2();
	// 	// rw.mapRow=mapRowDeDatos;
	// 	// rw.idElemento=idElementoADecidirSiOcultar;
	// 	// this.listaDeRowDeDatos.push(rw);
	// 	this.bd_rowElement.addRow(listaDeDatos);
	// }
	aplicarConfiguracionToggle() {
		//const idT=this.idText;
		//const thisAplicarFiltro=this.__metodoAplicarFiltro;
		const aplicarFiltro = () => this.__metodoAplicarFiltro(getValue(this.idText));
		// 	texto=getValue(idT);
		// };
		const mapIds = this.mapKeysYIdsCb;
		const idTodo = this.IdCB_Todo;

		// console.log("existe="+existe(idTodo));
		// console.log("idTodo="+idTodo);
		simularClick(idTodo);
		// console.log("todo seleccionado="+estaSeleccionado(idTodo));
		

		addOnClick(idTodo, () => {
			for (const idActual of mapIds.values()) {
				setSelectedCB(idActual, false);
			}
			setSelectedCB(idTodo, true);

			aplicarFiltro();

		});
		for (const idActual of mapIds.values()) {
			addOnClick(idActual, () => {
				setSelectedCB(idTodo, false);
				let ponerSelected=true;
				for (const idActual2 of mapIds.values()) {
					if (estaSeleccionado(idActual2)) {
						//return;
						ponerSelected=false;
						break;
					}
				}
				if(ponerSelected){
					setSelectedCB(idActual, true);
				}

				//setSelectedCB(idActual, ponerSelected);
				//console.log("se aplico el filtro?");
				aplicarFiltro();

			});

		}
		/*for (const idActual of mapIds.values()) {
			addOnClick(idActual, () => {
				setSelectedCB(idTodo, false);
				for (const idActual2 of mapIds.values()) {
					if (estaSeleccionado(idActual2)) {
						return;
					}
				}
				setSelectedCB(idActual, true);

				aplicarFiltro();

			});

		} */
		// console.log("todo seleccionado="+estaSeleccionado(idTodo));
	}
}



function setFiltroText(idText, lista, keyID_elemento_a_comprobar_en_lista, predicate_evaluar_propiedad) {
	//keyID_elemento_a_comprobar_en_lista es el elemtento por el que se va a obtener
	//el elemento que se va a ocultar o no
	//el valor que contenga cada keyID_elemento_a_comprobar_en_lista solo deve variar en el final con i->1..
	// ejemplo idAlgo1 idAlgo2 idAlgo3 ...
	//predicate_evaluar_propiedad (e)->{boolean} donde e va a ser el key actual y va aretornar si 
	//comparar el contenido de esta llave en la lista con el texto actual
	//la idea es seleccionar que elementos de la lista son los comparables y si estos elementos
	//son seleccionables en otro punto,saver cuales son los que hay que evaluar en el momento


	addOnKeyUp(idText, function (e) {
		textoActual = e.target.value
		//console.log(textoActual)
		for (let i = 0; i < lista.length; i++) {
			const element = lista[i];
			ocultarElemento = true;
			idElemento = null;
			//console.log("------------------------------")
			for (let j = 0; j < element.length; j++) {
				const parKeyValue = element[j];
				key = parKeyValue[0];
				value = parKeyValue[1];
				if (key !== keyID_elemento_a_comprobar_en_lista) {
					if ((ocultarElemento) && predicate_evaluar_propiedad(key)) {

						if (contains(value.toLowerCase(), textoActual.toLowerCase())) {
							//console.log("value="+value)
							//console.log("textoActual="+textoActual)
							ocultarElemento = false;
						}
					}
				} else {
					idElemento = value + (i + 1);
				}

			}
			//console.log("i="+idElemento)
			if (idElemento != null) {
				//console.log("ocultarElemento="+ocultarElemento)
				displayNone(idElemento, ocultarElemento)
			}



		}
	})
}
