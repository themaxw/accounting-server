import React from 'react';
import { useRouteMatch, Switch, Route } from 'react-router-dom';
import Product from './Product'
import Products from './Products'

function ProductsRouter(props) {
    let { path, url } = useRouteMatch()


    return (<Switch>
        <Route exact path={path}>
            <Products url={url} apiUrl={props.apiUrl} />
        </Route>
        <Route path={`${path}/:productName`}>
            <Product apiUrl={props.apiUrl} />
        </Route>
    </Switch>)
}

export default ProductsRouter