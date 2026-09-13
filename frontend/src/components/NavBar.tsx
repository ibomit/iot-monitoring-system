import { Link } from "react-router-dom";

function NavBar() {
    return <nav className="navbar">
        <div className="navbar-brand">
            <Link to="/">Movie App</Link>
        </div>
        <div className="navbar-links">
            <div>
                <Link to="/" className="nav-link">Home</Link>
            </div>
            <div>
                <Link to="/devices" className="nav-link">Devices</Link>
            </div>
        </div>
    </nav>
}

export default NavBar