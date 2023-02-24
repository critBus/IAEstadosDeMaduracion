//import reneJavaScript
//import reneJS_Clases

class Paginacion {
    constructor(listaDeIndices, iSeleccionado = -1) {
        this.listaDeIndices = listaDeIndices;
        this.iSeleccionado = iSeleccionado;
        //this.indiceSiguiente=-1;
        ///if(!this.isEmpty()){}
        //this.indiceAnterior=-1;
    }
    isEmpty() {
        return this.listaDeIndices.length == 0;
    }
    haySiguiente() {
        if (!this.isEmpty() && this.iSeleccionado != -1 && this.iSeleccionado != undefined && this.iSeleccionado != null) {
            return this.listaDeIndices.length > 1 && this.iSeleccionado != this.listaDeIndices.length - 1;
        }
        return false;
        //return this.indiceSiguiente!=-1&&this.indiceSiguiente!=undefined&&this.indiceSiguiente!=null;
    }
    hayAnterior() {
        if (!this.isEmpty() && this.iSeleccionado != -1 && this.iSeleccionado != undefined && this.iSeleccionado != null) {
            return this.listaDeIndices.length > 1 && this.iSeleccionado != 0;
        }
        return false;
        //return this.indiceAnterior!=-1&&this.indiceAnterior!=undefined&&this.indiceAnterior!=null;
    }
    getIndiceSiguiente() {
        return this.listaDeIndices[this.iSeleccionado] + 1;
    }
    getIndiceAnterior() {
        return this.listaDeIndices[this.iSeleccionado] - 1;
    }
    getIndice(i) {
        return this.listaDeIndices[i];
    }
    getIndiceSeleccionado() {
        return this.listaDeIndices[this.iSeleccionado];
    }
}

class GestorDePaginacionSimple {
    constructor(indiceActual, cantidadDeElementos, step, cantidadDeIndicesAMostrarMaximo) {
        //va intentar poner el indice actual en el medio
        //indiceActual: 1-... comienza en 1
        //step: saltos para cuando se va saltando talves de # durante la cantidadDeElementos
        // pero para casos donde solo se van a mostrar de 1 en 1 el step seria 1
        //cantidadDeIndicesAMostrarMaximo: 3-....  3 como minimo
        
        this.listaDeIndices = [];
        this.iActual = -1;

        this.cantidadDeElementos=cantidadDeElementos;
        this.step=step;
        this.cantidadDeIndicesAMostrarMaximo=cantidadDeIndicesAMostrarMaximo;

        this.indiceActual=indiceActual;

        this.actualizar(indiceActual);
        
    }

    actualizar(indiceActual){
        this.listaDeIndices = [];
        this.iActual = -1;
        this.indiceActual=indiceActual;

        let cantidadDeIndices = toInt(this.cantidadDeElementos / this.step);
        if (this.cantidadDeElementos % this.step != 0) {
            cantidadDeIndices += 1;
        }
        let cantidadDeIndicesALosLados = this.cantidadDeIndicesAMostrarMaximo - 1;
        if (this.cantidadDeIndicesAMostrarMaximo > 2) {
            cantidadDeIndicesALosLados = toInt((this.cantidadDeIndicesAMostrarMaximo - 1) / 2)
        }
        
        if (cantidadDeIndices > 0 && indiceActual <= cantidadDeIndices) {
            if (cantidadDeIndices == 1 && indiceActual == 1) {
                this.listaDeIndices = [1];
                this.iActual = 0;
            } else {
                let la = [];
                let ls = [];
                let indiceAnterior = -1;
                let indiceSiguiente = -1;
                while ((len(la) + len(ls) + 1) < this.cantidadDeIndicesAMostrarMaximo &&
                    (len(la) + len(ls) + 1) < cantidadDeIndices) {
                    if (indiceActual > 1) {
                        if (indiceAnterior == -1) {
                            indiceAnterior = indiceActual - 1
                            la.push(indiceAnterior)
                        } else if (indiceAnterior > 1) {
                            indiceAnterior = indiceAnterior - 1
                            la.push(indiceAnterior)
                        }
                    }


                    if (indiceActual<cantidadDeIndices){
                        if (indiceSiguiente==-1){
                            indiceSiguiente=indiceActual+1
                            ls.push(indiceSiguiente)
                        }else if(indiceSiguiente<cantidadDeIndices){
                            indiceSiguiente = indiceSiguiente + 1
                            ls.push(indiceSiguiente)
                        }
                    }
                    
                        


                }
                la.reverse();
                this.listaDeIndices.push(...la);
                this.listaDeIndices.push(indiceActual);
                this.listaDeIndices.push(...ls);
                this.iActual=len(la);
            }
        }
        return this;
    }
    getPaginacion(){
        
        
        return new Paginacion(this.listaDeIndices,this.iActual);
    }
}

