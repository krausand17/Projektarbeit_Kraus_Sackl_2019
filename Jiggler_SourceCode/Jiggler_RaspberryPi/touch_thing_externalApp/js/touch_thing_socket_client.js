var wsPath = 'ws://10.0.0.6:55555';
var ws;


function sendSth(data){
	ws.send(data);
}

function connectButton(){
	if(ws){
		quit();
		document.getElementById('conn').innerHTML = "Reconnect";
	}
	else {
		reconnect();		
	}
}

function reconnect(){
	ws = new WebSocket(wsPath);
	ws.onopen = function(){
		console.log("client connected");
		document.getElementById('h_conn').innerHTML = "Connected";		
		document.getElementById('h_conn').setAttribute("fill", "green");
		document.getElementById('conn').innerHTML = "Disconnect";		
	};
	
	ws.onclose = function(){
		console.log("client disconnected");
		document.getElementById('conn').innerHTML = "Connect";		
		document.getElementById('h_conn').innerHTML = "Disconnected";
		document.getElementById('h_conn').setAttribute("fill", "red");
		new Notification('Client Disconnected', {body: 'Connecton Terminated'});
		dev_power = 0;
		dev_speed = 0;
		dev_angle = 0;
		dev_dir = 0;
		adjustAllMeters();			
	};
	
	ws.onmessage = function(msg){
		console.log("client-message: " + msg.data);
		var obj = JSON.parse(msg.data);		
		dev_speed = obj.speed;
		dev_angle = obj.angle;
		if(obj.direction=="LEFT"){
			dev_dir = 0;
		}else{
			dev_dir = 1;
		}
		if(obj.power=="ON"){
			dev_power = 1;
		}else{
			dev_power = 0;
		}
		adjustAllMeters();		
	};
	console.log("ws: " + ws);
}

function quit(){
	//sendSth('quit');
	ws.close(1000, "bye");
	ws = "";
	console.log("ws empty, except: [" + ws + "]");
}