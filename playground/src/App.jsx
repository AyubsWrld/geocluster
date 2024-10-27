import { useState } from 'react' ; 
import './App.css' ;
import View from './pages/View.jsx' ; 
import{
  APIProvider , 
  Map , 
  AdvancedMarker , 
  Pin , 
  InfoWindow
} from '@vis.gl/react-google-maps' ; 

function App() {

  return (
    <>
      <div style={{}}>
        <View/>
      </div>
    </>
  )
}

export default App
