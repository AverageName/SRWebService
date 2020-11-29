import React from "react";
import './App.css';
import ImageLoader from './ImageLoader.js'
import SwaggerUI from "swagger-ui-react";
import '../node_modules/swagger-ui/dist/swagger-ui.css';

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          docs: false
        }
      }

    // componentDidMount() {
    //     SwaggerUI({
    //         domNode: document.getElementById("api-data"),
    //         url: "http://127.0.0.1:5000/static/swagger_1.json/"
    //     })
    // }

    changeState = () => {
        this.setState({
            docs: !this.state.docs
        });
    }

    componentDidUpdate() {
        let button = document.getElementById("docButton");

        if (this.state.docs === true) {
            button.value = "Go back to SR";
        }
        else {
            button.value = "Go to API doc";
        }
        console.log(button);
        console.log(this.state.docs);
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <div className="select">
                        <input type="submit" value="Go to API doc" onClick={this.changeState} id="docButton" className="docButton"/>
                    </div>
                    {this.state.docs ? <SwaggerUI url="http://127.0.0.1:5000/static/swagger_1.json/" /> : <ImageLoader/>}
                </header>
            </div>
        );
    }
}
