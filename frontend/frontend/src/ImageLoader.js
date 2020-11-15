import './ImageLoader.css';
import React from "react";

export default class ImageLoader extends React.Component {
    constructor(props) {
        super(props);
        this.setState({
            image: null,
        });
    }

    toDataUrl(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
            var reader = new FileReader();
            reader.onloadend = function() {
                callback(reader.result);
            }
            reader.readAsDataURL(xhr.response);
        };
        xhr.open('GET', url);
        xhr.responseType = 'blob';
        xhr.send();
    }

    loadFile = (event) => {
        let reader = new FileReader();
        let output = document.getElementById('output');
        // this.setState = {
        //     image: event.target.files[0]
        // };
        reader.onloadend = () => {
            //console.log(reader.result);
            // this.setState(state => ({...state, image: reader.result}));
            // console.log(this.state.image)
            this.setState({image: reader.result});
        }
        reader.readAsDataURL(event.target.files[0]);
        // console.log(this.state);
        console.log(event.target.files[0]);
        console.log(typeof(event.target.files[0]));
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
          URL.revokeObjectURL(output.src) // free memory
        }
    };

    sendData = async (event) => {
        const apiUrl = "http://172.18.0.1:5000/add";
        // var reader = new FileReader();
        console.log(this.state.image);
        const response = await fetch(apiUrl, {
            method: "POST",
            body: JSON.stringify({
                photo: this.state.image
            }),
            headers: {
                'Access-Control-Allow-Origin': 'http://172.18.0.1:5000'
            }
            })

        // console.log(response);

        const jsonResponse = await response.json();

        console.log(jsonResponse.id);

        const nnApiUrl = "http://172.18.0.1:5000/use_nn?id=" + jsonResponse.id;

        const nnResponse = await fetch(nnApiUrl, {
            method: "GET",
            headers: {
                'Access-Control-Allow-Origin': 'http://172.18.0.1:5000'
            }
        });

        const nnJsonResponse = await nnResponse.json();

        console.log(nnJsonResponse);

        document.getElementById('result')
            .setAttribute(
                'src', 'data:image/jpg;base64,' + nnJsonResponse.img);

        console.log('data:image/png;base64,' + nnJsonResponse.img)
        //let output = document.getElementById('output');
        //console.log(this.state.image);
        //data = this.toDataUrl(output.src, )
        // let can = document.getElementById('imgCanvas');
        // can.style.width = 0;
        // can.style.height = 0;
        // //can.style.visibility = "hidden";
        // let ctx = can.getContext("2d");
        // ctx.drawImage(output, 0, 0)
        //console.log(output.src);
        // console.log(can.toDataURL());

        // console.log(typeof(output.src));
        // reader.readAsDataURL(output.src);

    };

    render() {
        return (
            <div className="ImageLoader">
                    <input type='file' name="photo" className="uploadImage" accept="image/*" onChange={this.loadFile}/>
                    <img id="output"/>
                    <input type="submit" value="Send" onClick={this.sendData}/>
                    <img id="result"/>
            </div>
        );
    }
}
