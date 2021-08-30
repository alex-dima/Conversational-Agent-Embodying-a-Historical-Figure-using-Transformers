import "./Figure.css"
import React from 'react'
import { Link } from 'react-router-dom'

const Figure = (params) => {
    return (
        <Link to={encodeURIComponent(params.name)} className="card">
            <img src={params.picture} alt="Avatar"/>
            <h3>{params.name}</h3>
        </Link>
    )
}

export default Figure;