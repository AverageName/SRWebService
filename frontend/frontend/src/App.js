import React from "react";
import './App.css';
import ImageLoader from './ImageLoader.js'

export default class App extends React.Component {
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <ImageLoader/>
                </header>
            </div>
        );
    }
}
