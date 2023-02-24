//import Ploty

class DatosVisualesDelGrafico{
    constructor(){
        this.ancho=500;//"80%"//500;
        this.alto=500;//"80%"//500;
        this.colorDeFondo='#f9fbfd';
    }
}
class DatosParaMatrisDeConfusion{
    constructor(){
        this.listaDeEtiquetas=[];
        this.matrizDeResultados=[];
        this.titulo="";

        
    }
}
function graficarMatrisDeConfusion(idDiv,datosParaMatrisDeConfusion,datosVisuales){
    if(datosVisuales===undefined){
        datosVisuales=new DatosVisualesDelGrafico();
    }
    // var xValues = ['A', 'B', 'C', 'D', 'E'];

    // var yValues = ['W', 'X', 'Y', 'Z'];

    // var zValues = [
    // [0.00, 0.00, 0.75, 0.75, 0.00],
    // [0.00, 0.00, 0.75, 0.75, 0.00],
    // [0.75, 0.75, 0.75, 0.75, 0.75],
    // [0.00, 0.00, 0.00, 0.75, 0.00]
    // ];
    if(datosParaMatrisDeConfusion.matrizDeResultados.length>0){
        var xValues=datosParaMatrisDeConfusion.listaDeEtiquetas;
        var yValues=datosParaMatrisDeConfusion.listaDeEtiquetas.filter(v=>true).reverse();
        var zValues=datosParaMatrisDeConfusion.matrizDeResultados.reverse();
        var titulo=datosParaMatrisDeConfusion.titulo;

        var colorscaleValue = [
        [0, '#3D9970'],
        [1, '#001f3f']
        ];

        var data = [{
        x: xValues,
        y: yValues,
        z: zValues,
        type: 'heatmap',
        colorscale: colorscaleValue,
        showscale: false
        }];

        var layout = {
        title: titulo,
        annotations: [],
        
        width: datosVisuales.ancho,
        height: datosVisuales.alto,
        titlefont: { 
            size:20 
            // ,color:'rgb(100,150,200)'
            // ,family:'Lato'
        },
        // font: { 
        //     size:20 
        //     ,color:'rgba(200,255,0,0.1)'
        //     ,family:''
        // },
        margin: {
            l: 100,
            r: 30,
            b: 5,
            t: 90,
            // pad: 4
        },
        paper_bgcolor: datosVisuales.colorDeFondo,//'#7f7f7f',
        //plot_bgcolor: '#c7c7c7',

        xaxis: {
            ticks: '',
            side: 'top'
        },
        yaxis: {
            ticks: '',
            ticksuffix: ' ',
            // width: 300,
            // height: 300,
            // autosize: false
        }
        };

        for ( var i = 0; i < yValues.length; i++ ) {
        for ( var j = 0; j < xValues.length; j++ ) {
            var currentValue = zValues[i][j];
            if (currentValue !== 0.0) {
            var textColor = 'white';
            }else{
            var textColor = 'black';
            }
            var result = {
            xref: 'x1',
            yref: 'y1',
            x: xValues[j],
            y: yValues[i],
            text: zValues[i][j],
            font: {
                family: 'Arial',
                size: 12,
                color: textColor
            },
            showarrow: false,
            
            };
            layout.annotations.push(result);
            // font: {
            //     color: textColor color: 'rgb(50, 171, 96)'
            // }
        }
        }

        Plotly.newPlot(idDiv, data, layout);

    }
    

}
class DatosDeProgresoDeEntrenamiento{
    constructor(){
        this.titulo='Progreso';
        this.tituloAxisX='Epocas';
        this.listaDePrecisiones=[];
        this.listaDePerdidas=[];
    }
}

