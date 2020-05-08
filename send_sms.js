const accountSid = 'AC5fc241cde4594aab7638ad8ca6062e28';
const authToken = '4eceb4caecc570ef59af9074088c5431';
const client = require('twilio')(accountSid, authToken);

client.messages
	.create({
		body: 'Hello',
		from: '+12565634497',
		to: '+918921195608'
	})
	.then(message => console.log(message.sid));