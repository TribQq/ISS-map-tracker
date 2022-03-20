import {React, useState, useEffect} from 'react'
import ListItem from '../components/ListItem'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'


const NotePage = () => {
   let navigate = useNavigate();
   let {note_id} = useParams()
   note_id = {note_id}['note_id']

   let [note, setNote] = useState([])

   useEffect(()=>{
      getNote()
   }, [note_id])

   let getNote = async () =>{
      if (note_id==='note_create') return 
      let response = await fetch(`/api/note/${note_id}`)
      let data = await response.json()
      setNote(data)
   }


   let updadteNote = async () => {
      fetch(`/api/note/${note_id}/`, {
         method : "PUT",
         headers:{
            'Content-Type': 'application/json'
         },
         body: JSON.stringify(note)
      })
   }

   let deleteNote = async () => {
      await fetch(`/api/note/${note_id}/`, {
         method : 'DELETE',
         headers:{
            'Content-Type': 'application/json'
         }
      })
      navigate('../../')
   }

   let createNote = async () => {
      fetch(`/api/notes/`, {
         method : "POST",
         headers:{
            'Content-Type': 'application/json'
         },
         body:JSON.stringify(note) 
      })
      navigate('../../')
   }


   let handleSubmit = () =>{
      let len_note = 0;
      if (note.body) len_note = note.body.replace(/ /gi,'').replace(/\n/gi,'').length

      if (note_id !== 'note_create' && len_note === 0 ) deleteNote()
      else if (note_id !== 'note_create') updadteNote()
      else if (note_id === 'note_create' && len_note !== 0) createNote() 
      navigate('../../')
   }

   let myButton = (note_id) => {
      if (note_id !== 'note_create') {
         return <button onClick={deleteNote}> Delete </button>
      }else {
      return <button onClick={createNote}> Create </button>}
   }

   let handleChange = (value) => {
      setNote(note => ({ ...note, 'body': value }))
      console.log('Handle Change:', note)
  }

   return (
    <div>
       <div className='note'>
          <div className='note-header'>
               <h3>
                    <ArrowLeft onClick={handleSubmit} />
               </h3>
               {myButton(note_id)}
               
            </div>
            <textarea onChange={(e) => { handleChange(e.target.value) }} value={note.body}></textarea>
      
      </div>
    </div>
  )
}

export default NotePage

