//import reneJS_Clases

// Para activar lo tooltip
// Codigo de bootstrap
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function showDlgBostrap(id){
  $("#"+id).modal('show')
}

function hideDlgBostrap(id){
  $("#"+id).modal('hide')
}

function addOnShowDlgBostrap(id,metodo) {
$('#'+id).on('shown.bs.modal', function (e) {
    metodo(e);
})
}

function showDlgBostrapOnClick(idDlg,idBoton){
  addOnClick(idBoton,()=>showDlgBostrap(idDlg));
}


function setProgressBoostrap(idBr,idSpam,progreso){
  let progresoStr=progreso+"%";
  
  if(progreso<=15){
      //setText(idSpam,progresoStr);
      getEl(idSpam).style.width=(100-progreso)+"%";
      setHTML(idSpam,progresoStr);
      setHTML(idBr,"");
  }else{
      setText(idSpam,"");
      displayNone(idSpam);
      setHTML(idBr,progresoStr);
  }
  setAtr(idBr,"aria-valuenow",progreso);
  setAtr(idBr,"aria-valuenow",progreso);
  getEl(idBr).style.width=progreso+"%";
}

class ManagerDlg_Bootstrap extends ManagerDlg{
  constructor(id){
    super(id,v=>{
      showDlgBostrap(id);
    },v=>{
      hideDlgBostrap(id);
    });
  }
}

class ManagerDlg_ContenidoText_Bootstrap extends ManagerDlg_ContenidoText{
  constructor(id){
    super(id,v=>{
      showDlgBostrap(id);
    },v=>{
      hideDlgBostrap(id);
    });
  }
}

class ManagerDlg_Espera_ContenidoText_Bootstrap extends ManagerDlg_ContenidoText_Bootstrap{
	constructor(id){
		super(id);
        const self=this;
        addOnShowDlgBostrap(id,e=>{
          if(!self.esVisible){
            self.hide();
          }
        });
	}
}


class ManagerDlg_Aceptar_Bootstrap extends ManagerDlg_Aceptar{
  constructor(id){
    super(id,v=>{
      showDlgBostrap(id);
    },v=>{
      hideDlgBostrap(id);
    });
  }
}

class ManagerDlg_ProgresCancelar_Bootstrap extends ManagerDlg_Aceptar_Bootstrap{
  constructor(id){
    super(id);
    this.idBrProgreso;
    this.idSpamProgreso;
    //this.setTextoBotonAceptar("Cancelar");

  }
  setIdBotonCancelar(id){
    return this.setIdBotonAceptar(id);
  }
  setAccionAlCancelar(metodo){
    return this.setAccionAlAceptar(metodo);
  }
  setProgreso(progreso){
    setProgressBoostrap(this.idBrProgreso,this.idSpamProgreso,progreso);
    return this;
  }
}

class ManagerDlg_AceptarCancelar_Bootstrap extends ManagerDlg_AceptarCancelar{
  constructor(id){
    super(id,v=>{
      showDlgBostrap(id);
    },v=>{
      hideDlgBostrap(id);
    });
  }
}



