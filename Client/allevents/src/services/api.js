import instance from './axios.js'

export const searchArtists = async (query)=>{
    try{
        const response = await instance.get('/artists/search/',{params: {q: query}})
        return response.data

    }catch(e){
        console.log(e)
        throw e
    }
}

export const getArtistById = async (id)=>{
    try{
        const response = await instance.get(`/artists/${id}/`)
        return response.data
    }catch(e){
        console.log(e)
        throw e
    }
}