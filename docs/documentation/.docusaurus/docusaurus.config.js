export default {
  "plugins": [
    "/Applications/MAMP/htdocs/CKO Files/CKO_Projects/docusaurus/python/node_modules/@docusaurus/plugin-google-analytics/src/index.js"
  ],
  "themes": [],
  "customFields": {},
  "themeConfig": {
    "navbar": {
      "title": "checkout-sdk-python",
      "logo": {
        "alt": "cko-dotnet",
        "src": "img/logo.png"
      },
      "links": [
        {
          "to": "https://docs.checkout.com/",
          "activeBasePath": "docs",
          "label": "Docs",
          "position": "right"
        },
        {
          "href": "https://github.com/checkout/checkout-sdk-python",
          "label": "GitHub",
          "position": "right"
        }
      ]
    },
    "footer": {
      "style": "dark",
      "copyright": "© 2020 Checkout.com    "
    },
    "googleAnalytics": {
      "trackingID": "UA-165971486-1"
    }
  },
  "title": "checkout-sdk-python",
  "tagline": "Checkout.com SDK for Python",
  "url": "https://checkout.github.io",
  "baseUrl": "/checkout-sdk-python/",
  "favicon": "img/favicon.png",
  "organizationName": "checkout",
  "projectName": "checkout-sdk-python",
  "scripts": [
    "https://embed.runkit.com"
  ],
  "presets": [
    [
      "@docusaurus/preset-classic",
      {
        "docs": {
          "sidebarPath": "/Applications/MAMP/htdocs/CKO Files/CKO_Projects/docusaurus/python/sidebars.js",
          "routeBasePath": ""
        },
        "theme": {
          "customCss": "/Applications/MAMP/htdocs/CKO Files/CKO_Projects/docusaurus/python/src/css/custom.css"
        }
      }
    ]
  ]
};