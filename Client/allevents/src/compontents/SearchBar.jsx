import React, { useEffect, useRef, useState } from 'react'
import { getArtistById, searchArtists } from '../services/api'
import AutoSuggestions from './AutoSuggestions'

const SearchBar = ({ onArtistSelect }) => {
    const [query,setQuery] = useState('')
    const [loading,setLoading] = useState(false)
    const [suggestions,setSuggestions] = useState([])
    const [showSuggestions,setShowSuggestions] = useState(false)
    const searchTimeout = useRef(null)

    useEffect(()=>{
        if(query.length >= 2){
            setLoading(true)
            
            if(searchTimeout.current){
                clearTimeout(searchTimeout.current)
            }

            searchTimeout.current = setTimeout(async () => {
                try{
                    const result = await searchArtists(query)
                    console.log(result.suggestions)
                    setSuggestions(result.suggestions)
                    setShowSuggestions(true)
                }catch(e){
                    console.log(e)
                    setSuggestions([])
                }finally{
                    setLoading(false)
                }
            }, 500);
        }else{
            setSuggestions([])
            setShowSuggestions(false)
        }

        return ()=>{
            if(searchTimeout.current){
                clearTimeout(searchTimeout.current)
            }
        }
    },[query])

    const handleSuggestionClick = async (artist) => {
        console.log(">>>",artist.id)
        setQuery(artist.name)
        setShowSuggestions(false)
        
        setLoading(true)
        
        try {
            const fullArtistData = await getArtistById(artist.id)
            onArtistSelect(fullArtistData.data)
        } catch (error) {
            console.error("Error fetching artist details:", error)
            onArtistSelect(artist)
        } finally {
            setLoading(false)
        }
    }
    const handleInputChange  = (e)=>{
        setQuery(e.target.value)
    }
  return (
    <div className='search-container'>
      <div className='search-input-container'>
        <input
             type="text" 
             className="search-input" 
             placeholder='search for artists...'
             value={query}
             onChange={handleInputChange }
             onFocus={()=> query.length >= 2 && setShowSuggestions(true)}
        />
        {loading && <div>loading...</div>}
      </div>

      {showSuggestions && (
        <AutoSuggestions
            suggestions={suggestions}
            onSuggestionClick={handleSuggestionClick}
            searchQuery={query}
        />
      )}
    </div>
  )
}

export default SearchBar
