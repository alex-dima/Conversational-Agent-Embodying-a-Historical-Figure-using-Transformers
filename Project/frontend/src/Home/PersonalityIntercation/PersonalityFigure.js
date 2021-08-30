import "./PersonalityFigure.css"
import React from 'react'

const PersonalityFigure = (params) => {
    return (
        <div className="PersonalityCard">
            <h3>{params.name}</h3>
            <img src={params.picture} alt="Avatar"/>
        </div>
    )
}

export default PersonalityFigure;