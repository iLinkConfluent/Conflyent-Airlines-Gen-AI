import React, { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import '../Css/ChatBody.css'
import Logo from '../Assets/Conflyent-Logo.png';
import Close from '../Assets/close.png';
import Send from '../Assets/SendMessageIcon.png';
import UserMsg from './UserMsg';
import BotMsg from './BotMsg';

import { io } from 'socket.io-client';
const socket = io(process.env.REACT_APP_SOCKET_SERVER_URL); //SocketUrl

export default function ChatBody(props) {
    const messagesEndRef = useRef(null)
    const [message, setMessage] = useState([])
    const [showMsg, setShowMsg] = useState([])
    const [inputDisable, setInputDisable] = useState(false)
    const [msgGenerate, setMsgGenerate] = useState(false)
    const [messageId, setMessageId] = useState(uuidv4());
    const [botStr, setBotStr] = useState('')
    const [showBotMsg, setShowBotMsg] = useState(false)

    useEffect(() => {
        socket.on('connect', () => {
            console.log("[CLIENT] Socket Connection Established")
        })

        //Data is coming from socket and stored in data variable
        socket.on('consume-message', (data) => {
            console.log(`[CLIENT CONSUMER] message: `, data)
            setInputDisable(true)

            const messageStreamIndex = showMsg.findIndex((msg) => msg.messageId === messageId);
            if (messageStreamIndex > -1) {
                const oldMsgs = [...showMsg];
                oldMsgs[messageStreamIndex].message += data.message;
                setBotStr(oldMsgs);
            } else {
                if (data.sender === false) {
                    setBotStr((prevNewStr) => prevNewStr + data.message);
                }
            }

            if (data.seq_complete === true) {
                setInputDisable(false);
                setShowBotMsg(true)
            }
        });
        return () => {
            socket.off('connect');
            socket.off('consume-message');
        }
    }, [message, showMsg, messageId])

    //To set User Message into onClick send Icon
    const sendMsg = () => {
        const userMessage = { message: message, sender: true }
        setShowMsg([...showMsg, userMessage])
        setMessage('')
        setMsgGenerate(true)
        setInputDisable(true)
        setMessageId(uuidv4());
        socket.emit('produce-message', JSON.stringify({ message: message, chat_history: showMsg }));
    }

    //Hit on Enter keyword it will be send message
    const handleEvent = (event) => {
        if (event.key === 'Enter') {
            if (message.length > 0)
                sendMsg()
        }
    }

    //Scroll to the bottom whenever a new message is added
    useEffect(() => {
        messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        console.log('show msg', showMsg)
    }, [showMsg]);

    //Data from Backend is showing into frontend
    useEffect(() => {
        console.log('bot msg', botStr)
        if (showBotMsg === true) {
            setMsgGenerate(false);
            const botResponse = { message: botStr, sender: false }
            setShowMsg([...showMsg, botResponse])
            setShowBotMsg(false)
            setBotStr('')

        }
    }, [showBotMsg, showMsg, botStr]);

    return (
        <>
            <div className='chatPage'>
                <div className='chatHeader'>
                    <div className='head'>
                        <img className='logo' src={Logo} alt="" />
                        <div className='closeDiv' onClick={() => props.close(false)}>
                            <img className='icon' src={Close} alt='' />
                        </div>
                    </div>
                </div>

                <div className='chatBody'>
                    <BotMsg msg="Hi Rachel Groberman, Welcome to conFLYent Airlines! How can I help you?" />
                    {
                        showMsg.map((data) => (
                            data.sender ? <UserMsg msg={data.message} /> : <BotMsg msg={data.message} />
                        ))
                    }

                    {
                        msgGenerate === true ? <BotMsg msg="ConFLYent is composing a message" isComposing={true} /> : null
                    }
                    <div ref={messagesEndRef} />
                </div>

                <div className='chatFooter'>
                    <div className='footer'>
                        <input className='inputMessage' type='text' placeholder='Ask Something...' value={message} onKeyDown={handleEvent} onChange={(e) => { setMessage(e.target.value) }} disabled={inputDisable} />
                        {
                        inputDisable ? null : message.length > 0 ?
                            <div className='sendMessageIcon' onClick={sendMsg}>
                                <img className='icon' src={Send} alt="" />
                            </div> : null
                        }
                    </div>
                </div>

            </div>
        </>
    )
}
