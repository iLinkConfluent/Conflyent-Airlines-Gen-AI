const express = require("express");
var app = express();
var server = require("http").Server(app);
const cors = require('cors');
const io = require("socket.io")(server,{
    cors: {
        origin: "*"
    }
});
const port = 80;
const { Kafka, logLevel } = require('kafkajs');
require('dotenv').config({ path: 'properties.txt' })
const path = require('path');

// Define a static directory to serve files from
const staticDir = path.join(__dirname, './build');

// Use express.static middleware to serve static files
app.use(express.static(staticDir));
app.use(cors());
app.get('/', (req,res) =>{
    res.sendFile(path.join(__dirname , 'build', 'index.html'));
});

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

const kafka = new Kafka({
    clientId: 'chat-app',
    brokers: [`${process.env.CONFLUENT_KAFKA_CLUSTER_URL.replace('SASL_SSL://', '')}`],
    ssl: true,
    sasl: {
        mechanism: 'plain',
        username: `${process.env.CONFLUENT_KEY}`,
        password: `${process.env.CONFLUENT_SECRET_KEY}`
    },
    logLevel: logLevel.ERROR,
})

const producer = kafka.producer({
    logLevel: logLevel.ERROR,
    createPartitioner: (config) => {
        return ({ topic, partitionMetadata, message }) => {
            const socketId = JSON.parse(message.value.toString()).socket_id;
            console.log(`[PRODUCER] SocketId: ${socketId} | Hash: ${generateHashCode(socketId)} | Partition: ${generateHashCode(socketId) % partitionMetadata.length}`)
            return generateHashCode(socketId) % partitionMetadata.length;
        }
    },
});
const consumer = kafka.consumer({
    groupId: `cg-chat-${Math.random() * 1000}`,
    logLevel: logLevel.ERROR,
});

async function produceMessage({socketId, message}) {
    await producer.connect();
    const response = await producer.send({
        topic: 'Questions',
        messages: [{key: socketId, value: Buffer.from(message)}]
    })
    await producer.disconnect();
    return response;
}

async function runConsumer(cb) {
    await consumer.connect();
    await consumer.subscribe({ topics: ['Answers'] })
    await consumer.run({
        eachMessage: (data) => {
            console.log(`[CONSUMER] Partition: ${data.partition} | Offset: ${data.message.offset}`)
            cb(data)
        }
    })
}

runConsumer(async (data) => {
    const messagePayload = JSON.parse(data.message.value.toString())
    const fromSocket = messagePayload.socket_id;
    console.log(`[CONSUMER] Received Message Payload: ${JSON.stringify(messagePayload)}`)
    io.to(fromSocket).emit('consume-message', messagePayload);
})
io.disconnectSockets(); // Disconnect cached sockets from previous socket runtime
io.on('connection', (socket) => {
    console.log(`[SERVER] Client ${socket.id} Connected.`);
    socket.on('produce-message', async (msg) => {
        console.log(`[PRODUCER] Received Message: ${msg}`)
        msg = JSON.parse(msg);
        const payload = { message: msg.message, socket_id: socket.id, chat_history: msg.chat_history, timestamp: Date.now() }
        const response = await produceMessage({key: socket.id, message: JSON.stringify(payload)});
        console.log(`[PRODUCER] Kafka Response: ${JSON.stringify(response)}`)
    })

    socket.on('disconnect', () => {
        console.log(`[SERVER] Client ${socket.id} Disconnected.`);
        socket.disconnect();
    })
})
function generateHashCode(str) {
    let hash = 0;
    if (str.length === 0) {
        return hash;
    }
    for (let i = 0; i < str.length; i++) {
        let char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash);
}