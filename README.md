# discordthemeldr
A theme loader for unmodified Discord using a HTTP Proxy.

<h2>How does it work?</h2>

This project uses [mitmproxy](https://github.com/mitmproxy/mitmproxy) to bypass Discord's Content Security Policy
which blocks resources (such as images and stylesheets) from third-party sources from loading.
It achieves that by modifying Discord's response headers to make that policy more open. It also uses that opportunity
to inject itself into the Discord client when you start it, loading your themes automatically.

**TLDR:** It makes Discord allow loading 3rd party themes by modifying its server responses.

<h2>Something important that should be mentioned</h2>

Do not trust random people with installing and running programs and scripts on your computer,
they could easily abuse that to gain access to your Discord account.
Although this project won't do that, don't take my word for it and read the code yourself. If you do not know how to read the code, you probably should
not be using this project (and generally other software too)

<h2>Usage</h2>

This project should support all major platforms that are supported by Discord.

<h3>Setup</h3>

You need to have Python 3.10 and mitmproxy installed on your System. You can install it like this:

Linux: install them using your distro's package manager<br>
macOS: no idea (look it up)<br>
Windows: Download them here: [Python](https://www.python.org/downloads/windows/) (the setup.bat script installs mitmproxy automatically)
**(NOTE: When installing Python, make sure "Add to PATH" is checked!)**


- Clone this repo:<br>[Download the latest version](https://github.com/RoootTheFox/discordthemeldr/archive/refs/heads/main.zip)
and extract it somewhere you can remember<br>
Alternatively, if you have `git` installed, you can use that by executing `git clone https://github.com/RoootTheFox/discordthemeldr` in a Terminal.
- Open the folder you downloaded (and extracted) this repository to and open a Terminal<br>
  - On Windows, shift+right click somewhere in the folder and click on "Open PowerShell Window here" (may be named slightly different)<br>
  - On Linux: depends on your Distro/DE, if you are unsure open a Terminal and `cd` into the folder.

- **For Linux and Windows there are scripts that automate the following steps!**<br>
You can find them under `setup.sh` for Linux and `setup.bat` for Windows. If you don't want to use those, continue with the following steps:

- Install the required modules for the project to work using the Terminal:<br>
`pip install -r requirements.txt`<br>
If that command does not output any errors, you are ready to go to the next step

- Start the proxy using the Terminal:<br>
`mitmdump -s discord-proxy.py`<br>

- Install the proxy certificates:
  - Linux: `sudo trust anchor ~/.mitmproxy/mitmproxy-ca.pem`
  - Windows: `certutil -addstore root %USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer` (might require starting cmd/powershell as admin)
  - macOS: good luck figuring that out (if you did please submit a PR documenting it)

- Close Discord using CTRL+Q or ALT+F4 and make sure its fully closed (no Discord processes running)

- Start Discord with proxy-server set to '127.0.0.1:8080'
- - On Linux this can be done by running `discord --proxy-server="127.0.0.1:8080"
- - On Windows, you can set your System Proxy to 127.0.0.1 Port 8080 in Settings
- - On macOS you are on your own, look up how to change the System proxy I guess

- If you did everything correctly, the theme loader should now be enabled. You can load themes using DevTools console using these commands:
  - `loadTheme("direct link to a theme");` - loads a theme from a specified url (has to be the direct download link
  - `getThemes();` - gets a list of installed themes
  - `getEnabledThemes();` - gets a list of currently enabled themes
  - `disableTheme("Theme Name");` - disables a theme (case sensitive!)
