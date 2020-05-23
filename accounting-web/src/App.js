import React from 'react';
import './App.css';
import Header from './components/layout/Header'
import {
  BrowserRouter as Router,
  Switch, Route
} from 'react-router-dom'

import EnterBonRouter from './components/pages/EnterBonRouter'
import Home from './components/pages/Home'
import ProductsRouter from './components/pages/ProductsRouter'
import DetailsBon from './components/pages/DetailsBon'


function App() {
  let apiUrl = "http://192.168.178.21:5000/api/"
  return (

    <Router>
      <Header />
      <div className="col-sm-10 offset-sm-1">
        <Switch>
          <Route path="/enterBon">
            <EnterBonRouter apiUrl={apiUrl} />
          </Route>
          <Route path="/bon/:purchaseId">
            <DetailsBon apiUrl={apiUrl} />
          </Route>


          <Route path="/products">
            <ProductsRouter apiUrl={apiUrl} />
          </Route>
          <Route exact path="/">
            <Home apiUrl={apiUrl} />
          </Route>
          <Route path="*">404 Not Found</Route>
        </Switch>
      </div>

    </Router >

  );
}

export default App;
