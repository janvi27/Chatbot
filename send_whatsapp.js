const client = require('twilio')(accountSid, authToken);

module.exports = {
	sendMessage: async function(to: string, from: string, body: string) => {
		return new Promise((resolve, reject) => {
			client.messages
				.create({
					to,
					from,
					body
				})
				.then(message => {
					resolve(message.sid);
				})
				.catch(error => {
					reject(error)
				});
		});
	}
}