const config = require('./config/keys');

const twilioAccountID = config.twilioAccountID;
const twilioAuthToken = config.twilioAuthToken;
const myPhoneNumber = config.myPhoneNumber;

const client = require('twilio')(twilioAccountID,twilioAuthToken);

module.exports = {
	sendMessage: async function(to, from, body) {
		return new Promise((resolve, reject) => {
			client.messages.create({
				to: to,
				from: from,
				body: body
			}).then(message => {
				resolve(message.sid);
			}).catch(error => {
				reject(error);
			});
		});
	}
}
	