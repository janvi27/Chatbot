const chatbot = require('../chatbot/chatbot')

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
		client.messages.create({
			from: 'whatsapp:+14155238886',
			to: 'whatsapp:'+process.env.MY_PHONE_NUMBER,
			body: "Hello!"
		})
	});
}

