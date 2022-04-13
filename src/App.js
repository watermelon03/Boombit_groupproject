import React ,{ useEffect, useState }from 'react'
import { useForm } from 'react-hook-form';
import './App.css';
import { CountdownCircleTimer } from "react-countdown-circle-timer";
import axios from 'axios';
// import { Document, Page } from 'react-pdf';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import SinglePagePDFViewer from "./component/single-page";
import samplePDF from './boom_bit.pdf';
import ReactLoading from 'react-loading'

function App() {
  const { register,handleSubmit,formState: { errors } } = useForm();
  const [name,setUsername] = useState('')
  const [serial,setSerial] = useState('')
  const [gamestate,setGamestate] = useState('')  
  const [mode,setMode] = useState('') 
  const [isDisabled, setIsDisabled] = useState(false);
  const [time,setTime] = useState('') 
  const [end,setEnd] = useState() 
  const [loading,setLoading] = useState(false) 
  
  // const [numPages, setNumPages] = useState(null);
  // const [pageNumber, setPageNumber] = useState(1);

  // function onDocumentLoadSuccess({ numPages }) {
  //   setNumPages(numPages);
  // }

    
  const onSubmit = (e) =>{
    e.preventDefault();

    const block={name,serial,mode}
    setLoading(true)
    setIsDisabled(!isDisabled)
    setGamestate(true)

    // setEnd(1)
    // setLoading(false)
    // window.location.reload(false);
    fetch('http://localhost:5000/start_web', {
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(block),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });


    const temp_url1='http://localhost:5000/get_start/'
    const url=temp_url1+serial
    const myInterval = setInterval(fget, 1000);
    async function fget() {
      const response = await fetch(url);
      var ta = await response.json();
      console.log('play',ta[0].playing)
      if(ta[0].playing==1){
        setLoading(false)
        setGamestate(true)
        setTime(1)
        clearInterval(myInterval);
        
      } 
      else{
        // setEnd(1)
        // setLoading(false)
      }
    }
  // setEnd(1)
  }

  if(gamestate==1){
    const myInterval2 = setInterval(pollend, 1000);

    async function pollend() {
      const temp_url2='http://localhost:5000/get_record/'
      const end_url=temp_url2+serial

      const response = await fetch(end_url);
      var ta = await response.json();
      console.log('end',ta[0].result)
      // 0 lose
      if(ta[0].result==0){
        setGamestate(false)
        console.log('lose')
        //end 0 lose 
        setEnd(0)

      } 
      // 1 win stopwatch 
      if(ta[0].result==1){ 
    setLoading(false)
        setTime(0)
        console.log('win')
        //end 1 win 
        setEnd(1)
      }
      clearInterval(myInterval2);
    }
  }

  const renderTime = ({ remainingTime }) => {
    if (remainingTime === 0) {
      return <div className="timer">Too lale...</div>;
    }
    return (
      <div className="timer">
        <div className="text">Remaining</div>
        <div className="value">   : {remainingTime}</div>
        <div className="text">seconds</div>
      </div>
    );
  };
  


  return (
    <div className='APP'>

      <div className='top'>
        <h1>BOOM BIT</h1>
      </div>

      <div className='fieldInput'>
        <form className='field' onSubmit={onSubmit}>
          <input  className='textInput' type='text' 
          name='name' placeholder='your username' 
          disabled={isDisabled} 
          onChange={(e) => setUsername(e.target.value)}/>

          <input  className='textInput' type='text' 
          name='usernamee' placeholder='serial module' 
          disabled={isDisabled} 
          onChange={(e) => setSerial(e.target.value)}/>
          <div className='radio'>
            <input type="radio" name="mode" value='0'
            disabled={isDisabled}
            onChange={(e) => setMode(e.target.value)}/>Easy     
            <input type="radio" name="mode" value='1'
            disabled={isDisabled} 
            onChange={(e) => setMode(e.target.value)}/>Hard     
          </div>
          <div className='buuton'>
            <button className='btn' type='submit' disabled={isDisabled}  >GO!</button>
          </div>
        </form>
      </div>

      {loading && <ReactLoading className='loading' type={'bubbles'} color={'#3b70ac'} height={200} width={300} />}
      {gamestate  ? 
      <div className='game'>
        <div className='pdf'>
          <SinglePagePDFViewer pdf={samplePDF} />
        </div>
        <div className='time'>
          <CountdownCircleTimer
              isPlaying={time}
              duration={300}
              size={300}
              colors={["#004777", "#F7B801", "#A30000", "#A30000"]}
              colorsTime={[200, 100, 20, 0]}
              onComplete={() => ({ shouldRepeat: false, delay: 1 })}
            >
              {renderTime}
            </CountdownCircleTimer>
          </div> 
        </div>
      
        :
        <p></p>
      }
      {/* lose */}
      { end==0 ? 
      <div className='lose'>
        <button className='btn' onClick={(e) => window.location.reload(false) }>YOU LOSE</button>
      </div>
        :
        <p></p>
      }
      { end==1 ? 
      <div className='win'>
        <button className='btn' onClick={(e) => window.location.reload(false)}>YOU WIN</button>
      </div>
        :
        <p></p>
      }


   
    </div>
  );
}

export default App;