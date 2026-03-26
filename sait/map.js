const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/save-path", (req, res) => {

  console.log("Получен маршрут:");
  console.log(req.body);

  res.send("OK");
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});