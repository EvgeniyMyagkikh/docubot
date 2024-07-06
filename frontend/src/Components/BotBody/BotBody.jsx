import {useEffect, useRef, useState} from 'react';
import "./botbody.css"
import Message from "../Message/Message";
import axios from "axios";
import sendImg from "../../assets/send.svg"
import bot from "../../assets/bot.jpeg";

export const BotBody = () => {
    const [input, setInput] = useState("")
    const [typing, setTyping] = useState(0)
    const [messages, setMessages] = useState([{
            message: "Привет, меня зовут ДокуБот!",
            sender: "ДокуБот"
        }]
    )
    const chatRef = useRef()

    async function HandleSubmit(e) {
        e.preventDefault();
        if (input !== "" && input !== "``") {
            const newMessages = [...messages, {
                message: input,
                sender: "user"
            }]
            await setMessages(newMessages);
            await setInput("")

            const URL = import.meta.env.VITE_URL + encodeURIComponent(input);
            const VALUE = import.meta.env.VITE_HEADER_VALUE;

            await axios.get(URL, {
                    headers: new Headers({
                        "ngrok-skip-browser-warning": VALUE
                    })
                }
            ).then(response => {
                setTimeout(() => {
                    setMessages([...newMessages, {
                        message: response.data.result,
                        sender: "ДокуБот"
                    }])
                }, 1000);
            }).catch(
                function (error) {
                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                }
            )
            await setTyping(1)
            // Время в миллисекундах должно быть равно кол-ву секунд анимации TextTyping
            setTimeout(() => setTyping(0), 2000);
        }
    }

    async function InsertCodeBlock() {
        setInput(input + "``")
    }

    useEffect(() => {
        chatRef.current.scrollTop = chatRef.current.scrollHeight
    }, [messages, typing])

    return (
        <section>
            <h2 className="title">Задайте свой вопрос нашему боту-помощнику </h2>
            <div className="wrapper">
                <div className="bot_wrapper">
                    <div ref={chatRef} className="MessagesList">
                        {messages.map((message, i) => {
                            return <>
                                <Message key={i} content={message}/></>
                        })}
                    </div>
                    {/*<p className={typing ? "TextTyping" : "Hide"}>ДокуБот печатает...</p>*/}
                    <p className="TextTyping">ДокуБот печатает...</p>
                    <div className="FormWrapper">
                        <button onClick={InsertCodeBlock} className="CodeButton">``</button>
                        <form onSubmit={HandleSubmit}>
                        <textarea value={input} className={typing ? "TextInput" : "TextInput None"}
                                  placeholder="Введите Ваш вопрос..."
                                  onChange={(e) => setInput(e.target.value)}/>
                            <button type="submit" className="SubmitButton">
                                <img className="photo" src={sendImg} alt="" width="55"/>
                            </button>
                        </form>
                    </div>
                </div>
                <img className="bot" src={bot} height="200vh" style={{marginTop: "37vh"}} alt=""></img>
            </div>
        </section>
    );
}

export default BotBody;