import "./PersonalityInteraction.css"
import React, {useState, useEffect} from "react"
import { useParams, useHistory } from 'react-router-dom'
import PersonalityFigure from "./PersonalityFigure"
import axios from 'axios'
import Swal from 'sweetalert2'
import LoadingImage from '../loading.gif'

const PersonalityInteraction = () => {

    let {personality} = useParams()
    let history = useHistory()
    const [models, setModels] = useState([])
    const [ESr, setESr] = useState([])
    const [selectedModel, setSelectedModel] = useState("")
    const [selectedESr, setSelectedESr] = useState("")
    const [selectedFigure, setSelectedFigure] = useState({"name":"", "picture":""})
    const [messages, addMessage] = useState([<p className="ModelAnswer"><span>Hello! What would you like to know about {decodeURI(personality)}?</span></p>])
    const [userInput, setUserInput] = useState({"text":""})
    

    useEffect(() => {
        const Init = async () => {
            const response1 = await axios.get(`http://localhost:3000/api/models`)
            const response2 = await axios.get(`http://localhost:3000/api/indices`)
            const response3 = await axios.get(`http://localhost:3000/api/model`)
            const response4 = await axios.get(`http://localhost:3000/api/index`)
            const response5 = await axios.get(`http://localhost:3000/api/personality/${personality}`)

            setModels(response1.data.response.map((model, idx) => <option key={idx} value={model}>{model}</option>))
            setESr(response2.data.response.map((retrieval, idx) => <option key={idx} value={retrieval}>{retrieval}</option>))
            setSelectedModel(response3.data.response)
            setSelectedESr(response4.data.response)
            setSelectedFigure(response5.data.response)
        }
        Init()
    }, [personality])

    const changeModel = async (event) => {
        Swal.fire({
            title: 'Updating Model',
            text: 'Please Wait',
            imageUrl: LoadingImage,
            imageWidth: 200,
            imageHeight: 200,
            showCancelButton: false,
            showConfirmButton: false,
            allowEscapeKey: false,
            allowOutsideClick: false,
        });
        
        setSelectedModel(event.target.value)
        axios.put(`http://localhost:3000/api/model`, {"model": event.target.value})
        .then(response => {
            Swal.close()
            if('error' in response)
                Swal.fire({
                    title: 'Something went wrong',
                    icon: 'error',
                });

        })
    }

    const changeESRetrival = async (event) => {
        Swal.fire({
            title: 'Updating Index',
            text: 'Please Wait',
            imageUrl: LoadingImage,
            imageWidth: 200,
            imageHeight: 200,
            showCancelButton: false,
            showConfirmButton: false,
            allowEscapeKey: false,
            allowOutsideClick: false,
        });
        
        setSelectedESr(event.target.value)
        axios.put(`http://localhost:3000/api/index`, {"index": event.target.value})
        .then(response => {
            Swal.close()
            if('error' in response)
                Swal.fire({
                    title: 'Something went wrong',
                    icon: 'error',
                });
        })
    }

    const handleSend = () => {
        if (userInput["text"] !== "")
        {
            addMessage(oldMessages =>[<p className="UserQuestion"><span>{userInput["text"]}</span></p>, ...oldMessages])
            let question = userInput["text"]
            setUserInput({"text": ""})
            addMessage(oldMessages =>[<p className="ModelAnswer"><span>...</span></p>, ...oldMessages])
            axios.post(`http://localhost:3000/api/question`,{"question":question, "name":selectedFigure["name"], "index":selectedESr})
            .then(response => {
                addMessage(oldMessages => oldMessages.slice(1))
                addMessage(oldMessages =>[<p className="ModelAnswer"><span>{response.data.response}</span></p>, ...oldMessages])
            })
        }
    }
    return (
        <div id="Personality">
            <nav id="PersonalityNavigation">
                <div id="PersonalityMenu">
                    <h2>Questions About:</h2>
                    <PersonalityFigure name={selectedFigure["name"]} picture={selectedFigure["picture"]}/>
                </div>
                <div id="PersonalityConfigurations">
                    <h2>Configurations</h2>
                    <div id="PersonalityModel">
                        <label>Choose Model:</label>
                        <select onChange={changeModel} name="modelSelection"  value={selectedModel}>
                            {models}
                        </select>
                    </div>
                    <div id="PersonalityESRetrieval">
                        <label>Choose ES Retrieval Option:</label>
                        <select onChange={changeESRetrival} name="retreival_options" value={selectedESr}>
                            {ESr}
                        </select>
                    </div>
                </div>
                <button onClick={() => {history.goBack()}}>Go Back</button>
            </nav>
            <div id="PersonalityChat">
                <div id="ChatScreen">
                    <div id="ChatHistory">
                        {messages}
                    </div>
                    <div id="UserInputs">
                        <form onSubmit={e => { e.preventDefault(); handleSend();}}>
                            <input type="text" placeholder="Write Question" value={userInput["text"]}onChange={(event) => setUserInput(prevState => {return {...prevState, "text":event.target.value}})}></input>
                            <button type="button" onClick={handleSend}>Send</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PersonalityInteraction;