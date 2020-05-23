import React, { Component } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Autocomplete from 'react-autocomplete';

function EnterItemWrapper(props) {

    let { bonId } = useParams()


    return (<EnterItem bonId={bonId} apiUrl={props.apiUrl} />);

}

class EnterItem extends Component {
    constructor(props) {
        super(props);
        //this.itemInput = React.createRef();
        this.itemInput = null
        this.state = {
            autocompleteItems: [],
            productName: "",
            price: "",
            amount: "",
            bon: { items: [] },
            bonReceived: false
        }
    }

    componentDidMount = () => {
        axios.get(this.props.apiUrl + "bon/" + this.props.bonId).then((resp) => {
            this.setState({ bon: resp.data, bonReceived: true });
            axios.get(this.props.apiUrl + "auto/items/" + this.state.bon.shop).then((resp) => this.setState({ autocompleteItems: resp.data }))
        })

    }
    changeHandler = (event) => {
        let nam = event.target.name;
        let val = event.target.value;
        this.setState({ [nam]: val });
    }
    submitHandler = (event) => {
        event.preventDefault()
        let sendObject = { productName: this.state.productName, price: this.state.price, amount: this.state.amount === "" ? 1 : this.state.amount }
        axios.post(this.props.apiUrl + "bon/" + this.props.bonId, sendObject)
            .then((resp) => {

                this.setState({
                    bon: {
                        ...this.state.bon,
                        items: this.state.bon.items.concat(resp.data)
                    },
                    productName: "",
                    price: "",
                    amount: ""
                })
                this.itemInput.focus()
            }, (reason) => console.log(reason))
    }
    render() {
        if (!this.state.bonReceived) {
            return (<div></div>)
        }
        return (
            <div className="row">

                <div className="jumbotron col-sm-6">
                    <form className="form-horizontal" autoComplete="off" onSubmit={this.submitHandler}>
                        <legend>Enter Item</legend>
                        <div className="form-group">
                            <label className="control-label col-sm-5" htmlFor="productName">Product Name</label>
                            <div className="col-sm-8">
                                <Autocomplete
                                    inputProps={{ id: "productName", name: "productName", className: "form-control", autoFocus: true, required: true }}
                                    value={this.state.productName}
                                    items={this.state.autocompleteItems}
                                    getItemValue={(item) => item.productName}
                                    onChange={(event, value) => {
                                        this.setState({ productName: value })
                                    }}
                                    onSelect={(value, item) => {

                                        this.setState({ productName: item.productName })
                                        if (item.price) {
                                            this.setState({ price: "" + item.price })
                                        }
                                    }}
                                    shouldItemRender={(item, value) => {
                                        return (

                                            item.productName.toLowerCase().indexOf(value.toLowerCase()) !== -1 ||
                                            item.productName.toLowerCase().indexOf(value.toLowerCase()) !== -1
                                        )
                                    }}
                                    selectOnBlur={true}
                                    sortItems={(a, b, value) => {
                                        const aLower = a.productName.toLowerCase()
                                        const bLower = b.productName.toLowerCase()
                                        const valueLower = value.toLowerCase()
                                        const queryPosA = aLower.indexOf(valueLower)
                                        const queryPosB = bLower.indexOf(valueLower)
                                        if (queryPosA !== queryPosB) {
                                            return queryPosA - queryPosB
                                        }
                                        return aLower < bLower ? -1 : 1

                                    }}
                                    menuStyle={{}}
                                    renderMenu={children => (
                                        <div id="autocomplete-list" className="autocomplete-items col-sm-8">
                                            {children}
                                        </div>
                                    )}
                                    renderItem={(item, isHighlighted) => (
                                        <div
                                            className={`${isHighlighted ? 'autocomplete-active' : ''}`}
                                            key={"auto-" + item.productName}
                                        >{item.productName}</div>
                                    )}
                                    renderInput={(props) => {
                                        this.itemInput = props.ref
                                        return (
                                            <input {...props} ref={(itemInput) => {
                                                props.ref(itemInput);
                                                this.itemInput = itemInput
                                            }} />
                                        )
                                    }}
                                />

                            </div>
                        </div>
                        <div className="form-group">
                            <label className="control-label col-sm-5" htmlFor="price">Price</label>
                            <div className="col-sm-8">
                                <input id="price" name="price" required className="form-control" type="text" onChange={this.changeHandler} value={this.state.price} />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="control-label col-sm-5" htmlFor="amount">Amount</label>
                            <div className="col-sm-8">
                                <input id="amount" name="amount" className="form-control" type="text" onChange={this.changeHandler} value={this.state.amount} />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-sm-offset-2 col-sm-3">
                                <input className="btn btn-primary" id="submit" name="submit" type="submit" value="Send" />
                            </div>
                        </div>
                    </form>
                </div>
                <div className="col-sm-6">
                    <table className="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                                <th>Amount</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.bon.items.map((item => {
                                return (
                                    <tr key={item.itemId}>
                                        <td>{item.product.productName}</td>
                                        <td>{item.price}</td>
                                        <td>{item.amount}</td>
                                        <td><form onSubmit={(event) => {
                                            event.preventDefault()
                                            axios.delete(this.props.apiUrl + "bon/" + this.props.bonId + "/item/" + item.itemId).then((resp) => {
                                                console.log(this.props.apiUrl + "bon/" + this.props.bonId + "/item/" + item.itemId)
                                                this.setState({
                                                    bon: {
                                                        ...this.state.bon,
                                                        items: this.state.bon.items.filter((value) => value.itemId !== resp.data.itemId)
                                                    }
                                                })
                                            }
                                            )
                                        }} >
                                            <input className="btn btn-danger" type="submit" value="delete" />
                                        </form></td>
                                    </tr>)
                            }))}
                        </tbody>
                        <tfoot>
                            <tr>
                                <td>Total</td>
                                <td>{this.state.bon.items.reduce((value, item) => value = value + item.price * item.amount, 0)}/{this.state.bon.total}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div >);
    }
}

export default EnterItemWrapper;