//data = [];
//original = "";
//generar = 0;
//$(document).ready(function (){
//	 alert("hola");
//});

var Ciclovia = React.createClass({
	imprimir : function(){
		var inputs = $("input.imprimir");

		var global = {};
		global["rutas"] = [];
		global["name"] = $("#nombre-form").val();
		global["place"] = $("#NombreCiudad").val();
		global["type"] = "model";
		global["startHour"] = $("#HoraInicio").val();
		global["endHour"] = $("#HoraFin").val();
		global["numTracks"] = generar;

		var rutas = [];
		var ruta = {};
		var vecino = {};

		for (var i = 0; i < inputs.length; i++) {
			
			if ($(inputs[i]).attr("class") === "form-control imprimir rutaId"){
				if (i != 0){
					console.log("PUSHED RUTA");
					rutas.push(ruta);
					ruta = {};
				}
				ruta["id"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaDistancia"){
				ruta["distance"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaProbaInit"){
				//ruta["probabilityBegin"] = $(inputs[i]).val();
				ruta["probabilityBegin"] = 0.5
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaProbaFin"){
				//ruta["probabilityEnd"] = $(inputs[i]).val();
				ruta["probabilityEnd"] = 0.5
			}
			ruta["neighboor"] = [];

			if ($(inputs[i]).attr("class") === "form-control imprimir vecinoId"){
				vecino["id"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir vecinoDistancia"){
				//vecino["probability"] = $(inputs[i]).val();
				vecino["probability"] = 0.5
			}else if ($(inputs[i]).attr("class") === "form-control imprimir vecinoDesde"){
				vecino["direction"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir vecinoHacia"){
				vecino["from"] = $(inputs[i]).val();
				ruta["neighboor"].push(vecino);
				vecino = {};

				if (i + 1 < inputs.length){
					if ($(inputs[i + 1]).val() === "form-control imprimir rutaId"){
						startVecinos = false;
					}
				}else{
					rutas.push(ruta);
				}
			}				
		}

		global["track"] = rutas;

		mySendPost(global);

	},
	componentDidMount: function() {
		var arr = [];

		for (var i = 0; i < generar; i++) {
			var ruta = {};
			ruta["vecinos"] = [];
			for (var i = 0; i < 6; i++) {
				var vecino = {};
				vecino["a"] = 1;
				ruta["vecinos"].push(vecino);
			}
			ruta["numero"] = i + 1;
			arr.push(ruta);
		};

		this.setState({rutas:arr});

	},
	handleFormSubmit: function (){
		alert($("#NombreCiudad").val());
	},
	getInitialState: function() {
		var arr = [];
		return {data: [], rutas:arr};
	},
	render: function(){
		return(
			<div>
			<table className="InfoBasica">
				Por favor llenar la siguiente informacion
				<tbody id="principal">	
					<form>
						<div className="input-group">
							<span className="input-group-addon">Nombre del form</span>
							<input type="text" id="nombre-form" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
						</div>
						<br/>
					</form>
					<form>
						<div className="input-group">
							<span className="input-group-addon">Nombre de la ciudad</span>
							<input type="text" id="NombreCiudad" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
							<span className="input-group-addon">Hora Inicio</span>
							<input type="number" id="HoraInicio" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
							<span className="input-group-addon" >Hora Fin</span>
							<input type="number" id="HoraFin" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
						</div>
					</form>			
				</tbody>
				<thread>
				</thread>
			</table>

			<div>
				<br/>
				<div className="input-group">
					<span className="input-group-addon">N&uacute;mero de tramos:</span>
					<input type="number" id="generar" className="form-control" placeholder="Cuantas" aria-describedby="basic-addon1"> </input>
				</div>
				<br/>
				<button type="button" className="btn btn-default" onClick={this.generar}>Generar</button>			
			</div>

			<div className="">
				<Ruta rutas={this.state.rutas}> </Ruta>
				<button type="button" className="btn btn-default" onClick={this.imprimir}>Enviar</button>
				<br></br><br></br><br></br>
			</div>
			</div>

		);
	},
	generar: function(){
		var cuantasRutas = $("#generar").val();
		// alert(cuantasRutas);
		generar = parseInt(cuantasRutas);

		var arr = [];

		console.log("Generar: " + generar);

		for (var i = 0; i < generar; i++) {
			var ruta = {};
			ruta["vecinos"] = [];
			for (var j = 0; j < 6; j++) {
				var vecino = {};
				vecino["a"] = 1;
				ruta["vecinos"].push(vecino);
			}
			ruta["numero"] = i + 1;
			arr.push(ruta);
		};

		console.log("Longitud rutas: " + arr.length);


		this.setState({rutas:arr});
	}
});

var Ruta = React.createClass({
	render: function(){
		console.log(this.props.rutas);
		console.log(JSON.stringify(this.props.rutas));

		var rutas = this.props.rutas.map(function (ruta) {
			return (
				<div>
					<h3>TRAMO {ruta.numero}</h3>
					<input type="text" className="form-control imprimir rutaId" placeholder="ID tramo" aria-describedby="basic-addon1"> </input>
					<input type="text" className="form-control imprimir rutaDistancia" placeholder="Distancia" aria-describedby="basic-addon1"> </input>

					<Vecino vecino={ruta.vecinos}> </Vecino>	

					<h3>FIN TRAMO {ruta.numero} </h3>
				</div>	
			);
		});
		return (
			<div>
				{rutas}
				<hr></hr>
			</div>
		);
	}
});

var Vecino = React.createClass({
	render: function(){
		console.log(this.props);
		var vecinos = this.props.vecino.map(function (vecino) {
			return (
				<div className="row">
					<div className="col-md-1"></div> 
					<div className="col-md-11"> 
						<input type="text" className="form-control imprimir vecinoId" placeholder="ID tramo" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoDistancia" placeholder="Distancia" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoDesde" placeholder="desde" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoHacia" placeholder="hacia" aria-describedby="basic-addon1"> </input>
					</div>
					
					<p>Fin vecino</p>
				</div>	
			);
		});
		return (
			<div>
				<h4>Vecinos</h4>
				{vecinos}
			</div>
		);
	}
});

React.render(
	<Ciclovia  />, document.getElementById('container')
	);