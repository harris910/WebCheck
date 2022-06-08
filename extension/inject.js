var cookieGetter = document.__lookupGetter__("cookie").bind(document);
var cookieSetter = document.__lookupSetter__("cookie").bind(document);

var storageGetter = window.__lookupGetter__("localStorage").bind(window);
// var storageSetter = window.__lookupSetter__("localStorage").bind(window);

// const originalSetItem = localStorage.setItem;

// localStorage.setItem = function(key, value) {
//   const event = new Event('itemInserted');

//   event.value = value; // Optional..
//   event.key = key; // Optional..

//   document.dispatchEvent(event);

//   originalSetItem.apply(this, arguments);
// };

// const localStorageSetHandler = function(e) {
//   alert('localStorage.set("' + e.key + '", "' + e.value + '") was called');
// };

// document.addEventListener("itemInserted", localStorageSetHandler, false);

let originalFunction = window.Storage.prototype.setItem;
window.Storage.prototype.setItem = function(keyName, keyValue) {
    console.log(keyName);
    console.log(new Error().stack);
    originalFunction.apply(this, arguments);
    return;
}

//console.log(window.__lookupGetter__("localStorage"));
Object.defineProperty(document, 'cookie', {
    get: function() {
        var storedCookieStr = cookieGetter();
        // let data = '{"webpage":'+ window.location.href+',"function": getter,"cookie:"'+storedCookieStr+',"stack:"'+ new Error().stack +'}';
        // insertInfo(data);
        // console.log("here");
        fetch("http://localhost:3000/cookiestorage", {
        method: "POST", 
        body: JSON.stringify({"top_level_url": window.location.href,
        "function":"cookie_getter",
        "cookie:": storedCookieStr,
        "stack":new Error().stack}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("CookieStorage collected");
      }); 
        // console.log(storedCookieStr);
        // //console.trace();
        // console.log(new Error().stack);
    },

    set: function(cookieString) {
        fetch("http://localhost:3000/cookiestorage", {
        method: "POST", 
        body: JSON.stringify({"top_level_url": window.location.href,
        "function":"cookie_setter",
        "cookie:": cookieString,
        "stack":new Error().stack}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("CookieStorage collected");
      }); 
        // insertInfo(data);
        // console.log(cookieString);
    }
});

Object.defineProperty(window, 'localStorage', {
  get: function() {
        var storedStr = storageGetter();
        fetch("http://localhost:3000/cookiestorage", {
        method: "POST", 
        body: JSON.stringify({"top_level_url": window.location.href,
        "function":"indexdb_getter",
        "storage:": storedStr,
        "stack":new Error().stack}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("storage collected");
      });
    },

  set: function(storageString) {
        fetch("http://localhost:3000/cookiestorage", {
            method: "POST", 
            body: JSON.stringify({"top_level_url": window.location.href,
            "function":"indexdb_setter",
            "storage:": storageString,
            "stack":new Error().stack}),
            mode: 'cors',
            headers: {
              'Access-Control-Allow-Origin':'*',
              "Content-Type": "application/json"
            }
          }).then(res => {
            console.log("storage collected");
          });
    }
});