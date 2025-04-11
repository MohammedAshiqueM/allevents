import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SearchBar from './compontents/SearchBar'
import ArtistDetail from './compontents/ArtistDetail'

function App() {
    const [selectedArtist, setSelectedArtist] = useState(null);

    const handleArtistSelect = (artist) => {
      setSelectedArtist(artist);
    };

  return (
    <>
      <div className="app-container">
      <header className="app-header">
        <h1>Music Artist Search</h1>
        <p>Allevents machine task</p>
      </header>
      
      <main className="app-main">
        <SearchBar onArtistSelect={handleArtistSelect} />
        
        {selectedArtist ? (
          <ArtistDetail artist={selectedArtist} />
        ) : (
          <div className="welcome-message">
            <p>Type an artist name to get started</p>
          </div>
        )}
      </main>
      
    </div>
    </>
  )
}

export default App
