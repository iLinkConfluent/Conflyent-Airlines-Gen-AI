import React, { useState } from 'react';
import ChatBody from './ChatBody';
import '../Css/Home.css';
import ChatLauncher from '../Assets/ChatLauncher.svg';
import Form from '../Assets/Form.png';
import Navbar from "./Navbar";
import Mileage from '../Assets/Mileage Plan.png'

export default function Home() {

    const [openChat, setOpenChat] = useState(false)

    const closeChat = (data) => {
        setOpenChat(data)
    }

    return (

        <>
            <div className='container-fluid'>
                <div className="row full-screen-row">
                    <div className="col-12 full-screen-content">
                        <div className='homeBgImg'>
                            <Navbar />
                            <div className='banner-text' >
                                <p className='text'>Reach for the horizon</p>
                            </div>
                        </div>
                        <div className='row'>
                            <div className='homeFooter col-12'>
                                <div className='floating-form-wrap'>
                                    <img className='floating-form' src={Form} alt='' />
                                </div>
                                <div className='row'>
                                    <div className='col-6'>
                                    </div>
                                    <div className='col-6'>
                                        <div className="row">
                                            <div className='footerText col-6'>
                                                <img className='mileageText-wrap' src={Mileage} alt="" />
                                            </div>
                                            <div className='col-5'>
                                                <img className='Launcher' src={ChatLauncher} onClick={() => setOpenChat(true)} alt='' />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className='chatWindow'>
                            {
                                openChat ? <ChatBody close={closeChat} /> : null
                            }
                        </div>
                    </div>
                </div>
            </div>
        </>

    )
}
