# ZMP Console Shell Service

## Requirements

### Functional Requirements

- Login & Auth Management
  - Backend \
    . Check Login Session. Redirect when non-privileged session \
    . After login, redirect previous url reqeusted \
    . Login based on Keycloak \
    . Fetch Role and RBAC
  - Fronend \
    . Login view \
    . ID/Password finder view \
    . Register view
- User Profile Service \
  - Backend \
    . Fetch User's information \
    . Fetch notifications \
    . CRUD for user's information
  - Frontend \
    . Profile View \
    . Change basic information view \
    . Show instant notification and show badge \
    . View of notification list
- GNB Service
  - Backend \
    . Load product menu information \
    . Serve aligned with Role
  - Frontend \ 
    . Show breadcumbs \
    . Show menus
- LNB Service
  - Backend \
    . Load features menu information \
    . Serve aligned with Role
  - Frontend \ 
    . Show menus 
- Alarm Service




### Spec for Service Link

```json
"serviceLinks":[
        {
            "appID": "home",
            "name": "home",
            "title": "ZMP",
            "href": "/",
            "type": "htmx",
            "permission": ["all"]
        },
        {
            "appID": "k8s",
            "name": "node-explorer",
            "title": "K8S-Infra",
            "href": "/cluster/node",
            "type": "htmx",
            "permission": ["all"]
        }
        
    ]
```
``` html
<vue-loader id="app" data-message={remoteURL}>
  hello
</vue-loader>

<script>
  class VueLoader extends HTMLElement {
    constructor() {
      super();
      console.log('AstroGreet constructed');
      // Read the message from the data attribute.
      // const message = this.dataset.message;
      console.log('AstroGreet remoteURL', this.dataset.message);
      // import('http://localhost:9002/src/main.js').then((module) => {
      //   const setup = module.default;
      //   setup('todos');
      // });
      const script = document.createElement('script');
      script.type = 'module';
      script.textContent = `
        import('${this.dataset.message}').then((module) => {
          const setup = module.default;
          console.log('AstroGreet module', JSON.stringify(module));
          console.log('AstroGreet setup !!');
          setup('todos');
        });
      `;
      // script.src = 'http://localhost:9002/src/main.js';
      document.body.appendChild(script); // Appending to the body

    }
  }
  customElements.define('vue-loader', VueLoader);
</script>
```

 // need to know
    - remote application address to call by reverse proxy
    - type of remote app : htmx/vue/react to select component loader
      each component loader is different code