import React, { useState, useEffect, } from 'react';
import '../Css/ChatComp.css';
import BotIcon from '../Assets/BotIcon.png'

export default function BotMsg(props) {

  const [dots, setDots] = useState('');

  //set animation for three dots
  useEffect(() => {

    if (props.isComposing === true) {
      const interval = setInterval(() => {
        setDots((prevDots) => {
          if (prevDots === '...') return '';
          return prevDots + '.';
        });
      }, 1000);

      return () => clearInterval(interval);
    }
    //eslint-disable-next-line
  }, []);

  // Some Words make bold and some sentence show ito proper
  const inputText = props.msg;
  const flightPattern = /Flight {1}([A-Za-z0-9]+)/g;
  const mealPattern = /(AVML|DBML|avml|dbml)/g;
  const italicizedText = /ConFLYent is composing a message/g;

  const formattedText = inputText
    .replace(flightPattern, '<strong>$&</strong>')
    .replace(mealPattern, '<strong>$&</strong>')
    .replace(/\n/g, '<br/>').replace(/ {2}/g, '&nbsp;&nbsp;')
    .replace(italicizedText, '<i>$&</i>')

  return (

    <div style={{ justifyContent: 'left', display: 'flex' }}>
      <div className='botMsg'>
        <div className='botImg'> <img src={BotIcon} width='30' height='30' alt='' /></div>
        <div style={{ paddingTop: '4px' }}><text dangerouslySetInnerHTML={{ __html: `${formattedText}${dots}` }} /></div>
      </div>
    </div>

  )
}
