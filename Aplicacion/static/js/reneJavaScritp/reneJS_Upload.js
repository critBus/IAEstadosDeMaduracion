class DatosDeProgresoDeFileUpload{
    constructor(){
        this.porciento=0;
    }
}

class FileUpload {
    constructor(input) {
        this.input = input;
        this.max_length =1024 * 1024 * 3; //1024 * 1024 * 10; // 10 mb



        this.url_objetivo=null;//ejemplo '/fileUploader/'

        this.__metodo__alComenzarLaSubida=null;//(f:FileUpload,v:nombreArchivo)=>{}
        this.__metodo__alProgresarEnSubida=null;//(f:FileUpload,v:porcientoActual)=>{}
        this.__metodo__alTerminar=null;//(f:FileUpload,v:informacion)=>{}
        this.__metodo__alDarError=null;//(f:FileUpload,v:informacion)=>{}
        this.__metodo_GetDatosDeProgreso=null;//()=>DatosDeProgresoDeFileUpload

        this.__metodo__alDetenerUpload=null;//(f:FileUpload)=>{}
        this.__detener_upload=false;




        //this.end=null;
        //this.existingPath=null;
    }
    detenerUpload(){
        this.__detener_upload=true;
    }
    upload() {
        this.create_progress_bar();
        this.initFileUpload();
    }

    initFileUpload() {
        this.file = this.input.files[0];

        this.__alComenzarLaSubida(this.file.name);
        console.log("star 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!");
        this.upload_file(0, null);
    }

    __alDetenerUpload(){
        if(this.__metodo__alDetenerUpload!==undefined&&this.__metodo__alDetenerUpload!=null){
            this.__metodo__alDetenerUpload(this);
        }
    }

    __alComenzarLaSubida(nombreArchivo){
        this.__metodo__alComenzarLaSubida(this,nombreArchivo);
        // $('.filename').text(this.file.name)
        // $('.textbox').text("Uploading file")
    }
    __alProgresarEnSubida(porcientoActual){
        this.__metodo__alProgresarEnSubida(this,porcientoActual);
        // $('.progress-bar').css('width', percent + '%')
        // $('.progress-bar').text(percent + '%')
    }
    __alTerminar(informacion){
        this.__metodo__alTerminar(this,informacion);
        // $('.textbox').text(res.data);
        // alert(res.data)
    }
    __alDarError(informacion){
        if(this.__metodo__alDarError!==undefined&&this.__metodo__alDarError!==null){
            this.__metodo__alDarError(this,informacion);
        }

    }

    __getDatosDeProgreso(){
        //console.log("va a entrar");
        //this.__metodo_GetDatosDeProgreso();
        //console.log("va a entrar 00");
        //console.log("this.__metodo_GetDatosDeProgreso="+this.__metodo_GetDatosDeProgreso);
        if(this.__metodo_GetDatosDeProgreso!==undefined&&this.__metodo_GetDatosDeProgreso!==null){
            // console.log("entro -------");
            let d=this.__metodo_GetDatosDeProgreso();
            // console.log("d="+d);
            return d;
        }
        // console.log("no entro");
    }

    upload_file(start, path) {
        //var end;
        const self = this;
        let existingPath = path;
        //this.existingPath=path;
        const formData = new FormData();
        const nextChunk = start + this.max_length + 1;
        const currentChunk = this.file.slice(start, nextChunk);//obtiene lo que podria ser un byte[] con el troso a mandar
        const uploadedChunk = start + currentChunk.size

        console.log("start="+start);
         console.log("uploadedChunk="+uploadedChunk);
        console.log("this.file.size="+this.file.size);
         const end =uploadedChunk >= this.file.size?1:0;
        console.log("end="+end);
        // if (uploadedChunk >= this.file.size) {
        //     const end = 1;
        // } else {
        //     const end = 0;
        // }
        formData.append('file', currentChunk);//pasa al formulario el troso byte[] y el solito detecta que se trata de un tipo byte[] y lo pone en la seccion FILE (no en el POST)
        formData.append('filename', this.file.name);
        formData.append('end', end);
        formData.append('existingPath',existingPath);
        formData.append('nextSlice', nextChunk);
        let a=this.__getDatosDeProgreso();
        //console.log("a="+a);
        let b=a.porciento;
        //console.log("b="+b);
        formData.append('porciento', b);
        // $('.filename').text(this.file.name)
        // $('.textbox').text("Uploading file")
        //this.__alComenzarLaSubida(this.file.name);

        $.ajaxSetup({
        // make sure to send the header
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
            xhr: function () {
                let xhr = new XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        let percent=0;
                        if (self.file.size < self.max_length) {
                             percent= Math.round((e.loaded / e.total) * 100);
                        } else {
                            percent = Math.round((uploadedChunk / self.file.size) * 100);
                        }
                        // $('.progress-bar').css('width', percent + '%')
                        // $('.progress-bar').text(percent + '%')
                        self.__alProgresarEnSubida(percent);
                    }
                });
                return xhr;
            },

