var w;
var m_prPath;

function setProg(str){	
	m_prPath=str;
	console.debug("set m_prPath to " + m_prPath);
}
function startWorker() {
	console.debug("called startWorker()");
	if (typeof(Worker) !== "undefined") {
		if (typeof(w) == "undefined") {
			w = new Worker("./js/tt_prog_worker.js");
		}

		w.postMessage(m_prPath);


		w.onmessage = function(event) {
			if(event.data == "endPrgrm"){
				stopWorker();
			}
			
			else if(event.data.startsWith("Program Name:")){
				document.getElementById("prName").innerHTML = event.data;
			}
			else if(event.data.startsWith("Program Duration:")){
				document.getElementById("prDur").innerHTML = event.data;
			}
			else if(event.data){
				sendSth(event.data);				
							
			}					
		};
	} 
	else {
	document.getElementById("prName").innerHTML = "Sorry! No Web Worker support.";
	document.getElementById("prDur").innerHTML = "";
	}
}

function stopWorker() {
	console.debug("called stopWorker()");
	w.terminate();
	w = undefined;
}