import "./AddPersonality.css"
import React, {useState} from "react"
import { useHistory } from 'react-router-dom'
import axios from 'axios'
import Swal from "sweetalert2"
import LoadingImage from '../loading.gif'

const AddPersonality = () => {
    const [personality, setPersonality] = useState({url: ''})
    let history = useHistory()
    
    const handleSubmit =  async () =>{
        if(personality.url === '' || !personality.url.startsWith("https://en.wikipedia.org/wiki/") || personality.url.includes(' ')){
            Swal.fire({"icon": 'error', 'title':"Wikipedia URL isn't Valid"});
        }
        else{
            try {
                Swal.fire({
                    title: 'Adding Personality',
                    text: 'Please Wait',
                    imageUrl: LoadingImage,
                    imageWidth: 200,
                    imageHeight: 200,
                    showCancelButton: false,
                    showConfirmButton: false,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                });
                axios.post(`http://localhost:3000/api/personality`, personality)
                .then(response => {
                    if('error' in response.data)
                    {
                        Swal.close()
                        Swal.fire({
                            title: response.data.error,
                            icon: 'error',
                        });
                    }
                    else
                    {
                        
                        setTimeout( () => {Swal.close();history.goBack()}, 1000)
                    }
                })
            } catch(err){
                alert(`An Error Occured`)
            }
        }
    }

    return (
        <div onSubmit={e => { e.preventDefault(); handleSubmit();}} id="addPersonality">
            <form>
                <div>
                    <label>Add New Personality</label>
                    <input type="text" placeholder="URL to Personality Page on Wikipedia" onChange={(event) => setPersonality(prevState => {return {...prevState, url:event.target.value}})}></input>
                </div>
                <div id="buttons">
                    <button type="button" onClick={() => {history.goBack()}}>Go Back</button>
                    <button type="button" onClick={handleSubmit}>Add Personality</button>
                </div>
            </form>
        </div>
    )
}

export default AddPersonality