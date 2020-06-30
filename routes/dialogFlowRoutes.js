const chatbot = require('../chatbot/chatbot');
const config = require('../config/keys');
const twilio = require('../send_whatsapp');
const http = require('http');
const MessagingResponse = require('twilio').twiml.MessagingResponse;

const twilioAccountID = config.twilioAccountID;
const twilioAuthToken = config.twilioAuthToken;
const myPhoneNumber = config.myPhoneNumber;

const client = require('twilio')(twilioAccountID,twilioAuthToken);

module.exports = app => {

	app.get('/', (req,res) => {
		res.send('hi')
	});

	app.post('/api/detect_news', function(req, res) {
	var spawn = require('child_process').spawn;
	var sys = require('util');
	var label = spawn('python3', ['./LinearSVC-Nodejs.py', req.body.text]);
	//label.stdout.pipe(process.stdout);
	//label.stderr.pipe(process.stderr);
	label.stdout.on('data', (data) => {
		data = data.toString();
		const result = {"data": data};
		const obj = JSON.parse(JSON.stringify(result));
		res.json(obj);
	});
});

	app.post('/api/df_text_query', async (req,res) => {
		let responses = await chatbot.textQuery(req.body.text, req.body.parameters);	
		res.send(responses[0].queryResult);
	});

	app.post('/api/df_event_query', async (req,res) => {
		let responses = await chatbot.eventQuery(req.body.event, req.body.parameters);		
		res.send(responses[0].queryResult);
	});
	app.post('/api/whatsapp_query', async (req, res) =>{
		const messageType = require('../detect_message');
		const type = messageType.detectMessage(req.body);
		if (type === "text") {
			responses = await chatbot.textQuery(req.body.Body, req.body.parameters);
			console.log(req.body.To);
			twilio.sendMessage(String(req.body.From), String(req.body.To), responses[0].queryResult.fulfillmentText).then(result => {
					console.log(result);
				}).catch(error => {
					console.error("Error is: ", error);
				});
				res.writeHead(204);
		}
		else if (type === "news") {
			var spawn = require('child_process').spawn;
			var sys = require('util');
			var label = spawn('python3', ['./SVM-Model.py', req.body.Body]);
			label.stdout.pipe(process.stdout);
			label.stderr.pipe(process.stderr);
			label.stdout.on('data', (data) => {
				data = data.toString();
				const result = {"data": data};
				const obj = JSON.parse(JSON.stringify(result));
				console.log('Got result');
				console.log(obj.data);
				twilio.sendMessage(String(req.body.From), String(req.body.To), "The article is " + obj.data).then(result => {
					console.log('Twilio message sent: ' + result);
				}).catch(error => {
					console.error("Error is: ", error);
				});
				res.writeHead(204);
			});
		}
		else {
			var spawn = require('child_process').spawn;
		 	var sys = require('util');
		 	var image_text = spawn('python3', ['./Text-Detection-Nodejs.py', req.body.MediaUrl0]);
		 	image_text.stdout.pipe(process.stdout);
			image_text.stderr.pipe(process.stderr);
		 	image_text.stdout.on('data', (data) => {
		 		data = data.toString();
		 		const result = {"data": data};
		 		const obj = JSON.parse(JSON.stringify(result));
				twilio.sendMessage(String(req.body.From), String(req.body.To), "The detected text is: " + obj.data).then(result => {
					console.log(result);
				}).catch(error => {
					console.error("Error is: ", error);
				});
		 	});
			res.writeHead(204);
		}
	});
}

