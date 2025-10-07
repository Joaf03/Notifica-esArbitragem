import { Client } from "whatsapp-web.js"
import qrcode from "qrcode-terminal"

const client = new Client();

client.once('ready', () => {
    console.log("Client is ready.");
})

client.on('qr', (qr) => {
    console.log("QR Code received", qr);
})

client.initialize();