import React, { Component } from 'react';
import axios from 'axios'
import { Link } from 'react-router-dom'

class Home extends Component {
    state = { bons: [] }
    componentDidMount() {

        axios.get('http://127.0.0.1:5000/api/bons')
            .then((response) => {
                this.setState({ bons: response.data })
            },
                (reason) => { console.log("rejected because of", reason); })
    }
    render() {
        return (
            <table className="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Buyer</th>
                        <th>Shop</th>
                        <th>Total</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.bons.map(bon => {
                        return (

                            <tr key={bon.purchaseId}>

                                <td><Link to={"/bon/" + bon.purchaseId}>{bon.buyer}</Link></td>
                                <td><Link to={"/bon/" + bon.purchaseId}>{bon.shop}</Link></td>
                                <td><Link to={"/bon/" + bon.purchaseId}>{bon.total}</Link></td>
                                <td><Link to={"/bon/" + bon.purchaseId}>{bon.date}</Link></td>

                            </tr>

                        )
                    })}
                </tbody>
            </table >
        );
    }
}

export default Home;