import React from 'react'
import { Link } from 'react-router-dom'



let getDateUpd = (note) => {
  return new Date(note.updated_at).toLocaleDateString()
}

let getTitle = (note) => {
  let title = note.body.split('\n')[0]
  if(title.length > 30) return title.slice(0,30)  
  return title
}

let customizeTitle = (text) => {
  if (text.length===30) return text+'...'
  return text
}

let getContent = (note) => {
  let title = getTitle(note)
  let content = note.body.replaceAll('\n', ' ')
  content = content.replaceAll(title, '')
  if (content.length > 30){
    return content.slice(0,30) + '...'
  }else{
    return content
  }
}



function ListItem({note}) {
  return (
    <Link to={`/note/${note.id}`}>
      <div className='notes-list-item'>
        <h3>{customizeTitle(getTitle(note))}</h3>
        <p>
          <span>{getDateUpd(note)}</span>
          {getContent(note)}
        </p>
      </div>
    </Link> 
    
  )
}

export default ListItem