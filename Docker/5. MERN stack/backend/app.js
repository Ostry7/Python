const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://mongo:27017/testdb";

const MessageSchema = new mongoose.Schema({
  text: String
});
const Message = mongoose.model("Message", MessageSchema);

mongoose.connect(MONGO_URI)
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error(err));

app.get("/messages", async (req, res) => {
  const messages = await Message.find();
  res.json(messages);
});

app.post("/messages", async (req, res) => {
  const newMessage = new Message({ text: req.body.text });
  await newMessage.save();
  res.json(newMessage);
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
