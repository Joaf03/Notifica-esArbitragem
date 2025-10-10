import wwebjs from "whatsapp-web.js"
import qrcode from "qrcode-terminal"
import fs from "fs"
import { exec } from "child_process"
import express from "express"

const { Client, LocalAuth } = wwebjs;

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "bot_nomeacoes",
        dataPath: "./.wwebjs_auth"
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

const app = express();

app.use(express.json())

function createGreeting() {
    const date = Date();
    let greeting = "";

    if (date < 12) greeting = "Bom dia.";
    else if (date < 20) greeting = "Boa tarde.";
    else greeting = "Boa noite.";
    
    return greeting;
}

function createMessage(game) {
    const regex = /\p{L}+/u;
    const day_of_the_week = game["data"].match(regex)[0];
    // dizemos "na" segunda-feira mas dizemos "no" sábado
    const artigo_definido = (day_of_the_week == "sábado" || day_of_the_week == "domingo") ? "o" : "a";
    const message = `Tenho disponibilidade para realizar o jogo ${game["equipas_e_pavilhão"]} n${artigo_definido} ${day_of_the_week} às ${game["hora"]}`;

    return message;
}

app.post("/send-message", async (req, res) => {
    const body = req.body;
    try {
        const greeting = createGreeting();
        await client.sendMessage("351911841631@c.us", greeting);
        console.log("GREETING SENT");

        const message = createMessage(body.game);
        await client.sendMessage("351911841631@c.us", message);
        res.sendStatus(200);
    } catch (err) {
        console.error("Erro ao enviar mensagem:", err);
        res.sendStatus(500);
    }
});

app.listen(3000, () => console.log("Express server running on port 3000"));