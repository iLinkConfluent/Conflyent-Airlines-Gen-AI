import React from 'react';
import '../Css/ChatComp.css';
import UserIcon from '../Assets/UserIcon.png'

export default function UserMsg(props) {

  return (

    <div style={{ justifyContent: 'right', display: 'flex' }}>
      <div className='userMessage'>
        <div style={{ paddingTop: '4px' }}><text>{props.msg}</text></div>
        <div className='userImg'> <img src={UserIcon} width='30' height='30' alt='' /></div>
      </div>
    </div>

  )

}
