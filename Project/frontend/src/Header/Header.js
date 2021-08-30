import "./Header.css"
import { Link } from 'react-router-dom'
import Logo from "./histofigures.png"

const Header = () => {
    return (
        <header id="title">
            <Link to="/"><img src={Logo} alt="Diploma Project Logo"/></Link>
            <h1>Conversational Agent Embodying a Historical Figure</h1>
        </header>
    )
}

export default Header;