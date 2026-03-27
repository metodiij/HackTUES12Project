const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

let commandQueue = [];

// Приема маршрута от картата
app.post("/save-path", (req, res) => {
    commandQueue = req.body; 
    console.log(`Получени са ${commandQueue.length} команди.`);
    res.send("OK");
});

// Роботът извиква това, за да вземе следващата команда
app.get("/get-command", (req, res) => {
    if (commandQueue.length > 0) {
        res.json(commandQueue.shift());
    } else {
        res.json({ action: "idle", time: 0 });
    }
});

app.listen(3000, () => console.log("Сървърът работи на http://localhost:3000"));