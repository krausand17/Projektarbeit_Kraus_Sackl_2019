var progObject;
var prPath = "";

onmessage = function(e){		
	prPath = "http://localhost:8080/resources/tt_progs/" + e.data + ".json";
	getProgram(prPath);			
}



function getProgram(prPath){
		progObject = new XMLHttpRequest(); 				
	progObject.open("GET",prPath);
	progObject.onreadystatechange = function(){
		if( progObject.readyState == 4 && progObject.status == 200){
			
			console.debug("progObject.responseText:\n" + progObject.responseText);
			
			readyProg(progObject.responseText)
		}
	};	
	progObject.overrideMimeType("application/json");			
	progObject.send(null);
}


function readyProg(raw){		
	prJson = JSON.parse(raw);
	var data;
	data = "Program Name: " + prJson.name;
	postMessage(data);
	data = "Program Duration: " + prJson.totalLength;
	postMessage(data);
	
	var cmds = [];
	prJson.params.forEach(function(element) {
		cmds.push(element);
		console.debug("element in cmds: " + element);
	});
	
	//var cmds = prJson.params;
	console.debug("cmds: " + cmds);
	
	var i = 0;
	
	startProg(i,cmds);
	/* while (i<cmds.length-1){
		console.debug("DONE THE THING IN THE LOOP");
		postMessage(toString(cmds[i]));
		//setTimeout(to_cb,cmds[i+1]);
		timeout(cmds[i+1]);
		i += 2;
	}	 */
}

function to_cb(){
	console.debug("sent cmd and slept");
	
	}	


function startProg(i, cmds){
  if(i < cmds.length-1){
    setTimeout(function(){
      i +=2;
	  console.debug("DONE THE THING IN THE RECURSION");
	  postMessage(cmds[i]);
      startProg(i, cmds);
    }, cmds[i+1]*1000);
  }
}


















