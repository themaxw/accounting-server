import React, { Component } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function DetailsBonWrapper(props) {

    let { purchaseId } = useParams()
    return (<DetailsBon purchaseId={purchaseId} apiUrl={props.apiUrl} />);

}

class DetailsBon extends Component {
    state = {
        bon: {},
        bonReceived: false
    }
    componentDidMount = () => {
        axios.get(this.props.apiUrl + "bon/" + this.props.purchaseId).then((resp) => {
            this.setState({ bon: resp.data, bonReceived: true });
        })

    }
    render() {
        if (!this.state.bonReceived) return (<div></div>)
        return (<div >
            Einkauf { this.state.bon.purchaseId} am { this.state.bon.date} von {this.state.bon.buyer} über { this.state.bon.total} bei {this.state.bon.shop}.
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Price</th>
                        <th>Amount bought</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.bon.items.map((item) => {
                        return (
                            <tr key={item.itemId}>
                                <td><Link to={"/products/" + item.product.productName}>{item.product.productName}</Link></td>
                                <td><Link to={"/products/" + item.product.productName}>{item.price}</Link></td>
                                <td><Link to={"/products/" + item.product.productName}>{item.amount}</Link></td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>

        </div>);
    }
}


export default DetailsBonWrapper