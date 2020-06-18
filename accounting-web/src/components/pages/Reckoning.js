import React, { Component } from 'react';
import axios from 'axios'
//import moment from 'moment-range';
import DateRangePicker from 'react-daterange-picker';

const stateDefinitions = {
    available: {
        color: null,
        label: "available"
    }
}

class Reckoning extends Component {
    state = {
        value: null,
        response: []
    }

    handleSelect = (range, states) => {
        this.setState({
            value: range,
            states: states
        })
        axios.get(this.props.apiUrl + "abrechnung", { params: { startDate: range.start.format("YYYY-MM-DD"), endDate: range.end.format("YYYY-MM-DD") } })
            .then((resp) => {
                this.setState({ response: resp.data })

            })
    }
    renderTimeFrame = () => {
        if (this.state.value) {
            return (
                <div>
                    {"Time range: "}
                    {this.state.value.start.format("YYYY-MM-DD")}
                    {" - "}
                    {this.state.value.end.format("YYYY-MM-DD")}
                </div>
            )
        } else {
            return (<div>Select a time range</div>)
        }
    }
    renderResponseTable = () => {

        return (
            <table className="table table-striped table-hover">
                <thead>
                    <tr>
                        <th></th>
                        <th>Total Money Spent</th>
                        <th>Difference From Median</th>
                        <th>Excluded Spendings (On Cornflakes)</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.response.map((value) => (
                        <tr key={value.person}>
                            <td>{value.person}</td>
                            <td>{value.paid}€</td>
                            <td>{value.diff}€</td>
                            <td>{value.excl}€</td>
                        </tr>))}
                </tbody>
            </table>)

    }

    render() {
        return (
            <div className="jumbotron row">
                <div className="col-sm-6">
                    <DateRangePicker
                        firstOfWeek={1}

                        numberOfCalendars={1}
                        selectionType="range"
                        stateDefinitions={stateDefinitions}
                        defaultState="available"
                        value={this.state.value}
                        onSelect={this.handleSelect}
                        singleDateRange={true}
                    />
                </div>
                <div className="col-sm-6">
                    {this.renderTimeFrame()}
                    {this.renderResponseTable()}
                </div>
            </div>
        );
    }
}

export default Reckoning;