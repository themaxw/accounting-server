import React, { Component } from 'react';
import Autocomplete from 'react-autocomplete'
import axios from 'axios'
import { Redirect } from 'react-router-dom'
import Cookies from 'universal-cookie'

const cookies = new Cookies()



class EnterBon extends Component {
    constructor(props) {
        super(props);
        let buyer = cookies.get('buyer');
        if (!buyer) {
            buyer = "Max"
        }
        this.state = {
            buyers: ["Max", "Martha"],
            autocompleteShops: [],
            shopValue: "",
            buyer: buyer,
            total: "",
            date: "",
            redirect: false,
            redirectUrl: ""


        }
    }
    componentDidMount = () => {
        axios.get(this.props.apiUrl + "auto/shops").then((resp) => this.setState({ autocompleteShops: resp.data }))
    }
    changeHandler = (event) => {
        let nam = event.target.name;
        let val = event.target.value;
        this.setState({ [nam]: val });
    }
    submitHandler = (event) => {
        event.preventDefault()
        axios.post(this.props.apiUrl + "bon", { shop: this.state.shopValue, buyer: this.state.buyer, total: this.state.total, date: this.state.date })
            .then((resp) => {
                cookies.set('buyer', this.state.buyer);
                this.setState({ redirectUrl: '/enterBon/' + resp.data.purchaseId, redirect: true })
            })
    }

    render() {
        if (this.state.redirect === true) {
            return <Redirect to={this.state.redirectUrl} />
        }
        return (
            <div className="jumbotron">
                <form className="form-horizontal" autoComplete="off" onSubmit={this.submitHandler}>

                    <legend>Enter Bon</legend>
                    <div className="col-sm-offset-2 col-sm-10">
                        <div className="form-group">

                            {this.state.buyers.map((buyer) => {

                                return (
                                    <div key={buyer} className="custom-control custom-radio">
                                        <input id={"buyer-" + buyer} className="custom-control-input" name="buyer" type="radio" value={buyer} checked={this.state.buyer === buyer} onChange={this.changeHandler} />
                                        <label htmlFor={"buyer-" + buyer} className="custom-control-label">{buyer}</label>
                                    </div>
                                )


                            })}
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="control-label col-sm-2" htmlFor="shop">Shop</label>
                        <div className="col-sm-3">
                            <Autocomplete
                                inputProps={{ id: "shop", name: "shop", className: "form-control", autoFocus: true, required: true }}

                                value={this.state.shopValue}
                                items={this.state.autocompleteShops}
                                getItemValue={(item => item)}
                                onChange={(event, value) => {
                                    this.setState({ shopValue: value })
                                }}
                                onSelect={value => this.setState({ shopValue: value })}
                                shouldItemRender={(item, value) => {
                                    return (

                                        item.toLowerCase().indexOf(value.toLowerCase()) !== -1 ||
                                        item.toLowerCase().indexOf(value.toLowerCase()) !== -1
                                    )
                                }}
                                selectOnBlur={true}
                                sortItems={(a, b, value) => {
                                    const aLower = a.toLowerCase()
                                    const bLower = b.toLowerCase()
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
                                        key={item}
                                    >{item}</div>
                                )}
                            />

                        </div>

                    </div>

                    <div className="form-group">
                        <label className="control-label col-sm-2" htmlFor="total">Total Price</label>
                        <div className="col-sm-3">
                            <input id="total" className="form-control" name="total" required type="text" onChange={this.changeHandler} />
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="control-label col-sm-2" htmlFor="date">Date</label>
                        <div className="col-sm-3">
                            <input className="form-control" id="date" name="date" type="date" onChange={this.changeHandler} />
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-3">
                            <input className="btn btn-primary" id="submit" name="submit" type="submit" value="Send" />
                        </div>
                    </div>


                </form>

            </div>
        );
    }
}

export default EnterBon;