import "./Home.css"
import React, {useState, useEffect} from "react"
import { Link } from 'react-router-dom'
import Figure from "./Figure"
import axios from 'axios'
import Swal from 'sweetalert2'
import LoadingImage from './loading.gif'

const Home = () => {
    const [models, setModels] = useState([])
    const [ESr, setESr] = useState([])
    const [figures, setFigures] = useState([])
    const [selectedModel, setSelectedModel] = useState("")
    const [selectedESr, setSelectedESr] = useState("")

    useEffect(() => {
        const Init = async () => {
            const response1 = await axios.get(`http://localhost:3000/api/models`)
            const response2 = await axios.get(`http://localhost:3000/api/indices`)
            const response3 = await axios.get(`http://localhost:3000/api/finder`)
            const response4 = await axios.get(`http://localhost:3000/api/model`)
            const response5 = await axios.get(`http://localhost:3000/api/index`)

            setModels(response1.data.response.map((model, idx) => <option key={idx} value={model}>{model}</option>))
            setESr(response2.data.response.map((retrieval, idx) => <option key={idx} value={retrieval}>{retrieval}</option>))
            setFigures(response3.data.response.map((figure, idx) => <Figure key={idx} name={figure.name} picture={figure.picture}/>))
            setSelectedModel(response4.data.response)
            setSelectedESr(response5.data.response)
        }
        Init()
    }, [])

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

    return (
        <div id="content">
            <nav id="Configurations">
                <h2>Configurations</h2>
                <Link className="Box-3D" to="/add_figure">Add Historical Figure</Link>  
                <div id="model">
                    <label>Choose Model:</label>
                    <select onChange={changeModel} name="modelSelection"  value={selectedModel}>
                        {models}
                    </select>
                </div>
                <div id="ESRetrieval">
                    <label>Choose ES Retrieval Option:</label>
                    <select onChange={changeESRetrival} name="retreival_options" value={selectedESr}>
                        {ESr}
                    </select>
                </div>
            </nav>
            <nav id = "HistoricalFigures">
                <h2>Select Historical Figure</h2>
                <div id="HistoricalFiguresOptions">
                    {figures}
                </div>
            </nav>
        </div>
    )
}

export default Home;