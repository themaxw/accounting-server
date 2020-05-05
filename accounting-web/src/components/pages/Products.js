import React, { Component } from 'react';
import axios from 'axios'
import { Switch, Route, Link, useRouteMatch, useParams } from 'react-router-dom'
import Product from './Product'


class Products extends Component {
    constructor(props) {
        super(props);
        this.state = {
            products: []
        }
    }
    state = {}
    componentDidMount = () => {
        axios.get('http://127.0.0.1:5000/api/products')
            .then((response) => {
                this.setState({ products: response.data })
            })
    }
    render() {
        return (
            <table className="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Total</th>
                        <th>Amount Bought</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.products.map(product => {
                        return (

                            <tr key={product[0]}>

                                <td><Link to={`${this.props.url}/${product[0]}`}>{product[0]}</Link></td>
                                <td><Link to={`${this.props.url}/${product[0]}`}>{product[1]}</Link></td>
                                <td><Link to={`${this.props.url}/${product[0]}`}>{product[2]}</Link></td>

                            </tr>

                        )
                    })}
                </tbody>
            </table >
        );
    }
}

export default Products;