app.get('/detect-news', function(req, res) {
	var spawn = require("child_process").spawn;
	var process = spawn('python', ['./Neural-Networks-MLP-Nodejs.py', req.query.title, req.query.text]);

	process.stdout.on('data', function(data) {
		res.send(data.toString());
	})
})