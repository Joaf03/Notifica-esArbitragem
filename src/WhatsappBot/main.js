import wwebjs from "whatsapp-web.js"
import qrcode from "qrcode-terminal"
import fs from "fs"
import { exec } from "child_process"

const { Client, LocalAuth } = wwebjs;

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "bot_nomeacoes",
    })
});

client.once('ready', () => {
    console.log("Client is ready.");
}) 

client.on('qr', qr => {
    qrcode.generate(qr, {small: true})
})
 
client.on('message_create', async message => {
    let media;

    if (message.hasMedia) {
        media = await message.downloadMedia();

        if (media && media.mimetype == "application/pdf") {

            fs.writeFileSync(media.filename, media.data, { encoding: 'base64' });
            console.log(`PDF recebido e guardado: ${media.filename}`);

            exec(`python3 ../twilioTest.py ${media.filename}`, (error) => {
                if (error) {
                    console.error(`Error when running Python Twilio script: ${error.message}`);
                    return;
                }                
            });
        }
    }
    else {
        console.log("Message is not a pdf");
    }
})  
 
client.initialize();   