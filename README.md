# NodeReborn_v1.0.0

## Introduction
This is a python code to use in Houdini, some Houdini users have got used to with some nodes that are not currently available or have a preference with and old one. 
Old houdini's nodes are insight the software they are blocked 

![icon](https://github.com/DanteVFX/Houdini-NodeReborn/assets/156336362/7389762c-03af-4b82-976f-a22b46d73e79)

the name is based on one of the most famous card of Yu-Gi-Oh!

## How to install in Houdini: 
1. Copy the code of NodeRebornTool.py
2. Create a new Tool in the shelf Bar.
3. Paste the code into the Script tab.



## How it works:
This script gives you a list of locked nodes runing a command hscript
* Click on Show Hidden Nodes to send a hscript
* Select a node and click on Reborn the node
* Depending the contex /Obj /Task /Mat etc,  you can use filters




[!IMPORTANT]
> A json file will be created to avoid send a commad hscript each time you open the tool, it will be deleted if you clean the list







### Technical Part (Get the same list on Textport) 

The nodes which are unenable can be unlock sending a hscript command giving specific instructions about what node you want to unlock
you can send a basic command on textport tab to see all the nodes locked

1. Open a Texport Tab.
2. Type the next command 'Opunhide'.
3. You will recive a long list
   
   ![textport](https://github.com/DanteVFX/Houdini-NodeReborn/assets/156336362/50a8880c-3bb0-41f9-b2ed-9419bfdc1aab)
