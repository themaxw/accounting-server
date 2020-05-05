import React from 'react';
import './App.css';
import Header from './components/layout/Header'
import {
  BrowserRouter as Router,
  Switch, Route
} from 'react-router-dom'

import EnterBon from './components/pages/EnterBon'
import Home from './components/pages/Home'
import ProductsRouter from './components/pages/ProductsRouter'

function App() {
  return (
    <Router>
      <Header />
      <Switch>
        <Route path="/enterBon">
          <EnterBon />
        </Route>


        <Route path="/products">
          <ProductsRouter />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="*">404 Not Found</Route>
      </Switch>

    </Router>
  );
}

export default App;
