module.exports = {
	detectMessage: function(text) {
		if (text.NumMedia !== "0") {
			console.log("Image");
			return "image";
		}
		else {
			if (text.Body.length < 30)  {
				console.log("Text");
				return "text";
			}
			else {
				console.log("News");
				return "news";
			}
		}
	},
	detectFake: function(message) {
		console.log("In detect_fake");
		var spawn = require('child_process').spawn;
		var sys = require('util');
		var label = spawn('python3', ['./LinearSVC-Nodejs.py', message]); 
		//label.stdout.pipe(process.stdout);
		//label.stderr.pipe(process.stderr);
		label.stdout.on('data', (data) => {
			data = data.toString();
			//console.log(data);
			const result = {"data": data};
			const obj = JSON.parse(JSON.stringify(result));
			console.log('Got result');
			console.log(obj.data);
			return obj.data;
		});
	},
	detectImage: function(url) {
		console.log(url);
		 var spawn = require('child_process').spawn;
		 var sys = require('util');
		 var image_text = spawn('python3', ['./Text-Detection-Nodejs.py', url]);
		 image_text.stdout.on('data', (data) => {
		 	data = data.toString();
		 	console.log(data);
		 	const result = {"data": data};
		 	const obj = JSON.parse(JSON.stringify(result));
		 	return obj.data;
		 });
	}
}