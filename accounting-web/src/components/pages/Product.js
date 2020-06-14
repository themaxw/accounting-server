import React, { Component } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function Product(props) {

    let { productName } = useParams()


    return (<ActuallyProduct productName={productName} apiUrl={props.apiUrl} />);

}

class ActuallyProduct extends Component {
    constructor(props) {
        super(props);
        this.state = {
            productName: props.productName,
            product: {},
            received: false

        }
    }
    componentDidMount = () => {
        axios.get(this.props.apiUrl + "products/" + this.props.productName)
            .then((resp) => { this.setState({ product: resp.data, received: true }) })
    }
    render() {
        if (!this.state.received) {
            return (
                <div>Waiting for data for {this.props.productName}</div>
            )
        }
        return (<div className="row">
            <div className="col-md-4">
                <div className="card border-primary mb-3">
                    <h3 className="card-header">Übersicht für {this.props.productName}</h3>
                    <div className="card-body">
                        <canvas id="productinfo" height="400px"></canvas>
                    </div>
                </div>
            </div>
            <div className="col-md-8">
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Price</th>
                            <th>Amount bought</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.product.map(product => {
                            return (
                                <React.Fragment key={product.productId}>
                                    <tr>
                                        <th>{product.shop}</th>
                                        <th>avg Price: {product.avg}</th>
                                        <th>total Price: {product.total}</th>
                                        <th></th>
                                    </tr>
                                    {
                                        product.items.map(item => {
                                            return (
                                                <tr key="{item.purchaseId}">
                                                    <td></td>
                                                    <td>{item.price}</td>
                                                    <td>{item.amount}</td>
                                                    <td>{item.purchaseId}</td>
                                                </tr>
                                            )
                                        })}
                                </React.Fragment>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </div >


        );
    }
}





export default Product;