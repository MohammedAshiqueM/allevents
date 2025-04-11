import React from 'react';

const BaseUrl = import.meta.env.VITE_BASE_URL

const ArtistDetail = ({ artist }) => {
    console.log("????",artist)
  return (
    <div className="artist-detail">
      <div className="artist-header">
        <div className="artist-image">
          {artist.profile_url ? (
            <img src={`${BaseUrl}${artist.profile_url}`} alt={artist.name} />
          ) : (
            <div className="placeholder-image">
              {artist.name.charAt(0).toUpperCase()}
            </div>
          )}
        </div>
        
        <div className="artist-info">
          <h2 className="artist-name">{artist.name}</h2>
          <p><strong> Location: </strong>
          {artist.location ? <span className="artist-location">{artist.location}</span>:'N/A'}</p>
            
          <div className="artist-meta">
              <strong>Genre:&nbsp;</strong>
                {artist.gentre.length > 0 ? (
                    <span className="artist-genre">
                    {artist.gentre.map((genre) => genre.name).join(", ")}
                    </span>
                ):'N/A'}
           <br />
           </div>
        </div>
      </div>
    </div>
  );
};

export default ArtistDetail;