function cargaLentaImg(idContenedorImg,idImg,srcStr,htmlCargando,htmlLaImagenNoSePudoCargar) {
    image = new Image();
    image.id=idImg;
    image.src = srcStr;
    image.onload = function () {
        $('#'+idContenedorImg).empty().append(image);
    };
    image.onerror = function () {
        $('#'+idContenedorImg).empty().html(htmlLaImagenNoSePudoCargar);//.html('That image is not available.');
    }

    $('#'+idContenedorImg).empty().html(htmlCargando);//.html('Loading...');
}

function setSrcImagen(idImg,srcStr){
  var image = $('#'+idImg);
image.attr('src', srcStr);
//$('#image-holder').append(image);
//   var image = $('<img></img>');
// image.attr('src', 'images/image1.jpg');
// $('#image-holder').append(image);
}
function ejecutarAjax(post_url,argumentos_post_json,funcion_al_obtener_respuesta,funcion_al_dar_error){
    //funcion_al_obtener_respuesta (response)->{} donde  response.content.NOMBRE_ARGUMENTO
    // y aveces el .content tiene que ser agregado manualmente en el servidor ejempl { 'content':{}}
    let funcionError=funcion_al_dar_error;
    if(funcion_al_dar_error===undefined||funcion_al_dar_error===null){
      funcionError=function (xhr) {
        //alert(xhr.statusText);
      };
    }
    $.ajax({
        url : post_url,
        type: "POST",
        data : argumentos_post_json,
        success:funcion_al_obtener_respuesta,
        error: funcionError
    });

}

class ManagerLimitadorTamañoDeArchivo{
    constructor(){
        this.maxSize;//ejemplo 2 * 1024 * 1024
        this.idformulario;
        this.idInputFile;
        this.accionNoCumple;//(this)=>{}
    }
    aplicarConfiguracion(){
        $(this.idformulario).submit(function() {
            if (window.File && window.FileReader && window.FileList && window.Blob) {
              var file = $('#'+this.idInputFile)[0].files[0];
          
              if (file && file.size > this.maxSize) {
                this.accionNoCumple(this);
                return false;
              }
            }
          });
    }
}

$("form").submit(function() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
      var file = $('#id_file')[0].files[0];
  
      if (file && file.size > 2 * 1024 * 1024) {
        alert("File " + file.name + " of type " + file.type + " is too big");
        return false;
      }
    }
  });



  function ponerImagenAlCargar(idFile,idElementoQueTomaElClick,idImagen,idElementoDeEspera,eventoTerminarDeCargarLaImagen){
    displayNone(idImagen,true);
    __addActualizadorDeUploadFile(idFile,idElementoQueTomaElClick,n=>{
      let input=getEl(idFile);
      //console.log("va a mostrar",input.files.length);
      //if(!input.files.length) return;

      let file = input.files[0];


      setSrcImagen(idImagen, URL.createObjectURL(file));
      if(eventoTerminarDeCargarLaImagen!=null&&eventoTerminarDeCargarLaImagen!=undefined){
        eventoTerminarDeCargarLaImagen(n);
      }

    // console.log("idImagen="+idImagen);
    // console.log("idElementoDeEspera="+idElementoDeEspera);
    displayNone(idElementoDeEspera,true);
    displayNone(idImagen,false);
    });




  }


  function __addActualizadorDeUploadFile(idFile,idElementoQueTomaElClick,metodoAlCargarArchivo){
    //metodoAlCargarArchivo:   filename->{}
    jQuery('input[id='+idFile+']').change(function(){
      var filename = jQuery(this).val().split('\\').pop();
      var idname = jQuery(this).attr('id');
      console.log(jQuery(this));
      console.log(filename);
      console.log(idname);

      console.log(jQuery(this).val());

      metodoAlCargarArchivo(filename);

      //setAtr("idImagen","src",(jQuery(this).val()+""));



      // let byts=file.slice(0, file.size);
      // console.log(byts);
      //let start=0;

      // let end=false;
      // do{

      //   let nextChunk = start + this.max_length + 1;

      // }while(!end);

      // while(){

      // }

      //console.log(file);


      //document.getElementById(idElementoAponerNombreEnTexto).innerText=filename;

      //jQuery('span.'+idname).next().find('span').html(filename);
     });

     addOnClick(idElementoQueTomaElClick,v=>{
      simularClick(idFile);
    });

  }


  function addActualizadorDeUploadFile_Text(idFile,idElementoQueTomaElClick,idElementoAponerNombreEnTexto){
    addOnClick(idElementoAponerNombreEnTexto,v=>{
      simularClick(idFile);
    });
    __addActualizadorDeUploadFile(idFile,idElementoQueTomaElClick,
      filename=>{
        document.getElementById(idElementoAponerNombreEnTexto).innerText=filename;
      }
      );
  }

  function addActualizadorDeUploadFile_Value_v2(idFile,idElementoQueTomaElClick,idElementoAponerNombreEnTexto){

    addActualizadorDeUploadFile_Value(idFile,idElementoQueTomaElClick,idElementoAponerNombreEnTexto);
    displayNone(idFile,true);
  }



  function addActualizadorDeUploadFile_Value(idFile,idElementoQueTomaElClick,idElementoAponerNombreEnTexto){
    addOnClick(idElementoAponerNombreEnTexto,v=>{
      simularClick(idFile);
    });
    __addActualizadorDeUploadFile(idFile,idElementoQueTomaElClick,
      filename=>{
        setValue(idElementoAponerNombreEnTexto,filename);

      }
      );
  }


  function uploadAjaxImagen(idFile,urlPost,dicExtra={}
  ,evento_siTieneExito,evento_SiDaError
  ,keyByts="file",keyNombreImagen="filename",keySize="size",keyEnvioImagen="envioImagen"){
      console.log('llamo a enviar');
      let hayImagen=notEmpty_ArchivoEnInput(idFile);
      dicExtra[keyEnvioImagen]=hayImagen;
      if(hayImagen){
          function envento_alProgresar(porcentage){

          }

            console.log('prepara los lementos ha enviar');
            const input=document.querySelector('#'+idFile);
            const file = input.files[0];

            const start=0;
            const size=file.size;

            const formData = new FormData();
            const currentChunk = file.slice(start, size);
            const uploadedChunk = start + size;

            formData.append(keyByts, currentChunk);
            formData.append(keyNombreImagen, file.name);
            formData.append(keySize, file.size);

            // console.log("dicExtra"+dicExtra);
          for (const inputKey in dicExtra) {
              // console.log("inputKey"+inputKey);
              // console.log("dicExtra[inputKey]"+dicExtra[inputKey]);
              formData.append(inputKey, dicExtra[inputKey]);
          }

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
                        if (file.size < max_length) {
                             percent= Math.round((e.loaded / e.total) * 100);
                        } else {
                            percent = Math.round((uploadedChunk / file.size) * 100);
                        }
                        // $('.progress-bar').css('width', percent + '%')
                        // $('.progress-bar').text(percent + '%')
                        envento_alProgresar(percent);
                    }
                });
                return xhr;
            },

            //url: '/fileUploader/',
            url: urlPost,
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
            error: function (xhr) {
                //alert(xhr.statusText);
                evento_SiDaError(xhr.statusText);
            },
            success: function (res) {
                evento_siTieneExito(res);
            }
        });




          //-------------------
      }else{
          ejecutarAjax(urlPost,dicExtra,evento_siTieneExito,evento_SiDaError);
      }

}
