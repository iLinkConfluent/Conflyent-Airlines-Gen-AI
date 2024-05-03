import React from 'react';
import Logo from '../Assets/Conflyent-Logo.png';
import '../Css/Navbar.css';
import UserIcon from '../Assets/UserIcon.png'

export default function Navbar() {
    return (

        <div className='container-fluid'>
            <div className='row'>
                <div className='col-12'>

                    <nav class="navbar navbar-expand-lg">
                        <img className='navbarLogo' src={Logo} alt='' />

                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>

                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul>
                                <li>Flights</li>
                                <li>About</li>
                                <li>Rachel<img className='user' src={UserIcon} alt='' /></li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
        </div>

    )
}