
function __PaginacionVisual_Bootstrap_addAlDesactivarAnteriorOSiguiente(paginacionVisual){
    paginacionVisual.addAlDesactivarAnteriorOSiguiente(id=>{
      ponerClase(id,"disabled");
      let tag_a=getFirsEl(id);
      setAtr(tag_a,"tabindex","-1");
      setAtr(tag_a,"aria-disabled","true");
  });
}

class PaginacionVisual_Bootstrap extends PaginacionVisual{
  constructor(){
      super();
      __PaginacionVisual_Bootstrap_addAlDesactivarAnteriorOSiguiente(this);
      // this.addAlDesactivarAnteriorOSiguiente(id=>{
      //     ponerClase(id,"disabled");
      //     let tag_a=getFirsEl(id);
      //     setAtr(tag_a,"tabindex","-1");
      //     setAtr(tag_a,"aria-disabled","true");
      // });
  }
}


class PaginacionVisualIndependiente_Bootstrap extends PaginacionVisualIndependiente{
  constructor(){
      super();
      __PaginacionVisual_Bootstrap_addAlDesactivarAnteriorOSiguiente(this);
      // this.addAlDesactivarAnteriorOSiguiente(id=>{
      //     ponerClase(id,"disabled");
      //     let tag_a=getFirsEl(id);
      //     setAtr(tag_a,"tabindex","-1");
      //     setAtr(tag_a,"aria-disabled","true");
      // });
  }
}