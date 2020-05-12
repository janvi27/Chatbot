const client = require('twilio')();

client.messages.create({
	from: 'whatsapp:+14155238886',
	to: 'whatsapp:+918921195608',
	body: 'Hello!'
}).then(message => console.log(message.sid));