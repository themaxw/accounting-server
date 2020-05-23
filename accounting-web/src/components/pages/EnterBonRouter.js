import React from 'react';
import { useRouteMatch, Switch, Route } from 'react-router-dom';
import EnterBon from './EnterBon'
import EnterItem from './EnterItem'

function EnterBonRouter(props) {
    let { path, url } = useRouteMatch()


    return (<Switch>
        <Route exact path={path}>
            <EnterBon url={url} apiUrl={props.apiUrl} />
        </Route>
        <Route path={`${path}/:bonId`}>
            <EnterItem apiUrl={props.apiUrl} />
        </Route>
    </Switch>)
}

export default EnterBonRouter