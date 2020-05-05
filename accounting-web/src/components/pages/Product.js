import React, { Component } from 'react';
import { useParams } from 'react-router-dom';
function Product() {

    let { productName } = useParams()


    return (<h3>{productName}</h3>);

}



export default Product;