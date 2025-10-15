# 🏑 RefereeNotifications

## Context and Goal

**RefereeNotifications** is a project developed to automate the **notification of referee assignments in hockey games**.  
The goal is to simplify and automate communication and game management by allowing referees to receive **automatic alerts** via **phone calls**, when there are **games without referee assigned**. If they accept the game through phone call number input, an automatic **WhatsApp** message is sent to confirm their availability.

This system helps reduces communication delays, making the process faster, more efficient, and more reliable.

---

## What the Project Solves

- Can read and process **PDF files** containing referee assignments.
- Automatically checks **referee game assignments**.
- Notifies the user when **there are games with no assignment**.
- Makes **automated phone calls** using **Twilio**.
- Sends **automatic WhatsApp messages**.

---

## Motivation

Since i started refereeing hockey games I noticed a big fault in the space: every weekend there was at least 1 hockey game without referee assigned (either because of unavailability of the intial referee assigned or simply lack of referees). Sometimes a referee volunteered to referee that game, but sometimes the game would happen without referee.
So I thought about the following: what if I built a system that would notify me when there was an unassigned game and, if I was available, a message was sent automatically, informing my availability, before anyone else even opened the pdf to check if there was an unassigned game?

## How it works

1. A pdf is sent by the president to the referees group chat where the games for the week are assigned to specific referees.
2. If there is at least 1 game without a referee assigned, I get a call (from a phone number provided by Twilio) informing me of the game(s) without referee.
3. The automated voice lists the game(s) and, depending on my availability, I press "1" to accept the game (an automatic message is sent to the group chat informing my availability to referee that game) and "0" to reject it (it just skips to the next game if there is one, otherwise the call ends).

## Technologies Used

### Languages
- **Python** — for data processing and Twilio integration.  
- **JavaScript (Node.js)** — for WhatsApp automation using *whatsapp-web.js*.

### Frameworks and Libraries
- **FastAPI** — main backend API built in Python (used to manage the Twilio phone call).  
- **Express.js** — web server framework for Node.js applications (containes the message sending logic).  
- **whatsapp-web.js** — automation of WhatsApp messages.  
- **Twilio API** — automatic calls and message alerts.  
- **requests**, **json** — communication between services and data handling.  
- **qrcode-terminal** — QR code generation for WhatsApp authentication.  
- **child_process** — to run Python scripts from Node.js.
- **pdfplumber** — for extracting and parsing data from PDF files.
---

## Future Improvements
- Web interface for game assignment management.  
- Database for storing game and alert history.  

---

## Author
Developed by **João Afonso Santos** — a personal automation project for hockey referees.
