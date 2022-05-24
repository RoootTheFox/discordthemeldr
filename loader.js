// functions
console.log("THEME LOADER");

function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function _getElement(e, baseElement = document) {
    if (e instanceof Node) return e;
    return baseElement.querySelector(e);
}

function _escapeID(id) {
    return id.replace(/^[^a-z]+|[^\w-]+/gi, "-");
}

function _injectTheme(id, css) {
    id = "theme-" + _escapeID(id);
    const style = _getElement(`#${id}`) || document.createElement("style");
    console.log("id: " + id);
    style.id = id;
    style.textContent = css;
    document.head.append(style);
}

function loadTheme(url) {
    console.log("Loading theme from url: " + url);

    fetch(url)
        .then(response => response.text())
        .then(data => {
            console.log("* Loaded theme, length " + data.length);

            const data_string = data.toString();

            var themeName = "unknown-" + btoa((Math.random(2147483647)).toString(36).substring(2)).substring(0, 8);

            if (data_string.includes("@name ")) {
                var tmp = data_string.substring(data_string.indexOf("@name"));
                tmp = tmp.substring(6, tmp.indexOf("\n"));
                themeName = tmp;
            }

            themeName = _escapeID(themeName);

            // TODO: check what betterdiscord specific things exist
            addTheme(themeName, data_string, url);
        });
}

async function getThemes() {
    var response = await fetch("https://discord.com/themeldr/getthemes");
    var res_json = await response.json();
    return res_json;
}

async function getEnabledThemes() {
    var themes = await getThemes();
    var enabled = [];
    for (var i = 0; i < themes.length; i++) {
        if (themes[i].enabled) enabled.push(themes[i]);
    }
    return enabled;
}

async function addTheme(name, css, url) {
    var theme = css;
    if ( /*data.toString().contains("bd-")*/ true) {
        console.log("* Patching theme");

        // todo - add theme patching code here (if needed)

        console.log("* Injecting theme");

        _injectTheme(name, theme);
    } else {
        console.log("* Injecting theme");
        let theme = document.createElement("link");
        theme.rel = "stylesheet";
        theme.href = url;
        document.head.append(theme);
    }

    console.log("adding to cookie");
    var themes = await getThemes();
    var found = false;
    for (var i = 0; i < themes.length; i++) {
        if (themes[i].name == name) {
            console.log("found")
            found = true;
            themes[i].enabled = true;
            themes[i].url = url;
        }
    }

    if (!found) {
        console.log("not found, adding to themes array");
        themes.push({
            name: name,
            enabled: true,
            url: url
        });
    }

    fetch('https://discord.com/themeldr/modifytheme', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                enabled: true,
                url: url,
                data: theme
            })
        }).then(res => res.text())
        .then(res => console.log(res));
}

async function disableTheme(name) {
    var themes = await getThemes();
    for (var i = 0; i < themes.length; i++) {
        if (themes[i].name == name) {
            themes[i].enabled = false;
            var response = await fetch('https://discord.com/themeldr/modifytheme', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(themes[i])
            });
            if (response.status == 200) {
                var id = "theme-" + _escapeID(name);
                var style = document.getElementById(id)
                if(style == null) {
                    console.log("Theme is already disabled!");
                    return;
                }
                document.head.removeChild(style);
                console.log("Disabled theme " + name);
            }
        }
    }
}

console.log("Functions loaded. Use loadTheme(\"url\") to load a theme and clearTheme() or CTRL-R to unload.");

console.log("Getting saved themes");

async function themeldr_init() {
    var themes = await getThemes();
    var themes_enabled = await getEnabledThemes();

    console.log("Themes: " + JSON.stringify(themes));
    console.log("Enabled: " + JSON.stringify(themes_enabled));

    for (var i = 0; i < themes_enabled.length; i++) {
        if (themes_enabled[i].enabled) {
            loadTheme(themes_enabled[i].url);
        }
    }
}

function enableDevMode() {
    Object.defineProperty((webpackChunkdiscord_app.push([
        [''], {},
        e => {
            m = [];
            for (let c in e.c) m.push(e.c[c])
        }
    ]), m).find(m => m ?.exports ?.default ?.isDeveloper !== void 0).exports.default, "isDeveloper", {
        get: () => true
    });
}

setTimeout(function () {
    themeldr_init()
}, 10);
setTimeout(function () {
    enableDevMode()
}, 3000);