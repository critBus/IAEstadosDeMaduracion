//import reneJavaScript



class MangerElementoADesactivar{
	constructor(id,desactivado=false){
		this.id=id;
		setDisabled(desactivado,[this.id]);
		this.desactivado=desactivado;
	}
	desactivar(){
		if(!this.desactivado){
			setDisabled(true,[this.id]);
			this.desactivado=true;
		}
		return this;
	}
	activar(){
		if(this.desactivado){
			setDisabled(false,[this.id]);
			this.desactivado=false;
		}
		return this;
	}
}

class MangerElementoAOcultar{
	constructor(id,oculto=false){
		this.id=id;
		displayNone(this.id,oculto);
		this.oculto=oculto;
	}
	ocultar(){
		if(!this.oculto){
			displayNone(this.id,true);
			this.oculto=true;
		}
		return this;
	}
	desocultar(){
		if(this.oculto){
			displayNone(this.id,false);
			this.oculto=false;
		}
		return this;
	}
}

class MangerFuncionAutomatica{
	constructor(tiempoMilisegundos,metodo){
		this.tiempoMilisegundos=tiempoMilisegundos;
		this.metodo=metodo;
		this.id;
		this.enFuncionamiento=false;
	}
	comenzar(){
		if(!this.enFuncionamiento){
			this.id=setInterval(this.metodo,this.tiempoMilisegundos);
			this.enFuncionamiento=true;
		}
		return this;
	}
	detener(){
		if(this.enFuncionamiento){
			clearInterval(this.id);
			this.enFuncionamiento=false;
		}
		return this;
	}

}

class ConjuntoDeEventos{
	constructor(){
		this.listaDeMetodos=[];
	}
	
	clear(){
		
		//this.listaDeMetodos.clear();
		this.listaDeMetodos=[];
		return this;
	}
	add(metodo){
		this.listaDeMetodos.push(metodo);
		return this;
	}
	setMetodoUnico(metodo){
		this.clear();
		this.add(metodo);
		return this;
	}
	remove(metodo){
		this.listaDeMetodos.splice(this.listaDeMetodos.indexOf(metodo),1);
		return this;
	}
	ejecutar(...args){
		this.listaDeMetodos.forEach(element => {
			element(...args);
		});
	}
	addOnClick_SinArgs(...ids){
		const self=this;
		for (let index = 0; index < ids.length; index++) {
			const id = ids[index];
			addOnClick(id,v=>{self.ejecutar();});
		}
		return this;
	}
	addOnClick(id,...args){
		const self=this;
		addOnClick(id,v=>{self.ejecutar(...args);});
		return this;
	}
}

class ConjuntoDeEventos_ParaElemento extends ConjuntoDeEventos{
	constructor(id){
		super();
		this.id=id;
		
	}
	addOnClick(...args){
		return super.addOnClick(this.id,...args);
	}
}

class ManagerDlg{
	constructor(id,metodoShow,metodoHide){
		this.id=id;
		this.esVisible=false;//ConjuntoDeEventos
		//this.metodoShow=metodoShow;//(ManagerDlg)=>{}
		this.__metodoShow=new ConjuntoDeEventos().add(metodoShow);//(ManagerDlg)=>{}
		//this.metodoHide=metodoHide;//(ManagerDlg)=>{}
		this.__metodoHide=new ConjuntoDeEventos().add(metodoHide);//(ManagerDlg)=>{}

		//this.idBotonAceptar;
	}
	addOnShow(metodo){
		this.__metodoShow.add(metodo);
		return this;
	}
	addOnHide(metodo){
		this.__metodoHide.add(metodo);
		return this;
	}
	show(){
		//if(!this.esVisible){

			this.__metodoShow.ejecutar(this);//(this);
			this.esVisible=true;
		//}
		return this;
	}
	hide(){
		//console.log("this.esVisible="+this.esVisible);
		//if(this.esVisible){

			this.__metodoHide.ejecutar(this);//(this);
			this.esVisible=false;
		//}
		return this;
	}


}

class ManagerDlg_ContenidoText extends ManagerDlg{
	constructor(id,metodoShow,metodoHide){//idContenido
		super(id,metodoShow,metodoHide);
		this.idContenido;//=idContenido;
		this.idTitulo;
		this.idMensajeCargando;
	}
	setContenido(contenido){
		setHTML(this.idContenido,contenido);
		return this;
	}
	getContenido(){
		return getValue(this.idContenido);
	}
	setTitulo(titulo){
		setHTML(this.idTitulo,titulo);
		return this;
	}
	setMensajeCargando(mensaje){
		setHTML(this.idMensajeCargando,mensaje);
		return this;
	}
	showDlg(titulo,contenido){//mensajeCargando
		this.setTitulo(titulo);
		this.setContenido(contenido);
		//this.setMensajeCargando(mensajeCargando);
		this.show();
		return this;
	}
}



