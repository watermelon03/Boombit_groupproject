import React ,{ useEffect, useState }from 'react'
import { CountdownCircleTimer } from "react-countdown-circle-timer";

// import { Document, Page,pdfjs } from 'react-pdf';
// pdfjs.GlobalWorkerOptions.workerSrc = 'pdf.worker.min.js';


function Game(props) {
  const [playing,setPlaying] = useState(true);

  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }


  const renderTime = ({ remainingTime }) => {
    if (remainingTime === 0) {
      return <div className="timer">Too lale...</div>;
    }
    return (
      <div className="timer">
        <div className="text">Remaining</div>
        <div className="value">{remainingTime}</div>
        <div className="text">seconds</div>
      </div>
    );
  };
  
  const handlePause =(e)=>{
    setPlaying(!playing)
  }

  return (
    <div>
      <h1>game componen with this parameter {props.username} {props.mode} {props.serial} </h1>
      <CountdownCircleTimer
          // isPlaying={playing}
          isPlaying={props.gamestate}
          duration={90}
          colors={["#004777", "#F7B801", "#A30000", "#A30000"]}
          colorsTime={[10, 6, 3, 0]}
          onComplete={() => ({ shouldRepeat: false, delay: 1 })}
        >
          {renderTime}
        </CountdownCircleTimer>
        <button onClick={handlePause}>PPPPPPPPPPPPP</button>


      {/* <div>
        <Document file="https://s3-ap-southeast-1.amazonaws.com/happay-local/HVP/BILL20198261213473719445688HP.pdf"
          onLoadSuccess={onDocumentLoadSuccess}>
          <Page pageNumber={pageNumber} />
        </Document>
        <p>
          Page {pageNumber} of {numPages}
        </p>
      </div> */}

    </div>
  )
}

export default Game