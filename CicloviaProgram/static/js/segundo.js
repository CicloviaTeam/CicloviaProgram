data = [];
original = "";
generar = 0;
numTracks = 0;
var Ciclovia = React.createClass({
	componentDidMount: function() {
		this.setState({horas:[],tracks: [], participantes: [], grupos: []});
	},
	handleFormSubmit: function (){
		alert($("#NombreCiudad").val());
	},
	getInitialState: function() {
		return {data: [], horas:[], tracks: [], participantes: [], grupos: []};
	},
	render: function(){
		return(
			<div>
					
				<div className="row">	
					<div className="col-md-4">
						<span className="input-group-addon">Nombre</span>
						<input type="text" id="name-form" className="form-control" placeholder="Nombre que recibe esta ciclovía" aria-describedby="basic-addon1"> </input>
					</div>
					
					<div className="col-md-4">
						<span className="input-group-addon">Lugar</span>
						<input type="text" id="place-form" className="form-control" placeholder="Lugar donde esta la ciclovía" aria-describedby="basic-addon1"> </input>
					</div>
					
					<div className="col-md-4">
						<span className="input-group-addon">Tramo de referencia</span>
						<input type="number" id="referenceTrack-form" className="form-control" placeholder="El tramo en donde se realizó la medición" aria-describedby="basic-addon1"> </input>
					</div>
					
				</div>

			<br/><br/>

			<div className="row">
				<div className="col-md-6" style={{border: "1px solid blue", padding: "20px"}}>
				
					<div className="input-group">
						<span className="input-group-addon">N&uacute;mero de tramos:</span>
						<input type="number" id="generar-tracks" className="form-control" placeholder="Número de tramos de la ciclovía" aria-describedby="basic-addon1"> </input>
					</div>
					
					<button type="button" className="btn btn-default" onClick={this.generarTracks}>Generar</button>			

					<Track tracks={this.state.tracks}> </Track>
				</div>

				<div className="col-md-6" style={{border: "1px solid blue", padding: "20px"}}>
					
					<div className="input-group">
						<span className="input-group-addon">N&uacute;mero de horas que funciona la ciclovía:</span>
						<input type="number" id="generar-horas" className="form-control" placeholder="Número de horas" aria-describedby="basic-addon1"> </input>
					</div>
					
					<button type="button" className="btn btn-default" onClick={this.generarHoras}>Generar</button>			

					<Hora horas={this.state.horas}> </Hora>
				</div>
			</div>

			<div className="row">
				<div className="col-md-6" style={{border: "1px solid blue", padding: "20px"}}>
					
					<div className="input-group">
						<span className="input-group-addon">N&uacute;mero de actividades:</span>
						<input type="number" id="generar-participantes" className="form-control" placeholder="Actividades (caminar, trotar, bicicleta, patines, etc.)" aria-describedby="basic-addon1"> </input>
					</div>
					
					<button type="button" className="btn btn-default" onClick={this.generarParticipantes}>Generar</button>			

					<Participante participantes={this.state.participantes}> </Participante>
				</div>

				<div className="col-md-6" style={{border: "1px solid blue", padding: "20px"}}>
					
					<div className="input-group">
						<span className="input-group-addon">N&uacute;mero de tiempos:</span>
						<input type="number" id="generar-grupos" className="form-control" placeholder="¿Cuantos tiempos diferentes había en la encuesta?" aria-describedby="basic-addon1"> </input>
					</div>
					
					<button type="button" className="btn btn-default" onClick={this.generarGrupos}>Generar</button>

					<Grupo grupos={this.state.grupos}> </Grupo>			
				</div>
			</div>
				<div className="">
					<button type="button" className="btn btn-default" onClick={this.imprimir}>Enviar</button>
				</div>
			</div>

		);
	},
	imprimir: function(){
		var toPrint = {};

		toPrint["name"] = $("#name-form").val();
		toPrint["place"] = $("#place-form").val();		
		toPrint["arrivalRate"] = $("#arrivalRate-form").val();
		toPrint["unitsTime"] = $("#unitsTime-form").val();
		toPrint["referenceTrack"] = $("#referenceTrack-form").val();
		toPrint["referenceHour"] = $("#referenceHour-form").val();

		toPrint["track"] = [];

		var tracks = $(".track");
		var t = {};

		$.each(tracks, function(index,track){
			if (index % 2 == 0){
				t["id"] = $(track).val();
			}
			else{
				t["proportion"] = $(track).val();
				toPrint["track"].push(t);
				t = {};
			}
		});

		toPrint["hour"] = [];
		var horas = $(".hora");
		var h = {};

		$.each(horas, function(index,hora){
			if (index % 2 == 0){
				h["time"] = $(hora).val();
			}else{
				h["proportion"] = $(hora).val();
				toPrint["hour"].push(h);
				h = {};
			}
		});

		toPrint["participantType"] = [];
		var participantes = $(".participante");
		var p = {};

		$.each(participantes, function(index,participante){
			if (index % 3 == 0){
				p["activity"] = $(participante).val();
			}else if(index % 3 == 1){
				p["velocity"] = $(participante).val();
			}else{
				p["percentage"] = $(participante).val();
				toPrint["participantType"].push(p);
				p = {};
			}
		});

		toPrint["timeInSystem"] = {};
		toPrint["timeInSystem"]["group"] = [];
		var grupos = $(".grupo");
		var g = {};

		$.each(grupos, function(index,grupo){
			if (index % 2 == 0){
				g["time"] = $(grupo).val();
			}else{
				g["percentage"] = $(grupo).val();
				toPrint["timeInSystem"]["group"].push(g);
				g = {};
			}
		});

		alert(JSON.stringify(toPrint));
	},
	generarGrupos: function(){
		console.log("GENERAR TRACKS");

		var cuantasTracks = $("#generar-grupos").val();
		numTracks = parseInt(cuantasTracks);

		var arr = [];

		for (var i = 0; i < numTracks; i++) {
			track = {};
			track["numero"] = i+1;
			arr.push(track);
		};

		this.setState({grupos: arr});

		console.log("generando tracks con arreglo: " + arr);
	},
	generarParticipantes: function(){
		console.log("GENERAR TRACKS");

		var cuantasTracks = $("#generar-participantes").val();
		numTracks = parseInt(cuantasTracks);

		var arr = [];

		for (var i = 0; i < numTracks; i++) {
			track = {};
			track["numero"] = i+1;
			arr.push(track);
		};

		this.setState({participantes: arr});

		console.log("generando tracks con arreglo: " + arr);
	},
	generarTracks: function(){
		console.log("GENERAR TRACKS");

		var cuantasTracks = $("#generar-tracks").val();
		numTracks = parseInt(cuantasTracks);

		var arr = [];

		for (var i = 0; i < numTracks; i++) {
			track = {};
			track["numero"] = i+1;
			arr.push(track);
		};

		this.setState({tracks: arr});

		console.log("generando tracks con arreglo: " + arr);
	},
	generarHoras: function(){
		console.log("GENERAR HORAS");

		var cuantasTracks = $("#generar-horas").val();
		numTracks = parseInt(cuantasTracks);

		var arr = [];

		for (var i = 0; i < numTracks; i++) {
			track = {};
			track["numero"] = i+1;
			arr.push(track);
		};

		this.setState({horas: arr});

		console.log("generando horas con arreglo: " + arr);
	}
});

