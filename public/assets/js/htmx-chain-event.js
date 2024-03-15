(function () {
  var htmxApi;//HtmxInternalApi

  function handleErrorEvent (eventName,error){
    console.log('==== Error Event:' + eventName + ' Error:' + error);
    // var nextEvent = document.createEvent('CustomEvent');
    // nextEvent.initCustomEvent(eventName, true, true, { message: error });
    const evt = new CustomEvent(eventName, { detail: { message: error } });
    window.dispatchEvent(evt);
  };
  
  function handleNextEvent (eventName){
    // var nextEvent = document.createEvent('CustomEvent');
    // nextEvent.initCustomEvent(eventName, true, true, { message: "Publish " + eventName });
    console.log('==== Next Event:' + eventName);
    const evt = new CustomEvent(eventName, { detail: { message: "Publish " + eventName } });
    window.dispatchEvent(evt);
  }
  htmx.defineExtension('chain-event', {
    init: function (apiRef) {
      htmxApi = apiRef;
      if (htmx.config.responseTargetUnsetsError === undefined) {
        htmx.config.responseTargetUnsetsError = true;
      }
      if (htmx.config.responseTargetSetsError === undefined) {
        htmx.config.responseTargetSetsError = false;
      }
      if (htmx.config.responseTargetPrefersExisting === undefined) {
        htmx.config.responseTargetPrefersExisting = false;
      }
      if (htmx.config.responseTargetPrefersRetargetHeader === undefined) {
        htmx.config.responseTargetPrefersRetargetHeader = true;
      }
    },
    onEvent: function (name, evt) {
      if (name === 'htmx:afterRequest' && evt.detail.xhr && evt.detail.xhr.status >= 200) {
        // handleNextEvent(evt);
        var value = evt.detail.elt.getAttribute('hx-publish') || "";
        var list = value.split(/[\s,]/);
        list.forEach((eventName)=>{
          handleNextEvent(eventName);
        });
        return true;
      }else if(name === 'htmx:responseError'){
        var value = evt.detail.elt.getAttribute('hx-publish-error') || "";
        var list = value.split(/[\s,]/);
        list.forEach((eventName)=>{
          handleErrorEvent(eventName,evt.detail.error);
        });
        return true;
      }
      
      return true;
    }
  });
})();