class ManagerDlg_Aceptar extends ManagerDlg_ContenidoText{
	constructor(id,metodoShow,metodoHide){
		super(id,metodoShow,metodoHide);
		this.__conjuntoEventosAceptar;
		
		//this.idBotonAceptar;
		//this.eventosAceptar=new ConjuntoDeEventos();
	}
	setIdBotonAceptar(id){
		this.__conjuntoEventosAceptar=new ConjuntoDeEventos_ParaElemento(id);
		this.__conjuntoEventosAceptar.addOnClick();
	}
	setAccionAlAceptar(metodo){
		const self=this;
		this.__conjuntoEventosAceptar.setMetodoUnico(v=>{
			//self.hide();
			metodo();
			
		});
	}
	
	setTextoBotonAceptar(texto){
		setHTML(this.__conjuntoEventosAceptar.id,texto);
		return this;
	}
	showDlg(titulo,contenido,textoEnAceptar,metodoAlAceptar){
		this.setTitulo(titulo);
		this.setContenido(contenido);
		this.setTextoBotonAceptar(textoEnAceptar);
		this.setAccionAlAceptar(metodoAlAceptar);
		this.show();
		return this;
	}
}

class ManagerDlg_AceptarCancelar extends ManagerDlg_Aceptar{
	constructor(id,metodoShow,metodoHide){
		super(id,metodoShow,metodoHide);
	    this.__conjuntoEventosCancelar;

		//this.idBotonAceptar;
		//this.eventosAceptar=new ConjuntoDeEventos();
	}
	setIdBotonCancelar(id){
		this.__conjuntoEventosCancelar=new ConjuntoDeEventos_ParaElemento(id);
		this.__conjuntoEventosCancelar.addOnClick();
	}
	setAccionAlCancelar(metodo){
		const self=this;
		this.__conjuntoEventosCancelar.setMetodoUnico(v=>{
			//self.hide();
			metodo();

		});
	}

	showDlg(titulo,contenido,textoEnAceptar,metodoAlAceptar,metodoAlCancelar){
		this.setTitulo(titulo);
		this.setContenido(contenido);
		this.setTextoBotonAceptar(textoEnAceptar);
		this.setAccionAlAceptar(metodoAlAceptar);
		if(metodoAlCancelar!==null&&metodoAlCancelar!==undefined){
            this.setAccionAlCancelar(metodoAlCancelar);
        }
		this.show();
		return this;
	}
}

class ValorBD extends Object{
    constructor(valor){
        super(valor);
        this.valor=valor;
        this.getStr=v=>valor;
    }
    toString(){
        return this.getStr(this.valor);
    }
    toLocaleString(){
        return this.getStr(this.valor);
    }
    
}
class FilaRow{
	constructor(indice,map,bd){
		this.indice=indice;
		this.map=map;
		this.bd=bd;
	}
}

class BD_RowElement{
	constructor(){
		this.listaDeMapBD=[];
		this.llaves=[];
		this.listaDeNombresIds=[];//son el principio de un id, el real sera el id+indice del row que le toque

		this.metodoGetListaEmpty;
		this.__alVariarSize;// ConjuntoDeEventos

		this.__verBD=new ConjuntoDeEventos();//this=>{}
		
	}
	addAlVerBD(verBD){
		this.__verBD.add(verBD);
	}
	mirarBD(extra){
		if(extra!=null&&extra!=undefined){
			console.log(extra);
		}
		this.__verBD.ejecutar(this);
	}

	__initAlVariarSize(alVariarSize){
		//bd:BD_RowElement=>{}
		this.__alVariarSize=new ConjuntoDeEventos();
		this.__alVariarSize.add(alVariarSize);
	}
	addAlVariarSize(alVariarSize){
		//bd:BD_RowElement=>{}
		if(this.__alVariarSize!=undefined&&this.__alVariarSize!=null){
			this.__alVariarSize.add(alVariarSize);
            // const anterior=this.__alVariarSize;
            // this.__alVariarSize=(v)=>{
            //     anterior(v);
            //     alVariarSize(v);
            // };
            
        }else{
			this.__initAlVariarSize(alVariarSize);
            //this.__alVariarSize=alVariarSize;
        }
	}
	__llamarAlVariarSize(){
		if(this.__alVariarSize!=undefined&&this.__alVariarSize!=null){
			//this.__alVariarSize(this);
			this.__alVariarSize.ejecutar(this);
		}
	}
	removeAlVariarSize(alVariarSize){
		if(this.__alVariarSize!=undefined&&this.__alVariarSize!=null){
			this.__alVariarSize.remove(alVariarSize);
		}
	}
	
