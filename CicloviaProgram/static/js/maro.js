data = [];
original = "";
generar = 0;
$(document).ready(function (){
	// alert("hola");
});

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
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaCalidad"){
				ruta["calidad"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaSemaforos"){
				ruta["semaforos"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir rutaPendiente"){
				ruta["pendiente"] = $(inputs[i]).val();
				ruta["neighboor"] = [];
			}

			if ($(inputs[i]).attr("class") === "form-control imprimir vecinoId"){
				vecino["id"] = $(inputs[i]).val();
			}else if ($(inputs[i]).attr("class") === "form-control imprimir vecinoDistancia"){
				vecino["probability"] = $(inputs[i]).val();
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

		console.log(global);
		alert(JSON.stringify(global));
		// $.each(inputs, function(index,value){
		// 	console.log($(value).val());

		// });
	},
	componentDidMount: function() {
		var arr = [];

		for (var i = 0; i < generar; i++) {
			var ruta = {};
			ruta["vecinos"] = [];
			for (var j = 0; j < 6; j++) {
				var vecino = {};
				vecino["ruta"] = i + 1;
				vecino["vec"] = j + 1;
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
			<div className="row">
				<div className="col-md-3">
					<span className="input-group-addon">Nombre del form</span>
					<input type="text" id="nombre-form" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
				</div>
				<div className="col-md-3">
					<span className="input-group-addon">Nombre de la ciudad</span>
					<input type="text" id="NombreCiudad" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
				</div>
				<div className="col-md-3">
					<span className="input-group-addon">Hora Inicio</span>
					<input type="number" id="HoraInicio" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
				</div>
				<div className="col-md-3">
					<span className="input-group-addon" >Hora Fin</span>
					<input type="number" id="HoraFin" className="form-control" placeholder="" aria-describedby="basic-addon1"> </input>
				</div>

			<div>
				
				<br/><br/><br/><br/>

				<p>Introducir el n&uacute;mero de rutas:</p>
				<div className="input-group">
					<span className="input-group-addon">N&uacute;mero de rutas:</span>
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
				vecino["ruta"] = i + 1;
				vecino["vec"] = j + 1;
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
			var valID = "ruta-" + ruta.numero + "-id";
			var valDist = "ruta-" + ruta.numero + "-distancia";
			var calidad = "ruta-" + ruta.numero + "-calidad";
			var semaforo = "ruta-" + ruta.numero + "-semaforo";
			var pendiente = "ruta-" + ruta.numero + "-pendiente";

			return (
				<div>
					<h3>RUTA {ruta.numero}</h3>
					<input type="text" className="form-control imprimir rutaId" placeholder={valID} aria-describedby="basic-addon1"> </input>
					<input type="text" className="form-control imprimir rutaDistancia" placeholder={valDist} aria-describedby="basic-addon1"> </input>
					<input type="text" className="form-control imprimir rutaCalidad" placeholder={calidad} aria-describedby="basic-addon1"> </input>
					<input type="text" className="form-control imprimir rutaSemaforos" placeholder={semaforo} aria-describedby="basic-addon1"> </input>
					<input type="text" className="form-control imprimir rutaPendiente" placeholder={pendiente} aria-describedby="basic-addon1"> </input>

					<Vecino vecino={ruta.vecinos}> </Vecino>	

					<h3>FIN RUTA</h3>				
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
			var vecId = "vecino-" + vecino.ruta + "-" + vecino.vec + "-id";
			var vecDist = "vecino-" + vecino.ruta + "-" + vecino.vec + "-distancia";
			var vecDesde = "vecino-" + vecino.ruta + "-" + vecino.vec + "-desde";
			var vecHacia = "vecino-" + vecino.ruta + "-" + vecino.vec + "-hacia";

			return (
				<div className="row">
					<div className="col-md-1"></div> 
					<div className="col-md-11"> 
						<input type="text" className="form-control imprimir vecinoId" placeholder={vecId} aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoDistancia" placeholder={vecDist} aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoDesde" placeholder={vecDesde} aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control imprimir vecinoHacia" placeholder={vecHacia} aria-describedby="basic-addon1"> </input>
					</div>
					
					<p>Fin VECINO</p>
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
	<Ciclovia data={data} />, document.getElementById('container')
	);