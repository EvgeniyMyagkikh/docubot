import logo from "../../assets/RuStoreLOGO.svg"
import bot from "../../assets/bot.jpeg"
import "./header.css"

export const Header = () => {
    return (
        <section className="Header">
            <img className="logo" src ={logo} alt=""></img>
        </section>
    );
}

export default Header;