	__crearMapRow(listaDeDatos){
		let mapRow=new Map();
		for (let i = 0; i < listaDeDatos.length; i++) {
			//console.log("intenta agregar i="+i);
			let dato = listaDeDatos[i];
			mapRow.set(this.llaves[i],dato);
			
			
		}
		//console.log("los agrego");
		return mapRow
	}
	addRow(listaDeDatos){
		
		this.listaDeMapBD.push(this.__crearMapRow(listaDeDatos));
		this.__llamarAlVariarSize();
	}
	addRowEmpty(){
		let listaEmpty=[];
		if(this.metodoGetListaEmpty!=undefined&&this.metodoGetListaEmpty!=null){
			listaEmpty=this.metodoGetListaEmpty();
		}else{
			for (let index = 0; index < this.llaves.length; index++) {
				listaEmpty.push("");
				
			}
		}
		this.addRow(listaEmpty);
	}
	setRow(indice,listaDeDatos){
		this.listaDeMapBD[indice]=this.__crearMapRow(listaDeDatos);
	}

	getRow(indice){
		const row = this.listaDeMapBD[indice];
		return this.__crearMapIds(new Map(row),indice);
		// map2=new Map(row);
		// for (const idActual of lista.listaDeNombresIds) {
		// 	map2.set(idActual,idActual+""+indice);
		// }
		// return map2;
	}
	getFila(indice){
		return new FilaRow(indice,this.getRow(indice),this);
	}
	getLastRow(){
		leng=this.size();
		
		return  leng==0?null:this.getRow(leng-1);
	}
	getLastIndex(){
		return this.size()-1;
	}
	getMapIds(indice){
		return this.__crearMapIds(new Map(),indice);
		
	}
	getListaNombreIds_del(indice){
		let l=[];
		const idActual = this.listaDeNombresIds[indice];
		for (let i = 0; i < this.size(); i++) {
			
			l.push(idActual+""+i);
			
		}
		return l;
	}
	__crearMapIds(map,indice){
		for (const idActual of this.listaDeNombresIds) {
			map.set(idActual,idActual+""+indice);
		}
		return map;
	}
	size(){
		return this.listaDeMapBD.length;
	}

	contieneValorDeKey(key,valor){
		
		for (let i = 0; i < this.size(); i++) {
			let m= this.getRow(i);
			if(m.has(key)&&m.get(key)===valor){
				return true;
			}
		}
		return false;
	}
	isEmpty(){
		return this.size()==0;
	}
	remove(indiceOLisatDeIndices){
		if(esLista(indiceOLisatDeIndices)){
			let listaOrdenada=[...indiceOLisatDeIndices].sort();
			for (let index = 0; index < listaOrdenada.length; index++) {
				const indice = listaOrdenada[index];
				this.remove(indice-index);
			}
		}else{
			this.listaDeMapBD.splice(indiceOLisatDeIndices,1);
			this.__llamarAlVariarSize();
		}

		return this;
	}
	removeLast(){
		if(!this.isEmpty()){
			this.remove(this.getLastIndex());
		}
		return this;
	}
	swap(indiceA,indiceB){
		let rowA=this.listaDeMapBD[indiceA];
		let rowB=this.listaDeMapBD[indiceB];
		this.listaDeMapBD[indiceA]=rowB;
		this.listaDeMapBD[indiceB]=rowA;
		return this;
	}

	clear(){
		this.listaDeMapBD=[];
		this.__llamarAlVariarSize();
		return this;
	}
	set(indice,key,valor){
		return this.listaDeMapBD[indice].set(key,valor);
	}
	getFilaFor(key,value){
		for (let index = 0; index < this.size(); index++) {
			let fila=this.getFila(index);
			let map=fila.map;
			if(map.get(key)==value){
				//console.log("lo encontro");
				return fila;
			}
		}
		//console.log("fue null");
		return null;
	}
}




// class ManagerDlg_AceptarCancelar extends ManagerDlg_ContenidoText{
// 	constructor(id,metodoShow,metodoHide){
// 		super(id,"",metodoShow,metodoHide);
// 		this.__conjuntoEventosAceptar;
// 		this.idTitulo;
// 		//this.idBotonAceptar;
// 		//this.eventosAceptar=new ConjuntoDeEventos();
// 	}
// 	setIdBotonAceptar(id){
// 		this.__conjuntoEventosAceptar=new ConjuntoDeEventos_ParaElemento(id);
// 		this.__conjuntoEventosAceptar.addOnClick();
// 	}
// 	setAccionAlAceptar(metodo){
// 		const self=this;
// 		this.__conjuntoEventosAceptar.setMetodoUnico(v=>{
// 			self.hide();
// 			metodo();
			
// 		});
// 	}
// 	setTitulo(titulo){
// 		setHTML(this.idTitulo,titulo);
// 		return this;
// 	}
// 	setTextoBotonAceptar(texto){
// 		setHTML(this.__conjuntoEventosAceptar.id,texto);
// 		return this;
// 	}
// 	showDlg(titulo,contenido,textoEnAceptar,metodoAlAceptar){
// 		this.setTitulo(titulo);
// 		this.setContenido(contenido);
// 		this.setTextoBotonAceptar(textoEnAceptar);
// 		this.setAccionAlAceptar(metodoAlAceptar);
// 		this.show();
// 	}
// }