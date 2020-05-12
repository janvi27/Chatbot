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

	app.post('/api/df_text_query', async (req,res) => {
		let responses = await chatbot.textQuery(req.body.text, req.body.parameters);		
		res.send(responses[0].queryResult);
	});

	app.post('/api/df_event_query', async (req,res) => {
		let responses = await chatbot.eventQuery(req.body.event, req.body.parameters);		
		res.send(responses[0].queryResult);
	});
	app.post('/api/whatsapp_query', async (req, res) =>{
		responses = await chatbot.textQuery(req.body.Body, req.body.parameters);
		console.log(req.body.To);
		twilio.sendMessage(String(req.body.From), String(req.body.To), responses[0].queryResult.fulfillmentText).then(result => {
				console.log(result);
			}).catch(error => {
				console.error("Error is: ", error);
			});
			res.writeHead(204);
	});
}

