# EDMC-Screenshot
A plugin for EDMC that detects screenshot events are converts them to PNG format

The plugin takes the existing screenshot file and generate a new name based on the mask System(Body)_nnn.png
The converted file can be saved to a different directory from the orginal file. The original file can optionally be deleted. 


# Installation
Download the [latest release](https://github.com/NoFoolLikeOne/EDMC-Screenshot/archive/1.1.zip), open the archive (zip) and extract the folder to your EDMC plugin folder.

* Windows: `%LOCALAPPDATA%\EDMarketConnector\plugins` (usually `C:\Users\you\AppData\Local\EDMarketConnector\plugins`).
* Mac: `~/Library/Application Support/EDMarketConnector/plugins` (in Finder hold ⌥ and choose Go &rarr; Library to open your `~/Library` folder).
* Linux: `$XDG_DATA_HOME/EDMarketConnector/plugins`, or `~/.local/share/EDMarketConnector/plugins` if `$XDG_DATA_HOME` is unset.

You will need to re-start EDMC for it to notice the plugin.

## Configuration
Go to file/settings and put in: 
* the directory where the screenshots are stored in game
* the directory where you want the converted screenshots to go
* Choose whether to delete the original file

# To Do
* Add defensive code in case the directories do not exist or are otherwise invalid
* Add option to have a high and low res version when the game saves hi resolution
* Add an options to save a small version for easier up load 800x600 or the like 


# Elite Dangerous Screenshot event format

``` Event format
{
  "timestamp": "2017-08-26T03:12:19Z",
  "event": "Screenshot",
  "Filename": "\\ED_Pictures\\Screenshot_0255.bmp",
  "Width": 1920,
  "Height": 1080,
  "System": "Ceos",
  "Body": "New Dawn Station"
}
```
# Changelog

* Fixed an issue where files were being overwritten when the original was deleted
