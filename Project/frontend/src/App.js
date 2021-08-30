import "./App.css";
import React from "react";
import {BrowserRouter, Switch, Route} from "react-router-dom"
import Footer from "./Footer/Footer"
import Header from "./Header/Header"
import Home from "./Home/Home"
import AddPersonality from "./Home/AddPersonality/AddPersonality";
import PersonalityInteraction from "./Home/PersonalityIntercation/PersonalityInteraction";



const Layout = (props) => {
    return <div id="Layout">{props.children}</div>;
};

const App = () => {
    return (
        <Layout>
            <BrowserRouter basename="/">
            <Header />
                <Switch>
                    <Route path="/add_figure" component={AddPersonality}/>
                    <Route path="/:personality" component={PersonalityInteraction}/>
                    <Route path="/" component={Home}/>
                </Switch>
            </BrowserRouter>
            <Footer />
        </Layout>
    );
};

export default App;
