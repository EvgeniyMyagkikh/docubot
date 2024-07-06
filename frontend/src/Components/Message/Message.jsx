import "./message.css"
import avatar_bot from "../../assets/DocuBot.jpg"
import avatar_user from "../../assets/user.svg"
import ReactMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import dark from "react-syntax-highlighter/src/styles/hljs/dark.js";
const Message = (props) => {
    return (
        <>
            <div className="Message_wrapper">
                {/* eslint-disable-next-line react/prop-types */}
                <img className="Avatar" src={props.content.sender === "user" ? avatar_user : avatar_bot}  alt=""/>
                {/* eslint-disable-next-line react/prop-types */}
                <section className={props.content.sender === "user" ? "Message" : "Message Bot"}>
                    {/* eslint-disable-next-line react/prop-types,react/no-children-prop */}
                    <ReactMarkdown children={props.content.message} className={props.content.sender === "user" ? "MessageText" : "MessageText TextBot"} components={{
                        code({inline, className, children, ...props }) {
                            return !inline? (
                                <SyntaxHighlighter
                                    language={"python"}
                                    style={dark}
                                    {...props}
                                >{String(children).replace(/\n$/, "")}</SyntaxHighlighter>
                            ) : (
                                <code className={className} {...props}>
                                    {children}
                                </code>
                            );
                        }}}></ReactMarkdown>
                </section>
            </div>
        </>
    );}

export default Message;