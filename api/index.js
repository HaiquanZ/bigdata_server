const express = require("express");
const app = express();
const cors = require("cors");
const RabbitMQ = require("./config/rabbitmq")
app.use(cors({origin: true, credentials: true}));
app.use(express.urlencoded({extended: true}));
app.use(express.json());

const port = 8082;

app.post('/api', async (req, res) => {
    //do some things
    const { text } = req.body;
    let result = await RabbitMQ.getInstance().callRpc(text);
    console.log(result);
    res.status(200).json({
        msg: 'success',
        data: result
    })
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});