var Track = React.createClass({
	render: function(){
		console.log(this.props);
		var tracks = this.props.tracks.map(function (track) {
			return (
				<div className="row">
					<h3>Track {track.numero}</h3>
					<div className="col-md-12"> 
						<input type="text" className="form-control track" placeholder="ID" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control track" placeholder="Proporcion" aria-describedby="basic-addon1"> </input>
					</div>
				</div>	
			);
		});
		return (
			<div>
				<h4>Tramos</h4>
				{tracks}
			</div>
		);
	}
});

var Hora = React.createClass({
	render: function(){
		console.log(this.props);
		var horas = this.props.horas.map(function (hora) {
			return (
				<div className="row">
					<h3>Hora {hora.numero}</h3>
					<div className="col-md-12"> 
						<input type="number" className="form-control hora" placeholder="Ingresar la hora en la que se contó (8 a.m., 10 a.m., etc)" aria-describedby="basic-addon1"> </input>
						<input type="number" className="form-control hora" placeholder="Número de personas que ingresaron" aria-describedby="basic-addon1"> </input>
					</div>
				</div>	
			);
		});
		return (
			<div>
				<h4>Horas</h4>
				{horas}
			</div>
		);
	}
});

var Participante = React.createClass({
	render: function(){
		console.log(this.props);
		var participantes = this.props.participantes.map(function (participante) {
			return (
				<div className="row">
					<h3>Actividad {participante.numero}</h3>
					<div className="col-md-12"> 
						<input type="text" className="form-control participante" placeholder="Nombre de la actividad" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control participante" placeholder="Velocidad media de la actividad (km/h)" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control participante" placeholder="Número de personas que se contaron haciendo la actividad" aria-describedby="basic-addon1"> </input>
					</div>
				</div>	
			);
		});
		return (
			<div>
				<h4>Actividades</h4>
				{participantes}
			</div>
		);
	}
});

var Grupo = React.createClass({
	render: function(){
		console.log(this.props);
		var grupos = this.props.grupos.map(function (grupo) {
			return (
				<div className="row">
					<h3>Tiempo {grupo.numero}</h3>
					<div className="col-md-12"> 
						<input type="number" className="form-control grupo" placeholder="Indique el tiempo en minutos (30 min, 60 min, 120 min, etc.)" aria-describedby="basic-addon1"> </input>
						<input type="text" className="form-control grupo" placeholder="Número de personas" aria-describedby="basic-addon1"> </input>
			
					</div>
				</div>	
			);
		});
		return (
			<div>
				<h4>Tiempos</h4>
				{grupos}
			</div>
		);
	}
});

React.render(
	<Ciclovia data={data} />, document.getElementById('container')
	);