function graficarProgresoDeEntrenamiento(idDiv,datosDeProgresoDeEntrenamiento,datosVisuales){
    if(datosVisuales===undefined){
        datosVisuales=new DatosVisualesDelGrafico();
    }
    if(datosDeProgresoDeEntrenamiento.listaDePrecisiones.length>0&&datosDeProgresoDeEntrenamiento.listaDePerdidas.length>0){
        x_datos=[];
        for (let i = 0; i < datosDeProgresoDeEntrenamiento.listaDePerdidas.length; i++) {
            x_datos[x_datos.length]=i;
            
        }

        var trace1 = {
        x: x_datos,
        y: datosDeProgresoDeEntrenamiento.listaDePrecisiones,
        name: 'Precisiones',
       
        
        type: 'scatter'
       
        };
        
        var trace2 = {
        x: x_datos,
        y: datosDeProgresoDeEntrenamiento.listaDePerdidas,
        name: 'Perdidas',
        type: 'scatter',
        yaxis: 'y2'
        
        };
        
        var data = [trace1, trace2];//
        var layout = {
            width: datosVisuales.ancho,
            height: datosVisuales.alto,
            paper_bgcolor: datosVisuales.colorDeFondo,
            title:datosDeProgresoDeEntrenamiento.titulo,
            xaxis: {
                title: datosDeProgresoDeEntrenamiento.tituloAxisX,
                
            },
            yaxis: {
                title: 'Precisiones',
                
                
            },
            yaxis2: {
                title: 'Perdidas',
                titlefont: {color: 'rgb(148, 103, 189)'},
                tickfont: {color: 'rgb(148, 103, 189)'},
                overlaying: 'y',
                side: 'right'
            },
            margin: {
               
                t: 40,
                // pad: 4
            },
        };
        Plotly.newPlot(idDiv, data,layout);

    }
    

}
function graficarMatrisDeConfusion_SinTitulo(idDiv,datosParaMatrisDeConfusion,datosVisuales){
    if(datosVisuales===undefined){
        datosVisuales=new DatosVisualesDelGrafico();
    }
    // var xValues = ['A', 'B', 'C', 'D', 'E'];

    // var yValues = ['W', 'X', 'Y', 'Z'];

    // var zValues = [
    // [0.00, 0.00, 0.75, 0.75, 0.00],
    // [0.00, 0.00, 0.75, 0.75, 0.00],
    // [0.75, 0.75, 0.75, 0.75, 0.75],
    // [0.00, 0.00, 0.00, 0.75, 0.00]
    // ];
    if(datosParaMatrisDeConfusion.matrizDeResultados.length>0){
        var xValues=datosParaMatrisDeConfusion.listaDeEtiquetas;
        var yValues=datosParaMatrisDeConfusion.listaDeEtiquetas.filter(v=>true).reverse();
        var zValues=datosParaMatrisDeConfusion.matrizDeResultados.reverse();
        var titulo=datosParaMatrisDeConfusion.titulo;

        var colorscaleValue = [
        [0, '#3D9970'],
        [1, '#001f3f']
        ];

        var data = [{
        x: xValues,
        y: yValues,
        z: zValues,
        type: 'heatmap',
        colorscale: colorscaleValue,
        showscale: false
        }];

        var layout = {
        // title: titulo,
        annotations: [],

        width: datosVisuales.ancho,
        height: datosVisuales.alto,
        // titlefont: {
        //     size:20
        //     // ,color:'rgb(100,150,200)'
        //     // ,family:'Lato'
        // },
        // font: {
        //     size:20
        //     ,color:'rgba(200,255,0,0.1)'
        //     ,family:''
        // },
        margin: {
            l: 100,
            r: 30,
            b: 5,
            t: 15,
            // pad: 4
        },
        paper_bgcolor: datosVisuales.colorDeFondo,//'#7f7f7f',
        //plot_bgcolor: '#c7c7c7',

        xaxis: {
            ticks: '',
            side: 'top'
        },
        yaxis: {
            ticks: '',
            ticksuffix: ' ',
            // width: 300,
            // height: 300,
            // autosize: false
        }
        };

        for ( var i = 0; i < yValues.length; i++ ) {
        for ( var j = 0; j < xValues.length; j++ ) {
            var currentValue = zValues[i][j];
            if (currentValue !== 0.0) {
            var textColor = 'white';
            }else{
            var textColor = 'black';
            }
            var result = {
            xref: 'x1',
            yref: 'y1',
            x: xValues[j],
            y: yValues[i],
            text: zValues[i][j],
            font: {
                family: 'Arial',
                size: 12,
                color: textColor
            },
            showarrow: false,

            };
            layout.annotations.push(result);
            // font: {
            //     color: textColor color: 'rgb(50, 171, 96)'
            // }
        }
        }

        Plotly.newPlot(idDiv, data, layout);

    }


}


// var trace1 = {
//     x: x_datos,
//     y: datosDeProgresoDeEntrenamiento.listaDePerdidas,
//     type: 'scatter',
//     name: 'Perdidas'
//     };
    
//     var trace2 = {
//     x: x_datos,
//     y: datosDeProgresoDeEntrenamiento.listaDePrecisiones,
//     type: 'scatter',
//     name: 'Precisiones',
//     yaxis: 'y2',
    
//     };