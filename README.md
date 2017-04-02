# DevTools
Development and Management tools

## Module Manager
The Module Manager is a tool built for numerous purposes, and is made up of several components.
 - To eliminate some of the repetative (and sometimes confusing) initial steps when creating a module for the NAO-Engine. 
 - Ease in rapid development of modules by allowing modules to being edited and compiled outside of the NAO-Engine build system (i.e. using Visual Studio or XCode).
 - Automatically configure CMake files for required libraries and dependencies.
 - Allow modules in the NAO-Engine to be easily enabled or disabled, generally without any need to recompile the NAO-Engine.
 - Adds the ability for modules to be held on a remote server and installed seperately (i.e. hombrew style.)
 
### BCurses
BCurses is a custom python framework built around the included python curses library. The purpose of this framework is to allow interactive curses menus to easily be created. More details about the functions of this framework (along with all of our other tools) can be found on the wiki.
