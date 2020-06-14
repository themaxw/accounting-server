import React, { Component } from 'react';
import axios from 'axios'
import { Link } from 'react-router-dom'



class Products extends Component {
    constructor(props) {
        super(props);
        this.state = {
            products: []
        }
    }
    state = {}
    componentDidMount = () => {
        axios.get(this.props.apiUrl + 'products')
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