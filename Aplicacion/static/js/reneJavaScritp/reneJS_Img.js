class TipoDeImagen{
    constructor(extencion,extencionDesactivada){
        this.extencion = extencion
        this.extencionDesactivada=extencionDesactivada
    }

}

TipoDeImagen.PNG=new TipoDeImagen(".png", ".pn");
TipoDeImagen.JPEG=new TipoDeImagen(".jpeg", ".jep");
TipoDeImagen.JPG=new TipoDeImagen(".jpg", ".jp");
TipoDeImagen.WEPP=new TipoDeImagen(".webp", ".we");
TipoDeImagen.VALUES=[TipoDeImagen.PNG
                     ,TipoDeImagen.JPEG
                     ,TipoDeImagen.JPG
                     ,TipoDeImagen.WEPP]


TipoDeImagen.get=v=>{
    if(v==null||v==undefined){
        return null;
    }
    if( v instanceof TipoDeImagen){
        return v;
    }
    v=v.toLocaleLowerCase();
    for (const tipo of TipoDeImagen.VALUES) {
        if(v==tipo.extencion){
            return tipo;
        }
    }
    return null;
};

TipoDeImagen.pertence=v=>TipoDeImagen.get(v)!=null;


function esImagen(url){
    return TipoDeImagen.pertence(getExtencion(url));
}

function esImagen_InputFile_JPG_PNG(idInputFile){
    let extencion=getExtencionArchivoEnInput(idInputFile);
    if(esImagen(extencion)){
        let tipoImg=TipoDeImagen.get(extencion);
        return tipoImg==TipoDeImagen.PNG||tipoImg==TipoDeImagen.JPEG||tipoImg==TipoDeImagen.JPG;
    }

    return false;
}