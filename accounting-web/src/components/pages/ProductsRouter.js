import React, { Component } from 'react';
import { useRouteMatch, Switch, Route, useParams } from 'react-router-dom';
import Product from './Product'
import Products from './Products'

function ProductsRouter() {
    let { path, url } = useRouteMatch()
    let { productName } = useParams()

    return (<Switch>
        <Route exact path={path}>
            <Products url={url} />
        </Route>
        <Route path={`${path}/:productName`}>
            {console.log("reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", productName)}
            <Product productName={productName} />
        </Route>
    </Switch>)
}

export default ProductsRouter