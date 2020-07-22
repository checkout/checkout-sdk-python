
import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  
{
  path: '/checkout-sdk-python/',
  component: ComponentCreator('/checkout-sdk-python/'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/__docusaurus/debug',
  component: ComponentCreator('/checkout-sdk-python/__docusaurus/debug'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog',
  component: ComponentCreator('/checkout-sdk-python/blog'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/2020/04/14/blog-plugin',
  component: ComponentCreator('/checkout-sdk-python/blog/2020/04/14/blog-plugin'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/2020/04/14/large-blog-post',
  component: ComponentCreator('/checkout-sdk-python/blog/2020/04/14/large-blog-post'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/hello-world',
  component: ComponentCreator('/checkout-sdk-python/blog/hello-world'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/hola',
  component: ComponentCreator('/checkout-sdk-python/blog/hola'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags',
  component: ComponentCreator('/checkout-sdk-python/blog/tags'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags/blog',
  component: ComponentCreator('/checkout-sdk-python/blog/tags/blog'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags/docusaurus',
  component: ComponentCreator('/checkout-sdk-python/blog/tags/docusaurus'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags/facebook',
  component: ComponentCreator('/checkout-sdk-python/blog/tags/facebook'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags/hello',
  component: ComponentCreator('/checkout-sdk-python/blog/tags/hello'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/tags/hola',
  component: ComponentCreator('/checkout-sdk-python/blog/tags/hola'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/blog/welcome',
  component: ComponentCreator('/checkout-sdk-python/blog/welcome'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python',
  component: ComponentCreator('/checkout-sdk-python'),
  
  routes: [
{
  path: '/checkout-sdk-python/errors',
  component: ComponentCreator('/checkout-sdk-python/errors'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/getting_started',
  component: ComponentCreator('/checkout-sdk-python/getting_started'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/initialize',
  component: ComponentCreator('/checkout-sdk-python/initialize'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/install',
  component: ComponentCreator('/checkout-sdk-python/install'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/logging',
  component: ComponentCreator('/checkout-sdk-python/logging'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/payments',
  component: ComponentCreator('/checkout-sdk-python/payments'),
  exact: true,
  
},
{
  path: '/checkout-sdk-python/testing',
  component: ComponentCreator('/checkout-sdk-python/testing'),
  exact: true,
  
}],
},
  
  {
    path: '*',
    component: ComponentCreator('*')
  }
];
