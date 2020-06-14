import React from 'react'
import { Link } from 'react-router-dom'

function Header() {
    return (<nav className="navbar navbar-expand-lg navbar-dark bg-primary">

        <Link to="/" className="navbar-brand">Die Abrechnung</Link>
        <Link to="/enterBon" className="btn btn-danger navbar-btn">Enter New Bon</Link>
        <button className="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
        </button>
        <div className="navbar-collapse collapse" id="navbarColor01">
            <ul className="navbar-nav mr-auto">
                <li className="nav-item" id="abrechnung"><Link to="/reckoning" className="nav-link">Abrechnung</Link></li>
                <li className="nav-item" id="stats"><Link to="/stats" className="nav-link">Stats</Link></li>
                <li className="nav-item" id="products"><Link to="/products" className="nav-link"> Products</Link></li>
            </ul>
        </div>
    </nav>)
}

export default Header