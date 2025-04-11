import React from 'react';

const AutoSuggestions = ({ suggestions, onSuggestionClick, searchQuery }) => {
  if (!suggestions.length) {
    return (
      <div className="suggestions-container">
        <div className="no-suggestions">No artists found</div>
      </div>
    );
  }
  
  const highlightMatch = (text, query) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
  };
  
  return (
    <div className="suggestions-container">
      {suggestions.map(artist => (
        <div 
          key={artist.id}
          className="suggestion-item"
          onClick={() => onSuggestionClick(artist)}
        >
          <div className="suggestion-image">
          </div>
          <div className="suggestion-details">
            <div 
              className="suggestion-name"
              dangerouslySetInnerHTML={{ 
                __html: highlightMatch(artist.name, searchQuery) 
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export default AutoSuggestions;