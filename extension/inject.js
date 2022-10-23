var cookieGetter = document.__lookupGetter__("cookie").bind(document);
var cookieSetter = document.__lookupSetter__("cookie").bind(document);

let originalFunction = window.Storage.prototype.setItem;
window.Storage.prototype.setItem = function(keyName, keyValue) {
    fetch("http://localhost:3000/cookiestorage", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "function": "storage_setter",
            "storage": {
                "keyName": keyName,
                "keyValue": keyValue
            },
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("Localstorage collected");
    });
    originalFunction.apply(this, arguments);
    return;
}

let originalFunction2 = window.Storage.prototype.getItem;
window.Storage.prototype.getItem = function(keyName) {
    fetch("http://localhost:3000/cookiestorage", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "function": "storage_getter",
            "storage": {
                keyName
            },
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("Localstorage collected");
    });
    originalFunction2.apply(this, arguments);
    return;
}


Object.defineProperty(document, 'cookie', {
    get: function() {
        var storedCookieStr = cookieGetter();
        fetch("http://localhost:3000/cookiestorage", {
            method: "POST",
            body: JSON.stringify({
                "top_level_url": window.location.href,
                "function": "cookie_getter",
                "cookie": storedCookieStr,
                "stack": new Error().stack
            }),
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*',
                "Content-Type": "application/json"
            }
        }).then(res => {
            console.log("CookieStorage collected");
        });
    },

    set: function(cookieString) {
        fetch("http://localhost:3000/cookiestorage", {
            method: "POST",
            body: JSON.stringify({
                "top_level_url": window.location.href,
                "function": "cookie_setter",
                "cookie": cookieString,
                "stack": new Error().stack
            }),
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*',
                "Content-Type": "application/json"
            }
        }).then(res => {
            console.log("CookieStorage collected");
        });
    }
});

var addEventList = EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener = function(type, fn, capture) {
    this.addEventList = addEventList;
    this.addEventList(type, fn, capture);
    fetch("http://localhost:3000/eventset", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "event": 'addEventListener',
            "type": type,
            "function": fn,
            "capture": capture,
            "this": String(this),
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("addEventListener collected");
    });
}

var removeEventList = EventTarget.prototype.removeEventListener;
EventTarget.prototype.removeEventListener = function(type, fn, capture) {
    this.removeEventList = removeEventList;
    this.removeEventList(type, fn, capture);
    fetch("http://localhost:3000/eventset", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "event": 'removeEventListener',
            "type": type,
            "function": fn,
            "capture": capture,
            "this": String(this),
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("removeEventListener collected");
    });
}

var setAttrib = Element.prototype.setAttribute;
Element.prototype.setAttribute = function(name, value) {
    this.setAttrib = setAttrib;
    this.setAttrib(name, value);
    fetch("http://localhost:3000/eventset", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "event": "setAttribute",
            "name": name,
            "value": value,
            "this": String(this),
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("setAttribute collected");
    });
}

var getAttrib = Element.prototype.getAttribute;
Element.prototype.getAttribute = function(name) {
    this.getAttrib = getAttrib;
    this.getAttrib(name);
    fetch("http://localhost:3000/eventget", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "event": "getAttribute",
            "name": name,
            "this": String(this),
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("getAttribute collected");
    });
}

var removeAttrib = Element.prototype.removeAttribute;
Element.prototype.removeAttribute = function(name) {
    this.removeAttrib = removeAttrib;
    this.removeAttrib(name);
    fetch("http://localhost:3000/eventset", {
        method: "POST",
        body: JSON.stringify({
            "top_level_url": window.location.href,
            "event": "removeAttribute",
            "name": name,
            "this": String(this),
            "stack": new Error().stack
        }),
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "application/json"
        }
    }).then(res => {
        console.log("removeAttribute collected");
    });
}