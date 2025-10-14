import wwebjs from "whatsapp-web.js"
import qrcode from "qrcode-terminal"
import fs from "fs"
import { exec } from "child_process"
import express from "express"
import path from "path"

const { Client, LocalAuth } = wwebjs;

const client = new Client({
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    },
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

	    const pdf_path = path.join("/home/joao/RefereeNotifications/src/WhatsappBot", media.filename);
            fs.writeFileSync(pdf_path, media.data, { encoding: 'base64' });
            console.log(`PDF recebido e guardado: ${pdf_path}`);

            exec(`python3 /home/joao/RefereeNotifications/src/twilioTest.py ${pdf_path}`, { cwd: "/home/joao/RefereeNotifications/src" }, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error when running Python Twilio script: ${error.message}`);
                    return;
                }
                if (stdout) {
                    console.log('Python output:', stdout);
                }

                if (stderr) {
                    console.error('Python errors:', stderr);
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
    const date = new Date();
    const hour = date.getHours();
    let greeting = "";

    if (hour < 12) greeting = "Bom dia";
    else if (hour < 20) greeting = "Boa tarde";
    else greeting = "Boa noite";
    
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
        await client.sendMessage("120363279952337413@g.us", greeting);

        const message = createMessage(body.game);
        await client.sendMessage("120363279952337413@g.us", message);
        res.sendStatus(200);
    } catch (err) {
        console.error("Erro ao enviar mensagem:", err);
        res.sendStatus(500);
    }
});

app.listen(3000, () => console.log("Express server running on port 3000"));
