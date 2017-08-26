# EDMC-Screenshot
A plugin for EDMC that detects screenshot events are converts them to PNG format


# Installation
Download the [latest release](https://gitlab.com/mrsheepsheep/EDMC-Inara/repository/archive.zip?ref=master), open the archive (zip) and extract the folder (yup, the weird folder name, feel free to rename) to your EDMC plugin folder.

* Windows: `%LOCALAPPDATA%\EDMarketConnector\plugins` (usually `C:\Users\you\AppData\Local\EDMarketConnector\plugins`).
* Mac: `~/Library/Application Support/EDMarketConnector/plugins` (in Finder hold ⌥ and choose Go &rarr; Library to open your `~/Library` folder).
* Linux: `$XDG_DATA_HOME/EDMarketConnector/plugins`, or `~/.local/share/EDMarketConnector/plugins` if `$XDG_DATA_HOME` is unset.

You will need to re-start EDMC for it to notice the plugin.

# Elite Dangerous Screenshot event format


{
  "timestamp": "2017-08-26T03:12:19Z",
  "event": "Screenshot",
  "Filename": "\\ED_Pictures\\Screenshot_0255.bmp",
  "Width": 1920,
  "Height": 1080,
  "System": "Ceos",
  "Body": "New Dawn Station"
}