            //url: '/fileUploader/',
            url: self.url_objetivo,
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
            error: function (xhr) {
                //alert(xhr.statusText);
                self.__alDarError(xhr.statusText);
            },
            success: function (res) {
                if(res.termino_con_error){
                        console.log("error en ajaz de suvida");
                     self.__alDarError(res.data);
                     return;
                }

                if (self.__detener_upload) {
                    self.__alDetenerUpload();
                    // console.log("mando a detener !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                } else {
                    if (nextChunk < self.file.size) {
                        // upload file in chunks
                        let existingPath = res.existingPath
                        self.upload_file(nextChunk,  existingPath);
                        // console.log("sigue escribiendo")
                    } else {
                        // upload complete
                        // $('.textbox').text(res.data);
                        // alert(res.data)
                        self.__alTerminar(res.data);
                    }
                }
            }
        });
    }

    create_progress_bar() {
        //Se hace algo con el visual
        // var progress = `<div class="file-icon">
        //                     <i class="fa fa-file-o" aria-hidden="true"></i>
        //                 </div>
        //                 <div class="file-details">
        //                     <p class="filename"></p>
        //                     <small class="textbox"></small>
        //                     <div class="progress" style="margin-top: 5px;">
        //                         <div class="progress-bar bg-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
        //                         </div>
        //                     </div>
        //                 </div>`
        // document.getElementById('uploaded_files').innerHTML = progress
    }

}

class ManagerSubmitConProgress{
    constructor(){
        this.idInputFile;
        this.idBotonSubmit;

        this.url_objetivo;
        this.__metodo__alComenzarLaSubida;//(f:FileUpload,v:nombreArchivo)=>{}
        this.__metodo__alProgresarEnSubida;//(f:FileUpload,v:porcientoActual)=>{}
        this.__metodo__alTerminar;//(f:FileUpload,v:informacion)=>{}
        this.__metodo__alDarError=null;//(f:FileUpload,v:informacion)=>{}
        this.__metodo_GetDatosDeProgreso=null;//()=>DatosDeProgresoDeFileUpload

        this.fileUpload=null;


        this.condicionDeValidacion=()=>true;
        this.__accionSiNoEsValido=new ConjuntoDeEventos();

    }
    addSiNoEsValido(metodo){
        this.__accionSiNoEsValido.add(metodo);
    }

    detenerUpload(){
        if(this.fileUpload!=null&&this.fileUpload!=undefined){
            this.fileUpload.detenerUpload()
        }

    }
    aplicarConfiguracion(){
        const self=this;
        (function ($) {
            $('#'+self.idBotonSubmit).on('click', (event) => {
                event.preventDefault();
                if(self.condicionDeValidacion()){
                    let uploader = new FileUpload(document.querySelector('#'+self.idInputFile))
                    uploader.url_objetivo=self.url_objetivo;
                    uploader.__metodo__alComenzarLaSubida=self.__metodo__alComenzarLaSubida;
                    uploader.__metodo__alProgresarEnSubida=self.__metodo__alProgresarEnSubida;
                    uploader.__metodo__alTerminar=self.__metodo__alTerminar;
                    uploader.__metodo__alDarError=self.__metodo__alDarError;
                    uploader.__metodo_GetDatosDeProgreso=self.__metodo_GetDatosDeProgreso;
                    self.fileUpload=uploader;
                    uploader.upload();

                }else{
                    self.__accionSiNoEsValido.ejecutar();
                }



            });
        })(jQuery);
    }
}

// const ID_INPUT_FILE='fileupload';
// const ID_BOTON_SUBMIT='submit';



